"""Local-only Self Operator stop-state record schema and validation."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from alpha.self_operator.artifact_schema import ArtifactFinding, ValidationResult
from alpha.self_operator.artifact_store import ArtifactStoreError, resolve_artifact_path, write_artifact_json
from alpha.self_operator.redaction import contains_secret_marker, redact_value

STOP_STATE_SCHEMA_VERSION = "self_operator.stop_state_record.v1"
SUPPORTED_STOP_STATE_SCHEMA_VERSIONS = frozenset({STOP_STATE_SCHEMA_VERSION})


@dataclass(frozen=True)
class StopStateRecord:
    """Deterministic local stop-state record for blocked gate evaluations."""

    schema_version: str
    lane_id: str
    run_id: str
    stop_state: str
    reason_code: str
    message: str
    findings: tuple[ArtifactFinding, ...]
    blocked_surfaces: tuple[str, ...]
    source_preflight_result_summary: Mapping[str, Any]
    approval_result_summary: Mapping[str, Any]
    artifact_paths: tuple[str, ...]
    evidence_boundary: str
    redaction_status: str = "redacted"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "StopStateRecord":
        return cls(
            schema_version=str(payload.get("schema_version", "")),
            lane_id=str(payload.get("lane_id", "")),
            run_id=str(payload.get("run_id", "")),
            stop_state=str(payload.get("stop_state", "")),
            reason_code=str(payload.get("reason_code", "")),
            message=str(payload.get("message", "")),
            findings=tuple(_finding_from_mapping(item) for item in _items(payload.get("findings"))),
            blocked_surfaces=tuple(str(item) for item in _items(payload.get("blocked_surfaces"))),
            source_preflight_result_summary=(
                payload.get("source_preflight_result_summary", {})
                if isinstance(payload.get("source_preflight_result_summary", {}), Mapping)
                else {}
            ),
            approval_result_summary=(
                payload.get("approval_result_summary", {})
                if isinstance(payload.get("approval_result_summary", {}), Mapping)
                else {}
            ),
            artifact_paths=tuple(str(item) for item in _items(payload.get("artifact_paths"))),
            evidence_boundary=str(payload.get("evidence_boundary", "")),
            redaction_status=str(payload.get("redaction_status", "")),
            metadata=payload.get("metadata", {}) if isinstance(payload.get("metadata", {}), Mapping) else {},
        )

    def to_dict(self, *, redact: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "approval_result_summary": dict(self.approval_result_summary),
            "artifact_paths": list(self.artifact_paths),
            "blocked_surfaces": list(self.blocked_surfaces),
            "evidence_boundary": self.evidence_boundary,
            "findings": [finding.to_dict() for finding in self.findings],
            "lane_id": self.lane_id,
            "message": self.message,
            "metadata": dict(self.metadata),
            "reason_code": self.reason_code,
            "redaction_status": self.redaction_status,
            "run_id": self.run_id,
            "schema_version": self.schema_version,
            "source_preflight_result_summary": dict(self.source_preflight_result_summary),
            "stop_state": self.stop_state,
        }
        return redact_value(payload) if redact else payload

    def validate(self, *, output_root: Path | str | None = None) -> ValidationResult:
        """Validate the stop-state record and optional output-root artifact paths."""

        findings: list[ArtifactFinding] = []
        if self.schema_version not in SUPPORTED_STOP_STATE_SCHEMA_VERSIONS:
            findings.append(_finding("SELF_OPERATOR_STOP_STATE_UNSUPPORTED_SCHEMA_VERSION", "unsupported_schema"))
        if not self.lane_id.strip():
            findings.append(_finding("SELF_OPERATOR_STOP_STATE_LANE_ID_REQUIRED", "missing_lane_id"))
        if not self.run_id.strip():
            findings.append(_finding("SELF_OPERATOR_STOP_STATE_RUN_ID_REQUIRED", "missing_run_id"))
        if not self.stop_state.strip():
            findings.append(_finding("SELF_OPERATOR_STOP_STATE_REQUIRED", "missing_stop_state"))
        if not self.reason_code.strip():
            findings.append(_finding("SELF_OPERATOR_STOP_STATE_REASON_CODE_REQUIRED", "missing_reason_code"))
        if not self.evidence_boundary.strip():
            findings.append(_finding("SELF_OPERATOR_STOP_STATE_EVIDENCE_BOUNDARY_REQUIRED", "missing_evidence_boundary"))
        for item in self.findings:
            if not item.id.strip() or not item.reason_code.strip() or not item.message.strip():
                findings.append(_finding("SELF_OPERATOR_STOP_STATE_FINDING_MALFORMED", "malformed_finding"))
        if output_root is not None:
            for path in self.artifact_paths:
                try:
                    resolve_artifact_path(output_root, path)
                except ArtifactStoreError:
                    findings.append(
                        _finding("SELF_OPERATOR_STOP_STATE_ARTIFACT_PATH_UNSAFE", "artifact_path_unsafe")
                    )
        elif any(Path(path).is_absolute() or ".." in Path(path).parts for path in self.artifact_paths):
            findings.append(_finding("SELF_OPERATOR_STOP_STATE_ARTIFACT_PATH_UNSAFE", "artifact_path_unsafe"))
        if self.redaction_status != "redacted":
            findings.append(_finding("SELF_OPERATOR_STOP_STATE_REDACTION_REQUIRED", "redaction_not_confirmed"))
        if self.redaction_status != "redacted" and contains_secret_marker(self.to_dict(redact=False)):
            findings.append(_finding("SELF_OPERATOR_UNREDACTED_SECRET_MARKER", "unredacted_secret_marker"))
        return ValidationResult(valid=not findings, findings=tuple(sorted(set(findings))))


def write_stop_state_json(
    record: StopStateRecord | Mapping[str, Any],
    *,
    output_root: Path | str,
    relative_path: Path | str,
    overwrite: bool = False,
) -> Path:
    """Persist a stop-state JSON artifact below a caller-provided output root."""

    payload = record.to_dict(redact=True) if isinstance(record, StopStateRecord) else record
    return write_artifact_json(payload, output_root=output_root, relative_path=relative_path, overwrite=overwrite)


def _items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else list(value) if isinstance(value, tuple) else []


def _finding_from_mapping(payload: Any) -> ArtifactFinding:
    if isinstance(payload, ArtifactFinding):
        return payload
    if not isinstance(payload, Mapping):
        return ArtifactFinding(id="", reason_code="", message="", surface="stop_state_record")
    return ArtifactFinding(
        id=str(payload.get("id", "")),
        reason_code=str(payload.get("reason_code", "")),
        message=str(payload.get("message", "")),
        severity=str(payload.get("severity", "error")),
        surface=str(payload.get("surface", "stop_state_record")),
        stop_state=str(payload.get("stop_state", "blocked")),
    )


def _finding(id: str, reason_code: str, message: str | None = None) -> ArtifactFinding:
    return ArtifactFinding(
        id=id,
        reason_code=reason_code,
        message=message or reason_code.replace("_", " "),
        surface="stop_state_record",
    )
