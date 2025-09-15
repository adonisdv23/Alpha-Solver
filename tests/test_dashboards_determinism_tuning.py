import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient
from service.metrics import client as mclient

from service.tuning.report_export import export_tuning_report


def test_metrics_names_exposed_via_client():
    original = mclient.registry
    try:
        mclient.registry = mclient.CollectorRegistry()
        mclient.counter("alpha_solver_replay_runs_total", "runs")
        mclient.counter("alpha_solver_replay_flap_total", "flaps")
        mclient.histogram("alpha_solver_latency_ms", "latency", buckets=(1, 2, 3))
        mclient.counter("alpha_solver_route_decision_total", "decisions")

        app = FastAPI()

        @app.get("/metrics")
        def metrics() -> PlainTextResponse:  # pragma: no cover - simple bridge
            ct, payload = mclient.scrape()
            return PlainTextResponse(payload.decode("utf-8"))

        client = TestClient(app)
        text = client.get("/metrics").text
        for name in [
            "alpha_solver_replay_runs_total",
            "alpha_solver_replay_flap_total",
            "alpha_solver_latency_ms_bucket",
            "alpha_solver_route_decision_total",
        ]:
            assert name in text
    finally:
        mclient.registry = original


def test_export_tuning_report_schema(tmp_path: Path):
    sample = {
        "seed": 1,
        "before": {
            "accuracy": 0.78,
            "win_rate": 0.75,
            "weights": {"factor_a": 0.2},
        },
        "after": {
            "accuracy": 0.84,
            "win_rate": 0.82,
            "weights": {"factor_a": 0.25},
        },
        "delta": {"accuracy_pp": 6.0, "win_rate_pp": 7.0},
        "per_factor": [
            {"name": "factor_a", "before": 0.2, "after": 0.25, "delta": 0.05}
        ],
    }
    in_path = tmp_path / "input.json"
    out_path = tmp_path / "tuning_report.json"
    in_path.write_text(json.dumps(sample))
    export_tuning_report(in_path, out_path)
    data = json.loads(out_path.read_text())
    assert set(data) == {
        "seed",
        "before",
        "after",
        "delta",
        "per_factor",
    }
    assert data["before"]["weights"]["factor_a"] == 0.2
    assert data["after"]["weights"]["factor_a"] == 0.25
    assert data["delta"] == {"accuracy_pp": 6.0, "win_rate_pp": 7.0}
    assert data["per_factor"][0]["delta"] == 0.05


def test_dashboards_reference_expected_fields():
    base = Path("observability/grafana/dashboards")
    determinism = json.loads((base / "determinism.json").read_text())
    tuning = json.loads((base / "weights_tuning.json").read_text())

    titles = [p["title"] for p in determinism["panels"]]
    for t in [
        "Replay Pass %",
        "Flap Rate",
        "Runs by Status",
        "Latency p50/p95",
        "Errors Over Time",
        "Recent Replay Failures",
    ]:
        assert t in titles
    exprs = "\n".join(t["expr"] for p in determinism["panels"] for t in p.get("targets", []))
    for name in [
        "alpha_solver_replay_runs_total",
        "alpha_solver_replay_flap_total",
        "alpha_solver_latency_ms_bucket",
        "alpha_solver_route_decision_total",
    ]:
        assert name in exprs

    t_titles = [p["title"] for p in tuning["panels"]]
    for t in [
        "Accuracy BEFORE→AFTER",
        "Win Rate BEFORE→AFTER",
        "Factor Weights",
        "Top Deltas",
        "Report JSON",
    ]:
        assert t in t_titles
    t_exprs = "\n".join(
        tgt.get("expr", "") for p in tuning["panels"] for tgt in p.get("targets", [])
    )
    for key in [
        "before.accuracy",
        "after.accuracy",
        "before.win_rate",
        "after.win_rate",
        "before.weights",
        "after.weights",
        "per_factor",
        "delta",
    ]:
        assert key in t_exprs
    assert "artifacts/tuning_report.json" in json.dumps(tuning)
