from __future__ import annotations

import json
import logging
from typing import Dict

import pytest

from alpha.policy.safe_out_sm import SOConfig, SafeOutStateMachine


def _synthetic(confidence: float, reason: str = "ok") -> Dict[str, float | str]:
    return {"answer": "ans", "confidence": confidence, "reason": reason}


@pytest.mark.parametrize(
    "confidence,enable,route,phases",
    [
        (0.80, True, "tot", ["init", "assess", "finalize"]),
        (0.55, True, "cot_fallback", ["init", "assess", "fallback", "finalize"]),
        (0.55, False, "best_effort", ["init", "assess", "fallback", "finalize"]),
    ],
)
def test_state_machine_routes(confidence, enable, route, phases, caplog):
    cfg = SOConfig(enable_cot_fallback=enable)
    sm = SafeOutStateMachine(cfg)
    tot = _synthetic(confidence)
    with caplog.at_level(logging.INFO):
        result = sm.run(tot, "q")
    assert result["route"] == route
    assert result["phases"] == phases
    assert json.dumps(result)
    assert any("safe_out_phase" in r.message for r in caplog.records)


@pytest.mark.parametrize(
    "confidence,reason,enable,route,expected_reason",
    [
        (0.80, "timeout", False, "best_effort", "timeout"),
        (0.55, "below_threshold", True, "cot_fallback", "low_confidence"),
    ],
)
def test_state_machine_edge_cases(confidence, reason, enable, route, expected_reason):
    cfg = SOConfig(enable_cot_fallback=enable)
    sm = SafeOutStateMachine(cfg)
    tot = _synthetic(confidence, reason)
    result = sm.run(tot, "q")
    assert result["route"] == route
    assert result["reason"] == expected_reason
    assert reason in result["notes"]
    assert result["phases"] == ["init", "assess", "fallback", "finalize"]


def test_state_machine_determinism():
    cfg = SOConfig(seed=1)
    runs = [SafeOutStateMachine(cfg).run(_synthetic(0.55), "q") for _ in range(3)]
    assert runs[0] == runs[1] == runs[2]
    sample = runs[0]
    for key in ["final_answer", "route", "confidence", "reason", "notes", "tot", "cot", "phases"]:
        assert key in sample
