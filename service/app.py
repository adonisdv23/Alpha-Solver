"""FastAPI service exposing the Alpha Solver as a production-grade API."""
from __future__ import annotations

import csv
import json
import logging
import re
import time
import uuid
from collections import defaultdict, deque
from enum import Enum
from pathlib import Path
from typing import Any, Deque, DefaultDict, Dict, Optional

from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from alpha_solver_entry import _tree_of_thought
from alpha.core.config import APISettings
from alpha.core.telemetry import record_rate_limit, record_request, record_safe_out
from .security import validate_api_key, sanitize_query
from .otel import init_tracer


# ---------- logging ----------
class JsonFormatter(logging.Formatter):
    """Minimal JSON log formatter."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {"level": record.levelname, "msg": record.getMessage()}
        for field in ("request_id", "strategy"):
            if hasattr(record, field):
                payload[field] = getattr(record, field)
        return json.dumps(payload)


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])
logging.getLogger("uvicorn.access").handlers = [handler]
logger = logging.getLogger("alpha-solver.api")


# ---------- app & config ----------
cfg = APISettings()
app = FastAPI(title="Alpha Solver API", version=cfg.version)
app.state.config = cfg
app.state.ready = True
init_tracer(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.cors.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- models ----------
class StrategyEnum(str, Enum):
    """Supported reasoning strategies."""

    cot = "cot"
    react = "react"
    tot = "tot"


class SolveRequest(BaseModel):
    """Request model for the solve endpoint."""

    query: str = Field(..., examples=["hello"])
    context: Optional[Dict[str, Any]] = None
    strategy: Optional[StrategyEnum] = Field(
        default=None,
        description="Reasoning strategy",
        examples=["react", "cot", "tot"],
    )


# ---------- rate limiting ----------
_REQUESTS: DefaultDict[str, Deque[float]] = defaultdict(deque)


def rate_limiter(request: Request) -> None:
    key = validate_api_key(request, cfg)  # validates header & optionally enforces it
    request.state.api_key = key

    if not cfg.ratelimit.enabled:
        return

    identifier = key if cfg.auth.enabled else (request.client.host or "anon")
    now = time.time()
    window = cfg.ratelimit.window_seconds

    dq = _REQUESTS[identifier]
    while dq and dq[0] <= now - window:
        dq.popleft()

    if len(dq) >= cfg.ratelimit.max_requests:
        record_rate_limit(request.url.path)
        raise HTTPException(status_code=429, detail="rate limit exceeded")

    dq.append(now)


# ---------- SAFE-OUT helpers ----------
def _violates_basic_policy(query: str, answer: str) -> bool:
    """
    Minimal arithmetic sanity: if the query includes a single a op b (with + - * /),
    ensure the computed result appears in the answer. Otherwise trigger SAFE-OUT.
    This is intentionally small and conservative.
    """

    t = query or ""
    m = re.search(r"\b(\d+)\s*([+\-*/])\s*(\d+)\b", t)
    if not m:
        return False
    a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
    try:
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        else:
            # division: fall back to float string; we only check substring containment
            result = a / b
    except Exception:
        return True
    return str(result) not in (answer or "")


def safe_out(answer: str, query: str) -> str:
    """
    If answer is empty OR fails minimal arithmetic sanity, return a SAFE-OUT.
    Otherwise pass the original answer through unchanged.
    """

    if not answer or _violates_basic_policy(query, answer):
        record_safe_out("/v1/solve")
        return "SAFE-OUT: regex mismatch"
    return answer


# ---------- middleware & error handling ----------
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = req_id
    start = time.time()
    try:
        response = await call_next(request)
    except HTTPException:
        # let FastAPI turn these into proper responses
        raise
    except Exception:
        logger.exception("request error", extra={"request_id": req_id})
        record_safe_out(request.url.path)
        response = JSONResponse(status_code=500, content={"final_answer": "SAFE-OUT: internal error"})
    duration = time.time() - start
    record_request(request.url.path, duration)
    response.headers["X-Request-ID"] = req_id
    traceparent = request.headers.get("traceparent")
    if traceparent:
        response.headers["traceparent"] = traceparent
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    body = {"final_answer": f"SAFE-OUT: {exc.detail}"}
    headers = {"X-Request-ID": getattr(request.state, "request_id", "")}
    record_safe_out(request.url.path)
    return JSONResponse(status_code=exc.status_code, content=body, headers=headers)


# ---------- endpoint ----------
@app.post("/v1/solve", dependencies=[Depends(rate_limiter)])
async def solve_endpoint(
    req: SolveRequest = Body(...),
    request: Optional[Request] = None,
):
    if req.query is ...:
        raise HTTPException(status_code=422, detail="query required")

    query = sanitize_query(req.query)
    strategy = (req.strategy or "react")
    ctx = req.context or {}

    if request is not None:
        request.state.strategy = strategy

    start = time.time()
    # Strategy dispatch (keep behavior the project already uses)
    if strategy == "cot":
        # deterministic chain-of-thought option
        from alpha.reasoning.cot import run_cot  # type: ignore

        seed = ctx.get("seed", 0)
        max_steps = ctx.get("max_steps", 3)
        raw = run_cot(req.query, seed=seed, max_steps=max_steps)
        result: Dict[str, Any] = {
            "final_answer": raw.get("answer", ""),
            "steps": raw.get("steps", [])[:max_steps],
            "confidence": raw.get("confidence", 0.0),
            "meta": {"strategy": "cot", "seed": seed},
        }
    elif strategy == "tot":
        result = _tree_of_thought(req.query, **ctx)
        result.setdefault("meta", {})["strategy"] = "tot"
    else:
        # lightweight ReAct-style
        from alpha.reasoning.react_lite import run_react_lite  # type: ignore

        seed = ctx.get("seed", 0)
        max_steps = ctx.get("max_steps", 2)
        result = run_react_lite(req.query, seed=seed, max_steps=max_steps)
        result.setdefault("meta", {})["strategy"] = "react"

    duration_ms = (time.time() - start) * 1000.0
    cost = duration_ms * cfg.cost_per_ms
    _record_cost(duration_ms, cost)

    # Enforce SAFE-OUT before returning
    result["final_answer"] = safe_out(result.get("final_answer", ""), req.query)
    return JSONResponse(result)


# ---------- support routes ----------
@app.get("/openapi.json")
async def openapi_json() -> JSONResponse:
    root = Path(__file__).resolve().parents[1]
    with open(root / "openapi.json", "r") as f:
        data = json.load(f)
    return JSONResponse(data)


@app.get("/healthz")
async def health() -> Dict[str, str]:
    ok = bool(app.state.config)
    return {"status": "ok" if ok else "error"}


@app.get("/readyz")
async def ready() -> JSONResponse:
    if not app.state.ready:
        return JSONResponse(status_code=503, content={"status": "not ready"})
    return JSONResponse(content={"status": "ok"})


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# ---------- cost logging ----------
def _record_cost(duration_ms: float, cost: float) -> None:
    path = Path("artifacts/costs.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([time.time(), round(duration_ms, 3), round(cost, 5)])
    logger.info("cost", extra={"duration_ms": duration_ms, "cost": cost})


__all__ = ["app"]

