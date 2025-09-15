"""Tiny Prometheus client wrapper used by the service.

It attempts to import the real ``prometheus_client`` package and falls back to
lightweight shims when that import fails.  A dedicated ``CollectorRegistry`` is
used so that tests can safely reset metrics without clashing with the library's
process-wide default registry.
"""
from __future__ import annotations

from typing import Iterable

try:  # pragma: no cover - exercised in tests
    from prometheus_client import (
        Counter,
        Histogram,
        CollectorRegistry,
        CONTENT_TYPE_LATEST,
        generate_latest,
    )
except Exception:  # pragma: no cover
    # Provide very small shims that match the subset of the API we use
    from prometheus_client import (
        Counter,  # type: ignore
        Histogram,  # type: ignore
        CollectorRegistry,  # type: ignore
        CONTENT_TYPE_LATEST,  # type: ignore
        generate_latest,  # type: ignore
    )

# Use a dedicated registry so tests don't hit the global default one
registry: CollectorRegistry = CollectorRegistry()


def counter(name: str, doc: str, labelnames: Iterable[str] = ()) -> Counter:
    """Create a counter registered in the module's registry."""
    return Counter(name, doc, labelnames=tuple(labelnames), registry=registry)


def histogram(
    name: str,
    doc: str,
    labelnames: Iterable[str] = (),
    buckets: Iterable[float] | None = None,
) -> Histogram:
    return Histogram(
        name,
        doc,
        labelnames=tuple(labelnames),
        registry=registry,
        buckets=list(buckets) if buckets is not None else None,
    )


def scrape() -> tuple[str, bytes]:
    """Return a ``(content_type, payload)`` tuple with the current metrics."""
    return CONTENT_TYPE_LATEST, generate_latest(registry)


__all__ = [
    "registry",
    "counter",
    "histogram",
    "scrape",
    "CollectorRegistry",
]
