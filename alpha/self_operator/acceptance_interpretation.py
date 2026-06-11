"""Deterministic Self Operator acceptance import interpretation.

This module interprets local acceptance import summaries only. It does not run
Self Operator tasks, inspect real evidence directly, update external systems, or
claim MVP/release readiness.

Accepted input vocabularies for ``self_operator.acceptance_import_summary.v1``:
explicit per-task ``observed_outcome`` plus top-level safety booleans
(``redaction_safe``, ``evidence_boundary_preserved``, ``source_mutation_absent``,
``non_execution_proof``), and the result importer's emitted form: per-task
``status``/``expected_safety_block_confirmed`` plus top-level
``redaction_status``/``evidence_boundary_status``/
``source_artifact_mutation_status``/``non_execution_status``.

An optional, explicit operator-decision artifact
(``self_operator.expected_safety_block_operator_review.v1``) may additionally
be consumed. A valid ``ACCEPT_LEDGER_LEVEL_CONFIRMATION`` decision closes only
the MLA-006/MLA-007 ``EXPECTED_SAFETY_BLOCK_UNCONFIRMED`` blockers, recording
the confirmation of record as ``operator_ledger_level_acceptance`` — a
distinct confirmation type that is never machine-readable artifact
confirmation. An invalid, missing, ambiguous, or wrong-task decision is never
consumed and leaves interpretation blocked exactly as before.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

INTERPRETATION_SCHEMA_VERSION = "self_operator.acceptance_interpretation.v1"
LANE_ID = "ALPHA-SOLVER-POST-LEVEL-3-TO-LEVEL-14-SELF-OPERATOR-ACCEPTANCE-INTERPRETATION-ENGINE-001"
READINESS_BLOCKED = "blocked"
READINESS_NEEDS_REVIEW = "needs_review"
READINESS_ELIGIBLE_FOR_LATER_RELEASE_REVIEW = "eligible_for_later_release_review"
ALLOWED_READINESS_IMPLICATIONS = (
    READINESS_BLOCKED,
    READINESS_NEEDS_REVIEW,
    READINESS_ELIGIBLE_FOR_LATER_RELEASE_REVIEW,
)
REQUIRED_TASK_IDS = tuple(f"MLA-{index:03d}" for index in range(1, 11))
# Expectation map per the operator-supervised local acceptance plan and ledger:
# MLA-010 (non-execution proof) is an expected safety block confirmed by a
# stop-state, not an expected-safe task.
EXPECTED_SAFE_TASK_IDS = ("MLA-001", "MLA-008", "MLA-009")
EXPECTED_SAFETY_BLOCKED_TASK_IDS = (
    "MLA-002",
    "MLA-003",
    "MLA-004",
    "MLA-005",
    "MLA-006",
    "MLA-007",
    "MLA-010",
)
# Importer task statuses describe import readiness, not the proposed action's
# outcome; blocked_* importer statuses are import failures, not safety blocks.
IMPORTER_IMPORT_READY_STATUSES = frozenset({"import_ready", "import_ready_with_expected_blocks"})
IMPORTER_IMPORT_FAILURE_STATUSES = frozenset(
    {
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
# Importer top-level status fields equivalent to the boolean safety fields,
# with the values that confirm the safe condition.
TOP_LEVEL_SAFETY_STATUS_SYNONYMS = {
    "redaction_safe": ("redaction_status", frozenset({"redacted"})),
    "evidence_boundary_preserved": ("evidence_boundary_status", frozenset({"present"})),
    "source_mutation_absent": ("source_artifact_mutation_status", frozenset({"not_present"})),
    "non_execution_proof": ("non_execution_status", frozenset({"present"})),
}
DEFECT_SEVERITY_DESCRIPTIONS = {
    "P0": "evidence boundary or source mutation violation",
    "P1": "approval, identity, stop-state, or non-execution safety failure",
    "P2": "artifact schema, import-readiness, determinism, checksum, or redaction failure",
    "P3": "docs, clarity, or operator UX issue",
}
BLOCKING_CLASSIFICATIONS = (
    "blocked_missing_artifacts",
    "blocked_malformed_artifacts",
    "blocked_redaction_failure",
    "blocked_non_execution_failure",
    "blocked_evidence_boundary_failure",
    "blocked_source_mutation_concern",
    "blocked_unexpected_ready",
    "blocked_unexpected_failure",
)
# Explicit operator-decision artifact contract (PR #469 packet). The decision
# may close only the MLA-006/MLA-007 EXPECTED_SAFETY_BLOCK_UNCONFIRMED
# blockers; it is operator ledger-level acceptance, never machine-readable
# artifact confirmation.
OPERATOR_DECISION_SCHEMA_VERSION = "self_operator.expected_safety_block_operator_review.v1"
OPERATOR_DECISION_LANE_ID = (
    "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-TO-LEVEL-14-SELF-OPERATOR-"
    "EXPECTED-SAFETY-BLOCK-OPERATOR-REVIEW-001"
)
OPERATOR_DECISION_ACCEPT_LEDGER_LEVEL_CONFIRMATION = "ACCEPT_LEDGER_LEVEL_CONFIRMATION"
OPERATOR_DECISION_ACCEPTED_TASK_IDS = ("MLA-006", "MLA-007")
CONFIRMATION_TYPE_OPERATOR_LEDGER_LEVEL_ACCEPTANCE = "operator_ledger_level_acceptance"
CONFIRMATION_TYPE_MACHINE_READABLE_ARTIFACT = "machine_readable_artifact"
CONFIRMATION_UNCONFIRMED = "unconfirmed"
CONFIRMATION_OF_RECORD_TYPES = frozenset(
    {
        CONFIRMATION_TYPE_MACHINE_READABLE_ARTIFACT,
        CONFIRMATION_TYPE_OPERATOR_LEDGER_LEVEL_ACCEPTANCE,
    }
)


@dataclass(frozen=True)
class AcceptanceDefect:
    """A normalized defect found while interpreting imported acceptance results."""

    code: str
    severity: str
    message: str
    task_id: str | None = None
    classification: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "classification": self.classification,
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "severity_description": DEFECT_SEVERITY_DESCRIPTIONS[self.severity],
            "task_id": self.task_id,
        }


@dataclass(frozen=True)
class AcceptanceTaskInterpretation:
    """Interpretation for a single MLA task imported from local acceptance."""

    task_id: str
    expected_outcome: str
    observed_outcome: str
    import_ready: bool
    status: str
    expected_block_confirmation: str | None = None
    classifications: tuple[str, ...] = field(default_factory=tuple)
    defects: tuple[AcceptanceDefect, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "classifications": list(self.classifications),
            "defects": [defect.to_dict() for defect in self.defects],
            "expected_block_confirmation": self.expected_block_confirmation,
            "expected_outcome": self.expected_outcome,
            "import_ready": self.import_ready,
            "observed_outcome": self.observed_outcome,
            "status": self.status,
            "task_id": self.task_id,
        }


@dataclass(frozen=True)
class AcceptanceInterpretation:
    """Bounded readiness interpretation for an imported acceptance summary."""

    schema_version: str
    lane_id: str
    readiness_implication: str
    summary: Mapping[str, Any]
    classifications: Mapping[str, bool]
    tasks: tuple[AcceptanceTaskInterpretation, ...]
    defects: tuple[AcceptanceDefect, ...]
    operator_decision_consumption: Mapping[str, Any] = field(default_factory=dict)
    required_task_ids: tuple[str, ...] = REQUIRED_TASK_IDS
    expected_safe_task_ids: tuple[str, ...] = EXPECTED_SAFE_TASK_IDS
    expected_safety_blocked_task_ids: tuple[str, ...] = EXPECTED_SAFETY_BLOCKED_TASK_IDS
    non_claims: tuple[str, ...] = (
        "does not claim MVP readiness",
        "does not claim release readiness",
        "does not claim production readiness",
        "does not interpret real evidence directly",
        "does not treat operator ledger-level acceptance as machine-readable artifact confirmation",
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "classifications": dict(sorted(self.classifications.items())),
            "defect_severity_contract": dict(sorted(DEFECT_SEVERITY_DESCRIPTIONS.items())),
            "defects": [defect.to_dict() for defect in self.defects],
            "expected_safe_task_ids": list(self.expected_safe_task_ids),
            "expected_safety_blocked_task_ids": list(self.expected_safety_blocked_task_ids),
            "lane_id": self.lane_id,
            "non_claims": list(self.non_claims),
            "operator_decision_consumption": dict(sorted(self.operator_decision_consumption.items())),
            "readiness_implication": self.readiness_implication,
            "required_task_ids": list(self.required_task_ids),
            "schema_version": self.schema_version,
            "summary": dict(sorted(self.summary.items())),
            "tasks": [task.to_dict() for task in self.tasks],
        }


def interpret_acceptance_import_summary(
    import_summary: Mapping[str, Any],
    operator_decision: Mapping[str, Any] | None = None,
) -> AcceptanceInterpretation:
    """Interpret an acceptance import summary without mutating source artifacts.

    ``operator_decision`` is the optional, explicit
    ``self_operator.expected_safety_block_operator_review.v1`` artifact. When
    absent, behavior is unchanged from decision-unaware interpretation.
    """

    classifications = _empty_classifications()
    defects: list[AcceptanceDefect] = []
    task_interpretations: list[AcceptanceTaskInterpretation] = []

    decision_provided = operator_decision is not None
    decision_errors = validate_operator_decision(operator_decision) if decision_provided else ()
    decision_consumed = decision_provided and not decision_errors
    operator_accepted_task_ids = (
        frozenset(OPERATOR_DECISION_ACCEPTED_TASK_IDS) if decision_consumed else frozenset()
    )
    if decision_provided and decision_errors:
        classifications["blocked_malformed_artifacts"] = True
        defects.append(
            _defect(
                "OPERATOR_DECISION_INVALID",
                "P2",
                "Operator decision artifact was not consumed: " + "; ".join(decision_errors) + ".",
                "blocked_malformed_artifacts",
            )
        )

    if not isinstance(import_summary, Mapping):
        classifications["blocked_malformed_artifacts"] = True
        defects.append(_defect("IMPORT_SUMMARY_NOT_MAPPING", "P2", "Import summary is not a JSON object.", "blocked_malformed_artifacts"))
        return _build_interpretation(classifications, task_interpretations, defects, _operator_decision_consumption(decision_provided, decision_errors, task_interpretations))

    records = _extract_task_records(import_summary)
    if records is None:
        classifications["blocked_malformed_artifacts"] = True
        defects.append(_defect("IMPORT_SUMMARY_MISSING_TASK_RECORDS", "P2", "Import summary does not contain task records.", "blocked_malformed_artifacts"))
        return _build_interpretation(classifications, task_interpretations, defects, _operator_decision_consumption(decision_provided, decision_errors, task_interpretations))

    malformed_records = False
    seen_task_ids: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            malformed_records = True
            defects.append(_defect("TASK_RECORD_NOT_MAPPING", "P2", f"Task record at index {index} is not an object.", "blocked_malformed_artifacts"))
            continue
        task = _interpret_task(record, operator_accepted_task_ids)
        task_interpretations.append(task)
        seen_task_ids.add(task.task_id)
        defects.extend(task.defects)

    if malformed_records:
        classifications["blocked_malformed_artifacts"] = True

    missing_task_ids = tuple(task_id for task_id in REQUIRED_TASK_IDS if task_id not in seen_task_ids)
    if missing_task_ids:
        classifications["blocked_missing_artifacts"] = True
        defects.append(
            _defect(
                "REQUIRED_TASK_IDS_MISSING",
                "P2",
                "Required task IDs are missing: " + ", ".join(missing_task_ids) + ".",
                "blocked_missing_artifacts",
            )
        )

    for defect in _top_level_defects(import_summary):
        defects.append(defect)

    for defect in _incomplete_summary_defects(import_summary, task_interpretations):
        defects.append(defect)

    _merge_task_classifications(classifications, task_interpretations)
    _merge_defect_classifications(classifications, defects)
    _merge_top_level_classifications(classifications, import_summary)
    _merge_success_classifications(classifications, task_interpretations, missing_task_ids)

    return _build_interpretation(classifications, task_interpretations, defects, _operator_decision_consumption(decision_provided, decision_errors, task_interpretations))


def validate_operator_decision(operator_decision: Any) -> tuple[str, ...]:
    """Validate the explicit operator-decision artifact; return error reasons.

    An empty tuple means the decision is valid for consumption. Any other
    result means the decision must not be consumed: schema, lane ID, decision
    value, accepted tasks, confirmation type, and safety flags are all
    required to match the recorded #469 artifact exactly. In particular,
    ``machine_readable_artifact_confirmation`` must be ``false`` — a decision
    claiming machine-readable artifact confirmation on this path is rejected.
    """

    if not isinstance(operator_decision, Mapping):
        return ("operator decision is not a JSON object",)
    errors: list[str] = []
    schema = operator_decision.get("schema")
    if schema != OPERATOR_DECISION_SCHEMA_VERSION:
        errors.append(f"schema must be {OPERATOR_DECISION_SCHEMA_VERSION}, got {schema!r}")
    lane_id = operator_decision.get("lane_id")
    if lane_id != OPERATOR_DECISION_LANE_ID:
        errors.append(f"lane_id must be {OPERATOR_DECISION_LANE_ID}, got {lane_id!r}")
    decision_value = operator_decision.get("operator_decision")
    if decision_value != OPERATOR_DECISION_ACCEPT_LEDGER_LEVEL_CONFIRMATION:
        errors.append(
            f"operator_decision must be {OPERATOR_DECISION_ACCEPT_LEDGER_LEVEL_CONFIRMATION}, got {decision_value!r}"
        )
    accepted_tasks = operator_decision.get("accepted_tasks")
    if (
        not isinstance(accepted_tasks, Sequence)
        or isinstance(accepted_tasks, (str, bytes, bytearray))
        or sorted(str(task_id) for task_id in accepted_tasks) != sorted(OPERATOR_DECISION_ACCEPTED_TASK_IDS)
    ):
        errors.append(
            "accepted_tasks must be exactly "
            + str(list(OPERATOR_DECISION_ACCEPTED_TASK_IDS))
            + f", got {accepted_tasks!r}"
        )
    confirmation_type = operator_decision.get("confirmation_type")
    if confirmation_type != CONFIRMATION_TYPE_OPERATOR_LEDGER_LEVEL_ACCEPTANCE:
        errors.append(
            f"confirmation_type must be {CONFIRMATION_TYPE_OPERATOR_LEDGER_LEVEL_ACCEPTANCE}, got {confirmation_type!r}"
        )
    if operator_decision.get("machine_readable_artifact_confirmation") is not False:
        errors.append(
            "machine_readable_artifact_confirmation must be false: operator ledger-level "
            "acceptance is not machine-readable artifact confirmation"
        )
    if operator_decision.get("source_artifacts_mutated") is not False:
        errors.append("source_artifacts_mutated must be false")
    if operator_decision.get("readiness_claimed") is not False:
        errors.append("readiness_claimed must be false")
    return tuple(errors)


def _operator_decision_consumption(
    provided: bool,
    errors: Sequence[str],
    tasks: Sequence[AcceptanceTaskInterpretation],
) -> dict[str, Any]:
    """Build the deterministic record of how the operator decision was used."""

    consumed = provided and not errors
    applied_task_ids = sorted(
        task.task_id
        for task in tasks
        if task.expected_block_confirmation == CONFIRMATION_TYPE_OPERATOR_LEDGER_LEVEL_ACCEPTANCE
    )
    return {
        "accepted_task_ids": list(OPERATOR_DECISION_ACCEPTED_TASK_IDS) if consumed else [],
        "applied_task_ids": applied_task_ids,
        "confirmation_type": CONFIRMATION_TYPE_OPERATOR_LEDGER_LEVEL_ACCEPTANCE if consumed else None,
        "consumed": consumed,
        "decision": OPERATOR_DECISION_ACCEPT_LEDGER_LEVEL_CONFIRMATION if consumed else None,
        "decision_lane_id": OPERATOR_DECISION_LANE_ID if consumed else None,
        "decision_schema": OPERATOR_DECISION_SCHEMA_VERSION if consumed else None,
        "machine_readable_artifact_confirmation": False,
        "provided": provided,
        "validation_errors": list(errors),
    }


def write_acceptance_interpretation(interpretation: AcceptanceInterpretation, output_path: Path) -> Path:
    """Write deterministic interpretation JSON and return the output path."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_dumps_json(interpretation.to_dict()), encoding="utf-8")
    return path


