from __future__ import annotations

import json
import subprocess
from pathlib import Path

from alpha.self_operator.approval import APPROVAL_SCHEMA_VERSION, OPERATOR_CONFIRMATION_HARD_STOP, ApprovalRecord
from alpha.self_operator.artifact_store import dumps_artifact_json, read_artifact_json
from alpha.self_operator.execution_gate import evaluate_execution_gate, write_execution_gate_result_json

LANE_ID = "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-11-SELF-OPERATOR-APPROVAL-STOPSTATE-GATE-FOUNDATION-001"
RUN_ID = "unit-run-gate-001"
EVIDENCE_BOUNDARY = "local-only; no execution; no source-artifact mutation; no evidence promotion"
SCOPE_SUMMARY = "Approval, stop-state, and execution-gate foundation only."


def task(tmp_path: Path, **overrides):
    payload = {
        "lane_id": LANE_ID,
        "requested_action": "Evaluate local-only execution gate foundation.",
        "candidate_changed_files": (
            "alpha/self_operator/execution_gate.py",
            "tests/test_self_operator_execution_gate.py",
        ),
        "proposed_commands": ("python -m pytest -q tests/test_self_operator_execution_gate.py",),
        "operator_confirmation": True,
        "output_root": str(tmp_path),
        "evidence_boundary": EVIDENCE_BOUNDARY,
        "artifact_paths": ("gate-result.json",),
        "metadata": {"run_id": RUN_ID, "scope_summary": SCOPE_SUMMARY},
    }
    payload.update(overrides)
    return payload


def approval(**overrides) -> ApprovalRecord:
    payload = {
        "schema_version": APPROVAL_SCHEMA_VERSION,
        "lane_id": LANE_ID,
        "run_id": RUN_ID,
        "approved": True,
        "operator_confirmation": f"I approve this local-only lane; {OPERATOR_CONFIRMATION_HARD_STOP}",
        "approval_text": "Approved for local gate foundation tests only.",
        "approved_by": "unit-operator",
        "approved_at": "2026-06-09T00:00:00Z",
        "scope_summary": SCOPE_SUMMARY,
        "evidence_boundary": EVIDENCE_BOUNDARY,
        "redaction_status": "redacted",
        "metadata": {"test": "execution_gate"},
    }
    payload.update(overrides)
    return ApprovalRecord(**payload)


def assert_identity_mismatch_blocked(result) -> None:  # noqa: ANN001
    assert result.allowed_for_local_dry_run is False
    assert result.gate_status == "blocked_by_approval_identity_mismatch"
    assert result.reason_code == "approval_identity_mismatch"
    assert result.stop_state_record is not None
    assert result.stop_state_record.reason_code == "approval_identity_mismatch"
    assert "SELF_OPERATOR_APPROVAL_IDENTITY_MISMATCH" in {finding.id for finding in result.findings}


def test_missing_approval_returns_blocked_result_and_stop_state_record(tmp_path: Path) -> None:
    result = evaluate_execution_gate(task(tmp_path), None, timestamp_provider=lambda: "2026-06-09T00:00:00Z")
    assert result.allowed_for_local_dry_run is False
    assert result.gate_status == "blocked_by_missing_approval"
    assert result.stop_state_record is not None
    assert result.stop_state_record.reason_code == "missing_approval"


def test_approval_false_returns_blocked_result_and_stop_state_record(tmp_path: Path) -> None:
    result = evaluate_execution_gate(task(tmp_path), approval(approved=False))
    assert result.allowed_for_local_dry_run is False
    assert result.gate_status == "blocked_by_missing_approval"
    assert result.stop_state_record is not None
    assert "SELF_OPERATOR_APPROVAL_REQUIRED" in {finding.id for finding in result.findings}


def test_valid_approval_plus_failed_preflight_returns_blocked_result_and_stop_state_record(tmp_path: Path) -> None:
    result = evaluate_execution_gate(task(tmp_path, requested_action=""), approval())
    assert result.allowed_for_local_dry_run is False
    assert result.gate_status == "unclear_requires_operator_review"
    assert result.stop_state_record is not None


def test_valid_approval_plus_unsafe_command_remains_blocked(tmp_path: Path) -> None:
    result = evaluate_execution_gate(task(tmp_path, proposed_commands=("curl https://example.invalid",)), approval())
    assert result.allowed_for_local_dry_run is False
    assert result.gate_status == "blocked_by_failed_preflight"
    assert "SELF_OPERATOR_EXTERNAL_API_BLOCKED" in {finding.id for finding in result.findings}


def test_approval_lane_mismatch_blocks_with_stop_state_record(tmp_path: Path) -> None:
    result = evaluate_execution_gate(
        task(tmp_path, lane_id="ALPHA-SOLVER-POST-LEVEL-3-LEVEL-11-DIFFERENT-LANE-001"),
        approval(),
        timestamp_provider=lambda: "2026-06-09T00:00:00Z",
    )
    assert_identity_mismatch_blocked(result)
    rendered = dumps_artifact_json(result.to_dict())
    assert rendered == dumps_artifact_json(
        evaluate_execution_gate(
            task(tmp_path, lane_id="ALPHA-SOLVER-POST-LEVEL-3-LEVEL-11-DIFFERENT-LANE-001"),
            approval(),
            timestamp_provider=lambda: "2026-06-09T00:00:00Z",
        ).to_dict()
    )
    assert json.loads(rendered)["stop_state_record"]["reason_code"] == "approval_identity_mismatch"


