"""Deterministic triage for Self Operator acceptance-import source-mutation blockers.

This module reviews a local acceptance execution packet whose import was blocked
with ``blocked_source_mutation_concern`` and classifies the blocked marker. It
reads local files only, never mutates source artifacts, never fabricates
replacement artifacts, and never interprets acceptance success, failure, MVP
readiness, or release readiness.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from alpha.self_operator.result_import import (
    JSON_ARTIFACT_NAMES,
    SOURCE_MUTATION_BLOCKED_FINDING_ID,
    SOURCE_MUTATION_REASON_CODE,
    SourceMutationMarkerOccurrence,
    _artifact_ledger_by_task,
    _artifact_path,
    _expected_artifacts_by_task,
    _is_within,
    _json_dumps,
    _markdown_rows,
    _read_optional,
    _safe_relative,
    find_source_mutation_markers,
)

TRIAGE_SCHEMA_VERSION = "self_operator.import_blocker_triage.v1"
TRIAGE_LANE_ID = (
    "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-"
    "IMPORT-BLOCKER-RESOLUTION-AND-ACCEPTED-IMPORT-001"
)
TRIAGE_BLOCKER_FALLBACK_LANE = (
    "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-"
    "IMPORT-BLOCKER-RESOLUTION-AND-ACCEPTED-IMPORT-FIX-001"
)
DEFAULT_TASK_ID = "MLA-010"
CLASSIFICATIONS = (
    "true_violation",
    "expected_synthetic_marker",
    "malformed_artifact",
    "packet_generation_defect",
    "importer_false_positive",
    "inconclusive",
)
FIX_CLASSIFICATIONS = frozenset({"expected_synthetic_marker", "importer_false_positive"})
SAFETY_RULE = (
    "If the marker appears in a source artifact in a way that could indicate true "
    "source mutation, default to inconclusive unless the packet contract explicitly "
    "allows that marker."
)
EVIDENCE_BOUNDARY = (
    "local-only; read-only triage; no execution; no source-artifact mutation; "
    "no artifact fabrication; no evidence promotion"
)
_FOLLOWUP_FOR_FIX = "patch_importer_narrowly_add_regression_coverage_and_rerun_import"
_FOLLOWUP_FOR_BLOCK = "do_not_patch_importer_create_blocker_review_packet"


@dataclass(frozen=True)
class TriageArtifactRecord:
    """Read-only triage evidence for one expected task artifact."""

    artifact_name: str
    relative_path: str
    present: bool
    sha256: str = ""
    ledger_sha256: str = ""
    checksum_status: str = "not_applicable"
    parse_status: str = "not_applicable"
    marker_occurrences: tuple[SourceMutationMarkerOccurrence, ...] = field(default_factory=tuple)
    allowed_mutation_evidence: bool = False

    @property
    def unexpected_marker_count(self) -> int:
        return sum(1 for occurrence in self.marker_occurrences if not occurrence.expected_blocked_context)

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed_mutation_evidence": self.allowed_mutation_evidence,
            "artifact_name": self.artifact_name,
            "checksum_status": self.checksum_status,
            "ledger_sha256": self.ledger_sha256,
            "marker_occurrences": [occurrence.to_dict() for occurrence in self.marker_occurrences],
            "parse_status": self.parse_status,
            "present": self.present,
            "relative_path": self.relative_path,
            "sha256": self.sha256,
            "unexpected_marker_count": self.unexpected_marker_count,
        }


@dataclass(frozen=True)
class ImportBlockerTriageResult:
    """Deterministic classification of one source-mutation import blocker."""

    schema_version: str
    lane_id: str
    blocker_fallback_lane: str
    packet_dir: str
    task_id: str
    classification: str
    classification_reasons: tuple[str, ...]
    artifacts: tuple[TriageArtifactRecord, ...]
    ledger_row_text: str
    contract_expects_blocked_source_mutation: bool
    non_execution_proof_confirms_blocked: bool
    import_summary_path: str = ""
    import_summary_status: str = "not_provided"
    safety_rule: str = SAFETY_RULE
    evidence_boundary: str = EVIDENCE_BOUNDARY
    readiness_interpretation: str = "not_interpreted"
    mvp_readiness: str = "unclaimed"

    @property
    def recommended_followup(self) -> str:
        return _FOLLOWUP_FOR_FIX if self.classification in FIX_CLASSIFICATIONS else _FOLLOWUP_FOR_BLOCK

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifacts": [record.to_dict() for record in self.artifacts],
            "blocker_fallback_lane": self.blocker_fallback_lane,
            "classification": self.classification,
            "classification_reasons": list(self.classification_reasons),
            "contract_expects_blocked_source_mutation": self.contract_expects_blocked_source_mutation,
            "evidence_boundary": self.evidence_boundary,
            "import_summary_path": self.import_summary_path,
            "import_summary_status": self.import_summary_status,
            "lane_id": self.lane_id,
            "ledger_row_text": self.ledger_row_text,
            "mvp_readiness": self.mvp_readiness,
            "non_execution_proof_confirms_blocked": self.non_execution_proof_confirms_blocked,
            "packet_dir": self.packet_dir,
            "readiness_interpretation": self.readiness_interpretation,
            "recommended_followup": self.recommended_followup,
            "safety_rule": self.safety_rule,
            "schema_version": self.schema_version,
            "task_id": self.task_id,
        }


def triage_import_blocker(
    packet_dir: Path,
    task_id: str = DEFAULT_TASK_ID,
    import_summary_path: Path | None = None,
) -> ImportBlockerTriageResult:
    """Classify a source-mutation import blocker for one task without mutating the packet."""

    packet_root = packet_dir.resolve()
    summary_path_text, summary_status = _load_import_summary_status(import_summary_path)
    ledger_row_text = _task_execution_ledger_row(packet_root, task_id)
    contract_expects = _expects_blocked_source_mutation(ledger_row_text)
    proof_confirms = _non_execution_proof_confirms_blocked(packet_root, task_id)

    if not packet_root.exists() or not packet_root.is_dir():
        return _result(
            packet_root,
            task_id,
            "inconclusive",
            ("packet directory is missing; triage evidence is unavailable",),
            (),
            ledger_row_text,
            contract_expects,
            proof_confirms,
            summary_path_text,
            summary_status,
        )

    artifacts = _collect_artifacts(packet_root, task_id)
    classification, reasons = _classify(artifacts, contract_expects, proof_confirms)
    return _result(
        packet_root,
        task_id,
        classification,
        reasons,
        artifacts,
        ledger_row_text,
        contract_expects,
        proof_confirms,
        summary_path_text,
        summary_status,
    )


def write_triage_result(result: ImportBlockerTriageResult, output_path: Path) -> Path:
    """Write a deterministic JSON triage result."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_json_dumps(result.to_dict()) + "\n", encoding="utf-8")
    return output_path