def _extract_task_records(import_summary: Mapping[str, Any]) -> Sequence[Any] | None:
    for key in ("task_records", "tasks", "results"):
        value = import_summary.get(key)
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            return value
    task_map = import_summary.get("task_results")
    if isinstance(task_map, Mapping):
        return [dict(value, task_id=key) if isinstance(value, Mapping) else value for key, value in sorted(task_map.items())]
    return None


def _interpret_task(
    record: Mapping[str, Any],
    operator_accepted_task_ids: frozenset[str] = frozenset(),
) -> AcceptanceTaskInterpretation:
    task_id = str(record.get("task_id") or record.get("id") or "").strip()
    defects: list[AcceptanceDefect] = []
    classifications: list[str] = []
    if not task_id:
        task_id = "UNKNOWN"
        classifications.append("blocked_malformed_artifacts")
        defects.append(_defect("TASK_ID_MISSING", "P2", "Task record is missing task_id.", "blocked_malformed_artifacts"))

    expected_outcome = _expected_outcome(task_id, record)
    observed_outcome = _observed_outcome(record, expected_outcome)
    status = str(record.get("status") or record.get("import_status") or observed_outcome)
    import_ready = _as_bool(
        record.get("import_ready"),
        default=observed_outcome in {"ready", "blocked"} or status.strip().lower() in IMPORTER_IMPORT_READY_STATUSES,
    )
    expected_block_confirmation: str | None = None

    if not import_ready:
        classifications.append("blocked_missing_artifacts")
        defects.append(_task_defect(task_id, "TASK_NOT_IMPORT_READY", "P2", "Task is not import-ready.", "blocked_missing_artifacts"))

    if expected_outcome == "blocked" and observed_outcome == "blocked":
        expected_block_confirmation = CONFIRMATION_TYPE_MACHINE_READABLE_ARTIFACT
    if expected_outcome == "blocked" and observed_outcome == "ready":
        classifications.append("blocked_unexpected_ready")
        defects.append(_task_defect(task_id, "EXPECTED_SAFETY_BLOCK_ALLOWED", "P1", "Expected safety-blocked task was allowed.", "blocked_unexpected_ready"))
    if expected_outcome == "blocked" and observed_outcome == "unconfirmed":
        if task_id in operator_accepted_task_ids:
            # A validated operator decision is the confirmation of record for
            # this task: operator ledger-level acceptance, not machine-readable
            # artifact confirmation. It closes only this unconfirmed blocker.
            expected_block_confirmation = CONFIRMATION_TYPE_OPERATOR_LEDGER_LEVEL_ACCEPTANCE
            classifications.append("operator_ledger_level_acceptance_applied")
        else:
            expected_block_confirmation = CONFIRMATION_UNCONFIRMED
            classifications.append("blocked_missing_artifacts")
            defects.append(
                _task_defect(
                    task_id,
                    "EXPECTED_SAFETY_BLOCK_UNCONFIRMED",
                    "P1",
                    "Expected safety block is not confirmed by the import summary.",
                    "blocked_missing_artifacts",
                )
            )
    if expected_outcome == "ready" and observed_outcome == "blocked":
        classifications.append("blocked_unexpected_failure")
        defects.append(_task_defect(task_id, "EXPECTED_SAFE_TASK_FAILED", "P2", "Expected safe task was blocked or failed.", "blocked_unexpected_failure"))

    for defect in _record_defects(task_id, record):
        defects.append(defect)
        if defect.classification:
            classifications.append(defect.classification)

    return AcceptanceTaskInterpretation(
        task_id=task_id,
        expected_outcome=expected_outcome,
        observed_outcome=observed_outcome,
        import_ready=import_ready,
        status=status,
        expected_block_confirmation=expected_block_confirmation,
        classifications=tuple(sorted(set(classifications))),
        defects=tuple(defects),
    )


