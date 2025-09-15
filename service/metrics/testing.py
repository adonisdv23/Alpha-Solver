"""Testing helpers for the metrics client."""
from __future__ import annotations

from service.metrics import client as mclient


def reset_registry() -> None:
    """Reset the client registry and re-register app-level metrics."""
    mclient.registry = mclient.CollectorRegistry()
    try:
        from service import app as app_module

        app_module.MET_ROUTE_DECISION = mclient.counter(
            "alpha_solver_route_decision_total",
            "route decision counts",
            labelnames=("decision",),
        )
        app_module.MET_BUDGET_VERDICT = mclient.counter(
            "alpha_solver_budget_verdict_total",
            "budget verdicts",
            labelnames=("verdict",),
        )
        app_module.MET_LATENCY_MS = mclient.histogram(
            "alpha_solver_latency_ms",
            "latency ms",
            labelnames=("stage",),
            buckets=(5, 10, 25, 50, 100, 250, 500, 1000, 2000),
        )
        app_module.MET_TOKENS_TOTAL = mclient.counter(
            "alpha_solver_tokens_total",
            "token count",
            labelnames=("kind",),
        )
        app_module.MET_COST_USD_TOTAL = mclient.counter(
            "alpha_solver_cost_usd_total",
            "usd cost",
            labelnames=("kind",),
        )
    except Exception:  # pragma: no cover - app not imported
        pass
