"""Local-only Self Operator execution-gate evaluator.

The evaluator is a deterministic gate only. It never executes proposed commands,
never calls providers or external APIs, and never mutates source artifacts.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping

from alpha.self_operator.approval import ApprovalRecord, approval_from_mapping
from alpha.self_operator.artifact_schema import ArtifactFinding, ValidationResult
from alpha.self_operator.artifact_store import write_artifact_json
from alpha.self_operator.preflight import PreflightResult, ProposedTask, run_local_preflight
from alpha.self_operator.redaction import redact_value
from alpha.self_operator.stop_state import STOP_STATE_SCHEMA_VERSION, StopStateRecord

GATE_RESULT_SCHEMA_VERSION = "self_operator.execution_gate_result.v1"
DEFAULT_BLOCKED_STOP_STATE = "blocked"
ALLOWED_GATE_STATUS = "allowed_for_local_dry_run_wrapper"


@dataclass(frozen=True)
class ExecutionGateResult:
    """Serializable local execution-gate result."""

    schema_version: str
    lane_id: str
    run_id: str
    allowed_for_local_dry_run: bool
    gate_status: str
    reason_code: str
    findings: tuple[ArtifactFinding, ...]
    preflight_result_summary: Mapping[str, Any]
    approval_result_summary: Mapping[str, Any]
    stop_state_record: StopStateRecord | None
    artifact_paths: tuple[str, ...]
    evidence_boundary: str
    redaction_status: str = "redacted"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self, *, redact: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "allowed_for_local_dry_run": self.allowed_for_local_dry_run,
            "approval_result_summary": dict(self.approval_result_summary),
            "artifact_paths": list(self.artifact_paths),
            "evidence_boundary": self.evidence_boundary,
            "findings": [finding.to_dict() for finding in self.findings],
            "gate_status": self.gate_status,
            "lane_id": self.lane_id,
            "metadata": dict(self.metadata),
            "preflight_result_summary": dict(self.preflight_result_summary),
            "reason_code": self.reason_code,
            "redaction_status": self.redaction_status,
            "run_id": self.run_id,
            "schema_version": self.schema_version,
            "stop_state_record": self.stop_state_record.to_dict(redact=redact) if self.stop_state_record else None,
        }
        return redact_value(payload) if redact else payload


def evaluate_execution_gate(
    proposed_task: ProposedTask | Mapping[str, Any],
    approval_record: ApprovalRecord | Mapping[str, Any] | None,
    *,
    output_root: Path | str | None = None,
    preflight_result: PreflightResult | Mapping[str, Any] | None = None,
    timestamp_provider: Callable[[], str] | None = None,
) -> ExecutionGateResult:
    """Evaluate whether a proposal may advance to a future local dry-run wrapper.

    This function only validates local records and runs the non-executing #454
    preflight classifier when a preflight result is not provided.
    """

    proposed = proposed_task if isinstance(proposed_task, ProposedTask) else ProposedTask.from_mapping(proposed_task)
    if output_root is not None and not proposed.output_root.strip():
        proposed = ProposedTask.from_mapping({**proposed.to_dict(), "output_root": str(output_root)})
    run_id = _run_id(proposed, approval_record)
    timestamp = timestamp_provider() if timestamp_provider else "1970-01-01T00:00:00Z"

    preflight = _preflight_from_input(preflight_result) if preflight_result is not None else run_local_preflight(proposed)
    approval = approval_from_mapping(approval_record)
    approval_validation = _validate_approval(approval)
    identity_validation = _validate_approval_identity(proposed, approval)
    findings = list(approval_validation.findings) + list(identity_validation.findings) + list(preflight.findings)

    gate_status, reason_code = _gate_status(preflight, approval, approval_validation, identity_validation)
    stable_findings = tuple(sorted(set(findings)))
    approval_summary = _approval_summary(approval, approval_validation, identity_validation)
    preflight_summary = _preflight_summary(preflight)
    evidence_boundary = approval.evidence_boundary if approval and approval.evidence_boundary.strip() else preflight.evidence_boundary
    artifact_paths = tuple(preflight.artifact_paths)

    stop_state = None
    allowed = gate_status == ALLOWED_GATE_STATUS
    if not allowed:
        stop_state = _build_stop_state(
            lane_id=proposed.lane_id or (approval.lane_id if approval else ""),
            run_id=run_id,
            reason_code=reason_code,
            findings=stable_findings,
            preflight_summary=preflight_summary,
            approval_summary=approval_summary,
            artifact_paths=artifact_paths,
            evidence_boundary=evidence_boundary,
            timestamp=timestamp,
        )

    return ExecutionGateResult(
        schema_version=GATE_RESULT_SCHEMA_VERSION,
        lane_id=proposed.lane_id or (approval.lane_id if approval else ""),
        run_id=run_id,
        allowed_for_local_dry_run=allowed,
        gate_status=gate_status,
        reason_code=reason_code,
        findings=stable_findings,
        preflight_result_summary=preflight_summary,
        approval_result_summary=approval_summary,
        stop_state_record=stop_state,
        artifact_paths=artifact_paths,
        evidence_boundary=evidence_boundary,
        metadata={
            "created_at": timestamp,
            "dry_run_harness_contract": "readiness-only; wrapper remains selected next lane",
            "non_execution_boundary": (
                "no commands executed; no providers, external APIs, browsers, deployment, billing, "
                "credentials, Google Sheets, source-artifact mutation, or evidence promotion"
            ),
        },
    )


def write_execution_gate_result_json(
    result: ExecutionGateResult | Mapping[str, Any],
    *,
    output_root: Path | str,
    relative_path: Path | str,
    overwrite: bool = False,
) -> Path:
    """Persist a gate result below a caller-provided output root."""

    payload = result.to_dict(redact=True) if isinstance(result, ExecutionGateResult) else result
    return write_artifact_json(payload, output_root=output_root, relative_path=relative_path, overwrite=overwrite)


def _validate_approval(approval: ApprovalRecord | None) -> ValidationResult:
    if approval is None:
        return ValidationResult(
            valid=False,
            findings=(
                ArtifactFinding(
                    id="SELF_OPERATOR_APPROVAL_MISSING",
                    reason_code="missing_approval",
                    message="approval record is missing",
                    surface="approval_record",
                ),
            ),
        )
    return approval.validate()


def _gate_status(
    preflight: PreflightResult,
    approval: ApprovalRecord | None,
    approval_validation: ValidationResult,
    identity_validation: ValidationResult,
) -> tuple[str, str]:
    if approval is None:
        return "blocked_by_missing_approval", "missing_approval"
    if not approval_validation.valid:
        reason_codes = {finding.reason_code for finding in approval_validation.findings}
        if "unredacted_secret_marker" in reason_codes or "redaction_not_confirmed" in reason_codes:
            return "blocked_by_redaction_issue", "redaction_issue"
        if "missing_evidence_boundary" in reason_codes:
            return "blocked_by_evidence_boundary_issue", "evidence_boundary_issue"
        return "blocked_by_missing_approval", "approval_invalid"
    if not identity_validation.valid:
        return "blocked_by_approval_identity_mismatch", "approval_identity_mismatch"
    if not preflight.allowed:
        reason_codes = {finding.reason_code for finding in preflight.findings}
        if "artifact_path_outside_output_root" in reason_codes:
            return "blocked_by_unsafe_artifact_path", "unsafe_artifact_path"
        if "missing_evidence_boundary" in reason_codes:
            return "blocked_by_evidence_boundary_issue", "evidence_boundary_issue"
        if "unclear_requires_operator_review" in reason_codes or "scope_unclear" in reason_codes:
            return "unclear_requires_operator_review", "operator_review_required"
        return "blocked_by_failed_preflight", "failed_preflight"
    return ALLOWED_GATE_STATUS, "ready_for_local_dry_run_wrapper"


def _build_stop_state(
    *,
    lane_id: str,
    run_id: str,
    reason_code: str,
    findings: tuple[ArtifactFinding, ...],
    preflight_summary: Mapping[str, Any],
    approval_summary: Mapping[str, Any],
    artifact_paths: tuple[str, ...],
    evidence_boundary: str,
    timestamp: str,
) -> StopStateRecord:
    surfaces = tuple(sorted({finding.surface for finding in findings if finding.surface}))
    return StopStateRecord(
        schema_version=STOP_STATE_SCHEMA_VERSION,
        lane_id=lane_id,
        run_id=run_id,
        stop_state=DEFAULT_BLOCKED_STOP_STATE,
        reason_code=reason_code,
        message=f"execution gate blocked: {reason_code}",
        findings=findings,
        blocked_surfaces=surfaces,
        source_preflight_result_summary=preflight_summary,
        approval_result_summary=approval_summary,
        artifact_paths=artifact_paths,
        evidence_boundary=evidence_boundary,
        metadata={"created_at": timestamp, "local_only": True},
    )


def _approval_summary(
    approval: ApprovalRecord | None,
    validation: ValidationResult,
    identity_validation: ValidationResult,
) -> dict[str, Any]:
    if approval is None:
        return {
            "identity_match": False,
            "identity_finding_ids": [item.id for item in identity_validation.findings],
            "present": False,
            "valid": False,
            "finding_ids": [item.id for item in validation.findings],
        }
    return {
        "approved": approval.approved,
        "finding_ids": [item.id for item in validation.findings],
        "identity_finding_ids": [item.id for item in identity_validation.findings],
        "identity_match": identity_validation.valid,
        "lane_id": approval.lane_id,
        "present": True,
        "run_id": approval.run_id,
        "valid": validation.valid,
    }


def _validate_approval_identity(proposed: ProposedTask, approval: ApprovalRecord | None) -> ValidationResult:
    """Fail closed when an approval record does not match the proposed task identity."""

    if approval is None:
        return ValidationResult(valid=True)

    mismatches: list[str] = []
    if approval.lane_id.strip() and proposed.lane_id.strip() and approval.lane_id != proposed.lane_id:
        mismatches.append("lane_id")

    approval_run_id = approval.run_id.strip()
    proposed_run_id = _proposed_run_id(proposed).strip()
    if approval_run_id and proposed_run_id and approval_run_id != proposed_run_id:
        mismatches.append("run_id")

    approval_scope_identity = _approval_scope_identity(approval)
    proposed_scope_identity = _proposed_scope_identity(proposed)
    if approval_scope_identity and proposed_scope_identity and approval_scope_identity != proposed_scope_identity:
        mismatches.append("scope_identity")

    if not mismatches:
        return ValidationResult(valid=True)

    mismatch_text = ", ".join(sorted(mismatches))
    return ValidationResult(
        valid=False,
        findings=(
            ArtifactFinding(
                id="SELF_OPERATOR_APPROVAL_IDENTITY_MISMATCH",
                reason_code="approval_identity_mismatch",
                message=f"approval record does not match proposed task identity: {mismatch_text}",
                surface="approval_identity",
            ),
        ),
    )


def _preflight_summary(preflight: PreflightResult) -> dict[str, Any]:
    return {
        "allowed": preflight.allowed,
        "artifact_paths": list(preflight.artifact_paths),
        "evidence_boundary": preflight.evidence_boundary,
        "finding_ids": [item.id for item in preflight.findings],
        "lane_id": preflight.lane_id,
        "stop_state": preflight.stop_state,
    }


def _preflight_from_input(payload: PreflightResult | Mapping[str, Any]) -> PreflightResult:
    if isinstance(payload, PreflightResult):
        return payload
    findings = tuple(_finding_from_mapping(item) for item in _items(payload.get("findings")))
    return PreflightResult(
        allowed=payload.get("allowed") is True,
        stop_state=str(payload.get("stop_state", "")),
        lane_id=str(payload.get("lane_id", "")),
        findings=findings,
        command_classifications=(),
        evidence_boundary=str(payload.get("evidence_boundary", "")),
        artifact_paths=tuple(str(item) for item in _items(payload.get("artifact_paths"))),
    )


def _finding_from_mapping(payload: Any) -> ArtifactFinding:
    if isinstance(payload, ArtifactFinding):
        return payload
    if not isinstance(payload, Mapping):
        return ArtifactFinding(id="", reason_code="", message="", surface="execution_gate")
    return ArtifactFinding(
        id=str(payload.get("id", "")),
        reason_code=str(payload.get("reason_code", "")),
        message=str(payload.get("message", "")),
        severity=str(payload.get("severity", "error")),
        surface=str(payload.get("surface", "execution_gate")),
        stop_state=str(payload.get("stop_state", "blocked")),
    )


def _items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else list(value) if isinstance(value, tuple) else []


def _approval_scope_identity(approval: ApprovalRecord) -> str:
    metadata = approval.metadata if isinstance(approval.metadata, Mapping) else {}
    for key in ("task_identity", "scope_identity", "scope_summary", "requested_action"):
        value = metadata.get(key)
        if value is not None and str(value).strip():
            return _normalize_identity(value)
    return _normalize_identity(approval.scope_summary)


def _proposed_scope_identity(proposed: ProposedTask) -> str:
    metadata = proposed.metadata if isinstance(proposed.metadata, Mapping) else {}
    for key in ("task_identity", "scope_identity", "scope_summary"):
        value = metadata.get(key)
        if value is not None and str(value).strip():
            return _normalize_identity(value)
    return ""


def _normalize_identity(value: Any) -> str:
    return " ".join(str(value).split())


def _proposed_run_id(proposed: ProposedTask) -> str:
    metadata_run_id = proposed.metadata.get("run_id") if isinstance(proposed.metadata, Mapping) else None
    return str(metadata_run_id or "")


def _run_id(proposed: ProposedTask, approval_record: ApprovalRecord | Mapping[str, Any] | None) -> str:
    proposed_run_id = _proposed_run_id(proposed).strip()
    if proposed_run_id:
        return proposed_run_id
    if isinstance(approval_record, ApprovalRecord) and approval_record.run_id.strip():
        return approval_record.run_id
    if isinstance(approval_record, Mapping) and str(approval_record.get("run_id", "")).strip():
        return str(approval_record["run_id"])
    return "missing-approval-run"
