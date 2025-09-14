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


def _redact(d: dict) -> dict:
    """Remove keys that could carry PII or secrets."""

    return {
        k: v
        for k, v in d.items()
        if k != "pii_raw" and not (k.endswith("_token") or k.endswith("_secret"))
    }


def _sanitize(value: Optional[str]) -> Optional[str]:
    """Redact string values that may contain PII or secrets."""

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
        self._route_registered = False
        self._cost_registered = False

    # -- registration -----------------------------------------------------
    def register_route_explain(self) -> None:
        """Register counters and gauges related to routing decisions."""

        if self._route_registered:
            return
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
        self.confidence_gauge = Gauge(
            "confidence",
            "Latest decision confidence",
            namespace=self.namespace,
            registry=self.registry,
        )
        self._route_registered = True

    def register_cost_latency(self) -> None:
        """Register latency histogram and resource cost counters."""

        if self._cost_registered:
            return
        self.latency_histogram = Histogram(
            "latency_ms",
            "Latency in milliseconds",
            namespace=self.namespace,
            registry=self.registry,
            buckets=[5, 10, 25, 50, 100, 250, 500, 1000, 2000],
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
        self._cost_registered = True

    # -- recording --------------------------------------------------------
    def record_event(
        self,
        *,
        decision: str,
        confidence: Optional[float] = None,
        budget_verdict: Optional[str] = None,
        latency_ms: Optional[float] = None,
        tokens: Optional[int] = None,
        cost_usd: Optional[float] = None,
        policy_verdict: Optional[str] = None,
    ) -> None:
        """Record a single routing event.

        Parameters mirror the metrics that are exported. Any sensitive values are
        sanitized before being emitted.
        """

        if hasattr(self, "decision_counter"):
            decision_val = _sanitize((
                _redact({"decision": decision or "unknown"}).get("decision")
            )) or "unknown"
            self.decision_counter.labels(decision=decision_val).inc()
            if confidence is not None and hasattr(self, "confidence_gauge"):
                self.confidence_gauge.set(confidence)
        if hasattr(self, "budget_verdict_counter") and budget_verdict is not None:
            red = _redact({"budget_verdict": budget_verdict})
            if "budget_verdict" in red:
                val = _sanitize(red["budget_verdict"])
                self.budget_verdict_counter.labels(budget_verdict=val).inc()
        if hasattr(self, "latency_histogram") and latency_ms is not None:
            self.latency_histogram.observe(latency_ms)
        if hasattr(self, "tokens_counter") and tokens is not None:
            self.tokens_counter.inc(tokens)
        if hasattr(self, "cost_counter") and cost_usd is not None:
            self.cost_counter.inc(cost_usd)
        if policy_verdict is not None:
            _redact({"policy_verdict": policy_verdict})

    # -- app --------------------------------------------------------------
    def app(self) -> Starlette:
        """Return a Starlette application exposing ``/metrics``."""

        async def metrics_endpoint(request):  # pragma: no cover - simple wrapper
            data = generate_latest(self.registry)
            return PlainTextResponse(data, media_type=CONTENT_TYPE_LATEST)

        return Starlette(routes=[Route("/metrics", metrics_endpoint)])
