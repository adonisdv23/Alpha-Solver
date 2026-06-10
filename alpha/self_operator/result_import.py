"""Deterministic local importer for Self Operator acceptance execution packets.

This module validates and normalizes local-only operator-supervised acceptance
artifacts. It reads local files, computes checksums, and writes no conclusions
about MVP readiness, runtime readiness, or final acceptance meaning.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

ACCEPTANCE_IMPORT_SCHEMA_VERSION = "self_operator.acceptance_import_summary.v1"
EXECUTION_LANE_ID = (
    "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-"
    "OPERATOR-SUPERVISED-LOCAL-ACCEPTANCE-EXECUTION-001"
)
IMPORT_LANE_ID = (
    "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-"
    "LOCAL-ACCEPTANCE-RESULT-IMPORT-TOOLING-001"
)
SELECTED_NEXT_LANE = (
    "ALPHA-SOLVER-POST-LEVEL-3-TO-LEVEL-14-SELF-OPERATOR-"
    "ACCEPTANCE-INTERPRETATION-ENGINE-001"
)
BLOCKER_FALLBACK_LANE = (
    "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-"
    "LOCAL-ACCEPTANCE-RESULT-IMPORT-TOOLING-FIX-001"
)
TASK_IDS = tuple(f"MLA-{index:03d}" for index in range(1, 11))
JSON_ARTIFACT_NAMES = frozenset({"dry-run-result.json", "execution-gate-result.json", "stop-state.json"})
SOURCE_MUTATION_REASON_CODE = "source_artifact_mutation"
SOURCE_MUTATION_BLOCKED_FINDING_ID = "SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED"
IMPORT_STATUSES = frozenset(
    {
        "import_ready",
        "import_ready_with_expected_blocks",
        "blocked_missing_artifact",
        "blocked_malformed_artifact",
        "blocked_checksum_mismatch",
        "blocked_redaction_failure",
        "blocked_evidence_boundary_failure",
        "blocked_non_execution_missing",
        "blocked_source_mutation_concern",
        "blocked_unknown",
    }
)
BLOCKED_STATUSES = frozenset(status for status in IMPORT_STATUSES if status.startswith("blocked_"))


@dataclass(frozen=True)
class SourceMutationMarkerOccurrence:
    """One source-mutation marker string found inside an artifact payload."""

    json_path: str
    value: str
    expected_blocked_context: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "expected_blocked_context": self.expected_blocked_context,
            "json_path": self.json_path,
            "value": self.value,
        }


@dataclass(frozen=True)
class AcceptanceArtifactRecord:
    """Normalized record for one discovered or expected acceptance artifact."""

    task_id: str
    artifact_name: str
    path: str
    relative_path: str
    present: bool
    sha256: str = ""
    expected_sha256: str = ""
    checksum_status: str = "not_applicable"
    schema_version: str = ""
    lane_id: str = ""
    run_id: str = ""
    redaction_status: str = ""
    evidence_boundary: str = ""
    non_execution_confirmation: str = ""
    status: str = "import_ready"
    findings: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_name": self.artifact_name,
            "checksum_status": self.checksum_status,
            "evidence_boundary": self.evidence_boundary,
            "expected_sha256": self.expected_sha256,
            "findings": list(self.findings),
            "lane_id": self.lane_id,
            "non_execution_confirmation": self.non_execution_confirmation,
            "path": self.path,
            "present": self.present,
            "redaction_status": self.redaction_status,
            "relative_path": self.relative_path,
            "run_id": self.run_id,
            "schema_version": self.schema_version,
            "sha256": self.sha256,
            "status": self.status,
            "task_id": self.task_id,
        }


@dataclass(frozen=True)
class AcceptanceTaskImportRecord:
    """Normalized import record for one MLA task."""

    task_id: str
    status: str
    expected_artifacts: tuple[str, ...]
    missing_artifacts: tuple[str, ...]
    artifact_records: tuple[AcceptanceArtifactRecord, ...]
    expected_safety_block_confirmed: bool = False
    findings: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_records": [artifact.to_dict() for artifact in self.artifact_records],
            "expected_artifacts": list(self.expected_artifacts),
            "expected_safety_block_confirmed": self.expected_safety_block_confirmed,
            "findings": list(self.findings),
            "missing_artifacts": list(self.missing_artifacts),
            "status": self.status,
            "task_id": self.task_id,
        }


@dataclass(frozen=True)
class AcceptanceImportSummary:
    """Deterministic summary for a local acceptance execution packet import."""

    schema_version: str
    lane_id: str
    source_execution_lane_id: str
    packet_dir: str
    output_dir: str
    status: str
    task_records: tuple[AcceptanceTaskImportRecord, ...]
    artifacts: tuple[AcceptanceArtifactRecord, ...]
    coverage: tuple[str, ...]
    missing_tasks: tuple[str, ...]
    checksum_algorithm: str = "sha256"
    evidence_boundary_status: str = "not_checked"
    non_execution_status: str = "not_checked"
    redaction_status: str = "not_checked"
    source_artifact_mutation_status: str = "not_checked"
    readiness_interpretation: str = "not_interpreted"
    mvp_readiness: str = "unclaimed"
    selected_next_lane: str = SELECTED_NEXT_LANE
    blocker_fallback_lane: str = BLOCKER_FALLBACK_LANE
    findings: tuple[str, ...] = field(default_factory=tuple)

    @property
    def blocked(self) -> bool:
        return self.status in BLOCKED_STATUSES

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifacts": [artifact.to_dict() for artifact in self.artifacts],
            "blocker_fallback_lane": self.blocker_fallback_lane,
            "checksum_algorithm": self.checksum_algorithm,
            "coverage": list(self.coverage),
            "evidence_boundary_status": self.evidence_boundary_status,
            "findings": list(self.findings),
            "lane_id": self.lane_id,
            "missing_tasks": list(self.missing_tasks),
            "mvp_readiness": self.mvp_readiness,
            "non_execution_status": self.non_execution_status,
            "output_dir": self.output_dir,
            "packet_dir": self.packet_dir,
            "readiness_interpretation": self.readiness_interpretation,
            "redaction_status": self.redaction_status,
            "schema_version": self.schema_version,
            "selected_next_lane": self.selected_next_lane,
            "source_artifact_mutation_status": self.source_artifact_mutation_status,
            "source_execution_lane_id": self.source_execution_lane_id,
            "status": self.status,
            "task_records": [record.to_dict() for record in self.task_records],
        }


def import_acceptance_execution_packet(packet_dir: Path, output_dir: Path) -> AcceptanceImportSummary:
    """Import a local acceptance execution packet without mutating source artifacts."""

    packet_root = packet_dir.resolve()
    output_root = output_dir.resolve()
    findings: list[str] = []

    if not packet_root.exists() or not packet_root.is_dir():
        return _summary(
            packet_root,
            output_root,
            "blocked_missing_artifact",
            (),
            (),
            (),
            TASK_IDS,
            "missing",
            "missing",
            "missing",
            "not_checked",
            ("packet directory is missing",),
        )

    expected_by_task = _expected_artifacts_by_task(packet_root)
    ledger_by_task = _artifact_ledger_by_task(packet_root)
    task_records: list[AcceptanceTaskImportRecord] = []
    artifact_records: list[AcceptanceArtifactRecord] = []
    status_candidates: list[str] = []
    discovered_tasks: set[str] = set()

    for task_id in TASK_IDS:
        expected_artifacts = tuple(sorted(expected_by_task.get(task_id, ())))
        task_dir = packet_root / "raw-artifacts" / task_id
        if task_dir.exists():
            discovered_tasks.add(task_id)
        missing_artifacts: list[str] = []
        task_artifacts: list[AcceptanceArtifactRecord] = []
        task_findings: list[str] = []

        for artifact_name in expected_artifacts:
            ledger_entry = ledger_by_task.get(task_id, {}).get(artifact_name, {})
            artifact_path = _artifact_path(packet_root, task_id, artifact_name, ledger_entry)
            if not _is_within(artifact_path, packet_root):
                record = AcceptanceArtifactRecord(
                    task_id=task_id,
                    artifact_name=artifact_name,
                    path=str(artifact_path),
                    relative_path=_safe_relative(artifact_path, packet_root),
                    present=False,
                    expected_sha256=str(ledger_entry.get("checksum", "")),
                    status="blocked_malformed_artifact",
                    findings=("artifact path outside execution packet",),
                )
                task_artifacts.append(record)
                task_findings.append("artifact path outside execution packet")
                status_candidates.append(record.status)
                continue
            if not artifact_path.exists():
                missing_artifacts.append(artifact_name)
                record = AcceptanceArtifactRecord(
                    task_id=task_id,
                    artifact_name=artifact_name,
                    path=str(artifact_path),
                    relative_path=_safe_relative(artifact_path, packet_root),
                    present=False,
                    expected_sha256=str(ledger_entry.get("checksum", "")),
                    status="blocked_missing_artifact",
                    findings=("expected artifact is missing",),
                )
                task_artifacts.append(record)
                status_candidates.append(record.status)
                continue
            record = _validate_artifact(packet_root, task_id, artifact_name, artifact_path, ledger_entry)
            task_artifacts.append(record)
            status_candidates.append(record.status)

        stop_state_present = any(
            artifact.artifact_name == "stop-state.json" and artifact.present and artifact.status == "import_ready"
            for artifact in task_artifacts
        )
        expected_safety_block_confirmed = stop_state_present and bool(expected_artifacts)
        task_status = _combine_status([artifact.status for artifact in task_artifacts])
        if task_status == "import_ready" and stop_state_present:
            task_status = "import_ready_with_expected_blocks"
        if missing_artifacts:
            task_status = "blocked_missing_artifact"
        task_records.append(
            AcceptanceTaskImportRecord(
                task_id=task_id,
                status=task_status,
                expected_artifacts=expected_artifacts,
                missing_artifacts=tuple(sorted(missing_artifacts)),
                artifact_records=tuple(task_artifacts),
                expected_safety_block_confirmed=expected_safety_block_confirmed,
                findings=tuple(sorted(set(task_findings))),
            )
        )
        artifact_records.extend(task_artifacts)
        status_candidates.append(task_status)

    missing_tasks = tuple(task_id for task_id in TASK_IDS if task_id not in expected_by_task)
    if missing_tasks:
        status_candidates.append("blocked_missing_artifact")
        findings.append("MLA-001 through MLA-010 coverage is incomplete")

    evidence_boundary_status = _validate_evidence_boundary(packet_root, artifact_records)
    non_execution_status = _validate_non_execution(packet_root, artifact_records)
    redaction_status = _validate_redaction(packet_root, artifact_records)
    source_mutation_status = _validate_source_mutation(packet_root, artifact_records)
    for check_status in (evidence_boundary_status, non_execution_status, redaction_status, source_mutation_status):
        if check_status.startswith("blocked_"):
            status_candidates.append(check_status)

    status = _combine_status(status_candidates)
    if status == "import_ready" and any(record.status == "import_ready_with_expected_blocks" for record in task_records):
        status = "import_ready_with_expected_blocks"

    return _summary(
        packet_root,
        output_root,
        status,
        tuple(task_records),
        tuple(sorted(artifact_records, key=lambda item: (item.task_id, item.artifact_name, item.relative_path))),
        tuple(task_id for task_id in TASK_IDS if task_id in expected_by_task or task_id in discovered_tasks),
        missing_tasks,
        evidence_boundary_status,
        non_execution_status,
        redaction_status,
        source_mutation_status,
        tuple(sorted(set(findings))),
    )


def write_acceptance_import_summary(summary: AcceptanceImportSummary, output_path: Path) -> Path:
    """Write a deterministic JSON acceptance import summary."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_json_dumps(summary.to_dict()) + "\n", encoding="utf-8")
    return output_path


