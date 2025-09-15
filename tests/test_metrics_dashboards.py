import time
import json
from pathlib import Path
import pytest
import re

from service.metrics.exporter import MetricsExporter, _REGISTRY, Counter


@pytest.mark.metrics
def test_metrics_exporter_series_and_performance():
    errors = Counter(
        "alpha_solver_errors_total",
        "errors",
        ["type"],
        registry=_REGISTRY,
    )
    exp = MetricsExporter()
    client = exp.test_client()

    t0 = time.perf_counter()
    for i in range(50):
        exp.record_event(decision="allow", latency_ms=5, tokens=10, cost_usd=0.01, budget_verdict="ok")
    for i in range(50):
        exp.record_event(decision="deny", latency_ms=7, tokens=5, cost_usd=0.005, budget_verdict="over")
    errors.labels(type="internal").inc()
    text = client.get("/metrics").text
    elapsed_ms = (time.perf_counter() - t0) * 1000

    assert elapsed_ms < 200
    assert 'alpha_solver_route_decision_total{decision="allow"}' in text
    assert "alpha_solver_budget_verdict_total" in text
    assert "alpha_solver_latency_ms_bucket" in text
    assert "alpha_solver_errors_total" in text
    assert "alpha_solver_tokens_total" in text
    assert "alpha_solver_cost_usd_total" in text

    assert "pii_raw" not in text
    assert not re.search(r"_token([^s]|$)", text)
    assert "_secret" not in text

    # cover redaction helper
    assert MetricsExporter._redact({
        "keep": 1,
        "pii_raw": "secret",
        "api_token": "t",
        "db_secret": "s",
    }) == {"keep": 1}


@pytest.mark.metrics
def test_dashboards_have_required_panels():
    def _load(name: str) -> dict:
        with open(Path("dashboards") / name, encoding="utf-8") as fh:
            return json.load(fh)

    obs = _load("alpha_observability.json")
    cost = _load("cost_budget.json")
    assert len(obs["panels"]) >= 3
    assert len(cost["panels"]) >= 3
    obs_exprs = [t["expr"] for p in obs["panels"] for t in p.get("targets", [])]
    assert 'rate(alpha_solver_route_decision_total{decision="allow"}[5m])' in obs_exprs
    assert 'sum by (budget_verdict)(alpha_solver_budget_verdict_total)' in obs_exprs
    assert ('histogram_quantile(0.95, sum(rate(alpha_solver_latency_ms_bucket[5m])) by (le))'
            in obs_exprs)
    cost_exprs = [t["expr"] for p in cost["panels"] for t in p.get("targets", [])]
    assert 'sum(rate(alpha_solver_tokens_total[5m]))' in cost_exprs
    assert 'sum(rate(alpha_solver_cost_usd_total[5m]))' in cost_exprs
    assert 'avg(alpha_solver_confidence)' in cost_exprs


@pytest.mark.metrics
def test_new_grafana_dashboards():
    base = Path("observability/grafana/dashboards")
    overview = json.loads((base / "alpha_solver_overview.json").read_text())
    gates = json.loads((base / "alpha_gates.json").read_text())
    adapters = json.loads((base / "alpha_adapters.json").read_text())

    over_titles = [p["title"] for p in overview["panels"]]
    assert "Latency p95 ms" in over_titles
    assert "Error Rate %" in over_titles
    assert "Throughput req/s" in over_titles
    over_exprs = "\n".join(t["expr"] for p in overview["panels"] for t in p.get("targets", []))
    for name in [
        "alpha_solver_latency_ms_bucket",
        "alpha_solver_errors_total",
        "alpha_solver_route_decision_total",
        "alpha_solver_budget_verdict_total",
        "alpha_solver_tokens_total",
        "alpha_solver_cost_usd_total",
    ]:
        assert name in over_exprs
    lat_panel = next(p for p in overview["panels"] if p["title"] == "Latency p95 ms")
    assert any("trace" in l.get("url", "") for l in lat_panel.get("links", []))

    gate_exprs = "\n".join(t["expr"] for p in gates["panels"] for t in p.get("targets", []))
    for name in [
        "alpha_solver_gate_low_confidence_total",
        "alpha_solver_gate_clarify_total",
        "alpha_solver_gate_budget_block_total",
        "alpha_solver_gate_policy_redaction_total",
        "alpha_solver_gate_latency_ms_bucket",
    ]:
        assert name in gate_exprs

    ad_exprs = "\n".join(t["expr"] for p in adapters["panels"] for t in p.get("targets", []))
    for name in [
        "alpha_solver_adapter_calls_total",
        "alpha_solver_adapter_latency_ms_bucket",
        "alpha_solver_adapter_circuit_open",
    ]:
        assert name in ad_exprs
