"""FastAPI service exposing the Alpha Solver as a production-grade API."""

from __future__ import annotations

import csv
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from prometheus_fastapi_instrumentator import Instrumentator

from alpha_solver_entry import _tree_of_thought
from alpha.core.config import APISettings
from .security import validate_api_key, sanitize_query
from .otel import init_tracer

logger = logging.getLogger("alpha-solver.api")

cfg = APISettings()
limiter = Limiter(key_func=lambda request: request.headers.get("X-API-Key") or get_remote_address(request))
app = FastAPI(title="Alpha Solver API", version=cfg.version)
app.state.config = cfg

Instrumentator().instrument(app).expose(app)
init_tracer(app)


class SolveRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = req_id
    start = time.time()
    try:
        response = await call_next(request)
    finally:
        duration_ms = (time.time() - start) * 1000
        logger.info(
            "request",
            extra={
                "request_id": req_id,
                "path": request.url.path,
                "client": request.client.host if request.client else None,
                "duration_ms": duration_ms,
            },
        )
    response.headers["X-Request-ID"] = req_id
    return response


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):  # pragma: no cover - simple
    return JSONResponse(status_code=429, content={"detail": "rate limit exceeded"})


@app.post("/v1/solve")
@limiter.limit(f"{cfg.rate_limit_per_minute}/minute")
async def solve(req: SolveRequest, request: Request) -> JSONResponse:
    validate_api_key(request, cfg.api_key)
    query = sanitize_query(req.query)
    params = req.context or {}
    start = time.time()
    result = _tree_of_thought(query, **params)
    duration_ms = (time.time() - start) * 1000
    cost = duration_ms * cfg.cost_per_ms
    _record_cost(duration_ms, cost)
    return JSONResponse(result)


@app.get("/healthz")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def ready() -> Dict[str, str]:
    return {"status": "ok"}


def _record_cost(duration_ms: float, cost: float) -> None:
    path = Path("artifacts/costs.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([time.time(), round(duration_ms, 3), round(cost, 5)])
    logger.info("cost", extra={"duration_ms": duration_ms, "cost": cost})


__all__ = ["app"]