def _summary(
    packet_root: Path,
    output_root: Path,
    status: str,
    task_records: tuple[AcceptanceTaskImportRecord, ...],
    artifacts: tuple[AcceptanceArtifactRecord, ...],
    coverage: tuple[str, ...],
    missing_tasks: tuple[str, ...],
    evidence_boundary_status: str,
    non_execution_status: str,
    redaction_status: str,
    source_mutation_status: str,
    findings: tuple[str, ...],
) -> AcceptanceImportSummary:
    return AcceptanceImportSummary(
        schema_version=ACCEPTANCE_IMPORT_SCHEMA_VERSION,
        lane_id=IMPORT_LANE_ID,
        source_execution_lane_id=EXECUTION_LANE_ID,
        packet_dir=str(packet_root),
        output_dir=str(output_root),
        status=status,
        task_records=tuple(sorted(task_records, key=lambda item: item.task_id)),
        artifacts=artifacts,
        coverage=tuple(sorted(coverage)),
        missing_tasks=tuple(sorted(missing_tasks)),
        evidence_boundary_status=evidence_boundary_status,
        non_execution_status=non_execution_status,
        redaction_status=redaction_status,
        source_artifact_mutation_status=source_mutation_status,
        findings=findings,
    )


def _validate_artifact(
    packet_root: Path,
    task_id: str,
    artifact_name: str,
    artifact_path: Path,
    ledger_entry: Mapping[str, str],
) -> AcceptanceArtifactRecord:
    findings: list[str] = []
    status = "import_ready"
    digest = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
    expected_sha = str(ledger_entry.get("checksum", ""))
    checksum_status = "matched" if expected_sha and digest == expected_sha else "generated"
    if expected_sha and digest != expected_sha:
        status = "blocked_checksum_mismatch"
        checksum_status = "mismatched"
        findings.append("checksum mismatch")

    payload: Any = None
    if artifact_name in JSON_ARTIFACT_NAMES:
        try:
            payload = json.loads(artifact_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return AcceptanceArtifactRecord(
                task_id=task_id,
                artifact_name=artifact_name,
                path=str(artifact_path),
                relative_path=_safe_relative(artifact_path, packet_root),
                present=True,
                sha256=digest,
                expected_sha256=expected_sha,
                checksum_status=checksum_status,
                status="blocked_malformed_artifact",
                findings=("malformed JSON artifact",),
            )
        if not isinstance(payload, Mapping):
            status = _more_severe(status, "blocked_malformed_artifact")
            findings.append("JSON artifact root is not an object")
            payload = {}

    schema_version = str(_lookup(payload, "schema_version") or ledger_entry.get("schema_version", ""))
    lane_id = str(_lookup(payload, "lane_id") or ledger_entry.get("lane_id", ""))
    run_id = str(_lookup(payload, "run_id") or ledger_entry.get("run_id", ""))
    redaction_status = str(_lookup(payload, "redaction_status") or ledger_entry.get("redaction_status", ""))
    evidence_boundary = str(_lookup(payload, "evidence_boundary") or ledger_entry.get("evidence_boundary", ""))
    non_execution = str(_lookup(payload, "non_execution_confirmation") or ledger_entry.get("non_execution_marker", ""))

    metadata_task_id = _lookup(payload, "proposed_task_summary", "metadata", "mla_task_id")
    if metadata_task_id and str(metadata_task_id) != task_id:
        status = _more_severe(status, "blocked_malformed_artifact")
        findings.append("task ID mismatch")
    metadata_execution_lane = _lookup(payload, "proposed_task_summary", "metadata", "execution_lane_id")
    if metadata_execution_lane and str(metadata_execution_lane) != EXECUTION_LANE_ID:
        status = _more_severe(status, "blocked_malformed_artifact")
        findings.append("execution lane ID mismatch")
    metadata_run_id = _lookup(payload, "proposed_task_summary", "metadata", "run_id")
    if metadata_run_id and run_id and str(metadata_run_id) != run_id:
        status = _more_severe(status, "blocked_malformed_artifact")
        findings.append("run ID mismatch")
    for field_name, value in (("schema version", schema_version), ("lane ID", lane_id), ("run ID", run_id)):
        if artifact_name in JSON_ARTIFACT_NAMES and not value:
            status = _more_severe(status, "blocked_malformed_artifact")
            findings.append(f"missing {field_name}")
    ledger_lane = str(ledger_entry.get("lane_id", ""))
    if ledger_lane and lane_id and ledger_lane != lane_id:
        status = _more_severe(status, "blocked_malformed_artifact")
        findings.append("ledger lane ID mismatch")
    ledger_run = str(ledger_entry.get("run_id", ""))
    if ledger_run and run_id and ledger_run != run_id:
        status = _more_severe(status, "blocked_malformed_artifact")
        findings.append("ledger run ID mismatch")
    ledger_schema = str(ledger_entry.get("schema_version", ""))
    if ledger_schema and schema_version and ledger_schema != schema_version:
        status = _more_severe(status, "blocked_malformed_artifact")
        findings.append("ledger schema version mismatch")
    if redaction_status and redaction_status != "redacted":
        status = _more_severe(status, "blocked_redaction_failure")
        findings.append("redaction status is not redacted")
    payload_non_execution = str(_lookup(payload, "non_execution_confirmation") or "")
    if artifact_name == "dry-run-result.json" and "does not execute" not in payload_non_execution.lower():
        status = _more_severe(status, "blocked_non_execution_missing")
        findings.append("non-execution confirmation missing")
    if artifact_name in JSON_ARTIFACT_NAMES and not _evidence_boundary_is_safe(evidence_boundary):
        status = _more_severe(status, "blocked_evidence_boundary_failure")
        findings.append("evidence boundary missing safe markers")
    if any(not occurrence.expected_blocked_context for occurrence in find_source_mutation_markers(payload)):
        status = _more_severe(status, "blocked_source_mutation_concern")
        findings.append("source-artifact mutation marker present")

    return AcceptanceArtifactRecord(
        task_id=task_id,
        artifact_name=artifact_name,
        path=str(artifact_path),
        relative_path=_safe_relative(artifact_path, packet_root),
        present=True,
        sha256=digest,
        expected_sha256=expected_sha,
        checksum_status=checksum_status,
        schema_version=schema_version,
        lane_id=lane_id,
        run_id=run_id,
        redaction_status=redaction_status,
        evidence_boundary=evidence_boundary,
        non_execution_confirmation=non_execution,
        status=status,
        findings=tuple(sorted(set(findings))),
    )


def _expected_artifacts_by_task(packet_root: Path) -> dict[str, tuple[str, ...]]:
    raw_index = packet_root / "raw-artifacts-index.md"
    expected: dict[str, tuple[str, ...]] = {}
    if raw_index.exists():
        for row in _markdown_rows(raw_index):
            if len(row) < 3 or row[0] not in TASK_IDS:
                continue
            artifacts = _split_artifact_cell(row[1])
            expected[row[0]] = tuple(sorted(artifacts))
    if not expected:
        raw_root = packet_root / "raw-artifacts"
        for task_id in TASK_IDS:
            task_dir = raw_root / task_id
            if task_dir.exists():
                expected[task_id] = tuple(sorted(path.name for path in task_dir.glob("*.json")))
    return expected


def _artifact_ledger_by_task(packet_root: Path) -> dict[str, dict[str, dict[str, str]]]:
    ledger = packet_root / "artifact-ledger.md"
    by_task: dict[str, dict[str, dict[str, str]]] = {}
    if not ledger.exists():
        return by_task
    for row in _markdown_rows(ledger):
        if len(row) < 10 or row[0] not in TASK_IDS:
            continue
        by_task.setdefault(row[0], {})[row[1]] = {
            "artifact": row[1],
            "path": row[2],
            "checksum": row[3],
            "schema_version": row[4],
            "lane_id": row[5],
            "run_id": row[6],
            "redaction_status": row[7],
            "evidence_boundary": row[8],
            "non_execution_marker": row[9],
        }
    return by_task


def _markdown_rows(path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        cells = [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]
        if cells and cells[0] != "Task ID":
            rows.append(cells)
    return rows


def _split_artifact_cell(cell: str) -> tuple[str, ...]:
    if cell.lower() in {"none", "none produced", "n/a", ""}:
        return ()
    return tuple(part.strip().strip("`") for part in cell.split(";") if part.strip() and part.strip().lower() != "none")


def _artifact_path(packet_root: Path, task_id: str, artifact_name: str, ledger_entry: Mapping[str, str]) -> Path:
    ledger_path = str(ledger_entry.get("path", ""))
    if ledger_path:
        candidate = Path(ledger_path)
        if candidate.is_absolute():
            return candidate.resolve()
        packet_relative = (packet_root / candidate).resolve()
        if packet_relative.exists() or ".." in candidate.parts:
            return packet_relative
        return (Path.cwd() / candidate).resolve()
    return (packet_root / "raw-artifacts" / task_id / artifact_name).resolve()


def _validate_evidence_boundary(packet_root: Path, artifacts: tuple[AcceptanceArtifactRecord, ...]) -> str:
    text = _read_optional(packet_root / "evidence-boundary.md") + "\n" + _read_optional(packet_root / "evidence-boundary-review.md")
    if "local-only" not in text.lower():
        return "blocked_evidence_boundary_failure"
    # The packet may state its non-execution marker in the dedicated
    # non-execution-proof.md (separately validated by _validate_non_execution)
    # instead of repeating the phrase inside the boundary files.
    combined = text + "\n" + _read_optional(packet_root / "non-execution-proof.md")
    if not _evidence_boundary_is_safe(combined):
        return "blocked_evidence_boundary_failure"
    lower = text.lower()
    if "does not claim mvp readiness" not in lower and "no mvp readiness" not in lower:
        if "claim mvp readiness" in lower or "mvp readiness: ready" in lower:
            return "blocked_evidence_boundary_failure"
    if any(artifact.status == "blocked_evidence_boundary_failure" for artifact in artifacts):
        return "blocked_evidence_boundary_failure"
    return "present"


def _validate_non_execution(packet_root: Path, artifacts: tuple[AcceptanceArtifactRecord, ...]) -> str:
    text = _read_optional(packet_root / "non-execution-proof.md")
    lower = text.lower()
    if "does not execute" not in lower and "were not executed" not in lower:
        return "blocked_non_execution_missing"
    if any(artifact.status == "blocked_non_execution_missing" for artifact in artifacts):
        return "blocked_non_execution_missing"
    return "present"


def _validate_redaction(packet_root: Path, artifacts: tuple[AcceptanceArtifactRecord, ...]) -> str:
    text = _read_optional(packet_root / "redaction-review.md").lower()
    if "redaction status" not in text or "pass" not in text:
        return "blocked_redaction_failure"
    if "real credentials" in text and "none" not in text:
        return "blocked_redaction_failure"
    if any(artifact.status == "blocked_redaction_failure" for artifact in artifacts):
        return "blocked_redaction_failure"
    return "redacted"


def _validate_source_mutation(packet_root: Path, artifacts: tuple[AcceptanceArtifactRecord, ...]) -> str:
    packet_text = "\n".join(
        _read_optional(packet_root / name)
        for name in ("artifact-integrity-checks.md", "stop-state-review.md", "non-actions.md")
    )
    if "source-artifact mutation" in packet_text.lower() and "blocked" not in packet_text.lower():
        return "blocked_source_mutation_concern"
    if any(artifact.status == "blocked_source_mutation_concern" for artifact in artifacts):
        return "blocked_source_mutation_concern"
    return "not_present"


def _evidence_boundary_is_safe(text: str) -> bool:
    lower = text.lower()
    return "local-only" in lower and ("no execution" in lower or "does not execute" in lower or "not executed" in lower)


def find_source_mutation_markers(payload: Any) -> tuple[SourceMutationMarkerOccurrence, ...]:
    """Locate source-mutation marker strings and whether each sits in a blocked-finding context.

    A marker is expected only in the exact shapes the dry-run harness emits when it
    refuses a proposed source mutation (see ``command_classification``): the
    ``SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED`` finding ID and the
    ``source_artifact_mutation`` reason code inside blocked findings, ``finding_ids``
    lists, or ``command_reason_codes`` lists of a blocked summary. Every other
    occurrence is reported as unexpected so true mutation evidence keeps blocking.
    """

    occurrences: list[SourceMutationMarkerOccurrence] = []
    _collect_source_mutation_markers(payload, "$", None, None, occurrences)
    return tuple(occurrences)


def _collect_source_mutation_markers(
    value: Any,
    json_path: str,
    parent: Mapping[str, Any] | None,
    key: str | None,
    occurrences: list[SourceMutationMarkerOccurrence],
) -> None:
    if isinstance(value, Mapping):
        for child_key, child_value in value.items():
            child_key_text = str(child_key)
            if _contains_source_mutation_text(child_key_text):
                occurrences.append(
                    SourceMutationMarkerOccurrence(f"{json_path}.{child_key_text}<key>", child_key_text, False)
                )
            _collect_source_mutation_markers(child_value, f"{json_path}.{child_key_text}", value, child_key_text, occurrences)
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _collect_source_mutation_markers(item, f"{json_path}[{index}]", parent, key, occurrences)
        return
    if isinstance(value, str) and _contains_source_mutation_text(value):
        occurrences.append(
            SourceMutationMarkerOccurrence(json_path, value, _is_expected_blocked_marker_context(value, key, parent))
        )


def _contains_source_mutation_text(text: str) -> bool:
    lower = text.lower()
    return SOURCE_MUTATION_REASON_CODE in lower or SOURCE_MUTATION_BLOCKED_FINDING_ID.lower() in lower


def _is_expected_blocked_marker_context(text: str, key: str | None, parent: Mapping[str, Any] | None) -> bool:
    if not isinstance(parent, Mapping) or key is None:
        return False
    if key in {"id", "finding_ids"}:
        return text == SOURCE_MUTATION_BLOCKED_FINDING_ID and _mapping_indicates_blocked(parent)
    if key == "command_reason_codes":
        return text == SOURCE_MUTATION_REASON_CODE and _mapping_indicates_blocked(parent)
    if key == "reason_code":
        return (
            text == SOURCE_MUTATION_REASON_CODE
            and str(parent.get("id", "")) == SOURCE_MUTATION_BLOCKED_FINDING_ID
            and _mapping_indicates_blocked(parent)
        )
    return False


def _mapping_indicates_blocked(mapping: Mapping[str, Any]) -> bool:
    if str(mapping.get("stop_state", "")).lower() == "blocked":
        return True
    for status_key in ("gate_status", "dry_run_status"):
        if str(mapping.get(status_key, "")).lower().startswith("blocked"):
            return True
    return any(mapping.get(allowed_key) is False for allowed_key in ("allowed", "allowed_for_local_dry_run"))


def _lookup(payload: Any, *keys: str) -> Any:
    current = payload
    for key in keys:
        if not isinstance(current, Mapping):
            return None
        current = current.get(key)
    return current


def _read_optional(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _safe_relative(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def _combine_status(statuses: list[str] | tuple[str, ...]) -> str:
    for status in (
        "blocked_source_mutation_concern",
        "blocked_malformed_artifact",
        "blocked_missing_artifact",
        "blocked_redaction_failure",
        "blocked_evidence_boundary_failure",
        "blocked_non_execution_missing",
        "blocked_checksum_mismatch",
        "blocked_unknown",
    ):
        if status in statuses:
            return status
    if "import_ready_with_expected_blocks" in statuses:
        return "import_ready_with_expected_blocks"
    return "import_ready"


def _more_severe(current: str, candidate: str) -> str:
    return _combine_status([current, candidate])


def _json_dumps(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, separators=(",", ": "))