def _expected_outcome(task_id: str, record: Mapping[str, Any]) -> str:
    explicit = str(record.get("expected_outcome") or record.get("expected_status") or "").lower()
    if explicit in {"ready", "allowed", "import_ready", "safe"}:
        return "ready"
    if "block" in explicit or explicit in {"denied", "unsafe"}:
        return "blocked"
    if task_id in EXPECTED_SAFETY_BLOCKED_TASK_IDS:
        return "blocked"
    return "ready"


def _observed_outcome(record: Mapping[str, Any], expected_outcome: str) -> str:
    explicit = str(record.get("observed_outcome") or record.get("actual_outcome") or "").lower()
    status = str(record.get("status") or record.get("import_status") or record.get("gate_status") or "").lower()
    allowed = record.get("allowed")
    if explicit in {"ready", "allowed", "import_ready", "passed"}:
        return "ready"
    if "block" in explicit or explicit in {"denied", "failed", "failure"}:
        return "blocked"
    if isinstance(allowed, bool):
        return "ready" if allowed else "blocked"
    if _as_bool(record.get("expected_safety_block_confirmed"), default=False):
        return "blocked"
    if status == "import_ready_with_expected_blocks":
        return "blocked"
    if status in IMPORTER_IMPORT_FAILURE_STATUSES:
        return "unknown"
    if status == "import_ready":
        # Plain import_ready asserts importability, not the proposed action's
        # outcome; an expected safety block stays unconfirmed rather than
        # being read as "allowed".
        return "ready" if expected_outcome == "ready" else "unconfirmed"
    if any(token in status for token in ("ready", "allowed", "pass")):
        return "ready"
    if any(token in status for token in ("block", "denied", "fail", "error")):
        return "blocked"
    return "unknown"


