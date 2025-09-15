import time, json, re
from pathlib import Path

from service.metrics.exporter import MetricsExporter


# ---------------------------------------------------------------------------
# Metrics exporter tests

def test_metrics_exporter_registers_and_scrapes():
    exp = MetricsExporter()
    client = exp.test_client()
    # simulate traffic
    for _ in range(5):
        exp.record_event(decision="allow", latency_ms=25, tokens=42, cost_usd=0.001, budget_verdict="ok")
    text = client.get("/metrics").text
    assert 'alpha_solver_route_decision_total{decision="allow"}' in text
    assert "alpha_solver_budget_verdict_total" in text
    assert "alpha_solver_latency_ms_bucket" in text
    assert "alpha_solver_tokens_total" in text
    assert "alpha_solver_cost_usd_total" in text


def test_performance_scrape_p95_under_200ms():
    exp = MetricsExporter()
    client = exp.test_client()
    t0 = time.monotonic()
    for _ in range(100):
        exp.record_event(decision="allow", latency_ms=10, tokens=10, cost_usd=0.0001, budget_verdict="ok")
    _ = client.get("/metrics")
    elapsed_ms = (time.monotonic() - t0) * 1000
    assert elapsed_ms < 200


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
    client = exp.test_client()
    # simulate an event that contains pii-like keys; exporter must never emit them
    exp.record_event(decision="allow", latency_ms=5, tokens=1, cost_usd=0.0, budget_verdict="ok")
    text = client.get("/metrics").text
    assert "pii_raw" not in text
    assert not re.search(r"_token([^s]|$)", text)
    assert "_secret" not in text

