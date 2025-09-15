"""Minimal Prometheus client stub used in tests.

The real ``prometheus_client`` package is fairly heavy and not included in this
environment.  This stub implements just enough for unit tests and metrics
exporter functionality: counters, gauges, histograms with label support and a
``generate_latest`` helper.  It also exposes a global ``_REGISTRY`` list similar
to the real library's collector registry for simple scenarios.
"""

from __future__ import annotations

from typing import Dict, Iterable, Tuple

CONTENT_TYPE_LATEST = "text/plain; version=0.0.4"


class CollectorRegistry(list):
    """Simplistic collector registry."""


_REGISTRY: CollectorRegistry = CollectorRegistry()


class _MetricProxy:
    def __init__(self, metric: "_Metric", key: Tuple[str, ...]):
        self.metric = metric
        self.key = key

    def inc(self, amount: float = 1) -> None:
        self.metric._values[self.key] = self.metric._values.get(self.key, 0) + amount

    def set(self, value: float) -> None:
        self.metric._values[self.key] = value

    def observe(self, value: float) -> None:
        self.metric._values[self.key] = value

    # allow chaining like real client
    def labels(self, **kwargs: str) -> "_MetricProxy":  # pragma: no cover - trivial
        return self.metric.labels(**kwargs)


class _Metric:
    def __init__(
        self,
        name: str,
        documentation: str | None = None,
        labelnames: Iterable[str] | None = None,
        registry: CollectorRegistry | None = None,
        **kwargs,
    ) -> None:
        self.name = name
        self.labelnames = list(labelnames or [])
        self._values: Dict[Tuple[str, ...], float] = {}
        (registry or _REGISTRY).append(self)

    def labels(self, **kwargs: str) -> _MetricProxy:
        key = tuple(kwargs.get(n, "") for n in self.labelnames)
        return _MetricProxy(self, key)

    # direct ops when no labels
    def inc(self, amount: float = 1) -> None:
        self.labels().inc(amount)

    def set(self, value: float) -> None:
        self.labels().set(value)

    def observe(self, value: float) -> None:
        self.labels().observe(value)


class Counter(_Metric):
    pass


class Gauge(_Metric):
    pass


class Histogram(_Metric):
    pass


def generate_latest(registry: CollectorRegistry | None = None) -> bytes:
    registry = registry or _REGISTRY
    lines = []
    for metric in registry:
        for labels, value in metric._values.items():
            if metric.labelnames:
                label_str = ",".join(
                    f'{name}="{val}"' for name, val in zip(metric.labelnames, labels)
                )
                lines.append(f"{metric.name}{{{label_str}}} {value}")
            else:
                lines.append(f"{metric.name} {value}")
    return "\n".join(lines).encode()


def start_http_server(port: int) -> None:  # pragma: no cover - noop
    return None


__all__ = [
    "CollectorRegistry",
    "Counter",
    "Gauge",
    "Histogram",
    "generate_latest",
    "start_http_server",
    "_REGISTRY",
    "CONTENT_TYPE_LATEST",
]