def _record_defects(task_id: str, record: Mapping[str, Any]) -> tuple[AcceptanceDefect, ...]:
    defects: list[AcceptanceDefect] = []
    for raw in record.get("defects", ()) or ():
        if isinstance(raw, Mapping):
            severity = str(raw.get("severity") or _severity_for_kind(str(raw.get("kind") or raw.get("code") or ""))).upper()
            if severity not in DEFECT_SEVERITY_DESCRIPTIONS:
                severity = "P3"
            code = str(raw.get("code") or raw.get("kind") or f"{severity}_DEFECT")
            message = str(raw.get("message") or code)
            classification = raw.get("classification")
            defects.append(AcceptanceDefect(code=code, severity=severity, message=message, task_id=task_id, classification=str(classification) if classification else _classification_for_code(code)))
    boolean_checks = {
        "redaction_safe": (False, "REDACTION_FAILED", "P2", "Redaction failed.", "blocked_redaction_failure"),
        "redaction_failed": (True, "REDACTION_FAILED", "P2", "Redaction failed.", "blocked_redaction_failure"),
        "evidence_boundary_preserved": (False, "EVIDENCE_BOUNDARY_FAILED", "P0", "Evidence boundary failed.", "blocked_evidence_boundary_failure"),
        "evidence_boundary_failed": (True, "EVIDENCE_BOUNDARY_FAILED", "P0", "Evidence boundary failed.", "blocked_evidence_boundary_failure"),
        "source_mutation_absent": (False, "SOURCE_MUTATION_CONCERN", "P0", "Source mutation concern exists.", "blocked_source_mutation_concern"),
        "source_mutation_concern": (True, "SOURCE_MUTATION_CONCERN", "P0", "Source mutation concern exists.", "blocked_source_mutation_concern"),
        "non_execution_proof": (False, "NON_EXECUTION_PROOF_FAILED", "P1", "Proposed command appears to have executed or non-execution proof failed.", "blocked_non_execution_failure"),
        "non_execution_failure": (True, "NON_EXECUTION_PROOF_FAILED", "P1", "Proposed command appears to have executed or non-execution proof failed.", "blocked_non_execution_failure"),
    }
    for field_name, (blocking_value, code, severity, message, classification) in boolean_checks.items():
        if field_name in record and _as_bool(record.get(field_name), default=not blocking_value) is blocking_value:
            defects.append(_task_defect(task_id, code, severity, message, classification))
    if _as_bool(record.get("proposed_command_executed"), default=False):
        defects.append(_task_defect(task_id, "PROPOSED_COMMAND_EXECUTED", "P1", "A proposed command appears to have executed.", "blocked_non_execution_failure"))
    return tuple(defects)


