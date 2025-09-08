from alpha.core.budgets import gate_decision
from alpha.core.config import QualityGateConfig


def test_gate_decision_pass_and_fail():
    cfg = QualityGateConfig()
    good = {
        "metrics": {"em": 0.9},
        "latency": {"p95": 700, "p99": 1000},
        "cost_per_call": 0.005,
    }
    passed, reasons = gate_decision(good, cfg)
    assert passed
    assert reasons == []

    bad = {
        "metrics": {"em": 0.8},
        "latency": {"p95": 800, "p99": 1300},
        "cost_per_call": 0.02,
    }
    passed, reasons = gate_decision(bad, cfg)
    assert not passed
    assert reasons
