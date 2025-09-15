"""Compat wrapper around the metrics client used in tests and dashboards."""

from __future__ import annotations

from threading import Lock
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route
from starlette.testclient import TestClient

from service.metrics import client as mclient

Counter = mclient.Counter
Histogram = mclient.Histogram

_lock = Lock()
_REGISTRY = mclient.registry
_METRICS_CREATED = False

ROUTE_DECISION: Counter
BUDGET_VERDICT: Counter
TOKENS: Counter
COST_USD: Counter
LATENCY_MS: Histogram
_BUDGET_LABEL = "budget_verdict"


def _ensure_metrics() -> None:
    global _METRICS_CREATED, ROUTE_DECISION, BUDGET_VERDICT, TOKENS, COST_USD, LATENCY_MS
    if _METRICS_CREATED:
        return
    with _lock:
        if _METRICS_CREATED:
            return
        try:
            from service import app as app_module

            ROUTE_DECISION = app_module.MET_ROUTE_DECISION
            BUDGET_VERDICT = app_module.MET_BUDGET_VERDICT
            TOKENS = app_module.MET_TOKENS_TOTAL
            COST_USD = app_module.MET_COST_USD_TOTAL
            LATENCY_MS = app_module.MET_LATENCY_MS
            global _BUDGET_LABEL
            _BUDGET_LABEL = "verdict"
        except Exception:
            ROUTE_DECISION = Counter(
                "alpha_solver_route_decision_total",
                "route decisions",
                ["decision"],
                registry=_REGISTRY,
            )
            BUDGET_VERDICT = Counter(
                "alpha_solver_budget_verdict_total",
                "budget verdicts",
                ["budget_verdict"],
                registry=_REGISTRY,
            )
            TOKENS = Counter(
                "alpha_solver_tokens_total",
                "tokens used",
                ["kind"],
                registry=_REGISTRY,
            )
            COST_USD = Counter(
                "alpha_solver_cost_usd_total",
                "cost (USD)",
                ["kind"],
                registry=_REGISTRY,
            )
            LATENCY_MS = Histogram(
                "alpha_solver_latency_ms",
                "latency ms",
                ["stage"],
                registry=_REGISTRY,
                buckets=[5, 10, 25, 50, 100, 250, 500, 1000, 2000],
            )
        _METRICS_CREATED = True


class MetricsExporter:
    def __init__(self, namespace: str = "alpha_solver") -> None:
        self.namespace = namespace
        _ensure_metrics()

    def asgi_app(self):
        _ensure_metrics()

        async def metrics(_request):
            ct, payload = mclient.scrape()
            return Response(payload, media_type=ct)

        return Starlette(routes=[Route("/metrics", metrics)])

    # Back-compat alias some callers may use
    def app(self):  # pragma: no cover - legacy path
        return self.asgi_app()

    def test_client(self) -> TestClient:
        return TestClient(self.asgi_app())

    @staticmethod
    def _redact(d: dict) -> dict:
        return {
            k: v
            for k, v in d.items()
            if k != "pii_raw" and not (k.endswith("_token") or k.endswith("_secret"))
        }

    def record_event(
        self,
        *,
        decision: str,
        confidence: float | None = None,
        budget_verdict: str | None = None,
        latency_ms: float | None = None,
        tokens: int | None = None,
        cost_usd: float | None = None,
        policy_verdict: str | None = None,
    ) -> None:
        _ensure_metrics()
        d = decision or "unknown"
        ROUTE_DECISION.labels(decision=d).inc()
        if budget_verdict:
            BUDGET_VERDICT.labels(**{_BUDGET_LABEL: budget_verdict}).inc()
        if tokens is not None:
            TOKENS.labels(kind="generic").inc(tokens)
        if cost_usd is not None:
            COST_USD.labels(kind="generic").inc(cost_usd)
        if latency_ms is not None:
            LATENCY_MS.labels(stage="generic").observe(latency_ms)


__all__ = ["MetricsExporter", "_REGISTRY", "Counter"]

