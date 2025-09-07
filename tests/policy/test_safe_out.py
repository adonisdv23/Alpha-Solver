from __future__ import annotations

import json

from alpha.policy.safe_out import SafeOutPolicy


def _synthetic(confidence: float) -> dict:
    return {
        "answer": "ans",
        "confidence": confidence,
        "path": [],
        "explored_nodes": 0,
        "config": {},
        "reason": "ok",
    }


def test_safe_out_pass_through():
    policy = SafeOutPolicy()
    tot = _synthetic(0.80)
    result = policy.apply(tot, "q")
    assert result["route"] == "tot"
    assert result["reason"] == "ok"
    assert json.dumps(result)


def test_safe_out_cot_fallback():
    policy = SafeOutPolicy(enable_cot_fallback=True)
    tot = _synthetic(0.55)
    result = policy.apply(tot, "q")
    assert result["route"] == "cot_fallback"
    assert result["reason"] == "low_confidence"
    assert result["cot"] is not None
    assert json.dumps(result)


def test_safe_out_best_effort():
    policy = SafeOutPolicy(enable_cot_fallback=False)
    tot = _synthetic(0.55)
    result = policy.apply(tot, "q")
    assert result["route"] == "best_effort"
    assert result["reason"] == "low_confidence"
    assert result["cot"] is None
    assert json.dumps(result)
