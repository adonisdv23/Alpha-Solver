from __future__ import annotations

"""Regression tests for observability and replay features."""

import pytest

from alpha.core.telemetry import validate_event
from alpha.policy.safe_out_sm import SOConfig, SafeOutStateMachine
from alpha.reasoning.tot import TreeOfThoughtSolver
from alpha_solver_entry import _tree_of_thought
from alpha.core.observability import ObservabilityConfig, ObservabilityManager


def test_safe_out_threshold_edge_case() -> None:
    cfg = SOConfig(low_conf_threshold=0.6)
    sm = SafeOutStateMachine(cfg)
    env = sm.run({"answer": "ok", "confidence": 0.6}, "q")
    assert env["route"] == "tot"


def test_safe_out_fallback_route() -> None:
    cfg = SOConfig(low_conf_threshold=0.8, enable_cot_fallback=False)
    sm = SafeOutStateMachine(cfg)
    env = sm.run({"answer": "ok", "confidence": 0.1}, "q")
    assert env["route"] == "best_effort"


def test_tot_pruning_max_nodes() -> None:
    solver = TreeOfThoughtSolver(max_nodes=1, max_depth=2)
    res = solver.solve("hi")
    assert solver._explored_nodes <= 1
    assert "answer" in res


def test_replay_determinism(tmp_path) -> None:
    env1 = _tree_of_thought("demo", record="sess", log_path=str(tmp_path / "log1.jsonl"))
    sid = env1["diagnostics"]["replay_session"]
    env2 = _tree_of_thought("demo", replay=sid, log_path=str(tmp_path / "log2.jsonl"))
    assert env2["solution"] == env1["solution"]
    assert env2["diagnostics"]["replay_session"]


def test_telemetry_schema_validator() -> None:
    event = {
        "session_id": "s",
        "event": "x",
        "timestamp": "t",
        "version": 1,
        "properties": {},
    }
    assert validate_event(event)


def test_telemetry_schema_validator_missing() -> None:
    with pytest.raises(ValueError):
        validate_event({"event": "x"})


def test_offline_mode_disables_telemetry(tmp_path) -> None:
    cfg = ObservabilityConfig(
        enable_telemetry=True,
        telemetry_endpoint="http://example",
        offline_mode=True,
        log_path=str(tmp_path / "log.jsonl"),
    )
    manager = ObservabilityManager(cfg)
    assert manager.telemetry is None


def test_strict_accessibility_failure(monkeypatch) -> None:
    from alpha.core.observability import ObservabilityManager

    def bad_check(self, text):
        return {"readability": 0, "ok": False}

    monkeypatch.setattr(ObservabilityManager, "check_text", bad_check)
    with pytest.raises(ValueError):
        _tree_of_thought("demo", strict_accessibility=True)
