import json
import logging
import pytest

from alpha.core.governance import (
    AuditLogger,
    BudgetCapGate,
    CircuitBreaker,
    GovernanceError,
    PolicyDryRun,
)


def test_budget_cap_gate():
    gate = BudgetCapGate(max_steps=1)
    gate.check(1)
    with pytest.raises(GovernanceError):
        gate.check(2)


def test_circuit_breaker_trips():
    breaker = CircuitBreaker(max_errors=1, window=100)
    breaker.record_error()
    with pytest.raises(GovernanceError):
        breaker.record_error()


def test_audit_logger_writes(tmp_path):
    p = tmp_path / "audit.jsonl"
    logger = AuditLogger(str(p))
    logger.log_event("test", {"x": 1})
    lines = p.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    rec = json.loads(lines[0])
    assert rec["event"] == "test"
    assert rec["data"] == {"x": 1}


def test_policy_dryrun_supresses(caplog):
    gate = BudgetCapGate(max_steps=1)
    dry = PolicyDryRun(enabled=True)
    gate.check(1)
    with caplog.at_level(logging.WARNING):
        try:
            gate.check(2)
        except GovernanceError as err:
            dry.handle(err)
    assert "policy dry-run" in caplog.text
