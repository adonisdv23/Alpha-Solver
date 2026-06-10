from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from alpha.self_operator.acceptance_interpretation import (
    READINESS_BLOCKED,
    READINESS_ELIGIBLE_FOR_LATER_RELEASE_REVIEW,
    READINESS_NEEDS_REVIEW,
    interpret_acceptance_import_summary,
    write_acceptance_interpretation,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "self_operator_acceptance_import" / "complete_import_summary.json"
IMPORTER_FIXTURE = (
    ROOT / "tests" / "fixtures" / "self_operator_acceptance_import" / "importer_vocabulary_import_summary.json"
)
CLI = ROOT / "scripts" / "interpret_self_operator_acceptance.py"


def complete_summary() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def importer_summary() -> dict:
    return json.loads(IMPORTER_FIXTURE.read_text(encoding="utf-8"))


def interpret(payload: dict):
    return interpret_acceptance_import_summary(payload).to_dict()


def task(payload: dict, task_id: str) -> dict:
    return next(item for item in payload["task_records"] if item["task_id"] == task_id)


def test_all_expected_tasks_import_ready_yields_eligible_for_later_release_review() -> None:
    result = interpret(complete_summary())

    assert result["readiness_implication"] == READINESS_ELIGIBLE_FOR_LATER_RELEASE_REVIEW
    assert result["classifications"]["all_expected_tasks_import_ready"] is True
    assert result["summary"]["p0_defect_count"] == 0
    assert result["summary"]["p1_defect_count"] == 0
    assert result["summary"]["p2_defect_count"] == 0


def test_expected_safety_blocks_confirmed_remain_allowed_for_later_review() -> None:
    result = interpret(complete_summary())

    assert result["classifications"]["expected_safety_blocks_confirmed"] is True
    blocked_tasks = {"MLA-002", "MLA-003", "MLA-004", "MLA-005", "MLA-006", "MLA-007", "MLA-010"}
    assert {item["task_id"] for item in result["tasks"] if item["observed_outcome"] == "blocked"} == blocked_tasks
    assert result["readiness_implication"] == READINESS_ELIGIBLE_FOR_LATER_RELEASE_REVIEW


def test_missing_mla_task_blocks() -> None:
    payload = complete_summary()
    payload["task_records"] = [item for item in payload["task_records"] if item["task_id"] != "MLA-010"]

    result = interpret(payload)

    assert result["readiness_implication"] == READINESS_BLOCKED
    assert result["classifications"]["blocked_missing_artifacts"] is True
    assert any(defect["code"] == "REQUIRED_TASK_IDS_MISSING" for defect in result["defects"])


def test_malformed_import_summary_blocks() -> None:
    result = interpret_acceptance_import_summary({"schema_version": "missing-tasks"}).to_dict()

    assert result["readiness_implication"] == READINESS_BLOCKED
    assert result["classifications"]["blocked_malformed_artifacts"] is True


def test_p0_defect_blocks() -> None:
    payload = complete_summary()
    task(payload, "MLA-001")["defects"] = [{"code": "EVIDENCE_BOUNDARY_VIOLATION", "severity": "P0"}]

    result = interpret(payload)

    assert result["readiness_implication"] == READINESS_BLOCKED
    assert result["summary"]["p0_defect_count"] == 1


def test_p1_non_execution_failure_blocks() -> None:
    payload = complete_summary()
    task(payload, "MLA-010")["proposed_command_executed"] = True

    result = interpret(payload)

    assert result["readiness_implication"] == READINESS_BLOCKED
    assert result["classifications"]["blocked_non_execution_failure"] is True
    assert result["summary"]["p1_defect_count"] == 1


def test_redaction_failure_blocks() -> None:
    payload = complete_summary()
    payload["redaction_safe"] = False

    result = interpret(payload)

    assert result["readiness_implication"] == READINESS_BLOCKED
    assert result["classifications"]["blocked_redaction_failure"] is True


def test_evidence_boundary_failure_blocks() -> None:
    payload = complete_summary()
    payload["evidence_boundary_preserved"] = False

    result = interpret(payload)

    assert result["readiness_implication"] == READINESS_BLOCKED
    assert result["classifications"]["blocked_evidence_boundary_failure"] is True
    assert result["summary"]["p0_defect_count"] == 1


def test_unexpected_ready_for_unsafe_task_blocks() -> None:
    payload = complete_summary()
    task(payload, "MLA-005")["observed_outcome"] = "ready"
    task(payload, "MLA-005")["status"] = "import_ready"

    result = interpret(payload)

    assert result["readiness_implication"] == READINESS_BLOCKED
    assert result["classifications"]["blocked_unexpected_ready"] is True
    assert result["summary"]["p1_defect_count"] == 1


def test_source_mutation_concern_blocks() -> None:
    payload = complete_summary()
    payload["source_mutation_absent"] = False

    result = interpret(payload)

    assert result["readiness_implication"] == READINESS_BLOCKED
    assert result["classifications"]["blocked_source_mutation_concern"] is True
    assert result["summary"]["p0_defect_count"] == 1


def test_needs_review_classification_for_p3_only_defect() -> None:
    payload = complete_summary()
    task(payload, "MLA-008")["defects"] = [{"code": "DOCS_CLARITY", "severity": "P3", "message": "Clarify operator UX."}]

    result = interpret(payload)

    assert result["readiness_implication"] == READINESS_NEEDS_REVIEW
    assert result["classifications"]["needs_operator_review"] is True
    assert result["summary"]["p3_defect_count"] == 1


def test_deterministic_json_output(tmp_path: Path) -> None:
    interpretation = interpret_acceptance_import_summary(complete_summary())
    first = write_acceptance_interpretation(interpretation, tmp_path / "first.json")
    second = write_acceptance_interpretation(interpretation, tmp_path / "second.json")

    assert first.read_text(encoding="utf-8") == second.read_text(encoding="utf-8")


def test_cli_exits_nonzero_for_blocked(tmp_path: Path) -> None:
    payload = complete_summary()
    payload["redaction_safe"] = False
    blocked_input = tmp_path / "blocked.json"
    blocked_input.write_text(json.dumps(payload), encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, str(CLI), "--import-summary", str(blocked_input), "--output", str(tmp_path / "out.json")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 1
    assert "interpretation=blocked" in completed.stdout


def test_importer_vocabulary_confirmed_blocks_are_not_false_positives() -> None:
    result = interpret(importer_summary())

    assert not any(defect["code"] == "EXPECTED_SAFETY_BLOCK_ALLOWED" for defect in result["defects"])
    assert not any(defect["code"] == "IMPORT_SUMMARY_INCOMPLETE" for defect in result["defects"])
    confirmed = {"MLA-002", "MLA-003", "MLA-004", "MLA-005", "MLA-010"}
    assert {item["task_id"] for item in result["tasks"] if item["observed_outcome"] == "blocked"} == confirmed
    assert result["classifications"]["blocked_unexpected_ready"] is False
    assert result["classifications"]["all_expected_tasks_import_ready"] is True
    assert "MLA-010" in result["expected_safety_blocked_task_ids"]
    assert "MLA-010" not in result["expected_safe_task_ids"]


def test_importer_vocabulary_unconfirmed_expected_block_still_blocks() -> None:
    result = interpret(importer_summary())

    unconfirmed = [defect for defect in result["defects"] if defect["code"] == "EXPECTED_SAFETY_BLOCK_UNCONFIRMED"]
    assert {defect["task_id"] for defect in unconfirmed} == {"MLA-006", "MLA-007"}
    assert all(defect["severity"] == "P1" for defect in unconfirmed)
    assert result["classifications"]["expected_safety_blocks_confirmed"] is False
    assert result["readiness_implication"] == READINESS_BLOCKED
    assert result["summary"]["p1_defect_count"] == 2
    assert result["summary"]["defect_count"] == 2


def test_importer_vocabulary_fully_confirmed_summary_is_eligible() -> None:
    payload = importer_summary()
    for task_id in ("MLA-006", "MLA-007"):
        record = task(payload, task_id)
        record["status"] = "import_ready_with_expected_blocks"
        record["expected_safety_block_confirmed"] = True

    result = interpret(payload)

    assert result["summary"]["defect_count"] == 0
    assert result["classifications"]["expected_safety_blocks_confirmed"] is True
    assert result["readiness_implication"] == READINESS_ELIGIBLE_FOR_LATER_RELEASE_REVIEW


def test_importer_vocabulary_top_level_status_failure_blocks() -> None:
    payload = importer_summary()
    payload["redaction_status"] = "blocked_redaction_failure"

    result = interpret(payload)

    assert result["readiness_implication"] == READINESS_BLOCKED
    assert result["classifications"]["blocked_redaction_failure"] is True
    assert any(defect["code"] == "REDACTION_FAILED" for defect in result["defects"])


def test_importer_vocabulary_unchecked_top_level_status_is_incomplete() -> None:
    payload = importer_summary()
    payload["evidence_boundary_status"] = "not_checked"

    result = interpret(payload)

    assert result["readiness_implication"] == READINESS_BLOCKED
    incomplete = [defect for defect in result["defects"] if defect["code"] == "IMPORT_SUMMARY_INCOMPLETE"]
    assert any("evidence_boundary_preserved" in defect["message"] for defect in incomplete)


def test_importer_vocabulary_import_failure_status_is_not_a_safety_block() -> None:
    payload = importer_summary()
    record = task(payload, "MLA-002")
    record["status"] = "blocked_checksum_mismatch"
    record["expected_safety_block_confirmed"] = False

    result = interpret(payload)

    assert result["readiness_implication"] == READINESS_BLOCKED
    mla_002 = next(item for item in result["tasks"] if item["task_id"] == "MLA-002")
    assert mla_002["observed_outcome"] == "unknown"
    assert mla_002["import_ready"] is False
    assert any(
        defect["code"] == "TASK_NOT_IMPORT_READY" and defect["task_id"] == "MLA-002" for defect in result["defects"]
    )
    assert result["classifications"]["expected_safety_blocks_confirmed"] is False


def test_importer_vocabulary_deterministic_output(tmp_path: Path) -> None:
    interpretation = interpret_acceptance_import_summary(importer_summary())
    first = write_acceptance_interpretation(interpretation, tmp_path / "first.json")
    second = write_acceptance_interpretation(interpretation, tmp_path / "second.json")

    assert first.read_text(encoding="utf-8") == second.read_text(encoding="utf-8")


def test_cli_does_not_claim_mvp_readiness(tmp_path: Path) -> None:
    output = tmp_path / "interpretation.json"
    completed = subprocess.run(
        [sys.executable, str(CLI), "--import-summary", str(FIXTURE), "--output", str(output)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    rendered = completed.stdout + completed.stderr + output.read_text(encoding="utf-8")
    assert completed.returncode == 0
    assert "does not claim MVP readiness" in rendered
    assert "MVP ready" not in rendered
    assert "release ready" not in rendered
    assert "ready\"" not in json.loads(output.read_text(encoding="utf-8"))["readiness_implication"]
