import time

import alpha_solver_cli
from service.gating.gates import GateConfig, evaluate_gates


def test_allow_when_confident_and_budget_ok():
    decision, explain = evaluate_gates(0.9, 1000, {})
    assert decision == "allow"
    assert explain["budget_verdict"] == "ok"


def test_clarify_on_low_confidence():
    decision, explain = evaluate_gates(0.2, 1000, {})
    assert decision == "clarify"
    assert explain["budget_verdict"] == "clarify"


def test_clarify_on_low_budget():
    decision, explain = evaluate_gates(0.9, 10, {})
    assert decision == "clarify"
    assert explain["budget_verdict"] == "low"


def test_block_when_policy_flag_block():
    decision, _ = evaluate_gates(0.9, 1000, {"block": True})
    assert decision == "block"


def test_clarify_band_between_low_and_clarify_threshold():
    decision, _ = evaluate_gates(0.4, 1000, {})
    assert decision == "clarify"


def test_budget_verdict_present_in_route_explain():
    _, explain = evaluate_gates(0.8, 1000, {})
    assert "budget_verdict" in explain


def test_p95_latency_under_5ms():
    cfg = GateConfig()
    durations = []
    for _ in range(1000):
        start = time.perf_counter()
        evaluate_gates(0.8, 1000, {}, cfg)
        durations.append(time.perf_counter() - start)
    durations.sort()
    p95 = durations[int(len(durations) * 0.95)]
    assert p95 < 0.005


def test_deterministic_outcomes():
    inputs = (0.42, 500, {"block": False})
    decision1, explain1 = evaluate_gates(*inputs)
    decision2, explain2 = evaluate_gates(*inputs)
    assert decision1 == decision2
    assert explain1 == explain2


def test_cli_overrides_thresholds(monkeypatch):
    captured = {}

    def fake_tree(query, **kwargs):
        captured.update(kwargs)
        return {"ok": True}

    monkeypatch.setattr(alpha_solver_cli, "_tree_of_thought", fake_tree)
    alpha_solver_cli.main([
        "question",
        "--low-conf-threshold",
        "0.1",
        "--clarify-conf-threshold",
        "0.7",
        "--min-budget-tokens",
        "512",
        "--no-cot-fallback",
    ])
    assert captured["low_conf_threshold"] == 0.1
    assert captured["clarify_conf_threshold"] == 0.7
    assert captured["min_budget_tokens"] == 512
    assert captured["enable_cot_fallback"] is False
