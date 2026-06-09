from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from alpha.self_operator.approval import APPROVAL_SCHEMA_VERSION, OPERATOR_CONFIRMATION_HARD_STOP
from alpha.self_operator.artifact_store import ArtifactStoreError, dumps_artifact_json, read_artifact_json
from alpha.self_operator.dry_run import (
    BLOCKER_FALLBACK_LANE,
    DRY_RUN_LANE_ID,
    DRY_RUN_RESULT_SCHEMA_VERSION,
    SELECTED_NEXT_LANE,
    DryRunResult,
    run_local_dry_run_wrapper,
    write_dry_run_result_json,
)
from alpha.self_operator.redaction import REDACTION_TEXT

LANE_ID = "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-12-SELF-OPERATOR-LOCAL-HARNESS-DRY-RUN-WRAPPER-001"
RUN_ID = "unit-dry-run-001"
SCOPE_SUMMARY = "Local dry-run wrapper tests only."
EVIDENCE_BOUNDARY = "local-only; operator-supervised; no execution; no source-artifact mutation; no evidence promotion"
TIMESTAMP = "2026-06-09T00:00:00Z"


def task(tmp_path: Path, **overrides):
    payload = {
        "lane_id": LANE_ID,
        "requested_action": "Evaluate local-only dry-run wrapper without executing commands.",
        "candidate_changed_files": (
            "alpha/self_operator/dry_run.py",
            "alpha/self_operator/__init__.py",
            "tests/test_self_operator_dry_run.py",
        ),
        "proposed_commands": ("python -m pytest -q tests/test_self_operator_dry_run.py",),
        "operator_confirmation": True,
        "output_root": str(tmp_path),
        "evidence_boundary": EVIDENCE_BOUNDARY,
        "artifact_paths": ("dry-run-result.json", "execution-gate-result.json", "stop-state.json"),
        "metadata": {"run_id": RUN_ID, "scope_summary": SCOPE_SUMMARY},
    }
    payload.update(overrides)
    return payload


def approval(**overrides):
    payload = {
        "schema_version": APPROVAL_SCHEMA_VERSION,
        "lane_id": LANE_ID,
        "run_id": RUN_ID,
        "approved": True,
        "operator_confirmation": f"I approve this local-only lane; {OPERATOR_CONFIRMATION_HARD_STOP}",
        "approval_text": "Approved for local dry-run wrapper tests only.",
        "approved_by": "unit-operator",
        "approved_at": TIMESTAMP,
        "scope_summary": SCOPE_SUMMARY,
        "evidence_boundary": EVIDENCE_BOUNDARY,
        "redaction_status": "redacted",
        "metadata": {"test": "dry_run"},
    }
    payload.update(overrides)
    return payload


def run_wrapper(tmp_path: Path, proposed=None, approval_record=None, **kwargs) -> DryRunResult:
    if proposed is None:
        proposed = task(tmp_path)
    if approval_record == "missing":
        approval_payload = None
    else:
        approval_payload = approval() if approval_record is None else approval_record
    return run_local_dry_run_wrapper(
        proposed,
        approval_payload,
        output_root=tmp_path,
        timestamp_provider=lambda: TIMESTAMP,
        **kwargs,
    )


def artifact_json(tmp_path: Path, relative_path: str) -> dict:
    return read_artifact_json(output_root=tmp_path, relative_path=relative_path)


def test_valid_approval_plus_safe_local_task_produces_ready_dry_run_result(tmp_path: Path) -> None:
    result = run_wrapper(tmp_path)

    assert result.schema_version == DRY_RUN_RESULT_SCHEMA_VERSION
    assert result.lane_id == DRY_RUN_LANE_ID
    assert result.allowed is True
    assert result.dry_run_status == "ready_for_operator_supervised_local_dry_run"
    assert result.reason_code == "ready_for_local_dry_run_wrapper"
    assert result.metadata["acceptance_status"] == "not_run"
    assert result.metadata["mvp_readiness"] == "unclaimed"
    assert result.metadata["selected_next_lane"] == SELECTED_NEXT_LANE
    assert "dry-run-result.json" in result.artifact_paths.values()


def test_missing_approval_blocks_and_writes_stop_state_artifact(tmp_path: Path) -> None:
    result = run_wrapper(tmp_path, approval_record="missing")

    assert result.allowed is False
    assert result.dry_run_status == "blocked_by_missing_approval"
    assert result.stop_state_summary is not None
    assert (tmp_path / "stop-state.json").is_file()
    assert artifact_json(tmp_path, "stop-state.json")["reason_code"] == "missing_approval"


