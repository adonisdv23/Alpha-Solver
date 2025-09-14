from __future__ import annotations

"""Prometheus metrics exporter for Alpha Solver.

This module exposes :class:`MetricsExporter` which registers a small set of
counters, gauges and histograms and serves them via a Starlette application.
The exporter is intentionally lightweight and avoids exporting values that may
contain secrets or PII.
"""

from dataclasses import dataclass
from typing import Optional

import sys

# Ensure the real ``prometheus_client`` package from site-packages is used even
# if a lightweight stub exists in the repository (its path would otherwise take
# precedence in ``sys.path``).
_site_packages = [p for p in sys.path if "site-packages" in p]
sys.path = _site_packages + [p for p in sys.path if p not in _site_packages]

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


_REDACTION_VALUES = {"pii_raw"}
_REDACTION_SUFFIXES = ("_secret", "_token")


def _sanitize(value: Optional[str]) -> Optional[str]:
    """Redact values that may contain secrets.

    Any value equal to ``pii_raw`` or ending with ``_secret`` or ``_token`` is
    replaced with the string ``redacted``.
    """

    if value is None:
        return None
    if value in _REDACTION_VALUES or value.endswith(_REDACTION_SUFFIXES):
        return "redacted"
    return value


@dataclass
class MetricsExporter:
    """Minimal Prometheus metrics exporter."""

    namespace: str = "alpha_solver"

    def __post_init__(self) -> None:  # noqa: D401 - dataclass post init
        self.registry = CollectorRegistry()

    # -- registration -----------------------------------------------------
    def register_route_explain(self) -> None:
        """Register counters and gauges related to routing decisions."""

        self.decision_counter = Counter(
            "route_decision_total",
            "Total number of routing decisions",
            ["decision"],
            namespace=self.namespace,
            registry=self.registry,
        )
        self.budget_verdict_counter = Counter(
            "budget_verdict_total",
            "Total number of budget verdicts",
            ["budget_verdict"],
            namespace=self.namespace,
            registry=self.registry,
        )
        self.policy_verdict_counter = Counter(
            "policy_verdict_total",
            "Total number of policy verdicts",
            ["policy_verdict"],
            namespace=self.namespace,
            registry=self.registry,
        )
        self.confidence_gauge = Gauge(
            "confidence",
            "Latest decision confidence",
            namespace=self.namespace,
            registry=self.registry,
        )

    def register_cost_latency(self) -> None:
        """Register latency histogram and resource cost counters."""

        self.latency_histogram = Histogram(
            "latency_ms",
            "Latency in milliseconds",
            namespace=self.namespace,
            registry=self.registry,
            buckets=(10, 50, 100, 250, 500, 1000, 2500, 5000, 10000),
        )
        self.tokens_counter = Counter(
            "tokens_total",
            "Total tokens consumed",
            namespace=self.namespace,
            registry=self.registry,
        )
        self.cost_counter = Counter(
            "cost_usd_total",
            "Total cost in USD",
            namespace=self.namespace,
            registry=self.registry,
        )

    # -- recording --------------------------------------------------------
    def record_event(
        self,
        *,
        decision: str,
        confidence: float,
        budget_verdict: Optional[str],
        latency_ms: Optional[float],
        tokens: Optional[int],
        cost_usd: Optional[float],
        policy_verdict: Optional[str] = None,
    ) -> None:
        """Record a single routing event.

        Parameters mirror the metrics that are exported. Any sensitive values are
        sanitized before being emitted.
        """

        if hasattr(self, "decision_counter"):
            self.decision_counter.labels(decision=_sanitize(decision)).inc()
            self.confidence_gauge.set(confidence)
        if hasattr(self, "budget_verdict_counter") and budget_verdict is not None:
            self.budget_verdict_counter.labels(
                budget_verdict=_sanitize(budget_verdict)
            ).inc()
        if hasattr(self, "policy_verdict_counter") and policy_verdict is not None:
            self.policy_verdict_counter.labels(
                policy_verdict=_sanitize(policy_verdict)
            ).inc()
        if hasattr(self, "latency_histogram") and latency_ms is not None:
            self.latency_histogram.observe(latency_ms)
        if hasattr(self, "tokens_counter") and tokens is not None:
            self.tokens_counter.inc(tokens)
        if hasattr(self, "cost_counter") and cost_usd is not None:
            self.cost_counter.inc(cost_usd)

    # -- app --------------------------------------------------------------
    def app(self) -> Starlette:
        """Return a Starlette application exposing ``/metrics``."""

        async def metrics_endpoint(request):  # pragma: no cover - simple wrapper
            data = generate_latest(self.registry)
            return PlainTextResponse(data, media_type=CONTENT_TYPE_LATEST)

        return Starlette(routes=[Route("/metrics", metrics_endpoint)])