def _collect_artifacts(packet_root: Path, task_id: str) -> tuple[TriageArtifactRecord, ...]:
    expected = _expected_artifacts_by_task(packet_root).get(task_id, ())
    if not expected:
        task_dir = packet_root / "raw-artifacts" / task_id
        if task_dir.exists():
            expected = tuple(sorted(path.name for path in task_dir.glob("*.json")))
    ledger_by_task = _artifact_ledger_by_task(packet_root)
    records: list[TriageArtifactRecord] = []
    for artifact_name in sorted(expected):
        ledger_entry = ledger_by_task.get(task_id, {}).get(artifact_name, {})
        artifact_path = _artifact_path(packet_root, task_id, artifact_name, ledger_entry)
        relative_path = _safe_relative(artifact_path, packet_root)
        ledger_sha = str(ledger_entry.get("checksum", ""))
        if not _is_within(artifact_path, packet_root) or not artifact_path.exists():
            records.append(
                TriageArtifactRecord(
                    artifact_name=artifact_name,
                    relative_path=relative_path,
                    present=False,
                    ledger_sha256=ledger_sha,
                    checksum_status="not_recorded" if not ledger_sha else "not_applicable",
                    parse_status="missing",
                )
            )
            continue
        digest = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
        if not ledger_sha:
            checksum_status = "not_recorded"
        else:
            checksum_status = "matched" if digest == ledger_sha else "mismatched"
        parse_status = "not_applicable"
        occurrences: tuple[SourceMutationMarkerOccurrence, ...] = ()
        allowed_mutation = False
        if artifact_name in JSON_ARTIFACT_NAMES:
            try:
                payload = json.loads(artifact_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                parse_status = "malformed"
            else:
                parse_status = "parsed"
                occurrences = find_source_mutation_markers(payload)
                allowed_mutation = _records_allowed_source_mutation(payload)
        records.append(
            TriageArtifactRecord(
                artifact_name=artifact_name,
                relative_path=relative_path,
                present=True,
                sha256=digest,
                ledger_sha256=ledger_sha,
                checksum_status=checksum_status,
                parse_status=parse_status,
                marker_occurrences=occurrences,
                allowed_mutation_evidence=allowed_mutation,
            )
        )
    return tuple(records)


def _classify(
    artifacts: tuple[TriageArtifactRecord, ...],
    contract_expects: bool,
    proof_confirms: bool,
) -> tuple[str, tuple[str, ...]]:
    if not artifacts:
        return "inconclusive", ("no task artifacts are available to triage",)
    if any(not record.present for record in artifacts):
        missing = ", ".join(sorted(record.artifact_name for record in artifacts if not record.present))
        return "inconclusive", (f"expected artifacts are missing: {missing}",)
    if any(record.parse_status == "malformed" for record in artifacts):
        malformed = ", ".join(sorted(record.artifact_name for record in artifacts if record.parse_status == "malformed"))
        return "malformed_artifact", (f"artifacts are not valid JSON: {malformed}",)
    if any(record.allowed_mutation_evidence for record in artifacts):
        return "true_violation", (
            "an artifact affirmatively records a source-artifact mutation as allowed or executed",
        )
    if any(record.checksum_status == "mismatched" for record in artifacts):
        return "inconclusive", (
            "artifact checksums do not match the packet ledger; this could indicate true source mutation",
        )
    if any(record.checksum_status == "not_recorded" for record in artifacts):
        return "packet_generation_defect", (
            "the packet ledger does not record a checksum for an expected artifact",
        )
    total_markers = sum(len(record.marker_occurrences) for record in artifacts)
    if total_markers == 0:
        return "importer_false_positive", (
            "the importer reported a source-mutation marker but no marker exists in the artifacts",
        )
    if any(record.unexpected_marker_count for record in artifacts):
        return "inconclusive", (
            "a source-mutation marker appears outside the canonical blocked-finding context; "
            "this could indicate true source mutation",
        )
    if contract_expects:
        reasons = [
            "every source-mutation marker sits inside the canonical blocked-finding context "
            "emitted when the harness refuses a proposed mutation",
            "artifact checksums match the packet ledger, so the recorded artifacts were not altered",
            "the packet task-execution ledger explicitly expects the blocked source-mutation outcome",
        ]
        if proof_confirms:
            reasons.append(
                "the packet non-execution proof confirms the mutation command was blocked, not executed"
            )
        return "expected_synthetic_marker", tuple(reasons)
    return "inconclusive", (
        "markers sit in blocked context but the packet contract does not explicitly "
        "allow the blocked source-mutation marker for this task",
    )


def _records_allowed_source_mutation(payload: Any) -> bool:
    if isinstance(payload, Mapping):
        if str(payload.get("reason_code", "")) == SOURCE_MUTATION_REASON_CODE:
            stop_state = str(payload.get("stop_state", "")).lower()
            if payload.get("allowed") is True or stop_state in {"allowed", "completed", "executed"}:
                return True
        return any(_records_allowed_source_mutation(value) for value in payload.values())
    if isinstance(payload, (list, tuple)):
        return any(_records_allowed_source_mutation(item) for item in payload)
    return False


def _task_execution_ledger_row(packet_root: Path, task_id: str) -> str:
    ledger = packet_root / "task-execution-ledger.md"
    if not ledger.exists():
        return ""
    for row in _markdown_rows(ledger):
        if row and row[0] == task_id:
            return " | ".join(row)
    return ""


def _expects_blocked_source_mutation(ledger_row_text: str) -> bool:
    normalized = ledger_row_text.lower().replace("-", " ")
    return bool(normalized) and "source mutation" in normalized and "blocked" in normalized


def _non_execution_proof_confirms_blocked(packet_root: Path, task_id: str) -> bool:
    normalized = _read_optional(packet_root / "non-execution-proof.md").lower().replace("-", " ")
    normalized_task_id = task_id.lower().replace("-", " ")
    return normalized_task_id in normalized and "source mutation" in normalized and "blocked" in normalized


def _load_import_summary_status(import_summary_path: Path | None) -> tuple[str, str]:
    if import_summary_path is None:
        return "", "not_provided"
    if not import_summary_path.exists():
        return str(import_summary_path), "missing"
    try:
        payload = json.loads(import_summary_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return str(import_summary_path), "unreadable"
    if not isinstance(payload, Mapping):
        return str(import_summary_path), "unreadable"
    return str(import_summary_path), str(payload.get("status", "unknown"))


def _result(
    packet_root: Path,
    task_id: str,
    classification: str,
    reasons: tuple[str, ...],
    artifacts: tuple[TriageArtifactRecord, ...],
    ledger_row_text: str,
    contract_expects: bool,
    proof_confirms: bool,
    import_summary_path: str,
    import_summary_status: str,
) -> ImportBlockerTriageResult:
    return ImportBlockerTriageResult(
        schema_version=TRIAGE_SCHEMA_VERSION,
        lane_id=TRIAGE_LANE_ID,
        blocker_fallback_lane=TRIAGE_BLOCKER_FALLBACK_LANE,
        packet_dir=str(packet_root),
        task_id=task_id,
        classification=classification,
        classification_reasons=reasons,
        artifacts=artifacts,
        ledger_row_text=ledger_row_text,
        contract_expects_blocked_source_mutation=contract_expects,
        non_execution_proof_confirms_blocked=proof_confirms,
        import_summary_path=import_summary_path,
        import_summary_status=import_summary_status,
    )