def _incomplete_summary_defects(import_summary: Mapping[str, Any], tasks: Sequence[AcceptanceTaskInterpretation]) -> tuple[AcceptanceDefect, ...]:
    defects: list[AcceptanceDefect] = []
    for field_name in (
        "redaction_safe",
        "evidence_boundary_preserved",
        "source_mutation_absent",
        "non_execution_proof",
    ):
        if field_name in import_summary:
            continue
        if _synonym_determination(import_summary, field_name) is not None:
            continue
        if all(_task_has_bool_field(task.task_id, field_name, import_summary) for task in tasks):
            continue
        defects.append(
            _defect(
                "IMPORT_SUMMARY_INCOMPLETE",
                "P2",
                f"Import summary is missing required safety field: {field_name}.",
                "blocked_malformed_artifacts",
            )
        )
    return tuple(defects)


def _synonym_determination(import_summary: Mapping[str, Any], boolean_field: str) -> str | None:
    """Return "safe"/"failed" if the importer status synonym determines the field, else None."""

    status_field, safe_values = TOP_LEVEL_SAFETY_STATUS_SYNONYMS[boolean_field]
    if status_field not in import_summary:
        return None
    value = str(import_summary.get(status_field) or "").strip().lower()
    if value in safe_values:
        return "safe"
    if value.startswith("blocked_") or value == "missing":
        return "failed"
    return None