def test_approval_run_mismatch_blocks_when_run_identity_is_available(tmp_path: Path) -> None:
    result = evaluate_execution_gate(task(tmp_path), approval(run_id="unit-run-gate-other"))
    assert_identity_mismatch_blocked(result)
    assert result.run_id == RUN_ID


def test_approval_scope_mismatch_blocks_when_scope_identity_is_available(tmp_path: Path) -> None:
    result = evaluate_execution_gate(
        task(tmp_path, metadata={"run_id": RUN_ID, "scope_summary": "Different task scope."}),
        approval(),
    )
    assert_identity_mismatch_blocked(result)


def test_identity_mismatch_does_not_execute_proposed_task_commands(tmp_path: Path) -> None:
    sentinel = tmp_path / "identity-mismatch-command-executed"
    result = evaluate_execution_gate(
        task(
            tmp_path,
            lane_id="ALPHA-SOLVER-POST-LEVEL-3-LEVEL-11-DIFFERENT-LANE-001",
            proposed_commands=(f"touch {sentinel}",),
        ),
        approval(),
    )
    assert_identity_mismatch_blocked(result)
    assert not sentinel.exists()


def test_identity_mismatch_artifact_write_stays_under_temporary_output_root(tmp_path: Path) -> None:
    result = evaluate_execution_gate(task(tmp_path), approval(run_id="unit-run-gate-other"))
    assert_identity_mismatch_blocked(result)
    path = write_execution_gate_result_json(
        result,
        output_root=tmp_path,
        relative_path="records/identity-mismatch-gate-result.json",
    )
    assert path.is_relative_to(tmp_path)
    persisted = read_artifact_json(output_root=tmp_path, relative_path="records/identity-mismatch-gate-result.json")
    assert persisted["reason_code"] == "approval_identity_mismatch"


def test_valid_approval_plus_safe_local_preflight_returns_allowed_for_local_dry_run_result(tmp_path: Path) -> None:
    result = evaluate_execution_gate(task(tmp_path), approval())
    assert result.allowed_for_local_dry_run is True
    assert result.gate_status == "allowed_for_local_dry_run_wrapper"
    assert result.reason_code == "ready_for_local_dry_run_wrapper"
    assert result.stop_state_record is None


def test_no_commands_are_executed(tmp_path: Path) -> None:
    sentinel = tmp_path / "proposed-task-command-executed"
    result = evaluate_execution_gate(
        task(tmp_path, proposed_commands=(f"touch {sentinel}",)),
        approval(),
    )
    assert result.allowed_for_local_dry_run is False
    assert not sentinel.exists()


def test_forbidden_surfaces_are_not_called(monkeypatch, tmp_path: Path) -> None:
    def fail_subprocess(*args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        raise AssertionError("execution gate must not execute subprocesses")

    monkeypatch.setattr(subprocess, "run", fail_subprocess)
    result = evaluate_execution_gate(
        task(
            tmp_path,
            proposed_commands=(
                "openai responses create --model hosted",
                "playwright test",
                "kubectl apply -f deploy.yaml",
                "stripe invoices list",
                "cat .env",
                "python scripts/update_google_sheets.py",
                "python scripts/promote_evidence.py --acceptance-passed",
            ),
        ),
        approval(),
    )
    assert result.allowed_for_local_dry_run is False
    assert {
        "SELF_OPERATOR_PROVIDER_CALL_BLOCKED",
        "SELF_OPERATOR_BROWSER_AUTOMATION_BLOCKED",
        "SELF_OPERATOR_DEPLOYMENT_BLOCKED",
        "SELF_OPERATOR_BILLING_BLOCKED",
        "SELF_OPERATOR_CREDENTIAL_ACCESS_BLOCKED",
        "SELF_OPERATOR_GOOGLE_SHEETS_BLOCKED",
        "SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED",
    }.issubset({finding.id for finding in result.findings})


def test_gate_result_is_deterministic_and_json_serializable(tmp_path: Path) -> None:
    kwargs = {"timestamp_provider": lambda: "2026-06-09T00:00:00Z"}
    result = evaluate_execution_gate(task(tmp_path), approval(), **kwargs)
    rendered = dumps_artifact_json(result.to_dict())
    assert rendered == dumps_artifact_json(evaluate_execution_gate(task(tmp_path), approval(), **kwargs).to_dict())
    assert json.loads(rendered)["lane_id"] == LANE_ID


def test_gate_result_can_be_persisted_under_temporary_output_root(tmp_path: Path) -> None:
    result = evaluate_execution_gate(task(tmp_path), approval())
    path = write_execution_gate_result_json(result, output_root=tmp_path, relative_path="records/gate-result.json")
    assert path.is_file()
    assert read_artifact_json(output_root=tmp_path, relative_path="records/gate-result.json")["run_id"] == RUN_ID


def test_gate_result_preserves_evidence_boundary(tmp_path: Path) -> None:
    result = evaluate_execution_gate(task(tmp_path), approval())
    assert result.evidence_boundary == EVIDENCE_BOUNDARY
    assert result.to_dict()["evidence_boundary"] == EVIDENCE_BOUNDARY
