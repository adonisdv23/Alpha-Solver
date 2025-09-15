"""Prometheus metrics exporter for Alpha Solver.

This module exposes the :class:`MetricsExporter` which provides a tiny
wrapper around ``prometheus_client`` registry objects.  The exporter exposes
an ASGI application serving ``/metrics`` compatible with the Prometheus text
format.  Only the standard library and ``prometheus_client`` are used to keep
runtime light-weight.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import importlib.util
import sys
from pathlib import Path

if "prometheus_client" in sys.modules:
    del sys.modules["prometheus_client"]

def _load_prometheus_client():
    for path in sys.path:
        if "site-packages" not in path:
            continue
        candidate = Path(path) / "prometheus_client" / "__init__.py"
        if candidate.exists():
            spec = importlib.util.spec_from_file_location(
                "prometheus_client", candidate
            )
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            sys.modules["prometheus_client"] = module
            spec.loader.exec_module(module)  # type: ignore[assignment]
            return module
    raise ImportError("prometheus_client package not found")

prom = _load_prometheus_client()
CollectorRegistry = prom.CollectorRegistry
Counter = prom.Counter
Gauge = prom.Gauge
Histogram = prom.Histogram
generate_latest = prom.generate_latest

from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route

__all__ = ["MetricsExporter"]


def _is_redacted(name: str) -> bool:
    """Return ``True`` if a metric label should be redacted.

    Labels named ``pii_raw`` or ending with ``_secret``/``_token`` are
    considered sensitive and are never exported.
    """

    return name == "pii_raw" or name.endswith("_secret") or name.endswith("_token")


def _sanitize_labels(labels: Dict[str, str]) -> Dict[str, str]:
    """Filter out sensitive labels and normalise their values.

    Any label names matching :func:`_is_redacted` are dropped.  Values that
    themselves look sensitive are replaced with ``"redacted"``.
    """

    clean: Dict[str, str] = {}
    for key, value in labels.items():
        if _is_redacted(key):
            continue
        if isinstance(value, str) and _is_redacted(value):
            clean[key] = "redacted"
        else:
            clean[key] = value
    return clean


@dataclass
class _Metrics:
    decision: Counter
    budget: Counter
    policy: Counter
    confidence: Gauge
    latency: Histogram
    tokens: Counter
    cost: Counter


class MetricsExporter:
    """Small helper used by tests and services to expose Prometheus metrics."""

    def __init__(self, namespace: str = "alpha_solver") -> None:
        self.namespace = namespace
        self.registry = CollectorRegistry()
        self._metrics: Optional[_Metrics] = None

    # ------------------------------------------------------------------
    # Metric registration
    def register_route_explain(self) -> None:
        """Register counters and gauges for route explanations.

        Metrics registered:
        ``*_route_decision_total`` – counter labelled by ``decision``.
        ``*_budget_verdict_total`` – counter labelled by ``budget_verdict``.
        ``*_policy_verdict_total`` – counter labelled by ``policy_verdict``.
        ``*_confidence`` – gauge storing the latest confidence score.
        """

        if self._metrics is not None:
            return

        decision = Counter(
            f"{self.namespace}_route_decision_total",
            "Route decision count",
            ["decision"],
            registry=self.registry,
        )
        budget = Counter(
            f"{self.namespace}_budget_verdict_total",
            "Budget verdict count",
            ["budget_verdict"],
            registry=self.registry,
        )
        policy = Counter(
            f"{self.namespace}_policy_verdict_total",
            "Policy verdict count",
            ["policy_verdict"],
            registry=self.registry,
        )
        confidence = Gauge(
            f"{self.namespace}_confidence",
            "Latest confidence score",
            registry=self.registry,
        )
        # Placeholder metrics for latency, tokens and cost. These may be
        # redefined later if :meth:`register_cost_latency` is invoked.
        latency = Histogram(
            f"{self.namespace}_latency_ms",
            "Request latency in milliseconds",
            buckets=(1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000),
            registry=self.registry,
        )
        tokens = Counter(
            f"{self.namespace}_tokens_total",
            "Total tokens consumed",
            registry=self.registry,
        )
        cost = Counter(
            f"{self.namespace}_cost_usd_total",
            "Total cost in USD",
            registry=self.registry,
        )

        self._metrics = _Metrics(
            decision=decision,
            budget=budget,
            policy=policy,
            confidence=confidence,
            latency=latency,
            tokens=tokens,
            cost=cost,
        )

    def register_cost_latency(self) -> None:
        """No-op for backwards compatibility.

        The latency, token and cost metrics are initialised in
        :meth:`register_route_explain`, so this method simply ensures metrics
        are registered and is kept for API parity with the specification.
        """

        if self._metrics is None:
            self.register_route_explain()
        # Metrics already created; nothing further required.

    # ------------------------------------------------------------------
    # Recording
    def record_event(
        self,
        *,
        decision: str,
        confidence: float,
        budget_verdict: Optional[str],
        latency_ms: Optional[float],
        tokens: Optional[int],
        cost_usd: Optional[float],
        policy_verdict: Optional[str] | None = None,
    ) -> None:
        """Record a single routing event.

        Parameters mirror those described in the specification.  Any label
        values that look sensitive are redacted prior to export.
        """

        if self._metrics is None:
            raise RuntimeError("metrics not registered; call register_route_explain")

        m = self._metrics

        # Counters / gauge for routing decisions and verdicts
        labels = _sanitize_labels({"decision": decision})
        m.decision.labels(**labels).inc()
        if budget_verdict:
            bv = _sanitize_labels({"budget_verdict": budget_verdict})
            m.budget.labels(**bv).inc()
        if policy_verdict:
            pv = _sanitize_labels({"policy_verdict": policy_verdict})
            m.policy.labels(**pv).inc()

        m.confidence.set(confidence)

        # Cost / latency metrics
        if latency_ms is not None:
            m.latency.observe(latency_ms)
        if tokens is not None:
            m.tokens.inc(tokens)
        if cost_usd is not None:
            m.cost.inc(cost_usd)

    # ------------------------------------------------------------------
    # Application
    def app(self) -> Starlette:
        """Return an ASGI application exposing ``/metrics``."""

        async def metrics_endpoint(_request) -> Response:
            data = generate_latest(self.registry)
            return Response(
                data,
                media_type="text/plain; version=0.0.4; charset=utf-8",
            )

        return Starlette(routes=[Route("/metrics", metrics_endpoint)])

    def test_client(self):
        from starlette.testclient import TestClient

        return TestClient(self.app())
