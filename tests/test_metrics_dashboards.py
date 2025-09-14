import json
import time
from pathlib import Path

from starlette.testclient import TestClient

from service.metrics.exporter import MetricsExporter


def _scrape(client: TestClient) -> str:
    return client.get("/metrics").text


def test_metrics_exporter_registers_and_scrapes():
    exporter = MetricsExporter()
    exporter.register_route_explain()
    exporter.register_cost_latency()
    exporter.record_event(
        decision="allow",
        confidence=0.9,
        budget_verdict="within",
        latency_ms=5.0,
        tokens=3,
        cost_usd=0.02,
        policy_verdict="ok",
    )
    client = TestClient(exporter.app())
    body = _scrape(client)
    assert "alpha_solver_route_decision_total" in body
    assert "alpha_solver_budget_verdict_total" in body
    assert "alpha_solver_policy_verdict_total" in body
    assert "alpha_solver_latency_ms_bucket" in body
    assert "alpha_solver_tokens_total" in body
    assert "alpha_solver_cost_usd_total" in body
    assert "alpha_solver_confidence" in body


def test_record_event_updates_counters_histograms():
    exporter = MetricsExporter()
    exporter.register_route_explain()
    exporter.register_cost_latency()
    exporter.record_event(
        decision="allow",
        confidence=0.5,
        budget_verdict="within",
        latency_ms=123.0,
        tokens=7,
        cost_usd=0.03,
        policy_verdict="pass",
    )
    client = TestClient(exporter.app())
    metrics_text = _scrape(client)
    metrics = {}
    for line in metrics_text.splitlines():
        if not line or line.startswith("#"):
            continue
        name_and_labels, value = line.split()
        if "{" in name_and_labels:
            name, labels_str = name_and_labels.split("{", 1)
            labels_str = labels_str.rstrip("}")
            labels = tuple(
                sorted(
                    (part.split("=", 1)[0], part.split("=", 1)[1].strip('"'))
                    for part in labels_str.split(",")
                    if part
                )
            )
        else:
            name = name_and_labels
            labels = tuple()
        metrics[(name, labels)] = float(value)
    assert metrics[("alpha_solver_route_decision_total", (("decision", "allow"),))] == 1.0
    assert metrics[("alpha_solver_budget_verdict_total", (("budget_verdict", "within"),))] == 1.0
    assert metrics[("alpha_solver_policy_verdict_total", (("policy_verdict", "pass"),))] == 1.0
    assert metrics[("alpha_solver_tokens_total", tuple())] == 7.0
    assert metrics[("alpha_solver_cost_usd_total", tuple())] == 0.03
    assert metrics[("alpha_solver_latency_ms_count", tuple())] == 1.0
    assert metrics[("alpha_solver_latency_ms_sum", tuple())] == 123.0
    assert metrics[("alpha_solver_confidence", tuple())] == 0.5


def test_performance_scrape_p95_under_200ms():
    exporter = MetricsExporter()
    exporter.register_route_explain()
    exporter.register_cost_latency()
    client = TestClient(exporter.app())
    durations = []
    for _ in range(5):
        start = time.monotonic()
        for _ in range(100):
            exporter.record_event(
                decision="allow",
                confidence=0.1,
                budget_verdict="ok",
                latency_ms=1.0,
                tokens=1,
                cost_usd=0.001,
                policy_verdict="ok",
            )
        _scrape(client)
        durations.append(time.monotonic() - start)
    durations.sort()
    p95 = durations[int(len(durations) * 0.95)]
    assert p95 < 0.2


def test_dashboards_are_json_and_have_min_panels():
    base = Path("dashboards")

    with open(base / "alpha_observability.json", "r", encoding="utf-8") as fh:
        obs = json.load(fh)
    assert len(obs["panels"]) >= 3
    obs_exprs = [p["targets"][0]["expr"] for p in obs["panels"]]
    assert any(
        "rate(alpha_solver_route_decision_total{decision=\"allow\"}[5m])" in e
        for e in obs_exprs
    )
    assert any(
        "sum by (budget_verdict)(alpha_solver_budget_verdict_total)" in e
        for e in obs_exprs
    )
    assert any(
        "histogram_quantile(0.95, sum(rate(alpha_solver_latency_ms_bucket[5m])) by (le))"
        in e
        for e in obs_exprs
    )

    with open(base / "cost_budget.json", "r", encoding="utf-8") as fh:
        cost = json.load(fh)
    assert len(cost["panels"]) >= 3
    cost_exprs = [p["targets"][0]["expr"] for p in cost["panels"]]
    assert any("sum(rate(alpha_solver_tokens_total[5m]))" in e for e in cost_exprs)
    assert any("sum(rate(alpha_solver_cost_usd_total[5m]))" in e for e in cost_exprs)
    assert any("avg(alpha_solver_confidence)" in e for e in cost_exprs)


def test_no_pii_in_metrics_labels_or_values():
    exporter = MetricsExporter()
    exporter.register_route_explain()
    exporter.record_event(
        decision="pii_raw",
        confidence=1.0,
        budget_verdict="foo_secret",
        latency_ms=None,
        tokens=None,
        cost_usd=None,
        policy_verdict="bar_token",
    )
    client = TestClient(exporter.app())
    text = _scrape(client)
    assert "pii_raw" not in text
    assert "foo_secret" not in text
    assert "bar_token" not in text
    assert "redacted" in text
