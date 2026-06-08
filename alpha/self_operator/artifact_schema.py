"""Local-only Self Operator artifact schema and deterministic validation."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping

from alpha.self_operator.redaction import contains_secret_marker, redact_value

CURRENT_SCHEMA_VERSION = "self_operator.local_artifact.v1"
SUPPORTED_SCHEMA_VERSIONS = frozenset({CURRENT_SCHEMA_VERSION})


@dataclass(frozen=True, order=True)
class ArtifactFinding:
    """Stable finding shape shared by artifact validation and preflight."""

    id: str
    reason_code: str
    message: str
    severity: str = "error"
    surface: str = "artifact_schema"
    stop_state: str = "blocked"

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ValidationResult:
    """Deterministic validation result."""

    valid: bool
    findings: tuple[ArtifactFinding, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {"valid": self.valid, "findings": [finding.to_dict() for finding in self.findings]}


@dataclass(frozen=True)
class OperatorConfirmation:
    """Operator confirmation gate recorded in local artifacts."""

    explicit: bool
    confirmed_by: str = "local-operator"
    confirmation_text: str = "stop if explicit operator confirmation is missing"

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "OperatorConfirmation":
        return cls(
            explicit=payload.get("explicit") is True,
            confirmed_by=str(payload.get("confirmed_by", "local-operator")),
            confirmation_text=str(
                payload.get("confirmation_text", "stop if explicit operator confirmation is missing")
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SelfOperatorArtifact:
    """Serializable local artifact foundation for future Self Operator lanes."""

    schema_version: str
    lane_id: str
    run_id: str
    created_at: str
    operator_confirmation: OperatorConfirmation
    input_summary: Mapping[str, Any]
    preflight_result: Mapping[str, Any]
    findings: tuple[ArtifactFinding, ...]
    stop_state: str
    artifact_paths: tuple[str, ...]
    evidence_boundary: str
    redaction_status: str = "redacted"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "SelfOperatorArtifact":
        findings = tuple(_finding_from_mapping(item) for item in _require_list(payload.get("findings")))
        operator_payload = payload.get("operator_confirmation", {})
        operator_confirmation = (
            operator_payload
            if isinstance(operator_payload, OperatorConfirmation)
            else OperatorConfirmation.from_mapping(operator_payload if isinstance(operator_payload, Mapping) else {})
        )
        return cls(
            schema_version=str(payload.get("schema_version", "")),
            lane_id=str(payload.get("lane_id", "")),
            run_id=str(payload.get("run_id", "")),
            created_at=str(payload.get("created_at", "")),
            operator_confirmation=operator_confirmation,
            input_summary=payload.get("input_summary", {}) if isinstance(payload.get("input_summary", {}), Mapping) else {},
            preflight_result=payload.get("preflight_result", {}) if isinstance(payload.get("preflight_result", {}), Mapping) else {},
            findings=findings,
            stop_state=str(payload.get("stop_state", "")),
            artifact_paths=tuple(str(item) for item in _require_list(payload.get("artifact_paths"))),
            evidence_boundary=str(payload.get("evidence_boundary", "")),
            redaction_status=str(payload.get("redaction_status", "")),
            metadata=payload.get("metadata", {}) if isinstance(payload.get("metadata", {}), Mapping) else {},
        )

    def to_dict(self, *, redact: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "artifact_paths": list(self.artifact_paths),
            "created_at": self.created_at,
            "evidence_boundary": self.evidence_boundary,
            "findings": [finding.to_dict() for finding in self.findings],
            "input_summary": dict(self.input_summary),
            "lane_id": self.lane_id,
            "metadata": dict(self.metadata),
            "operator_confirmation": self.operator_confirmation.to_dict(),
            "preflight_result": dict(self.preflight_result),
            "redaction_status": self.redaction_status,
            "run_id": self.run_id,
            "schema_version": self.schema_version,
            "stop_state": self.stop_state,
        }
        return redact_value(payload) if redact else payload

    def to_json(self, *, redact: bool = True) -> str:
        return json.dumps(self.to_dict(redact=redact), ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    def validate(self, *, output_root: Path | str | None = None, require_stop_state: bool = True) -> ValidationResult:
        return validate_artifact(self, output_root=output_root, require_stop_state=require_stop_state)


def validate_artifact(
    artifact: SelfOperatorArtifact | Mapping[str, Any],
    *,
    output_root: Path | str | None = None,
    require_stop_state: bool = True,
) -> ValidationResult:
    """Validate an artifact without external access or source mutation."""

    model = artifact if isinstance(artifact, SelfOperatorArtifact) else SelfOperatorArtifact.from_mapping(artifact)
    findings: list[ArtifactFinding] = []
    if model.schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        findings.append(_finding("SELF_OPERATOR_ARTIFACT_UNSUPPORTED_SCHEMA_VERSION", "unsupported_schema_version", "unsupported schema version"))
    if not model.lane_id.strip():
        findings.append(_finding("SELF_OPERATOR_ARTIFACT_LANE_ID_REQUIRED", "missing_lane_id", "missing lane ID"))
    if not model.run_id.strip():
        findings.append(_finding("SELF_OPERATOR_ARTIFACT_RUN_ID_REQUIRED", "missing_run_id", "missing run ID"))
    if model.operator_confirmation.explicit is not True:
        findings.append(_finding("SELF_OPERATOR_APPROVAL_GATE_REQUIRED", "missing_operator_confirmation", "missing explicit operator confirmation", surface="approval_gate"))
    if require_stop_state and not model.stop_state.strip():
        findings.append(_finding("SELF_OPERATOR_STOP_STATE_REQUIRED", "missing_stop_state", "missing stop state when required", surface="stop_state"))
    if not model.evidence_boundary.strip():
        findings.append(_finding("SELF_OPERATOR_EVIDENCE_BOUNDARY_REQUIRED", "missing_evidence_boundary", "missing evidence boundary", surface="evidence_boundary"))
    findings.extend(_validate_findings(model.findings))
    unredacted_payload = model.to_dict(redact=False)
    if contains_secret_marker(unredacted_payload) and model.redaction_status != "redacted":
        findings.append(_finding("SELF_OPERATOR_UNREDACTED_SECRET_MARKER", "unredacted_secret_marker", "unredacted secret-like marker detected", surface="redaction"))
    if output_root is not None:
        findings.extend(_validate_artifact_paths(model.artifact_paths, Path(output_root)))
    return ValidationResult(valid=not findings, findings=tuple(sorted(findings)))


def _validate_findings(findings: tuple[ArtifactFinding, ...]) -> tuple[ArtifactFinding, ...]:
    validation_findings: list[ArtifactFinding] = []
    for index, finding in enumerate(findings):
        if not finding.id.strip() or not finding.reason_code.strip() or not finding.message.strip():
            validation_findings.append(
                _finding(
                    "SELF_OPERATOR_ARTIFACT_FINDING_MALFORMED",
                    "malformed_finding",
                    f"malformed finding at index {index}",
                )
            )
    return tuple(validation_findings)


def _validate_artifact_paths(paths: tuple[str, ...], output_root: Path) -> tuple[ArtifactFinding, ...]:
    output_root_resolved = output_root.resolve()
    findings: list[ArtifactFinding] = []
    for artifact_path in paths:
        candidate = Path(artifact_path)
        if candidate.is_absolute():
            resolved = candidate.resolve()
        else:
            resolved = (output_root_resolved / candidate).resolve()
        if ".." in candidate.parts or not _is_relative_to(resolved, output_root_resolved):
            findings.append(
                _finding(
                    "SELF_OPERATOR_ARTIFACT_PATH_OUTSIDE_OUTPUT_ROOT",
                    "artifact_path_outside_output_root",
                    f"artifact path is outside allowed output root: {artifact_path}",
                    surface="artifact_store",
                )
            )
    return tuple(findings)


def _is_relative_to(candidate: Path, root: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _require_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _finding_from_mapping(value: Any) -> ArtifactFinding:
    if isinstance(value, ArtifactFinding):
        return value
    if not isinstance(value, Mapping):
        return ArtifactFinding(id="", reason_code="", message="")
    return ArtifactFinding(
        id=str(value.get("id", "")),
        reason_code=str(value.get("reason_code", "")),
        message=str(value.get("message", "")),
        severity=str(value.get("severity", "error")),
        surface=str(value.get("surface", "artifact_schema")),
        stop_state=str(value.get("stop_state", "blocked")),
    )


def _finding(id: str, reason_code: str, message: str, *, surface: str = "artifact_schema") -> ArtifactFinding:
    return ArtifactFinding(id=id, reason_code=reason_code, message=message, surface=surface)
