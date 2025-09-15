import json
import time
import subprocess
from pathlib import Path

import pytest

from service.finops import simulator as fin_sim
from service.finops.simulator import Caps
from service.budget import simulator as svc_sim


@pytest.fixture
def sample_scenarios():
    return [
        {"id": "a", "intent": "test", "prompt_tokens": 100, "completion_tokens": 50, "route": "r"},
        {"id": "b", "intent": "test", "prompt_tokens": 200, "completion_tokens": 100, "route": "r"},
    ]


def test_parity_with_service(sample_scenarios):
    # service estimator
    svc_items = [
        {"id": s["id"], "prompt_tokens": s["prompt_tokens"], "completion_tokens": s["completion_tokens"], "latency_ms": 0.0}
        for s in sample_scenarios
    ]
    svc_models = svc_sim.load_cost_models()
    svc_result = svc_sim.simulate(svc_items, svc_models, provider="openai", model="gpt-4o")

    fin_result = fin_sim.simulate(sample_scenarios, "default")
    assert fin_result["summary"]["total_cost_usd"] == pytest.approx(
        svc_result["totals"]["cost_usd"], rel=0.01
    )


def test_caps_behaviour(sample_scenarios):
    caps = Caps(max_cost_usd=4.0, max_tokens=480, latency_budget_ms=1000)
    warn_result = fin_sim.simulate(sample_scenarios, "default", caps=caps)
    assert warn_result["summary"]["budget_verdict"] == "warn"

    caps = Caps(max_cost_usd=1.0, max_tokens=100, latency_budget_ms=10)
    block_result = fin_sim.simulate(sample_scenarios, "default", caps=caps)
    assert block_result["summary"]["budget_verdict"] == "block"


def test_what_if_delta(sample_scenarios):
    before_cfg = {"model_set": "default"}
    after_cfg = {"model_set": "cheap"}
    comp = fin_sim.compare(before_cfg, after_cfg, sample_scenarios)
    assert comp["after"]["summary"]["total_cost_usd"] < comp["before"]["summary"]["total_cost_usd"]
    assert comp["delta"]["total_cost_usd"] == pytest.approx(
        comp["after"]["summary"]["total_cost_usd"]
        - comp["before"]["summary"]["total_cost_usd"]
    )


def test_cli_outputs(tmp_path, sample_scenarios):
    scen_path = tmp_path / "scen.jsonl"
    with open(scen_path, "w", encoding="utf-8") as f:
        for s in sample_scenarios:
            f.write(json.dumps(s) + "\n")

    out_json = tmp_path / "report.json"
    out_csv = tmp_path / "report.csv"
    cmd = [
        "python",
        "-m",
        "cli.budget_sim",
        "--scenarios",
        str(scen_path),
        "--model-set",
        "default",
        "--out-json",
        str(out_json),
        "--out-csv",
        str(out_csv),
    ]
    subprocess.run(cmd, check=True)

    data = json.loads(out_json.read_text())
    assert "summary" in data and "scenarios" in data
    assert len(data["scenarios"]) == len(sample_scenarios)

    csv_text = out_csv.read_text().strip().splitlines()
    header = csv_text[0].split(",")
    assert header == [
        "id",
        "intent",
        "model_set",
        "route",
        "est_tokens",
        "est_cost_usd",
        "est_latency_ms",
        "verdict",
    ]


def test_performance_50_scenarios():
    scenarios = [
        {"id": str(i), "intent": "t", "prompt_tokens": 50, "completion_tokens": 50, "route": "r"}
        for i in range(50)
    ]
    start = time.perf_counter()
    fin_sim.simulate(scenarios, "default")
    assert time.perf_counter() - start < 5.0


def test_determinism(sample_scenarios):
    res1 = fin_sim.simulate(sample_scenarios, "default")
    res2 = fin_sim.simulate(sample_scenarios, "default")
    assert res1 == res2