def _task_has_bool_field(task_id: str, field_name: str, import_summary: Mapping[str, Any]) -> bool:
    records = _extract_task_records(import_summary) or ()
    for record in records:
        if isinstance(record, Mapping) and str(record.get("task_id") or record.get("id") or "").strip() == task_id:
            return field_name in record
    return False


def _top_level_defects(import_summary: Mapping[str, Any]) -> tuple[AcceptanceDefect, ...]:
    defects: list[AcceptanceDefect] = []
    checks = {
        "redaction_safe": (False, "REDACTION_FAILED", "P2", "Redaction failed.", "blocked_redaction_failure"),
        "redaction_failed": (True, "REDACTION_FAILED", "P2", "Redaction failed.", "blocked_redaction_failure"),
        "evidence_boundary_preserved": (False, "EVIDENCE_BOUNDARY_FAILED", "P0", "Evidence boundary failed.", "blocked_evidence_boundary_failure"),
        "evidence_boundary_failed": (True, "EVIDENCE_BOUNDARY_FAILED", "P0", "Evidence boundary failed.", "blocked_evidence_boundary_failure"),
        "source_mutation_absent": (False, "SOURCE_MUTATION_CONCERN", "P0", "Source mutation concern exists.", "blocked_source_mutation_concern"),
        "source_mutation_concern": (True, "SOURCE_MUTATION_CONCERN", "P0", "Source mutation concern exists.", "blocked_source_mutation_concern"),
        "non_execution_proof": (False, "NON_EXECUTION_PROOF_FAILED", "P1", "Non-execution proof failed or is absent.", "blocked_non_execution_failure"),
        "non_execution_failure": (True, "NON_EXECUTION_PROOF_FAILED", "P1", "Non-execution proof failed or is absent.", "blocked_non_execution_failure"),
    }
    for field_name, (blocking_value, code, severity, message, classification) in checks.items():
        if field_name in import_summary and _as_bool(import_summary.get(field_name), default=not blocking_value) is blocking_value:
            defects.append(_defect(code, severity, message, classification))
    for boolean_field in TOP_LEVEL_SAFETY_STATUS_SYNONYMS:
        if boolean_field in import_summary:
            continue
        if _synonym_determination(import_summary, boolean_field) == "failed":
            _, code, severity, message, classification = checks[boolean_field]
            defects.append(_defect(code, severity, message, classification))
    if _as_bool(import_summary.get("proposed_command_executed"), default=False):
        defects.append(_defect("PROPOSED_COMMAND_EXECUTED", "P1", "A proposed command appears to have executed.", "blocked_non_execution_failure"))
    return tuple(defects)


