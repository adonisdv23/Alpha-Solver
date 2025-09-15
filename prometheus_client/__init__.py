"""Minimal Prometheus client stub used in tests.

The real ``prometheus_client`` package is fairly heavy and not included in this
environment.  This stub implements just enough for unit tests and metrics
exporter functionality: counters, gauges, histograms with label support and a
``generate_latest`` helper.  It also exposes a global ``_REGISTRY`` list similar
to the real library's collector registry for simple scenarios.
"""

from __future__ import annotations

from typing import Dict, Iterable, Tuple

# match real client so tests can assert on exact header
CONTENT_TYPE_LATEST = "text/plain; version=0.0.4; charset=utf-8"


class CollectorRegistry(list):
    """Simplistic collector registry."""


_REGISTRY: CollectorRegistry = CollectorRegistry()


class _MetricProxy:
    def __init__(self, metric: "_Metric", key: Tuple[str, ...]):
        self.metric = metric
        self.key = key

    def inc(self, amount: float = 1) -> None:
        self.metric._inc(self.key, amount)

    def set(self, value: float) -> None:
        self.metric._set(self.key, value)

    def observe(self, value: float) -> None:
        self.metric._observe(self.key, value)

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

    # internal helpers used by proxy
    def _inc(self, key: Tuple[str, ...], amount: float = 1) -> None:
        self._values[key] = self._values.get(key, 0.0) + amount

    def _set(self, key: Tuple[str, ...], value: float) -> None:
        self._values[key] = value

    def _observe(self, key: Tuple[str, ...], value: float) -> None:
        self._set(key, value)

    # direct ops when no labels
    def inc(self, amount: float = 1) -> None:  # pragma: no cover - simple
        self.labels().inc(amount)

    def set(self, value: float) -> None:  # pragma: no cover - simple
        self.labels().set(value)

    def observe(self, value: float) -> None:  # pragma: no cover - simple
        self.labels().observe(value)


class Counter(_Metric):
    pass


class Gauge(_Metric):
    pass


class Histogram(_Metric):
    def __init__(
        self,
        name: str,
        documentation: str | None = None,
        labelnames: Iterable[str] | None = None,
        registry: CollectorRegistry | None = None,
        buckets: Iterable[float] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(name, documentation, labelnames, registry, **kwargs)
        # ensure buckets sorted and include +Inf as final bucket
        b = list(buckets or [])
        b.sort()
        self.buckets = b
        self._values: Dict[Tuple[str, ...], Dict[str, float]] = {}

    def _observe(self, key: Tuple[str, ...], value: float) -> None:
        data = self._values.setdefault(
            key,
            {
                "sum": 0.0,
                "count": 0.0,
                **{str(b): 0.0 for b in self.buckets},
                "+Inf": 0.0,
            },
        )
        data["sum"] += value
        data["count"] += 1
        placed = False
        for b in self.buckets:
            if value <= b:
                data[str(b)] += 1
                placed = True
        data["+Inf"] += 1


def generate_latest(registry: CollectorRegistry | None = None) -> bytes:
    registry = registry or _REGISTRY
    lines = []
    for metric in registry:
        if isinstance(metric, Histogram):
            for labels, data in metric._values.items():
                label_str = ",".join(
                    f'{name}="{val}"' for name, val in zip(metric.labelnames, labels)
                )
                for b in metric.buckets:
                    lines.append(
                        f"{metric.name}_bucket{{{label_str},le=\"{b}\"}} {data[str(b)]}"
                    )
                lines.append(
                    f"{metric.name}_bucket{{{label_str},le=\"+Inf\"}} {data['+Inf']}"
                )
                lines.append(f"{metric.name}_sum{{{label_str}}} {data['sum']}")
                lines.append(f"{metric.name}_count{{{label_str}}} {data['count']}")
        else:
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

