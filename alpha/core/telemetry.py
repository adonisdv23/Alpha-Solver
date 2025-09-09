from __future__ import annotations
import asyncio
from typing import Any, Awaitable, Callable, Dict, List

from prometheus_client import Counter, Histogram

# Prometheus metrics
REQUEST_COUNT = Counter(
    "alpha_request_total",
    "Total API requests",
    labelnames=("path", "strategy"),
)

REQUEST_LATENCY_MS = Histogram(
    "alpha_request_latency_ms",
    "API request latency in milliseconds",
    labelnames=("path", "strategy"),
)

RATE_LIMIT_COUNT = Counter(
    "alpha_rate_limit_total",
    "Rate limit events encountered",
)

SAFE_OUT_COUNT = Counter(
    "alpha_safe_out_total",
    "SAFE-OUT responses emitted",
    labelnames=("reason",),
)


def observe_request(path: str, strategy: str, duration_ms: float) -> None:
    """Record a request count and latency."""
    label = {"path": path, "strategy": strategy or ""}
    REQUEST_COUNT.labels(**label).inc()
    REQUEST_LATENCY_MS.labels(**label).observe(duration_ms)


def rate_limited() -> None:
    """Increment the rate limit counter."""
    RATE_LIMIT_COUNT.inc()


def safe_out(reason: str) -> None:
    """Increment the SAFE-OUT counter."""
    SAFE_OUT_COUNT.labels(reason=reason).inc()


class TelemetryExporter:
    """Asynchronous telemetry exporter with batching and retry."""

    def __init__(self, sender: Callable[[List[Dict[str, Any]]], Awaitable[None]], batch_size: int = 10, retry_seconds: float = 0.1):
        self.sender = sender
        self.batch_size = batch_size
        self.retry_seconds = retry_seconds
        self.queue: asyncio.Queue[Dict[str, Any] | None] = asyncio.Queue()
        self._task = asyncio.create_task(self._worker())

    async def _worker(self) -> None:
        batch: List[Dict[str, Any]] = []
        while True:
            item = await self.queue.get()
            if item is None:
                break
            batch.append(item)
            if len(batch) >= self.batch_size:
                await self._flush(batch)
                batch = []
        if batch:
            await self._flush(batch)

    async def _flush(self, batch: List[Dict[str, Any]]) -> None:
        while True:
            try:
                await self.sender(batch)
                break
            except Exception:
                await asyncio.sleep(self.retry_seconds)

    async def emit(self, event: Dict[str, Any]) -> None:
        """Queue a telemetry event after validating required fields."""
        event.setdefault("session_id", "unknown")
        event.setdefault("event", "unknown")
        event.setdefault("timestamp", "")
        event.setdefault("version", 1)
        event.setdefault("properties", {})
        # propagate deterministic ids when provided
        if "trace_id" in event:
            event.setdefault("request_id", event["trace_id"])
        if "request_id" in event:
            event.setdefault("trace_id", event["request_id"])
        validate_event(event)
        await self.queue.put(event)

    async def close(self) -> None:
        await self.queue.put(None)
        await self._task


def validate_event(event: Dict[str, Any]) -> bool:
    """Validate telemetry event contract.

    Required fields: session_id, event, timestamp, version, properties. When the
    ``event`` name is ``"router_decision"`` additional fields are expected in
    ``properties`` (``chosen_branches``, ``pruned_count`` and
    ``estimated_tokens_saved``).
    """

    required = {"session_id", "event", "timestamp", "version", "properties"}
    missing = required - event.keys()
    if missing:
        raise ValueError(f"missing fields: {sorted(missing)}")
    if event["event"] == "router_decision":
        props = event.get("properties", {})
        for key in ("chosen_branches", "pruned_count", "estimated_tokens_saved"):
            if key not in props:
                raise ValueError(f"router_decision missing field: {key}")
    return True


__all__ = [
    "TelemetryExporter",
    "validate_event",
    "observe_request",
    "rate_limited",
    "safe_out",
]
