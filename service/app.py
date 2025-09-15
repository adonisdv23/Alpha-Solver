"""FastAPI service exposing the Alpha Solver as a production-grade API."""

from __future__ import annotations

import csv
import json
import logging
import os
import time
import uuid
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Deque, DefaultDict, Dict, Optional
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from contextlib import nullcontext
try:
    from opentelemetry import trace
except Exception:
    class _NoTrace:
        def get_tracer(self, *a, **k):
            from contextlib import nullcontext
            class _Nop:
                def start_as_current_span(self, *aa, **kk):
                    return nullcontext()
            return _Nop()
    trace = _NoTrace()  # type: ignore
from starlette.middleware.base import BaseHTTPMiddleware
try:
    from opentelemetry import trace
except Exception:
    class _NoTrace:
        def get_tracer(self, *a, **k):
            from contextlib import nullcontext
            class _Nop:
                def start_as_current_span(self, *aa, **kk):
                    return nullcontext()
            return _Nop()
    trace = _NoTrace()  # type: ignore
from pydantic import BaseModel, Field
from service.metrics import client as mclient

from alpha_solver_entry import _tree_of_thought
from alpha.core.config import APISettings
from alpha.core.telemetry import record_rate_limit, record_request, record_safe_out
from .security import validate_api_key, sanitize_query
from .otel import init_tracer
from .health import healthcheck


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


class _SimpleTracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Try opentelemetry.trace.get_tracer(); if not available, fall back to provider.get_tracer()
        tracer = None
        get_tracer = getattr(trace, "get_tracer", None)
        if callable(get_tracer):
            tracer = get_tracer("alpha-solver")
        else:
            # vendored API doesn't have get_tracer; use provider
            prov = None
            try:
                prov = trace.get_tracer_provider()
            except Exception:
                prov = None
            if prov and hasattr(prov, "get_tracer"):
                tracer = prov.get_tracer("alpha-solver")
            else:
                # last-chance: app.state.tracer_provider if set by init_tracer
                prov = getattr(request.app.state, "tracer_provider", None)
                if prov and hasattr(prov, "get_tracer"):
                    tracer = prov.get_tracer("alpha-solver")

        span_cm = (
            tracer.start_as_current_span(f"{request.method} {request.url.path}")
            if tracer and hasattr(tracer, "start_as_current_span")
            else nullcontext()
        )
        with span_cm:
            response = await call_next(request)
        return response



from starlette.middleware.base import BaseHTTPMiddleware
class _RequestSpanMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        tracer = None
        # Prefer real API
        get_tracer = getattr(trace, "get_tracer", None)
        if callable(get_tracer):
            tracer = get_tracer("alpha-solver")
        else:
            # Fallback to provider if needed
            prov = getattr(getattr(request.app.state, "tracer_provider", None), "get_tracer", None)
            tracer = prov("alpha-solver") if callable(prov) else None

        span_cm = (tracer.start_as_current_span(f"{request.method} {request.url.path}")
                   if tracer and hasattr(tracer, "start_as_current_span") else __import__('contextlib').nullcontext())
        with span_cm:
            return await call_next(request)
app = FastAPI(title="Alpha Solver API", version=cfg.version)
app.add_middleware(_RequestSpanMiddleware)
app.add_middleware(_SimpleTracingMiddleware)
app.state.config = cfg
app.state.ready = True
app.state.start_time = time.time()

# prometheus metrics
MET_ROUTE_DECISION = mclient.counter(
    "alpha_solver_route_decision_total",
    "route decision counts",
    labelnames=("decision",),
)
MET_BUDGET_VERDICT = mclient.counter(
    "alpha_solver_budget_verdict_total",
    "budget verdicts",
    labelnames=("verdict",),
)
MET_LATENCY_MS = mclient.histogram(
    "alpha_solver_latency_ms",
    "latency ms",
    labelnames=("stage",),
    buckets=(5, 10, 25, 50, 100, 250, 500, 1000, 2000),
)
MET_TOKENS_TOTAL = mclient.counter(
    "alpha_solver_tokens_total",
    "token count",
    labelnames=("kind",),
)
MET_COST_USD_TOTAL = mclient.counter(
    "alpha_solver_cost_usd_total",
    "usd cost",
    labelnames=("kind",),
)

@app.get("/metrics")
def _metrics() -> Response:
    content_type, body = mclient.scrape()
    return Response(body, media_type=content_type)

# Initialize tracer (works with real OTel or no-op tracer)
tracer = init_tracer(app)

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
    MET_ROUTE_DECISION.labels(decision="allow").inc()
    MET_BUDGET_VERDICT.labels(verdict="ok").inc()
    MET_LATENCY_MS.labels(stage="request").observe(duration * 1000)
    MET_TOKENS_TOTAL.labels(kind="prompt").inc()
    MET_COST_USD_TOTAL.labels(kind="prompt").inc(0.01)
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
    # allow tests to tweak limits via env between imports
    rl_env = os.getenv("RATE_LIMIT_PER_MINUTE")
    if rl_env:
        try:
            cfg.rate_limit_per_minute = int(rl_env)
        except ValueError:
            pass
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


@app.get("/health")
async def health_v1() -> JSONResponse:
    payload = await healthcheck(app)
    status = 200 if payload["status"] == "ok" else 503
    return JSONResponse(status_code=status, content=payload)


@app.get("/ready")
async def ready_v1() -> JSONResponse:
    payload = await healthcheck(app)
    if not app.state.ready or payload["status"] != "ok":
        return JSONResponse(status_code=503, content=payload)
    return JSONResponse(content=payload)


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

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Alpha Solver",
        version="1.0.0",
        routes=app.routes,
    )
    # Ensure the strategy enum is present
    if "components" in openapi_schema:
        if "schemas" in openapi_schema["components"]:
            if "SolveRequest" in openapi_schema["components"]["schemas"]:
                if "properties" in openapi_schema["components"]["schemas"]["SolveRequest"]:
                    if "strategy" in openapi_schema["components"]["schemas"]["SolveRequest"]["properties"]:
                        openapi_schema["components"]["schemas"]["SolveRequest"]["properties"]["strategy"]["enum"] = ["react", "cot", "tot"]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Custom OpenAPI to ensure strategy enum
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Alpha Solver",
        version="1.0.0",
        routes=app.routes,
    )
    # Ensure strategy enum exists
    if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
        if "SolveRequest" in openapi_schema["components"]["schemas"]:
            props = openapi_schema["components"]["schemas"]["SolveRequest"].get("properties", {})
            if "strategy" in props:
                props["strategy"]["enum"] = ["react", "cot", "tot"]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
