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
from fastapi.responses import JSONResponse
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
from prometheus_client import generate_latest, start_http_server

from alpha_solver_entry import _tree_of_thought
from alpha.providers import (
    PROVIDER_REQUEST_COMPLETED,
    PROVIDER_REQUEST_FAILED,
    PROVIDER_REQUEST_STARTED,
    PROVIDER_REQUEST_TIMEOUT,
    OpenAIProviderClient,
    ProviderError,
    ProviderRequest,
    ProviderResult,
    build_provider_event,
    emit_provider_event,
)
from service.models.modelset_registry import ModelSet, ModelSetRegistry
from service.models.modelset_resolver import ModelSetResolver
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

# expose Prometheus metrics on a dedicated port
start_http_server(9000)
# Initialize tracer (works with real OTel or no-op tracer)
tracer = init_tracer(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.cors.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _is_openai_provider_enabled() -> bool:
    """Return True only for explicit OpenAI provider opt-in."""
    return os.getenv("MODEL_PROVIDER", "local").strip().lower() == "openai"


def _get_model_set(request: Request, params: Dict[str, Any]) -> ModelSet:
    requested = params.get("model_set") or os.getenv("MODEL_SET")
    route_explain: Dict[str, str] = {}
    registry = getattr(request.app.state, "model_set_registry", None)
    if registry is None:
        registry = ModelSetRegistry()
        request.app.state.model_set_registry = registry
    resolver = ModelSetResolver(registry)
    model_set, _reason = resolver.resolve(
        requested=str(requested) if requested else None,
        headers=request.headers,
        tenant_default=params.get("tenant_model_set"),
        route_explain=route_explain,
    )
    return model_set


def _provider_client_factory(model_set: ModelSet) -> OpenAIProviderClient:
    return OpenAIProviderClient(price_hint=model_set.price_hint)


def _get_provider_client(request: Request, model_set: ModelSet) -> Any:
    factory = getattr(request.app.state, "provider_client_factory", None)
    if factory is None:
        factory = _provider_client_factory
    return factory(model_set)


def _optional_number(params: Dict[str, Any], key: str) -> Any:
    value = params.get(key)
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _optional_int(params: Dict[str, Any], key: str) -> int | None:
    value = params.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _build_provider_request(
    *,
    query: str,
    params: Dict[str, Any],
    strategy: Any,
    request: Request,
    model_set: ModelSet,
) -> ProviderRequest:
    route = str(strategy or params.get("route") or "tot")
    tenant = params.get("tenant") or request.headers.get("X-Tenant-ID")
    system = params.get("system")
    return ProviderRequest(
        prompt=query,
        system=system if isinstance(system, str) and system else None,
        model=model_set.model,
        max_tokens=model_set.max_tokens,
        timeout_ms=model_set.timeout_ms,
        temperature=_optional_number(params, "temperature"),
        seed=_optional_int(params, "seed"),
        metadata={
            "request_id": getattr(request.state, "request_id", None),
            "route": route,
            "model_set": model_set.name,
            "tenant": str(tenant) if tenant else None,
        },
    )


def _provider_request_metadata(provider_request: ProviderRequest) -> dict[str, str | None]:
    return {
        "request_id": provider_request.request_id,
        "route": str(provider_request.metadata.get("route"))
        if provider_request.metadata.get("route") is not None
        else None,
        "model_set": str(provider_request.metadata.get("model_set"))
        if provider_request.metadata.get("model_set") is not None
        else None,
        "tenant": str(provider_request.metadata.get("tenant"))
        if provider_request.metadata.get("tenant") is not None
        else None,
    }


def _emit_provider_telemetry(
    request: Request, event: dict[str, Any]
) -> None:
    sink = getattr(request.app.state, "provider_telemetry_sink", None)
    emit_provider_event(event, sink=sink if callable(sink) else None)


def _provider_request_started_event(provider_request: ProviderRequest) -> dict[str, Any]:
    metadata = _provider_request_metadata(provider_request)
    return build_provider_event(
        PROVIDER_REQUEST_STARTED,
        provider="openai",
        model=provider_request.model,
        model_set=metadata["model_set"],
        route=metadata["route"],
        request_id=metadata["request_id"],
        tenant=metadata["tenant"],
        status="started",
    )


def _provider_request_completed_event(
    provider_request: ProviderRequest, result: ProviderResult
) -> dict[str, Any]:
    metadata = _provider_request_metadata(provider_request)
    provider_request_id = result.raw_metadata.get("provider_request_id")
    return build_provider_event(
        PROVIDER_REQUEST_COMPLETED,
        provider=result.provider,
        model=result.model,
        model_set=metadata["model_set"],
        route=metadata["route"],
        request_id=result.request_id or metadata["request_id"],
        tenant=metadata["tenant"],
        status="completed",
        retry_count=result.retry_count,
        latency_ms=result.latency_ms,
        input_tokens=result.usage.input_tokens,
        output_tokens=result.usage.output_tokens,
        total_tokens=result.usage.total_tokens,
        estimated_cost_usd=result.cost.estimated_usd,
        cost_source=result.cost.source,
        finish_reason=result.finish_reason,
        provider_request_id=str(provider_request_id) if provider_request_id is not None else None,
    )


def _provider_request_error_event(
    provider_request: ProviderRequest, error: ProviderError
) -> dict[str, Any]:
    metadata = _provider_request_metadata(provider_request)
    event_name = (
        PROVIDER_REQUEST_TIMEOUT if error.category == "timeout" else PROVIDER_REQUEST_FAILED
    )
    return build_provider_event(
        event_name,
        provider=error.provider,
        model=provider_request.model,
        model_set=metadata["model_set"],
        route=metadata["route"],
        request_id=error.request_id or metadata["request_id"],
        tenant=metadata["tenant"],
        status="timeout" if error.category == "timeout" else "failed",
        retry_count=error.retry_count,
        error_category=error.category,
        retryable=error.retryable,
        status_code=error.status_code,
        safe_message=error.safe_message,
    )


def _provider_success_response(result: ProviderResult, model_set: ModelSet) -> Dict[str, Any]:
    return {
        "final_answer": result.text,
        "meta": {
            "provider": result.provider,
            "model": result.model,
            "model_set": model_set.name,
            "finish_reason": result.finish_reason,
            "request_id": result.request_id,
            "usage": {
                "input_tokens": result.usage.input_tokens,
                "output_tokens": result.usage.output_tokens,
                "total_tokens": result.usage.total_tokens,
            },
            "cost": {
                "estimated_usd": result.cost.estimated_usd,
                "source": result.cost.source,
            },
            "latency_ms": result.latency_ms,
        },
    }


def _provider_error_status(error: ProviderError) -> int:
    return {
        "missing_credentials": 503,
        "auth": 502,
        "rate_limit": 429,
        "timeout": 504,
        "network": 503,
        "provider_5xx": 502,
        "invalid_request": 400,
        "content_filter": 400,
        "unknown": 502,
    }.get(error.category, 502)


def _provider_error_response(error: ProviderError) -> JSONResponse:
    return JSONResponse(
        status_code=_provider_error_status(error),
        content={
            "final_answer": f"SAFE-OUT: {error.safe_message}",
            "error": {
                "provider": error.provider,
                "category": error.category,
                "retryable": error.retryable,
            },
        },
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

    if _is_openai_provider_enabled():
        model_set = _get_model_set(request, params)
        provider_request = _build_provider_request(
            query=query,
            params=params,
            strategy=strategy,
            request=request,
            model_set=model_set,
        )
        try:
            provider_client = _get_provider_client(request, model_set)
            _emit_provider_telemetry(
                request, _provider_request_started_event(provider_request)
            )
            provider_result = provider_client.execute(provider_request)
        except ProviderError as exc:
            _emit_provider_telemetry(
                request, _provider_request_error_event(provider_request, exc)
            )
            record_safe_out(request.url.path)
            return _provider_error_response(exc)
        except Exception:
            record_safe_out(request.url.path)
            safe_error = ProviderError(
                provider="openai",
                category="unknown",
                retryable=False,
                safe_message="OpenAI request failed.",
                request_id=provider_request.request_id,
            )
            _emit_provider_telemetry(
                request, _provider_request_error_event(provider_request, safe_error)
            )
            return _provider_error_response(safe_error)
        _emit_provider_telemetry(
            request, _provider_request_completed_event(provider_request, provider_result)
        )
        return JSONResponse(_provider_success_response(provider_result, model_set))

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