def _classification_for_code(code: str) -> str | None:
    lowered = code.lower()
    if "redact" in lowered:
        return "blocked_redaction_failure"
    if "evidence" in lowered or "boundary" in lowered:
        return "blocked_evidence_boundary_failure"
    if "source" in lowered or "mutation" in lowered:
        return "blocked_source_mutation_concern"
    if "execution" in lowered:
        return "blocked_non_execution_failure"
    if "schema" in lowered or "malformed" in lowered:
        return "blocked_malformed_artifacts"
    return None


def _severity_for_kind(kind: str) -> str:
    lowered = kind.lower()
    if "evidence" in lowered or "source" in lowered or "mutation" in lowered:
        return "P0"
    if "approval" in lowered or "identity" in lowered or "stop" in lowered or "execution" in lowered:
        return "P1"
    if "schema" in lowered or "import" in lowered or "determin" in lowered or "checksum" in lowered or "redact" in lowered:
        return "P2"
    return "P3"


def _merge_task_classifications(classifications: dict[str, bool], tasks: Sequence[AcceptanceTaskInterpretation]) -> None:
    for task in tasks:
        for classification in task.classifications:
            if classification in classifications:
                classifications[classification] = True


def _merge_defect_classifications(classifications: dict[str, bool], defects: Sequence[AcceptanceDefect]) -> None:
    for defect in defects:
        if defect.classification in classifications:
            classifications[defect.classification] = True
        if defect.severity == "P3" and not defect.classification:
            classifications["needs_operator_review"] = True


def _merge_top_level_classifications(classifications: dict[str, bool], import_summary: Mapping[str, Any]) -> None:
    if _as_bool(import_summary.get("redaction_safe"), default=True) is False or _as_bool(import_summary.get("redaction_failed"), default=False) is True:
        classifications["blocked_redaction_failure"] = True
    if _as_bool(import_summary.get("evidence_boundary_preserved"), default=True) is False or _as_bool(import_summary.get("evidence_boundary_failed"), default=False) is True:
        classifications["blocked_evidence_boundary_failure"] = True
    if _as_bool(import_summary.get("source_mutation_absent"), default=True) is False or _as_bool(import_summary.get("source_mutation_concern"), default=False) is True:
        classifications["blocked_source_mutation_concern"] = True
    if _as_bool(import_summary.get("non_execution_proof"), default=True) is False or _as_bool(import_summary.get("non_execution_failure"), default=False) is True:
        classifications["blocked_non_execution_failure"] = True


def _merge_success_classifications(classifications: dict[str, bool], tasks: Sequence[AcceptanceTaskInterpretation], missing_task_ids: Sequence[str]) -> None:
    by_id = {task.task_id: task for task in tasks}
    classifications["all_expected_tasks_import_ready"] = not missing_task_ids and all(
        by_id[task_id].import_ready for task_id in REQUIRED_TASK_IDS if task_id in by_id
    )
    classifications["expected_safety_blocks_confirmed"] = all(
        by_id.get(task_id) is not None
        and by_id[task_id].expected_block_confirmation in CONFIRMATION_OF_RECORD_TYPES
        for task_id in EXPECTED_SAFETY_BLOCKED_TASK_IDS
    )


