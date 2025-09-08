from __future__ import annotations

import logging
from typing import Any, Dict

import pytest

from alpha.policy.safe_out_sm import SOConfig, SafeOutStateMachine


def _tot(conf: float) -> Dict[str, Any]:
    return {
        "answer": "ans",
        "confidence": conf,
        "path": [],
        "explored_nodes": 0,
        "config": {},
        "reason": "ok",
    }


EXPECTED_KEYS = {
    "final_answer",
    "route",
    "confidence",
    "reason",
    "notes",
    "tot",
    "cot",
    "phases",
}


@pytest.mark.parametrize(
    "conf, enable_cot, route, phases, reason",
    [
        (0.80, True, "tot", ["init", "assess", "finalize"], "ok"),
        (0.55, True, "cot_fallback", ["init", "assess", "fallback", "finalize"], "low_confidence"),
        (0.55, False, "best_effort", ["init", "assess", "fallback", "finalize"], "low_confidence"),
    ],
)
def test_safe_out_state_machine(conf, enable_cot, route, phases, reason, caplog):
    cfg = SOConfig(low_conf_threshold=0.60, enable_cot_fallback=enable_cot, seed=1, max_cot_steps=2)
    sm = SafeOutStateMachine(cfg)
    tot = _tot(conf)
    with caplog.at_level(logging.INFO):
        r1 = sm.run(tot, "q")
        r2 = sm.run(tot, "q")
        r3 = sm.run(tot, "q")
    assert r1 == r2 == r3
    assert r1["route"] == route
    assert r1["phases"] == phases
    assert r1["reason"] == reason
    assert set(r1.keys()) == EXPECTED_KEYS
    assert any("safe_out_phase" in rec.message for rec in caplog.records)
