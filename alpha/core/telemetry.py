from __future__ import annotations
import asyncio
from typing import Any, Awaitable, Callable, Dict, List

from prometheus_client import Counter, Histogram

# basic Prometheus metrics used across the service
_REQUEST_COUNT = Counter("alpha_requests_total", "Total API requests", ["endpoint"])
_REQUEST_LATENCY = Histogram(
    "alpha_request_latency_seconds", "Latency of API requests", ["endpoint"]
)
_RATE_LIMIT_COUNT = Counter(
    "alpha_ratelimit_total", "Total rate limit events", ["endpoint"]
)
_SAFE_OUT_COUNT = Counter(
    "alpha_safe_out_total", "Total SAFE-OUT events", ["endpoint"]
)


def record_request(endpoint: str, duration_seconds: float) -> None:
    """Record a request and its latency."""
    _REQUEST_COUNT.labels(endpoint=endpoint).inc()
    _REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration_seconds)


def record_rate_limit(endpoint: str) -> None:
    """Record a rate limit event."""
    _RATE_LIMIT_COUNT.labels(endpoint=endpoint).inc()


def record_safe_out(endpoint: str) -> None:
    """Record a SAFE-OUT event."""
    _SAFE_OUT_COUNT.labels(endpoint=endpoint).inc()


class TelemetryExporter:
    """Asynchronous telemetry exporter with batching and retry."""

    def __init__(
        self,
        sender: Callable[[List[Dict[str, Any]]], Awaitable[None]],
        batch_size: int = 10,
        retry_seconds: float = 0.1,
    ):
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
        req_id = event.get("request_id")
        trace_id = event.get("trace_id")
        if req_id and not trace_id:
            trace_id = req_id
        if trace_id and not req_id:
            req_id = trace_id
        if req_id:
            event["request_id"] = req_id
        if trace_id:
            event["trace_id"] = trace_id
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
    "record_request",
    "record_rate_limit",
    "record_safe_out",
]
