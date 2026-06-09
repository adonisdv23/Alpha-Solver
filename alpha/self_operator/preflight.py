"""Local-only Self Operator preflight runner.

The runner classifies proposed work and commands. It does not perform requested
work, execute proposed commands, call providers, mutate source artifacts, or
promote evidence.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping

from alpha.self_operator.artifact_schema import ArtifactFinding
from alpha.self_operator.artifact_store import ArtifactStoreError, resolve_artifact_path
from alpha.self_operator.command_classification import CommandClassification, classify_commands

DEFAULT_ALLOWED_CHANGED_PREFIXES = (
    "alpha/self_operator/",
    "tests/test_self_operator_",
    "tests/fixtures/self_operator_",
    "docs/evals/runs/alpha-solver-post-level-3-level-11-self-operator-local-artifact-preflight-foundation/",
)
FORBIDDEN_CHANGED_PREFIXES = (
    "alpha/providers/",
    "alpha/adapters/",
    "alpha/api/",
    "alpha/dashboard/",
    "alpha/cli/",
    "service/adapters/",
    "service/app.py",
    "service/auth/",
    "service/budget/",
    "dashboards/",
    "infrastructure/",
    "cli/",
)


@dataclass(frozen=True)
class ProposedTask:
    lane_id: str
    requested_action: str
    candidate_changed_files: tuple[str, ...]
    proposed_commands: tuple[str | tuple[str, ...], ...]
    operator_confirmation: bool
    output_root: str
    evidence_boundary: str
    artifact_paths: tuple[str, ...] = ()
    allowed_changed_prefixes: tuple[str, ...] = DEFAULT_ALLOWED_CHANGED_PREFIXES
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "ProposedTask":
        return cls(
            lane_id=str(payload.get("lane_id", "")),
            requested_action=str(payload.get("requested_action", "")),
            candidate_changed_files=tuple(str(item) for item in payload.get("candidate_changed_files", ())),
            proposed_commands=tuple(_normalize_command(item) for item in payload.get("proposed_commands", ())),
            operator_confirmation=payload.get("operator_confirmation") is True,
            output_root=str(payload.get("output_root", "")),
            evidence_boundary=str(payload.get("evidence_boundary", "")),
            artifact_paths=tuple(str(item) for item in payload.get("artifact_paths", ())),
            allowed_changed_prefixes=tuple(
                str(item) for item in payload.get("allowed_changed_prefixes", DEFAULT_ALLOWED_CHANGED_PREFIXES)
            ),
            metadata=payload.get("metadata", {}) if isinstance(payload.get("metadata", {}), Mapping) else {},
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["proposed_commands"] = [
            list(command) if isinstance(command, tuple) else command for command in self.proposed_commands
        ]
        return payload


@dataclass(frozen=True)
class PreflightResult:
    allowed: bool
    stop_state: str
    lane_id: str
    findings: tuple[ArtifactFinding, ...]
    command_classifications: tuple[CommandClassification, ...]
    evidence_boundary: str
    artifact_paths: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "artifact_paths": list(self.artifact_paths),
            "command_classifications": [classification.to_dict() for classification in self.command_classifications],
            "evidence_boundary": self.evidence_boundary,
            "findings": [finding.to_dict() for finding in self.findings],
            "lane_id": self.lane_id,
            "stop_state": self.stop_state,
        }


def run_local_preflight(task: ProposedTask | Mapping[str, Any]) -> PreflightResult:
    """Classify a proposed local-only task without executing it."""

    proposed = task if isinstance(task, ProposedTask) else ProposedTask.from_mapping(task)
    findings: list[ArtifactFinding] = []
    if not proposed.operator_confirmation:
        findings.append(_finding("SELF_OPERATOR_APPROVAL_GATE_REQUIRED", "missing_operator_confirmation", "stop if explicit operator confirmation is missing", surface="approval_gate"))
    if not proposed.lane_id.strip() or not proposed.requested_action.strip():
        findings.append(_finding("SELF_OPERATOR_SCOPE_UNCLEAR", "scope_unclear", "scope is unclear", surface="scope"))
    if not proposed.evidence_boundary.strip():
        findings.append(_finding("SELF_OPERATOR_EVIDENCE_BOUNDARY_REQUIRED", "missing_evidence_boundary", "evidence boundary is missing", surface="evidence_boundary"))
    findings.extend(_classify_changed_files(proposed))
    findings.extend(_classify_artifact_paths(proposed))
    command_classifications = classify_commands(proposed.proposed_commands)
    for classification in command_classifications:
        findings.extend(classification.findings)
    stable_findings = tuple(sorted(findings))
    return PreflightResult(
        allowed=not stable_findings,
        stop_state="passed" if not stable_findings else "blocked",
        lane_id=proposed.lane_id,
        findings=stable_findings,
        command_classifications=command_classifications,
        evidence_boundary=proposed.evidence_boundary,
        artifact_paths=proposed.artifact_paths,
    )


def _classify_changed_files(proposed: ProposedTask) -> tuple[ArtifactFinding, ...]:
    findings: list[ArtifactFinding] = []
    for path in proposed.candidate_changed_files:
        normalized = path.replace("\\", "/")
        if any(normalized.startswith(prefix) for prefix in FORBIDDEN_CHANGED_PREFIXES):
            findings.append(_finding("SELF_OPERATOR_FORBIDDEN_SURFACE_CHANGED_FILE", "forbidden_changed_file_surface", f"changed file targets forbidden surface: {path}", surface="changed_file_scope"))
        elif not any(normalized.startswith(prefix) for prefix in proposed.allowed_changed_prefixes):
            findings.append(_finding("SELF_OPERATOR_CHANGED_FILE_OUT_OF_SCOPE", "changed_file_out_of_scope", f"changed file exceeds allowed scope: {path}", surface="changed_file_scope"))
        if normalized.startswith("docs/evals/runs/") and "acceptance" in normalized:
            findings.append(_finding("SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED", "evidence_promotion", f"acceptance/evidence promotion path is forbidden: {path}", surface="evidence_promotion"))
    return tuple(findings)


def _classify_artifact_paths(proposed: ProposedTask) -> tuple[ArtifactFinding, ...]:
    findings: list[ArtifactFinding] = []
    if not proposed.output_root.strip():
        return (_finding("SELF_OPERATOR_OUTPUT_ROOT_REQUIRED", "missing_output_root", "output root is required", surface="artifact_store"),)
    for path in proposed.artifact_paths:
        try:
            resolve_artifact_path(Path(proposed.output_root), path)
        except ArtifactStoreError:
            findings.append(_finding("SELF_OPERATOR_ARTIFACT_PATH_OUTSIDE_OUTPUT_ROOT", "artifact_path_outside_output_root", f"artifact path is unsafe: {path}", surface="artifact_store"))
    return tuple(findings)


def _normalize_command(command: Any) -> str | tuple[str, ...]:
    if isinstance(command, (list, tuple)):
        return tuple(str(item) for item in command)
    return str(command)


def _finding(id: str, reason_code: str, message: str, *, surface: str) -> ArtifactFinding:
    return ArtifactFinding(id=id, reason_code=reason_code, message=message, surface=surface)
