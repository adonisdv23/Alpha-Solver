"""No-secret provider cost accounting helpers.

Provider cost accounting is intentionally allowlist-based. Callers pass only
already-safe request metadata plus a normalized ``ProviderResult``. This module
never inspects raw provider request/response payloads, exception objects,
dataclass ``__dict__`` values, or raw provider metadata dumps.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

from .base import ProviderResult

PROVIDER_COST_RECORDED = "provider.cost.recorded"

_ACCOUNTING_SOURCE = "service:/v1/solve"
_BUDGET_STATUS_RECORDED = "recorded"
_PROVIDER_ACCOUNTING_LOGGER = logging.getLogger("alpha.providers.accounting")
_PROVIDER_ACCOUNTING_CONTEXT_SINK: ContextVar[Callable[[dict[str, Any]], None] | None] = (
    ContextVar("provider_accounting_context_sink", default=None)
)

_ALLOWED_FIELDS = {
    "event",
    "provider",
    "model",
    "model_set",
    "route",
    "request_id",
    "tenant",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "estimated_cost_usd",
    "cost_source",
    "retry_count",
    "budget_status",
    "accounting_source",
    "provider_request_id",
}


@contextmanager
def capture_provider_accounting(
    sink: Callable[[dict[str, Any]], None],
) -> Iterator[None]:
    """Capture provider accounting records for the current async context only."""

    token = _PROVIDER_ACCOUNTING_CONTEXT_SINK.set(sink)
    try:
        yield
    finally:
        _PROVIDER_ACCOUNTING_CONTEXT_SINK.reset(token)


def build_provider_accounting_record(
    *,
    result: ProviderResult,
    model_set: str | None,
    route: str | None,
    request_id: str | None,
    tenant: str | None = None,
    provider_request_id: str | None = None,
) -> dict[str, Any]:
    """Build a post-call provider cost accounting record from safe fields only.

    ``None`` values are dropped to avoid inventing unknown usage or cost. Cost
    values are copied from ``ProviderResult.cost`` and are not recomputed here.
    """

    record: dict[str, Any] = {
        "event": PROVIDER_COST_RECORDED,
        "provider": result.provider,
        "model": result.model,
        "model_set": model_set,
        "route": route,
        "request_id": result.request_id or request_id,
        "tenant": tenant,
        "input_tokens": result.usage.input_tokens,
        "output_tokens": result.usage.output_tokens,
        "total_tokens": result.usage.total_tokens,
        "estimated_cost_usd": result.cost.estimated_usd,
        "cost_source": result.cost.source,
        "retry_count": result.retry_count,
        "budget_status": _BUDGET_STATUS_RECORDED,
        "accounting_source": _ACCOUNTING_SOURCE,
        "provider_request_id": provider_request_id,
    }
    return {
        key: value
        for key, value in record.items()
        if key in _ALLOWED_FIELDS and value is not None
    }


def emit_provider_accounting(
    record: dict[str, Any], sink: Callable[[dict[str, Any]], None] | None = None
) -> None:
    """Emit a prebuilt provider accounting record to a sink or structured logger."""

    safe_record = {
        key: record[key]
        for key in _ALLOWED_FIELDS
        if key in record and record[key] is not None
    }
    context_sink = _PROVIDER_ACCOUNTING_CONTEXT_SINK.get()
    if context_sink is not None:
        context_sink(dict(safe_record))
    if sink is not None:
        sink(dict(safe_record))
        return
    _PROVIDER_ACCOUNTING_LOGGER.info(
        json.dumps(safe_record, sort_keys=True, separators=(",", ":"))
    )


__all__ = [
    "PROVIDER_COST_RECORDED",
    "capture_provider_accounting",
    "build_provider_accounting_record",
    "emit_provider_accounting",
]
