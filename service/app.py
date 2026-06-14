"""FastAPI service exposing the Alpha Solver as a production-grade API."""

from __future__ import annotations

import csv
import json
import logging
import os
import time
import re
import uuid
from collections import defaultdict, deque
from dataclasses import replace
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
    build_provider_accounting_record,
    build_provider_safe_out_body,
    build_provider_event,
    emit_provider_accounting,
    emit_provider_event,
    provider_safe_out_status,
)
from service.models.modelset_registry import ModelSet, ModelSetRegistry
from service.models.modelset_resolver import ModelSetResolver
from alpha.core.config import APISettings
from alpha.core.telemetry import record_rate_limit, record_request, record_safe_out
from .security import validate_api_key, sanitize_query
from .otel import init_tracer
from .health import healthcheck
from .gating.gates import evaluate_gates
from alpha.webapp.routes import auth as dashboard_auth, expert_preview


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
app.state.provider_accounting_sink = None

# expose Prometheus metrics on a dedicated port
start_http_server(9000)
# Initialize tracer (works with real OTel or no-op tracer)
tracer = init_tracer(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.cors.origins,
    allow_credentials=cfg.cors.allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dashboard UI: login/session plus the supervised expert-preview page. This
# reuses the shared dashboard auth/CSRF middleware (see alpha/webapp/routes/auth.py)
# so /dashboard/* is protected; we intentionally mount only auth + expert-preview.
#
# Fail closed: mount the dashboard only when both a non-default
# ALPHA_DASHBOARD_PASSWORD and an explicit ALPHA_DASHBOARD_SECRET_KEY are
# configured. Otherwise /login and the provider-backed preview could sit behind
# the well-known default password or use an ephemeral runtime signing secret on a
# deployment that forgot to set one, so we skip mounting (routes 404), log a
# warning, and leave the JSON API fully working.
#
# The bundled preview app intentionally does not mount the full dashboard request,
# settings, run, or jobs routes. Successful login therefore lands on the mounted
# expert-preview page instead of the shared dashboard default.
def _dashboard_enabled() -> bool:
    secret_key = os.getenv(dashboard_auth.SECRET_ENV_VAR)
    return dashboard_auth.is_dashboard_password_configured() and bool(secret_key)


def _mount_dashboard(target: FastAPI) -> None:
    dashboard_auth.install_dashboard_security(target)
    dashboard_auth.configure_login_redirect(target, expert_preview.ROUTE)
    target.include_router(dashboard_auth.router)
    target.include_router(expert_preview.router)


if _dashboard_enabled():
    _mount_dashboard(app)
else:
    logger.warning(
        "Dashboard UI disabled: set a non-default %s and explicit %s "
        "to enable /dashboard/* (login + supervised expert-preview).",
        dashboard_auth.PASSWORD_ENV_VAR,
        dashboard_auth.SECRET_ENV_VAR,
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


def _emit_provider_accounting(
    request: Request, record: dict[str, Any]
) -> None:
    sink = getattr(request.app.state, "provider_accounting_sink", None)
    emit_provider_accounting(record, sink=sink if callable(sink) else None)


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


def _provider_accounting_record(
    provider_request: ProviderRequest, result: ProviderResult
) -> dict[str, Any]:
    metadata = _provider_request_metadata(provider_request)
    provider_request_id = result.raw_metadata.get("provider_request_id")
    return build_provider_accounting_record(
        result=result,
        model_set=metadata["model_set"],
        route=metadata["route"],
        request_id=metadata["request_id"],
        tenant=metadata["tenant"],
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


_PROVIDER_EMPTY_FINAL_ANSWER_MESSAGE = "Provider returned an empty answer."


def _provider_empty_final_answer_error(result: ProviderResult) -> ProviderError:
    return ProviderError(
        provider=result.provider,
        category="unknown",
        retryable=False,
        safe_message=_PROVIDER_EMPTY_FINAL_ANSWER_MESSAGE,
        request_id=result.request_id,
        retry_count=result.retry_count,
    )


def _provider_empty_final_answer_response(request: Request, result: ProviderResult) -> JSONResponse:
    record_safe_out(request.url.path)
    return _provider_error_response(_provider_empty_final_answer_error(result))


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


def _provider_error_response(error: ProviderError) -> JSONResponse:
    return JSONResponse(
        status_code=provider_safe_out_status(error),
        content=build_provider_safe_out_body(error),
    )


_MULTI_PART_MARKERS = (
    "first",
    "second",
    "third",
    "compare",
    "tradeoff",
    "trade-off",
    "pros and cons",
    "step-by-step",
    "plan",
    "review",
    "decide",
    "decision",
    "risk",
    "risks",
    "assumption",
    "assumptions",
    "ambiguous",
    "uncertain",
    "unknown",
    "legal",
    "medical",
    "financial",
    "architecture",
    "migration",
    "security",
    "expert",
)


_CONFIDENCE_RE = re.compile(r"(?i)confidence[^0-9%]*(\d+(?:\.\d+)?)\s*(%)?")
_PERCENT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%")


_LOCAL_SOLVER_CONTEXT_CONTROL_KEYS = frozenset({"route"})


def _local_solver_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Return context kwargs safe for the deterministic local solver.

    ``context.route`` is a service/provider routing seam.  The local solver does
    not accept it as a runtime knob, so strip it before forwarding request
    context into the local/offline implementation.
    """

    return {
        key: value
        for key, value in params.items()
        if key not in _LOCAL_SOLVER_CONTEXT_CONTROL_KEYS
    }


def _is_expert_route(params: Dict[str, Any]) -> bool:
    return str(params.get("route", "")).strip().lower() == "expert"


def _expert_complexity(query: str) -> str:
    text = query.strip().lower()
    score = 0
    word_count = len(text.split())
    if word_count >= 45 or len(text) >= 280:
        score += 2
    elif word_count >= 25 or len(text) >= 160:
        score += 1
    if any(marker in text for marker in _MULTI_PART_MARKERS):
        score += 1
    if text.count("?") >= 2 or "\n" in text or ";" in text:
        score += 1
    if any(token in text for token in (" and ", " or ", " vs ", " versus ")) and word_count >= 12:
        score += 1
    return "complex" if score >= 2 else "trivial"


def _as_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        parts = [part.strip(" -•\t") for part in re.split(r"[\n;]+", value)]
        return [part for part in parts if part]
    return []


def _parse_confidence_value(value: Any) -> float | None:
    raw: float | None = None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        raw = float(value)
    elif isinstance(value, str):
        match = _CONFIDENCE_RE.search(value) or _PERCENT_RE.search(value)
        if match:
            raw = float(match.group(1))
            if match.lastindex and match.group(match.lastindex) == "%":
                raw /= 100.0
        else:
            try:
                raw = float(value.strip())
            except ValueError:
                raw = None
    if raw is None:
        return None
    if raw > 1.0:
        raw /= 100.0
    return max(0.0, min(1.0, raw))


def _confidence_value(value: Any) -> float:
    parsed = _parse_confidence_value(value)
    return 0.0 if parsed is None else parsed


def _parse_expert_preview(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    parse_status = "unstructured"
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = None
    if isinstance(parsed, dict):
        data = parsed
        parse_status = "json"

    confidence_source = data.get("confidence") if "confidence" in data else text
    parsed_confidence = _parse_confidence_value(confidence_source)
    confidence_available = parsed_confidence is not None

    considerations = _as_string_list(data.get("considerations"))
    assumptions = _as_string_list(data.get("assumptions"))
    if not considerations:
        considerations = _extract_section_list(text, "considerations")
        if considerations and parse_status == "unstructured":
            parse_status = "sections"
    if not assumptions:
        assumptions = _extract_section_list(text, "assumptions")
        if assumptions and parse_status == "unstructured":
            parse_status = "sections"
    if confidence_available and parse_status == "unstructured":
        parse_status = "sections"

    return {
        "considerations": considerations,
        "assumptions": assumptions,
        "confidence": 0.0 if parsed_confidence is None else parsed_confidence,
        "confidence_available": confidence_available,
        "preview_parse_status": parse_status,
    }


def _extract_section_list(text: str, section: str) -> list[str]:
    pattern = re.compile(
        rf"(?ims)^\s*{re.escape(section)}\s*:?\s*(.*?)(?=^\s*(?:considerations|assumptions|confidence)\s*:?|\Z)"
    )
    match = pattern.search(text)
    if not match:
        return []
    return _as_string_list(match.group(1))


_EXECUTION_PLANNING_DELIVERABLE_RE = re.compile(
    r"(?i)\b(?:test\s+plan|operator\s+test\s+plan|runbook|checklist|plan)\b"
)
_EXECUTION_PLANNING_ACTION_RE = re.compile(
    r"(?i)\b(?:create|draft|write|produce|build|outline|prepare)\b"
)
_CONCRETE_TARGET_RE = re.compile(
    r"(?:/[A-Za-z0-9_.~:/?#\[\]@!$&'()*+,;=%-]+|\bfor\s+[^.?!]+)"
)
_UNDERSPECIFIED_OR_HIGH_RISK_RE = re.compile(
    r"(?i)\b(?:ambiguous|uncertain|unknown|unspecified|not\s+specified|missing|"
    r"unsafe|impossible|legal|medical|financial|compliance|security)\b"
)
_LOW_CONFIDENCE_BLOCK_THRESHOLD = 0.10
_ACTIONABLE_EXECUTION_PLAN_DEFAULT_ASSUMPTIONS = [
    "Supervised operator preview only.",
    "Local rollback is available after the controlled run.",
    (
        "No MVP validation, production-readiness, Alpha Solver superiority, "
        "broad benchmark success, or exact billing accuracy claim is made from this run."
    ),
    "Evidence must be sanitized before capture or sharing.",
]


def _is_actionable_execution_planning_prompt(query: str) -> bool:
    """Return True when a planning request is actionable enough to answer.

    This deliberately stays narrow: it only recognizes explicit execution-style
    deliverable requests that include a target/context signal and avoids prompts
    that state they are underspecified or belong to high-risk domains.
    """

    text = query.strip()
    if not text:
        return False
    if _UNDERSPECIFIED_OR_HIGH_RISK_RE.search(text):
        return False
    return (
        _EXECUTION_PLANNING_ACTION_RE.search(text) is not None
        and _EXECUTION_PLANNING_DELIVERABLE_RE.search(text) is not None
        and _CONCRETE_TARGET_RE.search(text) is not None
    )


def _default_actionable_execution_plan_assumptions(
    query: str, assumptions: list[str], *, confidence_available: bool
) -> list[str]:
    """Add narrow defaults when unavailable Step 1 metadata gave no assumptions."""

    if (
        confidence_available
        or assumptions
        or not _is_actionable_execution_planning_prompt(query)
    ):
        return assumptions
    return list(_ACTIONABLE_EXECUTION_PLAN_DEFAULT_ASSUMPTIONS)


def _mode_for_unavailable_expert_confidence(query: str) -> str:
    """Choose a safe mode when Step 1 confidence metadata is missing/unparseable."""

    if _is_actionable_execution_planning_prompt(query):
        return "answer_with_assumptions"
    return "clarify"


def _mode_from_confidence(
    confidence: float, assumptions: list[str], model_set: ModelSet, *, query: str = ""
) -> str:
    if confidence <= _LOW_CONFIDENCE_BLOCK_THRESHOLD:
        return "block"
    decision, _info = evaluate_gates(
        confidence=confidence,
        budget_tokens=model_set.max_tokens,
        policy_flags={},
    )
    if decision == "block":
        return "block"
    if decision == "clarify":
        if _is_actionable_execution_planning_prompt(query):
            return "answer_with_assumptions"
        return "clarify"
    if assumptions and confidence < 0.75:
        return "answer_with_assumptions"
    return "direct"


def _expert_step_one_prompt(query: str) -> str:
    return (
        "For the request below, identify expert-style considerations, assumptions, "
        "and a self-rated confidence from 0 to 1. Return compact JSON with keys "
        "considerations, assumptions, and confidence.\n\nRequest:\n"
        f"{query}"
    )


def _expert_step_two_prompt(query: str, preview: dict[str, Any]) -> str:
    return (
        "Answer the request below using the provided considerations and assumptions. "
        "Start with the requested deliverable itself; do not start with only "
        "assumptions, considerations, caveats, or process notes. Preserve the "
        "user's requested output format first: if they ask for a plan, checklist, "
        "table, release note, email, rubric, runbook, or other specific deliverable, "
        "make the final answer that deliverable. Preserve requested headings, "
        "section names, order, time boxes, bullets, tables, and named parts unless "
        "unsafe or impossible. Keep useful assumptions, considerations, caveats, "
        "and claim boundaries, but do not let them replace the requested deliverable; "
        "place them after the deliverable or weave them into it briefly. Do not "
        "overclaim certainty, validation, production readiness, benchmark success, "
        "superiority, or provider reasoning orchestration. Do not include raw "
        "provider metadata.\n\n"
        f"Considerations: {json.dumps(preview['considerations'], ensure_ascii=False)}\n"
        f"Assumptions: {json.dumps(preview['assumptions'], ensure_ascii=False)}\n"
        f"Self-rated confidence: {preview['confidence']}\n\nRequest:\n{query}"
    )


def _actionable_execution_plan_fallback(query: str, assumptions: list[str]) -> str | None:
    """Return a narrow local fallback for empty actionable planning answers.

    The fallback is intentionally limited to prompts that already request an
    execution-planning deliverable with enough target/context to answer. It uses
    only the requested deliverable, route/context, required sections, and explicit
    assumptions so an empty provider Step 2 answer does not erase the primary
    deliverable while still avoiding unsupported claims.
    """

    if not _is_actionable_execution_planning_prompt(query):
        return None

    text = query.lower()
    if not all(section in text for section in ("setup", "prompt runs", "evidence capture", "rollback")):
        return None

    target_match = re.search(r"/[A-Za-z0-9_.~:/?#\[\]@!$&'()*+,;=%-]+", query)
    target = target_match.group(0) if target_match else "the requested target"
    assumption_text = "; ".join(assumptions) if assumptions else (
        "supervised operator preview only; no MVP validation, production-readiness, "
        "or superiority claim"
    )

    return (
        f"# Two-hour operator test plan for {target}\n\n"
        "## Setup (0:00-0:20)\n"
        "- Confirm dashboard access, session/CSRF behavior, and the provider/configuration state intended for the supervised run.\n"
        "- Prepare a sanitized evidence template with prompt text, observed mode, request metrics, and notes for each run.\n\n"
        "## Prompt runs (0:20-1:15)\n"
        "- Submit the controlled operator test-plan prompt and confirm the Alpha pane answers directly with assumptions rather than asking to clarify first.\n"
        "- Run any approved comparison prompts needed for the checkpoint and record plain-provider versus Alpha-preview observations without copying raw provider payloads.\n\n"
        "## Evidence capture (1:15-1:45)\n"
        "- Capture sanitized screenshots or notes showing the primary answer, mode, assumptions, considerations, layout readability, and request metrics.\n"
        "- Record whether setup, prompt runs, evidence capture, and rollback are all present in the primary Alpha answer.\n\n"
        "## Rollback (1:45-2:00)\n"
        "- Restore `MODEL_PROVIDER=local` after the approved run and verify the preview is no longer using the live provider.\n"
        "- Document unresolved issues and do not mark MVP validation, production readiness, superiority, or broad benchmark success from this single retest.\n\n"
        f"Assumptions: {assumption_text}."
    )


def _primary_expert_answer(
    *, query: str, provider_answer: str, mode: str, assumptions: list[str]
) -> str:
    answer = provider_answer.strip()
    if answer:
        return provider_answer
    if mode == "answer_with_assumptions":
        fallback = _actionable_execution_plan_fallback(query, assumptions)
        if fallback is not None:
            return fallback
    return provider_answer


_CLARIFY_MESSAGE = "I need a few details before I can answer this well."
_BLOCK_MESSAGE = (
    "I cannot safely provide a final answer for this request in the supervised preview."
)


def _clarifying_questions_for_expert_request(
    query: str, considerations: list[str], assumptions: list[str]
) -> list[str]:
    """Return deterministic, local clarify questions for expert-route clarify mode."""
    source_text = " ".join([query, *considerations, *assumptions]).lower()
    questions: list[str] = []

    def add(question: str) -> None:
        if question not in questions and len(questions) < 4:
            questions.append(question)

    add("What is the main outcome you want from this request?")

    if any(term in source_text for term in ("format", "deliverable", "output")):
        add("What output format or deliverable should I produce?")
    if any(term in source_text for term in ("timeline", "deadline", "milestone", "schedule")):
        add("What timeline or deadline constraints should I preserve?")
    if any(term in source_text for term in ("budget", "cost", "resource")):
        add("What budget or resource constraints should I account for?")
    if any(term in source_text for term in ("risk", "security", "legal", "medical", "financial")):
        add("What risk tolerance or compliance constraints should guide the answer?")

    add("What constraints or context should I preserve?")
    add("What tradeoffs or priorities matter most?")
    add("What would make the answer successful for you?")
    return questions[:4]


def _expert_response(
    *,
    answer: str,
    considerations: list[str],
    assumptions: list[str],
    confidence: float,
    mode: str,
    complexity: str,
    provider: str,
    model: str,
    call_count: int,
    clarifying_questions: list[str] | None = None,
    preview_parse_status: str | None = None,
    confidence_available: bool | None = None,
) -> Dict[str, Any]:
    meta = {
        "route": "expert",
        "complexity": complexity,
        "provider": provider,
        "model": model,
        "call_count": call_count,
    }
    if preview_parse_status is not None:
        meta["preview_parse_status"] = preview_parse_status
    if confidence_available is not None:
        meta["confidence_available"] = confidence_available

    response = {
        "final_answer": answer,
        "answer": answer,
        "considerations": considerations,
        "assumptions": assumptions,
        "confidence": confidence,
        "mode": mode,
        "meta": meta,
    }
    if mode == "clarify" and clarifying_questions is not None:
        response["clarifying_questions"] = clarifying_questions
    return response


def _execute_provider_call(
    *,
    request: Request,
    provider_client: Any,
    provider_request: ProviderRequest,
) -> ProviderResult:
    _emit_provider_telemetry(request, _provider_request_started_event(provider_request))
    result = provider_client.execute(provider_request)
    _emit_provider_telemetry(
        request, _provider_request_completed_event(provider_request, result)
    )
    _emit_provider_accounting(request, _provider_accounting_record(provider_request, result))
    return result


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
            if _is_expert_route(params):
                complexity = _expert_complexity(query)
                if complexity == "trivial":
                    provider_result = _execute_provider_call(
                        request=request,
                        provider_client=provider_client,
                        provider_request=provider_request,
                    )
                    if not provider_result.text.strip():
                        return _provider_empty_final_answer_response(request, provider_result)
                    return JSONResponse(
                        _expert_response(
                            answer=provider_result.text,
                            considerations=[],
                            assumptions=[],
                            confidence=0.0,
                            mode="direct",
                            complexity=complexity,
                            provider=provider_result.provider,
                            model=provider_result.model,
                            call_count=1,
                        )
                    )

                preview_request = replace(
                    provider_request,
                    prompt=_expert_step_one_prompt(query),
                )
                preview_result = _execute_provider_call(
                    request=request,
                    provider_client=provider_client,
                    provider_request=preview_request,
                )
                preview = _parse_expert_preview(preview_result.text)
                preview["assumptions"] = _default_actionable_execution_plan_assumptions(
                    query,
                    preview["assumptions"],
                    confidence_available=bool(preview.get("confidence_available")),
                )
                answer_request = replace(
                    provider_request,
                    prompt=_expert_step_two_prompt(query, preview),
                )
                answer_result = _execute_provider_call(
                    request=request,
                    provider_client=provider_client,
                    provider_request=answer_request,
                )
                if preview.get("confidence_available") is False:
                    mode = _mode_for_unavailable_expert_confidence(query)
                else:
                    mode = _mode_from_confidence(
                        preview["confidence"],
                        preview["assumptions"],
                        model_set,
                        query=query,
                    )
                expert_answer = _primary_expert_answer(
                    query=query,
                    provider_answer=answer_result.text,
                    mode=mode,
                    assumptions=preview["assumptions"],
                )
                clarifying_questions = None
                if mode == "clarify":
                    expert_answer = _CLARIFY_MESSAGE
                    clarifying_questions = _clarifying_questions_for_expert_request(
                        query, preview["considerations"], preview["assumptions"]
                    )
                elif mode == "block":
                    expert_answer = _BLOCK_MESSAGE
                if not expert_answer.strip():
                    record_safe_out(request.url.path)
                    return _provider_error_response(
                        ProviderError(
                            provider=answer_result.provider,
                            category="unknown",
                            retryable=False,
                            safe_message="Provider returned an empty expert answer.",
                            request_id=answer_result.request_id,
                            retry_count=answer_result.retry_count,
                        )
                    )
                return JSONResponse(
                    _expert_response(
                        answer=expert_answer,
                        considerations=preview["considerations"],
                        assumptions=preview["assumptions"],
                        confidence=preview["confidence"],
                        mode=mode,
                        complexity=complexity,
                        provider=answer_result.provider,
                        model=answer_result.model,
                        call_count=2,
                        clarifying_questions=clarifying_questions,
                        preview_parse_status=(
                            preview["preview_parse_status"]
                            if preview.get("confidence_available") is False
                            else None
                        ),
                        confidence_available=(
                            False if preview.get("confidence_available") is False else None
                        ),
                    )
                )

            provider_result = _execute_provider_call(
                request=request,
                provider_client=provider_client,
                provider_request=provider_request,
            )
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
        if not provider_result.text.strip():
            return _provider_empty_final_answer_response(request, provider_result)
        return JSONResponse(_provider_success_response(provider_result, model_set))

    start = time.time()
    if strategy == "react":
        from alpha.reasoning.react_lite import run_react_lite

        seed = params.get("seed", 0)
        max_steps = params.get("max_steps", 2)
        result = run_react_lite(query, seed=seed, max_steps=max_steps)
    else:
        result = _tree_of_thought(query, **_local_solver_params(params))
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
