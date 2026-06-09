"""Local-only Self Operator approval record schema and validation."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from alpha.self_operator.artifact_schema import ArtifactFinding, ValidationResult
from alpha.self_operator.redaction import contains_secret_marker, redact_value

APPROVAL_SCHEMA_VERSION = "self_operator.approval_record.v1"
SUPPORTED_APPROVAL_SCHEMA_VERSIONS = frozenset({APPROVAL_SCHEMA_VERSION})
OPERATOR_CONFIRMATION_HARD_STOP = "stop if explicit operator confirmation is missing"


@dataclass(frozen=True)
class ApprovalRecord:
    """Deterministic local approval record for a bounded Self Operator lane."""

    schema_version: str
    lane_id: str
    run_id: str
    approved: bool
    operator_confirmation: str
    approval_text: str
    approved_by: str
    approved_at: str
    scope_summary: str
    evidence_boundary: str
    redaction_status: str = "redacted"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "ApprovalRecord":
        return cls(
            schema_version=str(payload.get("schema_version", "")),
            lane_id=str(payload.get("lane_id", "")),
            run_id=str(payload.get("run_id", "")),
            approved=payload.get("approved") is True,
            operator_confirmation=str(payload.get("operator_confirmation", "")),
            approval_text=str(payload.get("approval_text", "")),
            approved_by=str(payload.get("approved_by", "")),
            approved_at=str(payload.get("approved_at", "")),
            scope_summary=str(payload.get("scope_summary", "")),
            evidence_boundary=str(payload.get("evidence_boundary", "")),
            redaction_status=str(payload.get("redaction_status", "")),
            metadata=payload.get("metadata", {}) if isinstance(payload.get("metadata", {}), Mapping) else {},
        )

    def to_dict(self, *, redact: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "approval_text": self.approval_text,
            "approved": self.approved,
            "approved_at": self.approved_at,
            "approved_by": self.approved_by,
            "evidence_boundary": self.evidence_boundary,
            "lane_id": self.lane_id,
            "metadata": dict(self.metadata),
            "operator_confirmation": self.operator_confirmation,
            "redaction_status": self.redaction_status,
            "run_id": self.run_id,
            "schema_version": self.schema_version,
            "scope_summary": self.scope_summary,
        }
        return redact_value(payload) if redact else payload

    def validate(self, *, require_scope_summary: bool = True) -> ValidationResult:
        """Fail closed unless explicit local approval is complete and redacted."""

        findings: list[ArtifactFinding] = []
        if self.schema_version not in SUPPORTED_APPROVAL_SCHEMA_VERSIONS:
            findings.append(_finding("SELF_OPERATOR_APPROVAL_UNSUPPORTED_SCHEMA_VERSION", "unsupported_schema"))
        if not self.lane_id.strip():
            findings.append(_finding("SELF_OPERATOR_APPROVAL_LANE_ID_REQUIRED", "missing_lane_id"))
        if not self.run_id.strip():
            findings.append(_finding("SELF_OPERATOR_APPROVAL_RUN_ID_REQUIRED", "missing_run_id"))
        if self.approved is not True:
            findings.append(_finding("SELF_OPERATOR_APPROVAL_REQUIRED", "approval_false_or_missing"))
        if not self.operator_confirmation.strip():
            findings.append(
                _finding(
                    "SELF_OPERATOR_OPERATOR_CONFIRMATION_MISSING",
                    "missing_operator_confirmation",
                    OPERATOR_CONFIRMATION_HARD_STOP,
                )
            )
        if OPERATOR_CONFIRMATION_HARD_STOP not in self.operator_confirmation:
            findings.append(
                _finding(
                    "SELF_OPERATOR_APPROVAL_HARD_STOP_TEXT_REQUIRED",
                    "missing_hard_stop_text",
                    OPERATOR_CONFIRMATION_HARD_STOP,
                )
            )
        if not self.approval_text.strip():
            findings.append(_finding("SELF_OPERATOR_APPROVAL_TEXT_REQUIRED", "missing_approval_text"))
        if not self.approved_by.strip():
            findings.append(_finding("SELF_OPERATOR_APPROVED_BY_REQUIRED", "missing_approved_by"))
        if not self.approved_at.strip():
            findings.append(_finding("SELF_OPERATOR_APPROVED_AT_REQUIRED", "missing_approved_at"))
        if require_scope_summary and not self.scope_summary.strip():
            findings.append(_finding("SELF_OPERATOR_APPROVAL_SCOPE_SUMMARY_REQUIRED", "missing_scope_summary"))
        if not self.evidence_boundary.strip():
            findings.append(
                _finding("SELF_OPERATOR_APPROVAL_EVIDENCE_BOUNDARY_REQUIRED", "missing_evidence_boundary")
            )
        if self.redaction_status != "redacted":
            findings.append(_finding("SELF_OPERATOR_APPROVAL_REDACTION_REQUIRED", "redaction_not_confirmed"))
        if self.redaction_status != "redacted" and contains_secret_marker(self.to_dict(redact=False)):
            findings.append(
                _finding("SELF_OPERATOR_UNREDACTED_SECRET_MARKER", "unredacted_secret_marker")
            )
        return ValidationResult(valid=not findings, findings=tuple(sorted(findings)))


def approval_from_mapping(payload: ApprovalRecord | Mapping[str, Any] | None) -> ApprovalRecord | None:
    """Normalize approval input while preserving missing approval as None."""

    if payload is None:
        return None
    if isinstance(payload, ApprovalRecord):
        return payload
    return ApprovalRecord.from_mapping(payload)


def _finding(id: str, reason_code: str, message: str | None = None) -> ArtifactFinding:
    return ArtifactFinding(
        id=id,
        reason_code=reason_code,
        message=message or reason_code.replace("_", " "),
        surface="approval_record",
    )