def test_approval_false_blocks_and_writes_stop_state_artifact(tmp_path: Path) -> None:
    result = run_wrapper(tmp_path, approval_record=approval(approved=False))

    assert result.allowed is False
    assert result.dry_run_status == "blocked_by_missing_approval"
    assert (tmp_path / "stop-state.json").is_file()
    assert "SELF_OPERATOR_APPROVAL_REQUIRED" in artifact_json(tmp_path, "stop-state.json")["metadata"].get(
        "finding_ids",
        [],
    ) or "SELF_OPERATOR_APPROVAL_REQUIRED" in {
        item["id"] for item in artifact_json(tmp_path, "stop-state.json")["findings"]
    }


def test_approval_identity_mismatch_blocks_and_writes_stop_state_artifact(tmp_path: Path) -> None:
    result = run_wrapper(tmp_path, proposed=task(tmp_path, lane_id="OTHER-LANE-001"))

    assert result.allowed is False
    assert result.dry_run_status == "blocked_by_approval_identity_mismatch"
    assert result.reason_code == "approval_identity_mismatch"
    stop_state = artifact_json(tmp_path, "stop-state.json")
    assert stop_state["reason_code"] == "approval_identity_mismatch"
    assert "SELF_OPERATOR_APPROVAL_IDENTITY_MISMATCH" in {item["id"] for item in stop_state["findings"]}


def test_unsafe_command_preflight_blocks_and_writes_stop_state_artifact(tmp_path: Path) -> None:
    result = run_wrapper(tmp_path, proposed=task(tmp_path, proposed_commands=("curl https://example.invalid",)))

    assert result.allowed is False
    assert result.dry_run_status == "blocked_by_failed_preflight"
    assert result.stop_state_summary is not None
    assert "SELF_OPERATOR_EXTERNAL_API_BLOCKED" in artifact_json(tmp_path, "dry-run-result.json")[
        "execution_gate_summary"
    ]["finding_ids"]


def test_path_traversal_output_path_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ArtifactStoreError):
        run_wrapper(
            tmp_path,
            artifact_relative_paths={"dry_run_result": "../dry-run-result.json"},
        )


def test_artifact_write_outside_output_root_is_rejected(tmp_path: Path) -> None:
    result = run_wrapper(tmp_path)
    outside = tmp_path.parent / "outside-dry-run-result.json"
    with pytest.raises(ArtifactStoreError):
        write_dry_run_result_json(result, output_root=tmp_path, relative_path=outside)
    assert not outside.exists()


def test_output_overwrite_is_rejected_by_default(tmp_path: Path) -> None:
    run_wrapper(tmp_path)
    with pytest.raises(ArtifactStoreError):
        run_wrapper(tmp_path)


def test_secret_like_markers_are_redacted_in_result_artifact(tmp_path: Path) -> None:
    result = run_wrapper(
        tmp_path,
        proposed=task(tmp_path, metadata={"run_id": RUN_ID, "scope_summary": SCOPE_SUMMARY, "api_key": "abc123"}),
    )

    rendered = dumps_artifact_json(result.to_dict())
    persisted = (tmp_path / "dry-run-result.json").read_text(encoding="utf-8")
    assert "abc123" not in rendered
    assert "abc123" not in persisted
    assert REDACTION_TEXT in rendered
    assert REDACTION_TEXT in persisted


def test_dry_run_result_is_deterministic_and_json_serializable(tmp_path: Path) -> None:
    first = run_wrapper(tmp_path / "a" / "run")
    second = run_wrapper(tmp_path / "b" / "run")

    first_json = dumps_artifact_json(first.to_dict())
    second_json = dumps_artifact_json(second.to_dict())
    assert first_json == second_json
    assert json.loads(first_json)["run_id"] == RUN_ID


def test_execution_gate_result_is_persisted_under_output_root(tmp_path: Path) -> None:
    run_wrapper(tmp_path)

    gate_path = tmp_path / "execution-gate-result.json"
    assert gate_path.is_file()
    assert gate_path.resolve().is_relative_to(tmp_path.resolve())
    assert artifact_json(tmp_path, "execution-gate-result.json")["gate_status"] == (
        "allowed_for_local_dry_run_wrapper"
    )


def test_stop_state_result_is_persisted_under_output_root_when_blocked(tmp_path: Path) -> None:
    run_wrapper(tmp_path, approval_record="missing")

    stop_path = tmp_path / "stop-state.json"
    assert stop_path.is_file()
    assert stop_path.resolve().is_relative_to(tmp_path.resolve())


