from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from .error_taxonomy import MCPError, map_exception, is_retryable, to_route_explain


__all__ = [
    "start_call",
    "record_success",
    "record_error",
    "to_jsonl",
    "from_jsonl",
]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _iso_utc() -> str:
    """Return an ISO formatted UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


_SECRET_SUFFIXES: Iterable[str] = ("_secret", "_token")


def _redact(extra: Dict[str, Any]) -> Dict[str, Any]:
    """Return a new dict dropping obvious secret keys."""
    if not extra:
        return {}
    return {
        k: v
        for k, v in extra.items()
        if k != "pii_raw" and not any(k.endswith(suf) for suf in _SECRET_SUFFIXES)
    }


# ---------------------------------------------------------------------------
# context manager
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class _CallCtx:
    tool: str
    request_id: str
    idempotency_key: Optional[str]
    attempt: int = 1
    start: float | None = None
    latency_ms: float | None = None


class _CallTimer:
    def __init__(self, ctx: _CallCtx):
        self.ctx = ctx

    def __enter__(self) -> _CallCtx:
        self.ctx.start = time.monotonic()
        return self.ctx

    def __exit__(self, exc_type, exc, tb) -> bool:
        end = time.monotonic()
        if self.ctx.start is not None:
            self.ctx.latency_ms = (end - self.ctx.start) * 1000.0
        return False


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------


def start_call(tool: str, request_id: str, *, idempotency_key: str | None = None) -> _CallTimer:
    """Create a context manager for an MCP tool call."""
    ctx = _CallCtx(tool=tool, request_id=request_id, idempotency_key=idempotency_key)
    return _CallTimer(ctx)


def _base_event(ctx: _CallCtx, route_explain: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "tool": ctx.tool,
        "request_id": ctx.request_id,
        "idempotency_key": ctx.idempotency_key,
    }
    meta = {
        "attempt": ctx.attempt,
        "latency_ms": ctx.latency_ms,
    }
    return {
        "ts": _iso_utc(),
        "name": "mcp.call",
        "route_explain": route_explain,
        "payload": payload,
        "meta": meta,
    }


def record_success(
    ctx: _CallCtx,
    *,
    confidence: float,
    budget_verdict: str = "ok",
    extra: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Return an event dict for a successful MCP call."""
    route_explain: Dict[str, Any] = {
        "decision": "success",
        "confidence": confidence,
        "budget_verdict": budget_verdict,
    }
    if extra:
        route_explain.update(_redact(extra))

    event = _base_event(ctx, route_explain)
    event["meta"].update({"error_class": None, "retryable": False})
    return event


def record_error(
    ctx: _CallCtx,
    mcp_error: Exception | MCPError,
    *,
    confidence: float = 0.0,
    budget_verdict: str = "ok",
) -> Dict[str, Any]:
    """Return an event dict for a failed MCP call."""
    err = mcp_error if isinstance(mcp_error, MCPError) else map_exception(mcp_error)
    route_explain: Dict[str, Any] = {
        "decision": "error",
        "confidence": confidence,
        "budget_verdict": budget_verdict,
    }
    route_explain.update(to_route_explain(err))

    event = _base_event(ctx, route_explain)
    event["meta"].update(
        {
            "error_class": err.cls.value,
            "retryable": is_retryable(err),
        }
    )
    return event


# ---------------------------------------------------------------------------
# jsonl helpers
# ---------------------------------------------------------------------------


def to_jsonl(event: Dict[str, Any]) -> str:
    """Serialize an event to a single JSON line."""
    return json.dumps(event, separators=(",", ":"), sort_keys=True)


def from_jsonl(line: str) -> Dict[str, Any]:
    """Parse a JSON line back into an event dict."""
    return json.loads(line)

