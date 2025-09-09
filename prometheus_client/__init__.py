"""Very small subset of the ``prometheus_client`` API used for tests.

This module implements ``Counter`` and ``Histogram`` collectors and a
``generate_latest`` helper to expose metrics in the Prometheus text format.
It is intentionally tiny to avoid pulling the real dependency.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

CONTENT_TYPE_LATEST = "text/plain; version=0.0.4; charset=utf-8"


_METRICS: List["_Metric"] = []


class _Metric:
    def __init__(self, name: str, doc: str, labelnames: Iterable[str] | None = None):
        self.name = name
        self.doc = doc
        self.labelnames = tuple(labelnames or [])
        self.samples: Dict[Tuple[str, ...], object] = {}
        _METRICS.append(self)

    def labels(self, **kwargs):
        key = tuple(str(kwargs.get(lbl, "")) for lbl in self.labelnames)
        if key not in self.samples:
            self.samples[key] = self._init_value()
        return self._child(self, key)

    def _init_value(self):  # pragma: no cover - overridden
        return 0

    def _child(self, parent, key):  # pragma: no cover - overridden
        raise NotImplementedError


class Counter(_Metric):
    class _Child:
        def __init__(self, parent: "Counter", key: Tuple[str, ...]):
            self.parent = parent
            self.key = key

        def inc(self, amount: int = 1) -> None:
            self.parent.samples[self.key] += amount

    def _child(self, parent, key):
        return Counter._Child(parent, key)


class Histogram(_Metric):
    class _Child:
        def __init__(self, parent: "Histogram", key: Tuple[str, ...]):
            self.parent = parent
            self.key = key

        def observe(self, value: float) -> None:
            self.parent.samples[self.key].append(value)

    def _init_value(self):
        return []

    def _child(self, parent, key):
        return Histogram._Child(parent, key)


def generate_latest() -> bytes:
    lines: List[str] = []
    for metric in _METRICS:
        mtype = "counter" if isinstance(metric, Counter) else "histogram"
        lines.append(f"# HELP {metric.name} {metric.doc}")
        lines.append(f"# TYPE {metric.name} {mtype}")
        for key, value in metric.samples.items():
            labels = []
            for name, val in zip(metric.labelnames, key):
                if val:
                    labels.append(f'{name}="{val}"')
            label_str = f"{{{','.join(labels)}}}" if labels else ""
            val = value if isinstance(metric, Counter) else sum(value)
            lines.append(f"{metric.name}{label_str} {val}")
    return "\n".join(lines).encode("utf-8")


__all__ = [
    "Counter",
    "Histogram",
    "generate_latest",
    "CONTENT_TYPE_LATEST",
]

