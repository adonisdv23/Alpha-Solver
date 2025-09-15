import json
import time
from pathlib import Path

from service.metrics.exporter import MetricsExporter


# ---------------------------------------------------------------------------
# Metrics exporter tests

def _scrape(exporter: MetricsExporter) -> str:
    client = exporter.test_client()
    resp = client.get("/metrics")
    assert resp.status_code == 200
    return resp.text


def test_metrics_exporter_registers_and_scrapes():
    exp = MetricsExporter()
    exp.register_route_explain()
    exp.register_cost_latency()
    exp.record_event(
        decision="allow",
        confidence=0.9,
        budget_verdict="under",
        latency_ms=12.0,
        tokens=3,
        cost_usd=0.01,
        policy_verdict="clean",
    )
    metrics_text = _scrape(exp)
    assert "alpha_solver_route_decision_total" in metrics_text
    assert "alpha_solver_budget_verdict_total" in metrics_text
    assert "alpha_solver_latency_ms_bucket" in metrics_text


def test_record_event_updates_counters_histograms():
    exp = MetricsExporter()
    exp.register_route_explain()
    exp.register_cost_latency()
    for _ in range(3):
        exp.record_event(
            decision="allow",
            confidence=0.5,
            budget_verdict="under",
            latency_ms=100,
            tokens=10,
            cost_usd=0.01,
            policy_verdict="clean",
        )
    text = _scrape(exp)
    assert 'alpha_solver_route_decision_total{decision="allow"} 3.0' in text
    assert 'alpha_solver_budget_verdict_total{budget_verdict="under"} 3.0' in text
    assert 'alpha_solver_tokens_total 30.0' in text
    assert 'alpha_solver_cost_usd_total 0.03' in text


def test_performance_scrape_p95_under_200ms():
    exp = MetricsExporter()
    exp.register_route_explain()
    exp.register_cost_latency()
    start = time.monotonic()
    for _ in range(100):
        exp.record_event(
            decision="allow",
            confidence=0.5,
            budget_verdict="under",
            latency_ms=10,
            tokens=1,
            cost_usd=0.001,
            policy_verdict="clean",
        )
    _scrape(exp)
    duration_ms = (time.monotonic() - start) * 1000
    assert duration_ms < 200


# ---------------------------------------------------------------------------
# Dashboard tests

def _load_dash(path: str) -> dict:
    with open(Path("dashboards") / path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def test_dashboards_are_json_and_have_min_panels():
    obs = _load_dash("alpha_observability.json")
    cost = _load_dash("cost_budget.json")

    assert len(obs["panels"]) >= 3
    assert len(cost["panels"]) >= 3

    obs_exprs = [t["expr"] for p in obs["panels"] for t in p.get("targets", [])]
    assert 'rate(alpha_solver_route_decision_total{decision="allow"}[5m])' in obs_exprs
    assert 'sum by (budget_verdict)(alpha_solver_budget_verdict_total)' in obs_exprs
    assert (
        'histogram_quantile(0.95, sum(rate(alpha_solver_latency_ms_bucket[5m])) by (le))'
        in obs_exprs
    )

    cost_exprs = [t["expr"] for p in cost["panels"] for t in p.get("targets", [])]
    assert 'sum(rate(alpha_solver_tokens_total[5m]))' in cost_exprs
    assert 'sum(rate(alpha_solver_cost_usd_total[5m]))' in cost_exprs
    assert 'avg(alpha_solver_confidence)' in cost_exprs


def test_no_pii_in_metrics_labels_or_values():
    exp = MetricsExporter()
    exp.register_route_explain()
    exp.register_cost_latency()
    exp.record_event(
        decision="pii_raw",
        confidence=0.1,
        budget_verdict="under_secret",
        latency_ms=1,
        tokens=1,
        cost_usd=0.001,
        policy_verdict="over_token",
    )
    text = _scrape(exp)
    assert "pii_raw" not in text
    assert "under_secret" not in text
    assert "over_token" not in text