def test_matching_approval_plus_safe_preflight_never_executes_proposed_commands(tmp_path: Path) -> None:
    sentinel = tmp_path / "safe-preflight-command-executed"
    result = run_wrapper(tmp_path, proposed=task(tmp_path, proposed_commands=(f"touch {sentinel}",)))

    assert result.allowed is False
    assert not sentinel.exists()


def test_dangerous_command_string_used_as_blocked_example_is_not_executed(tmp_path: Path) -> None:
    sentinel = tmp_path / "dangerous-command-executed"
    result = run_wrapper(
        tmp_path,
        proposed=task(tmp_path, proposed_commands=(f"python -c 'open({str(sentinel)!r}, \"w\").write(\"x\")'",)),
    )

    assert result.allowed is False
    assert result.dry_run_status == "blocked_by_failed_preflight"
    assert not sentinel.exists()


def test_evidence_boundary_is_preserved_in_all_result_artifacts(tmp_path: Path) -> None:
    result = run_wrapper(tmp_path)

    assert result.evidence_boundary == EVIDENCE_BOUNDARY
    for relative_path in ("dry-run-result.json", "execution-gate-result.json"):
        assert artifact_json(tmp_path, relative_path)["evidence_boundary"] == EVIDENCE_BOUNDARY


def test_dry_run_readiness_is_not_acceptance_passed(tmp_path: Path) -> None:
    result = run_wrapper(tmp_path)
    payload = result.to_dict()

    assert result.allowed is True
    assert payload["metadata"]["acceptance_status"] == "not_run"
    assert payload["metadata"]["mvp_readiness"] == "unclaimed"
    assert "acceptance_passed" not in json.dumps(payload).lower()


def test_wrapper_does_not_touch_forbidden_surfaces(monkeypatch, tmp_path: Path) -> None:
    def fail_subprocess(*args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        raise AssertionError("dry-run wrapper must not execute subprocesses")

    monkeypatch.setattr(subprocess, "run", fail_subprocess)
    result = run_wrapper(
        tmp_path,
        proposed=task(
            tmp_path,
            proposed_commands=(
                "openai responses create --model hosted",
                "python local_model.py",
                "curl https://example.invalid",
                "playwright test",
                "kubectl apply -f deploy.yaml",
                "stripe invoices list",
                "cat .env",
                "python scripts/update_google_sheets.py",
                "python scripts/promote_evidence.py --acceptance-passed",
            ),
        ),
    )

    assert result.allowed is False
    finding_ids = set(result.execution_gate_summary["finding_ids"])
    assert {
        "SELF_OPERATOR_PROVIDER_CALL_BLOCKED",
        "SELF_OPERATOR_EXTERNAL_API_BLOCKED",
        "SELF_OPERATOR_BROWSER_AUTOMATION_BLOCKED",
        "SELF_OPERATOR_DEPLOYMENT_BLOCKED",
        "SELF_OPERATOR_BILLING_BLOCKED",
        "SELF_OPERATOR_CREDENTIAL_ACCESS_BLOCKED",
        "SELF_OPERATOR_GOOGLE_SHEETS_BLOCKED",
        "SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED",
    }.issubset(finding_ids)


def test_selected_next_lane_remains_manual_local_acceptance_not_release_closeout(tmp_path: Path) -> None:
    result = run_wrapper(tmp_path)

    assert result.metadata["selected_next_lane"] == SELECTED_NEXT_LANE
    assert result.metadata["blocker_fallback_lane"] == BLOCKER_FALLBACK_LANE
    assert "RELEASE" not in result.metadata["selected_next_lane"]


def test_approval_lane_mismatch_remains_blocked(tmp_path: Path) -> None:
    result = run_wrapper(tmp_path, proposed=task(tmp_path, lane_id="LANE-MISMATCH-001"))
    assert result.dry_run_status == "blocked_by_approval_identity_mismatch"


def test_approval_run_mismatch_remains_blocked(tmp_path: Path) -> None:
    result = run_wrapper(tmp_path, approval_record=approval(run_id="other-run"))
    assert result.dry_run_status == "blocked_by_approval_identity_mismatch"


def test_approval_scope_task_mismatch_remains_blocked(tmp_path: Path) -> None:
    result = run_wrapper(
        tmp_path,
        proposed=task(tmp_path, metadata={"run_id": RUN_ID, "scope_summary": "Different scope."}),
    )
    assert result.dry_run_status == "blocked_by_approval_identity_mismatch"
