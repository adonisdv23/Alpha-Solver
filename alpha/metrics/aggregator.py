"""Prometheus metrics aggregation and export service."""

from __future__ import annotations

from threading import Lock
import inspect

from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route
from starlette.testclient import TestClient

try:
    from prometheus_client import (
        CONTENT_TYPE_LATEST,
        CollectorRegistry,
        Counter,
        Histogram,
        generate_latest,
    )
except Exception:  # pragma: no cover - fallback for stub
    from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest  # type: ignore

    class CollectorRegistry(list):
        pass

_lock = Lock()
_REGISTRY = CollectorRegistry()
_METRICS_CREATED = False

GATES = None
REPLAY = None
BUDGET = None
ADAPTER_CALLS = None
ADAPTER_LATENCY_MS = None


def _ensure_metrics() -> None:
    """Lazily create metrics in a thread-safe way."""
    global _METRICS_CREATED, GATES, REPLAY, BUDGET, ADAPTER_CALLS, ADAPTER_LATENCY_MS
    if _METRICS_CREATED:
        return
    with _lock:
        if _METRICS_CREATED:
            return
        GATES = Counter(
            "alpha_solver_gate_total",
            "gate decisions",
            ["gate"],
            registry=_REGISTRY,
        )
        REPLAY = Counter(
            "alpha_solver_replay_total",
            "replay outcomes",
            ["result"],
            registry=_REGISTRY,
        )
        BUDGET = Counter(
            "alpha_solver_budget_total",
            "budget verdicts",
            ["verdict"],
            registry=_REGISTRY,
        )
        ADAPTER_CALLS = Counter(
            "alpha_solver_adapter_calls_total",
            "adapter calls",
            ["adapter"],
            registry=_REGISTRY,
        )
        ADAPTER_LATENCY_MS = Histogram(
            "alpha_solver_adapter_latency_ms",
            "adapter latency ms",
            ["adapter"],
            buckets=[5, 10, 25, 50, 100, 250, 500, 1000],
            registry=_REGISTRY,
        )
        _METRICS_CREATED = True


class MetricsAggregator:
    """Aggregate metrics and expose a `/metrics` endpoint."""

    def __init__(self) -> None:
        _ensure_metrics()

    def record_gate(self, gate: str) -> None:
        _ensure_metrics()
        GATES.labels(gate=gate or "unknown").inc()

    def record_replay(self, result: str) -> None:
        _ensure_metrics()
        REPLAY.labels(result=result or "unknown").inc()

    def record_budget(self, verdict: str) -> None:
        _ensure_metrics()
        BUDGET.labels(verdict=verdict or "unknown").inc()

    def record_adapter(self, adapter: str, latency_ms: float | None = None) -> None:
        _ensure_metrics()
        adapter = adapter or "unknown"
        ADAPTER_CALLS.labels(adapter=adapter).inc()
        if latency_ms is not None:
            ADAPTER_LATENCY_MS.labels(adapter=adapter).observe(latency_ms)

    def asgi_app(self):
        _ensure_metrics()

        async def metrics(_request):
            # ``generate_latest`` signature differs between the real library and the
            # lightweight stub used in tests. Introspect to call it correctly.
            sig = inspect.signature(generate_latest)
            if sig.parameters:
                payload = generate_latest(_REGISTRY)  # type: ignore[arg-type]
            else:  # pragma: no cover - stub path
                payload = generate_latest()
            return Response(payload, media_type=CONTENT_TYPE_LATEST)

        return Starlette(routes=[Route("/metrics", metrics)])

    def test_client(self) -> TestClient:
        return TestClient(self.asgi_app())


__all__ = ["MetricsAggregator", "_REGISTRY"]