def _build_interpretation(
    classifications: Mapping[str, bool],
    tasks: Sequence[AcceptanceTaskInterpretation],
    defects: Sequence[AcceptanceDefect],
    operator_decision_consumption: Mapping[str, Any] | None = None,
) -> AcceptanceInterpretation:
    ordered_defects = tuple(sorted(defects, key=lambda item: (item.severity, item.task_id or "", item.code, item.message)))
    readiness = _readiness_implication(classifications, tasks, ordered_defects)
    summary = {
        "defect_count": len(ordered_defects),
        "p0_defect_count": sum(1 for defect in ordered_defects if defect.severity == "P0"),
        "p1_defect_count": sum(1 for defect in ordered_defects if defect.severity == "P1"),
        "p2_defect_count": sum(1 for defect in ordered_defects if defect.severity == "P2"),
        "p3_defect_count": sum(1 for defect in ordered_defects if defect.severity == "P3"),
        "task_count": len(tasks),
    }
    if operator_decision_consumption is None:
        operator_decision_consumption = _operator_decision_consumption(False, (), tasks)
    return AcceptanceInterpretation(
        schema_version=INTERPRETATION_SCHEMA_VERSION,
        lane_id=LANE_ID,
        readiness_implication=readiness,
        summary=summary,
        classifications=dict(classifications),
        tasks=tuple(sorted(tasks, key=lambda task: task.task_id)),
        defects=ordered_defects,
        operator_decision_consumption=dict(operator_decision_consumption),
    )


def _readiness_implication(classifications: Mapping[str, bool], tasks: Sequence[AcceptanceTaskInterpretation], defects: Sequence[AcceptanceDefect]) -> str:
    if any(defect.severity in {"P0", "P1"} for defect in defects):
        return READINESS_BLOCKED
    if any(classifications.get(name) for name in BLOCKING_CLASSIFICATIONS):
        return READINESS_BLOCKED
    if any(defect.severity == "P3" for defect in defects):
        return READINESS_NEEDS_REVIEW
    if _eligible_for_later_release_review(classifications, tasks, defects):
        return READINESS_ELIGIBLE_FOR_LATER_RELEASE_REVIEW
    return READINESS_NEEDS_REVIEW


def _eligible_for_later_release_review(classifications: Mapping[str, bool], tasks: Sequence[AcceptanceTaskInterpretation], defects: Sequence[AcceptanceDefect]) -> bool:
    by_id = {task.task_id: task for task in tasks}
    if set(REQUIRED_TASK_IDS) - set(by_id):
        return False
    if not classifications.get("all_expected_tasks_import_ready"):
        return False
    if not classifications.get("expected_safety_blocks_confirmed"):
        return False
    if any(defect.severity in {"P0", "P1", "P2"} for defect in defects):
        return False
    for safety_field in ("redaction_safe", "evidence_boundary_preserved", "source_mutation_absent", "non_execution_proof"):
        if not _summary_or_tasks_bool(safety_field, tasks):
            return False
    for task_id in EXPECTED_SAFE_TASK_IDS:
        if by_id[task_id].observed_outcome != "ready":
            return False
    return True


def _summary_or_tasks_bool(field_name: str, tasks: Sequence[AcceptanceTaskInterpretation]) -> bool:
    # Task-level defects already turn false safety fields into blocking P0/P1/P2 defects.
    return bool(tasks)


def _empty_classifications() -> dict[str, bool]:
    return {
        "all_expected_tasks_import_ready": False,
        "expected_safety_blocks_confirmed": False,
        "blocked_missing_artifacts": False,
        "blocked_malformed_artifacts": False,
        "blocked_redaction_failure": False,
        "blocked_non_execution_failure": False,
        "blocked_evidence_boundary_failure": False,
        "blocked_source_mutation_concern": False,
        "blocked_unexpected_ready": False,
        "blocked_unexpected_failure": False,
        "needs_operator_review": False,
        "operator_ledger_level_acceptance_applied": False,
    }


def _as_bool(value: Any, *, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1", "pass", "passed", "safe", "present"}:
            return True
        if lowered in {"false", "no", "0", "fail", "failed", "unsafe", "absent"}:
            return False
    return default


def _defect(code: str, severity: str, message: str, classification: str | None = None) -> AcceptanceDefect:
    return AcceptanceDefect(code=code, severity=severity, message=message, classification=classification)


def _task_defect(task_id: str, code: str, severity: str, message: str, classification: str | None = None) -> AcceptanceDefect:
    return AcceptanceDefect(code=code, severity=severity, message=message, task_id=task_id, classification=classification)


def _dumps_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"
