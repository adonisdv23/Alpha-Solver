"""Lightweight Prometheus metrics helpers."""

from __future__ import annotations

try:  # pragma: no cover - the real library is preferred
    from prometheus_client import CollectorRegistry, Counter, Histogram
    from prometheus_client.exposition import generate_latest
except Exception:  # pragma: no cover - lightweight fallback
    class CollectorRegistry(dict):
        """Very small stand-in used when prometheus_client is unavailable."""

        def register(self, metric: object) -> None:  # pragma: no cover - trivial
            self[metric.name] = metric

    class _BaseMetric:
        def __init__(self, name: str, documentation: str, registry: CollectorRegistry):
            self.name = name
            self.documentation = documentation
            registry.register(self)

    class Counter(_BaseMetric):
        def __init__(self, name: str, documentation: str, registry: CollectorRegistry):
            super().__init__(name, documentation, registry)
            self.value = 0.0

        def inc(self, amount: float = 1.0) -> None:
            self.value += amount

    class Histogram(_BaseMetric):
        def __init__(
            self,
            name: str,
            documentation: str,
            *,
            buckets: tuple[int, ...] | tuple[float, ...],
            registry: CollectorRegistry,
        ) -> None:
            super().__init__(name, documentation, registry)
            self.value = 0.0

        def observe(self, amount: float) -> None:
            self.value += amount

    def generate_latest(registry: CollectorRegistry) -> bytes:  # pragma: no cover - trivial
        lines: list[str] = []
        for metric in registry.values():
            mtype = "counter" if isinstance(metric, Counter) else "histogram"
            lines.append(f"# HELP {metric.name} {metric.documentation}")
            lines.append(f"# TYPE {metric.name} {mtype}")
            lines.append(f"{metric.name} {metric.value}")
        return "\n".join(lines).encode("utf-8")

# A single, module-level registry keeps exports cheap.
REGISTRY: CollectorRegistry = CollectorRegistry()
# Backwards compatibility for existing imports.
_REGISTRY = REGISTRY

# Pre-register core series.  No dynamic labels to keep cardinality low.
gate_decisions_total = Counter(
    "gate_decisions_total", "Total gate decisions", registry=REGISTRY
)
replay_pass_total = Counter(
    "replay_pass_total", "Total successful replays", registry=REGISTRY
)
budget_spend_cents = Counter(
    "budget_spend_cents", "Budget spend in cents", registry=REGISTRY
)
adapter_latency_ms = Histogram(
    "adapter_latency_ms",
    "Adapter latency in milliseconds",
    buckets=(10, 25, 50, 75, 100, 250, 500, 1000),
    registry=REGISTRY,
)


def get_metrics_text(
    extra: dict | None = None, *, registry: CollectorRegistry = REGISTRY
) -> str:
    """Return Prometheus metrics in text format.

    The optional ``extra`` mapping allows callers to bump counters in a
    low-overhead fashion immediately before export.
    """

    if extra:
        if (val := extra.get("gates")):
            gate_decisions_total.inc(val)
        if (val := extra.get("replays")):
            replay_pass_total.inc(val)
        if (val := extra.get("budget_cents")):
            budget_spend_cents.inc(val)
        if (val := extra.get("adapter_latency_ms")):
            adapter_latency_ms.observe(val)

    # ``generate_latest`` returns ``bytes``; decode once and return.
    return generate_latest(registry).decode("utf-8")


class MetricsAggregator:
    """Compatibility wrapper exposing methods used in older code paths."""

    def record_gate(self, count: int = 1) -> None:
        gate_decisions_total.inc(count)

    def record_replay(self, count: int = 1) -> None:
        replay_pass_total.inc(count)

    def record_budget(self, cents: int) -> None:
        budget_spend_cents.inc(cents)

    def record_adapter(self, latency_ms: float) -> None:
        adapter_latency_ms.observe(latency_ms)

    def get_metrics_text(self, extra: dict | None = None) -> str:
        return get_metrics_text(extra)


__all__ = [
    "REGISTRY",
    "_REGISTRY",
    "gate_decisions_total",
    "replay_pass_total",
    "budget_spend_cents",
    "adapter_latency_ms",
    "get_metrics_text",
    "MetricsAggregator",
]

