from __future__ import annotations

import pytest

from alpha.policy.safe_out import SafeOutPolicy
from alpha.reasoning.tot import Node, TreeOfThoughtSolver
from alpha.core.replay import ReplayHarness
from alpha.core.telemetry import validate_event
from alpha_solver_entry import _tree_of_thought


def test_safe_out_threshold_edge() -> None:
    policy = SafeOutPolicy(low_conf_threshold=0.5)
    res = policy.apply({"answer": "hi", "confidence": 0.5}, "q")
    assert res["route"] == "tot"


def test_safe_out_no_fallback() -> None:
    policy = SafeOutPolicy(low_conf_threshold=0.9, enable_cot_fallback=False)
    res = policy.apply({"answer": "hi", "confidence": 0.1}, "q")
    assert res["route"] == "best_effort"


def test_dynamic_prune_removes_low_nodes() -> None:
    solver = TreeOfThoughtSolver(seed=0)
    high = Node("hi", ("hi",), 1, score=0.9, id=1)
    low = Node("lo", ("lo",), 1, score=0.1, id=2)
    solver._frontier = [solver._priority(high), solver._priority(low)]
    solver._retrace_and_prune(0.9)
    assert len(solver._frontier) == 1


def test_replay_harness_determinism(tmp_path, enforce_accessibility) -> None:
    harness1 = ReplayHarness(base_dir=tmp_path)
    query = "The cat sits. It is fun. We play."
    result = _tree_of_thought(query, replay_harness=harness1)
    enforce_accessibility(result["final_answer"])
    session_id = harness1.save()
    recorded = harness1.events.copy()

    harness2 = ReplayHarness(base_dir=tmp_path)
    session = harness2.load(session_id)
    _tree_of_thought(query, replay_harness=harness2)
    def strip_ts(events):
        cleaned = []
        for ev in events:
            ev = dict(ev)
            ev.pop("timestamp", None)
            cleaned.append(ev)
        return cleaned

    assert strip_ts(harness2.events) == strip_ts(session.events) == strip_ts(recorded)


def test_telemetry_schema_validation_pass() -> None:
    validate_event({"session_id": "s", "event": "e", "timestamp": 0, "version": "1", "data": {}})


def test_telemetry_schema_validation_fail() -> None:
    with pytest.raises(ValueError):
        validate_event({"session_id": "s"})
