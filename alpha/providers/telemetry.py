"""No-secret provider telemetry event helpers.

Provider telemetry is intentionally allowlist-based. Callers pass only already-safe
metadata and this module never inspects provider request/response payloads,
exception objects, dataclass ``__dict__`` values, or raw provider metadata.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from typing import Any

PROVIDER_REQUEST_STARTED = "provider.request.started"
PROVIDER_REQUEST_COMPLETED = "provider.request.completed"
PROVIDER_REQUEST_FAILED = "provider.request.failed"
PROVIDER_REQUEST_TIMEOUT = "provider.request.timeout"

_PROVIDER_EVENT_LOGGER = logging.getLogger("alpha.providers.telemetry")

_ALLOWED_FIELDS = {
    "event",
    "provider",
    "model",
    "model_set",
    "route",
    "request_id",
    "status",
    "tenant",
    "retry_count",
    "latency_ms",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "estimated_cost_usd",
    "cost_source",
    "finish_reason",
    "error_category",
    "retryable",
    "status_code",
    "safe_message",
    "provider_request_id",
}


def build_provider_event(
    event_name: str,
    *,
    provider: str,
    model: str | None,
    model_set: str | None,
    route: str | None,
    request_id: str | None,
    tenant: str | None = None,
    status: str | None = None,
    retry_count: int | None = None,
    latency_ms: int | None = None,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    total_tokens: int | None = None,
    estimated_cost_usd: float | None = None,
    cost_source: str | None = None,
    finish_reason: str | None = None,
    error_category: str | None = None,
    retryable: bool | None = None,
    status_code: int | None = None,
    safe_message: str | None = None,
    provider_request_id: str | None = None,
) -> dict[str, Any]:
    """Build a provider lifecycle event from explicit safe fields only.

    ``None`` values are dropped to avoid implying that unknown usage or cost was
    observed. Unknown usage/cost should therefore be omitted unless a future
    schema requires explicit nulls.
    """

    event: dict[str, Any] = {
        "event": event_name,
        "provider": provider,
        "model": model,
        "model_set": model_set,
        "route": route,
        "request_id": request_id,
        "status": status,
        "tenant": tenant,
        "retry_count": retry_count,
        "latency_ms": latency_ms,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "estimated_cost_usd": estimated_cost_usd,
        "cost_source": cost_source,
        "finish_reason": finish_reason,
        "error_category": error_category,
        "retryable": retryable,
        "status_code": status_code,
        "safe_message": safe_message,
        "provider_request_id": provider_request_id,
    }
    return {key: value for key, value in event.items() if key in _ALLOWED_FIELDS and value is not None}


def emit_provider_event(
    event: dict[str, Any], sink: Callable[[dict[str, Any]], None] | None = None
) -> None:
    """Emit a prebuilt provider event to a test sink or structured logger."""

    safe_event = {key: event[key] for key in _ALLOWED_FIELDS if key in event and event[key] is not None}
    if sink is not None:
        sink(dict(safe_event))
        return
    _PROVIDER_EVENT_LOGGER.info(
        json.dumps(safe_event, sort_keys=True, separators=(",", ":"))
    )


__all__ = [
    "PROVIDER_REQUEST_STARTED",
    "PROVIDER_REQUEST_COMPLETED",
    "PROVIDER_REQUEST_FAILED",
    "PROVIDER_REQUEST_TIMEOUT",
    "build_provider_event",
    "emit_provider_event",
]
