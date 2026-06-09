"""Local-only Self Operator dry-run harness wrapper.

The wrapper is deterministic and evidence-boundary safe. It evaluates preflight
and the corrected execution gate, persists local JSON artifacts, and never
executes proposed commands or calls external systems.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping

from alpha.self_operator.approval import ApprovalRecord
from alpha.self_operator.artifact_store import resolve_artifact_path, write_artifact_json
from alpha.self_operator.execution_gate import (
    ALLOWED_GATE_STATUS,
    ExecutionGateResult,
    evaluate_execution_gate,
    write_execution_gate_result_json,
)
from alpha.self_operator.preflight import PreflightResult, ProposedTask, run_local_preflight
from alpha.self_operator.redaction import redact_value
from alpha.self_operator.stop_state import StopStateRecord, write_stop_state_json

DRY_RUN_RESULT_SCHEMA_VERSION = "self_operator.dry_run_result.v1"
DRY_RUN_LANE_ID = "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-12-SELF-OPERATOR-LOCAL-HARNESS-DRY-RUN-WRAPPER-001"
SELECTED_NEXT_LANE = (
    "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-MANUAL-LOCAL-ACCEPTANCE-PACKET-001"
)
BLOCKER_FALLBACK_LANE = (
    "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-12-SELF-OPERATOR-LOCAL-HARNESS-DRY-RUN-WRAPPER-FIX-001"
)
READY_FOR_OPERATOR_SUPERVISED_LOCAL_DRY_RUN = "ready_for_operator_supervised_local_dry_run"
DEFAULT_ARTIFACT_RELATIVE_PATHS = {
    "dry_run_result": "dry-run-result.json",
    "execution_gate_result": "execution-gate-result.json",
    "stop_state": "stop-state.json",
}
NON_EXECUTION_CONFIRMATION = (
    "wrapper does not execute proposed commands; it only classifies proposed command text"
)
EVIDENCE_BOUNDARY = (
    "local-only; operator-supervised; no execution; no providers or external systems; "
    "no acceptance; no source-artifact mutation; no evidence promotion"
)


@dataclass(frozen=True)
class DryRunResult:
    """Serializable local dry-run wrapper result."""

    schema_version: str
    lane_id: str
    run_id: str
    dry_run_status: str
    allowed: bool
    reason_code: str
    proposed_task_summary: Mapping[str, Any]
    approval_summary: Mapping[str, Any]
    preflight_summary: Mapping[str, Any]
    execution_gate_summary: Mapping[str, Any]
    stop_state_summary: Mapping[str, Any] | None
    artifact_paths: Mapping[str, str]
    output_root_summary: Mapping[str, Any]
    evidence_boundary: str
    redaction_status: str
    non_execution_confirmation: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self, *, redact: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "allowed": self.allowed,
            "approval_summary": dict(self.approval_summary),
            "artifact_paths": dict(self.artifact_paths),
            "dry_run_status": self.dry_run_status,
            "evidence_boundary": self.evidence_boundary,
            "execution_gate_summary": dict(self.execution_gate_summary),
            "lane_id": self.lane_id,
            "metadata": dict(self.metadata),
            "non_execution_confirmation": self.non_execution_confirmation,
            "output_root_summary": dict(self.output_root_summary),
            "preflight_summary": dict(self.preflight_summary),
            "proposed_task_summary": dict(self.proposed_task_summary),
            "reason_code": self.reason_code,
            "redaction_status": self.redaction_status,
            "run_id": self.run_id,
            "schema_version": self.schema_version,
            "stop_state_summary": dict(self.stop_state_summary) if self.stop_state_summary else None,
        }
        return redact_value(payload) if redact else payload


def run_local_dry_run_wrapper(
    proposed_task: ProposedTask | Mapping[str, Any],
    approval_record: ApprovalRecord | Mapping[str, Any] | None,
    *,
    output_root: Path | str,
    preflight_result: PreflightResult | Mapping[str, Any] | None = None,
    timestamp_provider: Callable[[], str] | None = None,
    artifact_relative_paths: Mapping[str, Path | str] | None = None,
    overwrite: bool = False,
) -> DryRunResult:
    """Run the local dry-run wrapper without executing proposed commands.

    The wrapper writes deterministic JSON artifacts below ``output_root`` only.
    Readiness means the proposal is ready for a future operator-supervised local
    dry-run handoff; it is not acceptance, release, or MVP readiness.
    """

    root = Path(output_root)
    artifact_paths = _artifact_relative_paths(artifact_relative_paths)
    _validate_artifact_relative_paths(root, artifact_paths)
    proposed = proposed_task if isinstance(proposed_task, ProposedTask) else ProposedTask.from_mapping(proposed_task)
    proposed = ProposedTask.from_mapping({**proposed.to_dict(), "output_root": str(root)})
    timestamp = timestamp_provider() if timestamp_provider else "1970-01-01T00:00:00Z"
    preflight = _preflight_from_input(preflight_result) if preflight_result else run_local_preflight(proposed)
    gate_result = evaluate_execution_gate(
        proposed,
        approval_record,
        output_root=root,
        preflight_result=preflight,
        timestamp_provider=lambda: timestamp,
    )

    persisted: dict[str, str] = {}
    gate_path = write_execution_gate_result_json(
        gate_result,
        output_root=root,
        relative_path=artifact_paths["execution_gate_result"],
        overwrite=overwrite,
    )
    persisted["execution_gate_result"] = _relative_artifact_path(root, gate_path)

    if gate_result.stop_state_record is not None:
        stop_path = write_stop_state_json(
            gate_result.stop_state_record,
            output_root=root,
            relative_path=artifact_paths["stop_state"],
            overwrite=overwrite,
        )
        persisted["stop_state"] = _relative_artifact_path(root, stop_path)

    planned_dry_run_path = resolve_artifact_path(root, artifact_paths["dry_run_result"])
    persisted["dry_run_result"] = _relative_artifact_path(root, planned_dry_run_path)
    result = _build_dry_run_result(
        proposed=proposed,
        preflight=preflight,
        gate_result=gate_result,
        artifact_paths=persisted,
        output_root=root,
        timestamp=timestamp,
    )
    dry_run_path = write_dry_run_result_json(
        result,
        output_root=root,
        relative_path=artifact_paths["dry_run_result"],
        overwrite=overwrite,
    )
    persisted["dry_run_result"] = _relative_artifact_path(root, dry_run_path)

    return result


def write_dry_run_result_json(
    result: DryRunResult | Mapping[str, Any],
    *,
    output_root: Path | str,
    relative_path: Path | str,
    overwrite: bool = False,
) -> Path:
    """Persist a dry-run result below a caller-provided output root."""

    payload = result.to_dict(redact=True) if isinstance(result, DryRunResult) else result
    return write_artifact_json(payload, output_root=output_root, relative_path=relative_path, overwrite=overwrite)


def _build_dry_run_result(
    *,
    proposed: ProposedTask,
    preflight: PreflightResult,
    gate_result: ExecutionGateResult,
    artifact_paths: Mapping[str, str],
    output_root: Path,
    timestamp: str,
) -> DryRunResult:
    dry_status = _dry_run_status(gate_result)
    return DryRunResult(
        schema_version=DRY_RUN_RESULT_SCHEMA_VERSION,
        lane_id=DRY_RUN_LANE_ID,
        run_id=gate_result.run_id,
        dry_run_status=dry_status,
        allowed=gate_result.allowed_for_local_dry_run,
        reason_code=gate_result.reason_code,
        proposed_task_summary=_proposed_task_summary(proposed),
        approval_summary=gate_result.approval_result_summary,
        preflight_summary=_preflight_summary(preflight),
        execution_gate_summary=_execution_gate_summary(gate_result),
        stop_state_summary=_stop_state_summary(gate_result.stop_state_record),
        artifact_paths=dict(sorted(artifact_paths.items())),
        output_root_summary=_output_root_summary(output_root),
        evidence_boundary=gate_result.evidence_boundary or preflight.evidence_boundary or EVIDENCE_BOUNDARY,
        redaction_status="redacted",
        non_execution_confirmation=NON_EXECUTION_CONFIRMATION,
        metadata={
            "acceptance_status": "not_run",
            "created_at": timestamp,
            "evidence_boundary": EVIDENCE_BOUNDARY,
            "mvp_readiness": "unclaimed",
            "selected_next_lane": SELECTED_NEXT_LANE,
            "blocker_fallback_lane": BLOCKER_FALLBACK_LANE,
            "operator_supervision": "required_for_manual_local_acceptance",
            "provider_external_surface_status": "not_called",
        },
    )


def _dry_run_status(gate_result: ExecutionGateResult) -> str:
    if gate_result.gate_status == ALLOWED_GATE_STATUS:
        return READY_FOR_OPERATOR_SUPERVISED_LOCAL_DRY_RUN
    if gate_result.gate_status == "blocked_by_missing_approval":
        return "blocked_by_missing_approval"
    if gate_result.gate_status == "blocked_by_approval_identity_mismatch":
        return "blocked_by_approval_identity_mismatch"
    if gate_result.gate_status == "blocked_by_failed_preflight":
        return "blocked_by_failed_preflight"
    if gate_result.gate_status == "blocked_by_unsafe_artifact_path":
        return "blocked_by_artifact_path"
    if gate_result.gate_status == "blocked_by_evidence_boundary_issue":
        return "blocked_by_evidence_boundary"
    if gate_result.gate_status == "blocked_by_redaction_issue":
        return "blocked_by_redaction"
    return "blocked_requires_operator_review"


def _proposed_task_summary(proposed: ProposedTask) -> dict[str, Any]:
    return {
        "artifact_path_count": len(proposed.artifact_paths),
        "candidate_changed_files": list(proposed.candidate_changed_files),
        "command_count": len(proposed.proposed_commands),
        "evidence_boundary_present": bool(proposed.evidence_boundary.strip()),
        "lane_id": proposed.lane_id,
        "metadata": dict(proposed.metadata),
        "operator_confirmation_present": proposed.operator_confirmation,
        "requested_action": proposed.requested_action,
        "run_id": str(proposed.metadata.get("run_id", "")),
    }


def _preflight_summary(preflight: PreflightResult) -> dict[str, Any]:
    return {
        "allowed": preflight.allowed,
        "artifact_paths": list(preflight.artifact_paths),
        "command_reason_codes": [item.reason_code for item in preflight.command_classifications],
        "evidence_boundary": preflight.evidence_boundary,
        "finding_ids": [item.id for item in preflight.findings],
        "lane_id": preflight.lane_id,
        "stop_state": preflight.stop_state,
    }


def _execution_gate_summary(gate_result: ExecutionGateResult) -> dict[str, Any]:
    return {
        "allowed_for_local_dry_run": gate_result.allowed_for_local_dry_run,
        "finding_ids": [item.id for item in gate_result.findings],
        "gate_status": gate_result.gate_status,
        "reason_code": gate_result.reason_code,
        "redaction_status": gate_result.redaction_status,
        "schema_version": gate_result.schema_version,
        "stop_state_present": gate_result.stop_state_record is not None,
    }


def _stop_state_summary(stop_state: StopStateRecord | None) -> dict[str, Any] | None:
    if stop_state is None:
        return None
    return {
        "blocked_surfaces": list(stop_state.blocked_surfaces),
        "finding_ids": [item.id for item in stop_state.findings],
        "reason_code": stop_state.reason_code,
        "redaction_status": stop_state.redaction_status,
        "schema_version": stop_state.schema_version,
        "stop_state": stop_state.stop_state,
    }


def _output_root_summary(output_root: Path) -> dict[str, Any]:
    return {
        "basename": output_root.name,
        "provided_by_caller": True,
        "raw_path_recorded": False,
    }


def _artifact_relative_paths(paths: Mapping[str, Path | str] | None) -> dict[str, Path | str]:
    merged: dict[str, Path | str] = dict(DEFAULT_ARTIFACT_RELATIVE_PATHS)
    if paths:
        merged.update(paths)
    return merged


def _validate_artifact_relative_paths(output_root: Path, paths: Mapping[str, Path | str]) -> None:
    for relative_path in paths.values():
        resolve_artifact_path(output_root, relative_path)


def _relative_artifact_path(output_root: Path, artifact_path: Path) -> str:
    return artifact_path.resolve().relative_to(output_root.resolve()).as_posix()


def _preflight_from_input(payload: PreflightResult | Mapping[str, Any]) -> PreflightResult:
    if isinstance(payload, PreflightResult):
        return payload
    return PreflightResult(
        allowed=payload.get("allowed") is True,
        stop_state=str(payload.get("stop_state", "")),
        lane_id=str(payload.get("lane_id", "")),
        findings=(),
        command_classifications=(),
        evidence_boundary=str(payload.get("evidence_boundary", "")),
        artifact_paths=tuple(str(item) for item in payload.get("artifact_paths", ())),
    )
