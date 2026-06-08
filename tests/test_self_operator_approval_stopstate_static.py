"""Static approval-gate and stop-state tests for inert Self Operator fixtures."""
from __future__ import annotations

from tests.helpers.self_operator_static_scan import FIXTURE_ROOT, finding_ids, scan_path


def fixture(name: str):
    return FIXTURE_ROOT / name


def test_missing_explicit_operator_confirmation_returns_approval_gate_required() -> None:
    findings = scan_path(fixture("missing_operator_confirmation.json"))
    assert "SELF_OPERATOR_APPROVAL_GATE_REQUIRED" in finding_ids(findings)
    assert "SELF_OPERATOR_ARTIFACT_SCHEMA_INCOMPLETE" not in finding_ids(findings)
    assert "SELF_OPERATOR_STOP_STATE_REQUIRED" not in finding_ids(findings)


def test_missing_stop_state_returns_stop_state_required() -> None:
    findings = scan_path(fixture("incomplete_artifact_schema.json"))
    assert "SELF_OPERATOR_STOP_STATE_REQUIRED" in finding_ids(findings)
