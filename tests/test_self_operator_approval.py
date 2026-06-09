from __future__ import annotations

import json

from alpha.self_operator.approval import (
    APPROVAL_SCHEMA_VERSION,
    OPERATOR_CONFIRMATION_HARD_STOP,
    ApprovalRecord,
)
from alpha.self_operator.artifact_store import dumps_artifact_json
from alpha.self_operator.redaction import REDACTION_TEXT

LANE_ID = "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-11-SELF-OPERATOR-APPROVAL-STOPSTATE-GATE-FOUNDATION-001"
RUN_ID = "unit-run-approval-001"
EVIDENCE_BOUNDARY = "local-only; no execution; no source-artifact mutation; no evidence promotion"


def approval(**overrides) -> ApprovalRecord:
    payload = {
        "schema_version": APPROVAL_SCHEMA_VERSION,
        "lane_id": LANE_ID,
        "run_id": RUN_ID,
        "approved": True,
        "operator_confirmation": f"I approve this local-only lane; {OPERATOR_CONFIRMATION_HARD_STOP}",
        "approval_text": "Approved for local gate foundation tests only.",
        "approved_by": "unit-operator",
        "approved_at": "2026-06-09T00:00:00Z",
        "scope_summary": "Approval, stop-state, and execution-gate foundation only.",
        "evidence_boundary": EVIDENCE_BOUNDARY,
        "redaction_status": "redacted",
        "metadata": {"test": "approval"},
    }
    payload.update(overrides)
    return ApprovalRecord(**payload)


def ids(record: ApprovalRecord) -> set[str]:
    return {finding.id for finding in record.validate().findings}


def test_valid_approval_record_passes_validation() -> None:
    result = approval().validate()
    assert result.valid is True
    assert result.findings == ()


def test_missing_approval_blocks() -> None:
    result = ApprovalRecord.from_mapping({}).validate()
    assert result.valid is False
    assert "SELF_OPERATOR_APPROVAL_REQUIRED" in {finding.id for finding in result.findings}


def test_approval_false_blocks() -> None:
    assert "SELF_OPERATOR_APPROVAL_REQUIRED" in ids(approval(approved=False))


def test_missing_operator_confirmation_blocks() -> None:
    assert "SELF_OPERATOR_OPERATOR_CONFIRMATION_MISSING" in ids(approval(operator_confirmation=""))


def test_missing_hard_stop_confirmation_text_blocks() -> None:
    assert "SELF_OPERATOR_APPROVAL_HARD_STOP_TEXT_REQUIRED" in ids(
        approval(operator_confirmation="I approve this local-only lane.")
    )


def test_missing_lane_id_blocks() -> None:
    assert "SELF_OPERATOR_APPROVAL_LANE_ID_REQUIRED" in ids(approval(lane_id=""))


def test_missing_run_id_blocks() -> None:
    assert "SELF_OPERATOR_APPROVAL_RUN_ID_REQUIRED" in ids(approval(run_id=""))


def test_missing_evidence_boundary_blocks() -> None:
    assert "SELF_OPERATOR_APPROVAL_EVIDENCE_BOUNDARY_REQUIRED" in ids(approval(evidence_boundary=""))


def test_secret_like_marker_is_redacted_or_rejected() -> None:
    record = approval(metadata={"api_key": "fake-api-key-for-redaction-only"})
    assert REDACTION_TEXT in dumps_artifact_json(record.to_dict(redact=True))
    unredacted = approval(
        redaction_status="unredacted",
        metadata={"note": "token=fake-token-for-redaction-only"},
    )
    assert "SELF_OPERATOR_UNREDACTED_SECRET_MARKER" in ids(unredacted)


def test_approval_record_is_json_serializable_and_deterministic() -> None:
    rendered = dumps_artifact_json(approval().to_dict())
    assert rendered == dumps_artifact_json(approval().to_dict())
    assert json.loads(rendered)["lane_id"] == LANE_ID
