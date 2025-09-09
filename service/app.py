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
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator

from alpha_solver_entry import _tree_of_thought
from alpha.core.config import APISettings
from alpha.core.telemetry import observe_request, rate_limited, safe_out
from .security import validate_api_key, sanitize_query
from .otel import init_tracer

logger = logging.getLogger("alpha-solver.api")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover - formatting
        payload = {"level": record.levelname.lower(), "msg": record.getMessage()}
        for key in ("request_id", "path", "client", "duration_ms", "strategy"):
            val = getattr(record, key, None)
            if val is not None:
                payload[key] = val
        return json.dumps(payload)


_handler = logging.StreamHandler()
_handler.setFormatter(JsonFormatter())
logger.handlers = [_handler]
logger.setLevel(logging.INFO)
uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.handlers = [_handler]
uvicorn_logger.propagate = False
uvicorn_logger.setLevel(logging.INFO)

cfg = APISettings()
app = FastAPI(title="Alpha Solver API", version=cfg.version)
app.state.config = cfg
app.state.ready = True

Instrumentator().instrument(app).expose(app)
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


_REQUESTS: DefaultDict[str, Deque[float]] = defaultdict(deque)

app.routes[("GET", "/openapi.json")] = lambda: {
    "openapi": "3.0.0",
    "components": {
        "schemas": {
            "SolveRequest": {
                "properties": {"strategy": {"enum": ["cot", "react", "tot"]}}
            }
        }
    },
}


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = req_id
    request.state.trace_id = req_id
    start = time.time()
    try:
        response = await call_next(request)
    except HTTPException:  # let FastAPI handlers deal with it
        raise
    except Exception:  # pragma: no cover - safety
        logger.exception("request error")
        safe_out("internal error")
        response = JSONResponse(
            status_code=500, content={"final_answer": "SAFE-OUT: internal error"}
        )
    duration_ms = (time.time() - start) * 1000
    observe_request(
        request.url.path,
        getattr(request.state, "strategy", ""),
        duration_ms,
    )
    logger.info(
        "request",
        extra={
            "request_id": req_id,
            "path": request.url.path,
            "client": request.client.host if request.client else None,
            "duration_ms": duration_ms,
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
    safe_out(str(exc.detail))
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
        rate_limited()
        raise HTTPException(status_code=429, detail="rate limit exceeded")
    dq.append(now)


@app.post("/v1/solve", dependencies=[Depends(rate_limiter)])
async def solve(req: SolveRequest, request: Request) -> JSONResponse:
    query = sanitize_query(req.query)
    params = req.context or {}
    strategy = req.strategy or params.get("strategy")
    request.state.strategy = strategy or ""
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
async def health() -> JSONResponse:
    if not getattr(app.state, "config", None):
        return JSONResponse(status_code=500, content={"status": "config-missing"})
    return JSONResponse(content={"status": "ok"})


@app.get("/readyz")
async def ready() -> JSONResponse:
    if not app.state.ready:
        return JSONResponse(status_code=503, content={"status": "not ready"})
    return JSONResponse(content={"status": "ok"})


def _record_cost(duration_ms: float, cost: float) -> None:
    path = Path("artifacts/costs.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([time.time(), round(duration_ms, 3), round(cost, 5)])
    logger.info("cost", extra={"duration_ms": duration_ms, "cost": cost})


__all__ = ["app"]
