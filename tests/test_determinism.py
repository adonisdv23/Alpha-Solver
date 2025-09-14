import random
from pathlib import Path

import pytest
import yaml

from service.determinism.harness import DeterminismHarness, inject_factor_noise
from service.determinism.report import summarize, tiebreak_diff


def test_exact_replay_10_of_10():
    events = [
        {"id": 1, "decision": "allow", "confidence": 0.9, "budget_verdict": "ok"}
        for _ in range(10)
    ]
    h = DeterminismHarness()
    result = h.run_replay(events)
    assert result["flaps"] == 0
    assert result["cases"][0]["stable"] is True


def test_no_flaps_with_noise_3pct_on_non_semantic_fields():
    h = DeterminismHarness(runs=20)

    def fn(latency: float) -> dict:
        return {
            "decision": "allow",
            "confidence": 0.9,
            "budget_verdict": "ok",
            "latency_ms": inject_factor_noise(latency, h.factor_noise_pct),
        }

    result = h.run_callable(fn, inputs=[{"id": 0, "latency": 100.0}])
    assert result["flaps"] == 0
    assert result["cases"][0]["stable"] is True


def test_flap_detection_when_decision_changes():
    random.seed(0)
    h = DeterminismHarness(runs=10)

    def flappy() -> dict:
        return {
            "decision": random.choice(["allow", "deny"]),
            "confidence": 0.9,
            "budget_verdict": "ok",
        }

    result = h.run_callable(flappy, inputs=[{"id": 0}])
    assert result["flaps"] == 1
    case = result["cases"][0]
    assert case["stable"] is False
    assert any(d.startswith("decision:") for d in case["diffs"])


def test_report_summarizes_and_diff_is_deterministic():
    a = {"decision": "allow", "confidence": 0.8, "budget_verdict": "ok"}
    b = {"decision": "clarify", "confidence": 0.7, "budget_verdict": "ok"}
    diff1 = tiebreak_diff(a, b, keys=["decision", "confidence", "budget_verdict"])
    diff2 = tiebreak_diff(a, b, keys=["decision", "confidence", "budget_verdict"])
    assert diff1 == diff2 == ["confidence: 0.8 vs 0.7", "decision: allow vs clarify"]
    result = {"total": 1, "flaps": 1, "cases": [{"id": 1, "stable": False, "variants": 2, "first": a, "diffs": diff1, "timings": [0.01]}]}
    summary = summarize(result)
    assert summary["flap_rate"] == 1.0
    assert summary["top_keys"] == {"confidence": 1, "decision": 1}
    assert summary["p95_ms"] >= 10


def test_config_defaults_loaded():
    cfg_path = Path(__file__).resolve().parent.parent / "config" / "determinism.yaml"
    cfg = yaml.safe_load(cfg_path.read_text())
    assert cfg == {
        "runs": 100,
        "factor_noise_pct": 3,
        "float_tol": 1e-6,
        "compare_keys": [
            "decision",
            "confidence",
            "budget_verdict",
            "score",
            "tool",
            "sandbox_decision",
        ],
        "fail_on_flap": True,
    }


def test_ci_gate_blocks_on_any_flap():
    h = DeterminismHarness(runs=5, fail_on_flap=True)
    random.seed(1)

    def flappy() -> dict:
        return {
            "decision": random.choice(["allow", "deny"]),
            "confidence": 0.9,
            "budget_verdict": "ok",
        }

    result = h.run_callable(flappy, inputs=[{"id": 0}])
    with pytest.raises(RuntimeError):
        if h.fail_on_flap and result["flaps"]:
            raise RuntimeError("flaps detected")
