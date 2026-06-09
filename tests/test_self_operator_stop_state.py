from __future__ import annotations

import json

import pytest

from alpha.self_operator.artifact_schema import ArtifactFinding
from alpha.self_operator.artifact_store import ArtifactStoreError, dumps_artifact_json, read_artifact_json
from alpha.self_operator.stop_state import STOP_STATE_SCHEMA_VERSION, StopStateRecord, write_stop_state_json

LANE_ID = "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-11-SELF-OPERATOR-APPROVAL-STOPSTATE-GATE-FOUNDATION-001"
RUN_ID = "unit-run-stop-state-001"
EVIDENCE_BOUNDARY = "local-only; no execution; no source-artifact mutation; no evidence promotion"


def finding() -> ArtifactFinding:
    return ArtifactFinding(
        id="SELF_OPERATOR_APPROVAL_MISSING",
        reason_code="missing_approval",
        message="approval record is missing",
        surface="approval_record",
    )


def stop_state(**overrides) -> StopStateRecord:
    payload = {
        "schema_version": STOP_STATE_SCHEMA_VERSION,
        "lane_id": LANE_ID,
        "run_id": RUN_ID,
        "stop_state": "blocked",
        "reason_code": "missing_approval",
        "message": "execution gate blocked",
        "findings": (finding(),),
        "blocked_surfaces": ("approval_record",),
        "source_preflight_result_summary": {"allowed": True, "stop_state": "passed"},
        "approval_result_summary": {"present": False, "valid": False},
        "artifact_paths": ("stop-state.json",),
        "evidence_boundary": EVIDENCE_BOUNDARY,
        "redaction_status": "redacted",
        "metadata": {"created_at": "2026-06-09T00:00:00Z"},
    }
    payload.update(overrides)
    return StopStateRecord(**payload)


def ids(record: StopStateRecord, *, output_root=None) -> set[str]:
    return {finding.id for finding in record.validate(output_root=output_root).findings}


def test_stop_state_record_is_json_serializable_and_deterministic() -> None:
    rendered = dumps_artifact_json(stop_state().to_dict())
    assert rendered == dumps_artifact_json(stop_state().to_dict())
    assert json.loads(rendered)["reason_code"] == "missing_approval"


def test_missing_stop_state_blocks_validation() -> None:
    assert "SELF_OPERATOR_STOP_STATE_REQUIRED" in ids(stop_state(stop_state=""))


def test_missing_reason_code_blocks_validation() -> None:
    assert "SELF_OPERATOR_STOP_STATE_REASON_CODE_REQUIRED" in ids(stop_state(reason_code=""))


def test_malformed_findings_block_validation() -> None:
    malformed = ArtifactFinding(id="", reason_code="", message="")
    assert "SELF_OPERATOR_STOP_STATE_FINDING_MALFORMED" in ids(stop_state(findings=(malformed,)))


def test_unsafe_artifact_path_blocks_validation(tmp_path) -> None:
    assert "SELF_OPERATOR_STOP_STATE_ARTIFACT_PATH_UNSAFE" in ids(
        stop_state(artifact_paths=("../stop-state.json",)),
        output_root=tmp_path,
    )


def test_stop_state_artifact_can_be_written_under_temporary_output_root(tmp_path) -> None:
    path = write_stop_state_json(stop_state(), output_root=tmp_path, relative_path="records/stop-state.json")
    assert path.read_text(encoding="utf-8") == dumps_artifact_json(stop_state().to_dict())
    assert read_artifact_json(output_root=tmp_path, relative_path="records/stop-state.json")["lane_id"] == LANE_ID


def test_path_traversal_is_rejected(tmp_path) -> None:
    with pytest.raises(ArtifactStoreError):
        write_stop_state_json(stop_state(), output_root=tmp_path, relative_path="../stop-state.json")
