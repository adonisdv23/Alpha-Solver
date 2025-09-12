"""FastAPI service exposing the Alpha Solver as a production-grade API."""

from __future__ import annotations

import csv
import json
import logging
import time
import uuid
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Deque, DefaultDict, Dict, Optional
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from prometheus_client import generate_latest, start_http_server

from alpha_solver_entry import _tree_of_thought
from alpha.core.config import APISettings
from alpha.core.telemetry import record_rate_limit, record_request, record_safe_out
from .security import validate_api_key, sanitize_query
from .otel import init_tracer


class JsonFormatter(logging.Formatter):
    """Minimal JSON log formatter."""

    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover - trivial
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


cfg = APISettings()
app = FastAPI(title="Alpha Solver API", version=cfg.version)
app.state.config = cfg
app.state.ready = True

# expose Prometheus metrics on a dedicated port
start_http_server(9000)
init_tracer(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.cors.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StrategyEnum(str, Enum):
    cot = "cot"
    react = "react"
    tot = "tot"


class SolveRequest(BaseModel):
    query: str = Field(..., examples=["hello"])
    context: Optional[Dict[str, Any]] = None
    strategy: Optional[StrategyEnum] = Field(
        default=None,
        description="Reasoning strategy",
        examples=["cot", "react", "tot"],
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title=app.title, version=app.version, routes=app.routes)
    solve = schema.get("components", {}).get("schemas", {}).get("SolveRequest", {})
    props = solve.get("properties", {})
    strategy = props.get("strategy", {})
    if "enum" not in strategy:
        strategy["enum"] = ["react", "cot", "tot"]
    props["strategy"] = strategy
    solve["properties"] = props
    schema.setdefault("components", {}).setdefault("schemas", {})["SolveRequest"] = solve
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi


_REQUESTS: DefaultDict[str, Deque[float]] = defaultdict(deque)


@app.get("/openapi.json")
def openapi_json() -> JSONResponse:
    spec_path = Path(__file__).resolve().parents[1] / "openapi.json"
    with spec_path.open("r", encoding="utf-8") as f:
        spec = json.load(f)
    return JSONResponse(spec)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = req_id
    start = time.time()
    try:
        response = await call_next(request)
    except HTTPException:  # let FastAPI handlers deal with it
        raise
    except Exception:  # pragma: no cover - safety
        logger.exception("request error", extra={"request_id": req_id})
        record_safe_out(request.url.path)
        response = JSONResponse(
            status_code=500, content={"final_answer": "SAFE-OUT: internal error"}
        )
    duration = time.time() - start
    record_request(request.url.path, duration)
    logger.info(
        "request",
        extra={
            "request_id": req_id,
            "path": request.url.path,
            "client": request.client.host if request.client else None,
            "duration_ms": duration * 1000,
            "strategy": getattr(request.state, "strategy", None),
        },
    )
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


def rate_limiter(request: Request) -> None:
    key = validate_api_key(request, cfg)
    request.state.api_key = key
    if not cfg.ratelimit.enabled:
        return
    identifier = key if cfg.auth.enabled else request.client.host or "anon"
    now = time.time()
    window = cfg.ratelimit.window_seconds
    dq = _REQUESTS[identifier]
    while dq and dq[0] <= now - window:
        dq.popleft()
    if len(dq) >= cfg.ratelimit.max_requests:
        record_rate_limit(request.url.path)
        raise HTTPException(status_code=429, detail="rate limit exceeded")
    dq.append(now)


@app.post("/v1/solve", dependencies=[Depends(rate_limiter)])
async def solve(req: SolveRequest, request: Request) -> JSONResponse:
    query = sanitize_query(req.query)
    params = req.context or {}
    strategy = req.strategy or params.get("strategy")
    request.state.strategy = strategy
    start = time.time()
    if strategy == "react":
        from alpha.reasoning.react_lite import run_react_lite

        seed = params.get("seed", 0)
        max_steps = params.get("max_steps", 2)
        result = run_react_lite(query, seed=seed, max_steps=max_steps)
    else:
        result = _tree_of_thought(query, **params)
    duration_ms = (time.time() - start) * 1000
    cost = duration_ms * cfg.cost_per_ms
    _record_cost(duration_ms, cost)
    return JSONResponse(result)


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
def metrics():
    # Legacy test compatibility: tests call .json() and expect a plain string.
    # We return the Prometheus exposition format as a JSON string.
    text = generate_latest().decode("utf-8")
    return JSONResponse(text)


def _record_cost(duration_ms: float, cost: float) -> None:
    path = Path("artifacts/costs.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([time.time(), round(duration_ms, 3), round(cost, 5)])
    logger.info("cost", extra={"duration_ms": duration_ms, "cost": cost})


__all__ = ["app"]
