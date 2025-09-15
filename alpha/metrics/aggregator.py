from __future__ import annotations

from typing import Dict, Optional

from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest

__all__ = ["get_metrics_text"]

_REGISTRY = CollectorRegistry()
_counters: Dict[str, Counter] = {
    "gate_decisions_total": Counter(
        "gate_decisions_total", "Number of gate decisions", registry=_REGISTRY
    ),
    "replay_pass_total": Counter(
        "replay_pass_total", "Replay passes", registry=_REGISTRY
    ),
    "budget_spend_cents": Counter(
        "budget_spend_cents", "Budget spent in cents", registry=_REGISTRY
    ),
}
_histogram = Histogram(
    "adapter_latency_ms",
    "Latency of adapters in ms",
    buckets=(1, 5, 10, 25, 50, 100, 250, 500, 1000),
    registry=_REGISTRY,
)


def _get_or_create_counter(name: str) -> Counter:
    if name in _counters:
        return _counters[name]
    metric = Counter(f"{name}_total", name, registry=_REGISTRY)
    _counters[name] = metric
    return metric


def get_metrics_text(extra: Optional[Dict[str, int]] = None) -> str:
    """Return Prometheus metrics text.

    ``extra`` may contain metric increments, e.g. ``{"throttles": 3}``.
    """

    if extra:
        for key, value in extra.items():
            counter = _get_or_create_counter(key)
            counter.inc(value)
    return generate_latest(_REGISTRY).decode()
