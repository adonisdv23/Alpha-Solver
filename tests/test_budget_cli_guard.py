from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from service.budget.simulator import load_cost_models, simulate
from service.budget.guard import BudgetGuard

ROOT = Path(__file__).resolve().parents[0]  # tests directory
REPO_ROOT = ROOT.parent


def run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)
    return subprocess.run(
        [sys.executable, "-m", "service.budget.cli", *args],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
    )


def test_guard_ok_under_thresholds():
    models = load_cost_models()
    items = [
        {"prompt_tokens": 100, "completion_tokens": 0, "latency_ms": 0.0}
    ]
    sim = simulate(items, models, provider="openai", model="gpt-4o")
    guard = BudgetGuard(max_cost_usd=10.0, max_tokens=500)
    res = guard.check(sim)
    assert res["ok"]
    assert res["budget_verdict"] == "ok"
    assert res["route_explain"] == {"decision": "allow", "budget_verdict": "ok"}


def test_guard_blocks_when_over_cost():
    models = load_cost_models()
    items = [
        {"prompt_tokens": 1000, "completion_tokens": 0, "latency_ms": 0.0}
    ]
    sim = simulate(items, models, provider="openai", model="gpt-4o")
    guard = BudgetGuard(max_cost_usd=1.0)
    res = guard.check(sim)
    assert not res["ok"]
    assert res["budget_verdict"] == "over_cost"
    assert res["route_explain"]["decision"] == "block"


def test_guard_blocks_when_over_tokens():
    models = load_cost_models()
    items = [
        {"prompt_tokens": 1000, "completion_tokens": 0, "latency_ms": 0.0}
    ]
    sim = simulate(items, models, provider="openai", model="gpt-4o")
    guard = BudgetGuard(max_cost_usd=100.0, max_tokens=500)
    res = guard.check(sim)
    assert not res["ok"]
    assert res["budget_verdict"] == "over_tokens"
    assert res["route_explain"]["decision"] == "block"


def test_cli_reads_json_and_jsonl_and_sets_exit_codes(tmp_path: Path):
    items = [
        {"prompt_tokens": 1000, "completion_tokens": 0, "latency_ms": 0.0}
    ]
    json_path = tmp_path / "items.json"
    json_path.write_text(json.dumps(items))
    jsonl_path = tmp_path / "items.jsonl"
    with jsonl_path.open("w") as f:
        for it in items:
            f.write(json.dumps(it) + "\n")

    ok_proc = run_cli([
        "--provider", "openai",
        "--model", "gpt-4o",
        "--items", str(json_path),
        "--max-cost", "10",
    ])
    assert ok_proc.returncode == 0, ok_proc.stderr
    verdict_ok = json.loads(ok_proc.stdout.strip().splitlines()[-1])["budget_verdict"]
    assert verdict_ok == "ok"

    bad_proc = run_cli([
        "--provider", "openai",
        "--model", "gpt-4o",
        "--items", str(jsonl_path),
        "--max-cost", "1",
    ])
    assert bad_proc.returncode == 2, bad_proc.stderr
    verdict_bad = json.loads(bad_proc.stdout.strip().splitlines()[-1])["budget_verdict"]
    assert verdict_bad == "over_cost"


def test_cli_writes_jsonl_output_and_contains_route_explain(tmp_path: Path):
    items = [
        {
            "prompt_tokens": 10,
            "completion_tokens": 0,
            "latency_ms": 0.0,
            "pii_raw": "secret",
            "api_token": "123",
        }
    ]
    jsonl_path = tmp_path / "items.jsonl"
    with jsonl_path.open("w") as f:
        for it in items:
            f.write(json.dumps(it) + "\n")
    out_path = tmp_path / "out.jsonl"
    proc = run_cli([
        "--provider", "openai",
        "--model", "gpt-4o",
        "--items", str(jsonl_path),
        "--max-cost", "10",
        "--jsonl-out", str(out_path),
    ])
    assert proc.returncode == 0, proc.stderr
    assert out_path.exists()
    first = json.loads(out_path.read_text().splitlines()[0])
    assert "route_explain" in first
    assert first["route_explain"]["decision"] == "simulate"
    assert "pii_raw" not in first
    assert "api_token" not in first


def test_performance_p95_under_2s_for_200_items():
    models = load_cost_models()
    items = [
        {"prompt_tokens": 100, "completion_tokens": 100, "latency_ms": 1.0}
        for _ in range(200)
    ]
    guard = BudgetGuard(max_cost_usd=1000.0, max_tokens=1000000)
    times: list[float] = []
    for _ in range(20):
        start = time.monotonic()
        sim = simulate(items, models, provider="openai", model="gpt-4o")
        guard.check(sim)
        times.append(time.monotonic() - start)
    times.sort()
    idx = max(0, int(len(times) * 0.95) - 1)
    p95 = times[idx]
    assert p95 < 2.0


def test_deterministic_outputs_plus_minus_point1pct():
    models = load_cost_models()
    items = [
        {"prompt_tokens": 50, "completion_tokens": 25, "latency_ms": 0.0}
        for _ in range(5)
    ]
    sim1 = simulate(items, models, provider="openai", model="gpt-4o")
    sim2 = simulate(items, models, provider="openai", model="gpt-4o")
    guard = BudgetGuard(max_cost_usd=100.0, max_tokens=100000)
    res1 = guard.check(sim1)
    res2 = guard.check(sim2)
    c1 = res1["totals"]["cost_usd"]
    c2 = res2["totals"]["cost_usd"]
    assert c1 == pytest.approx(c2, rel=0.001)
    assert res1["totals"]["tokens"] == res2["totals"]["tokens"]
