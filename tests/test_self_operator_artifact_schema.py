from __future__ import annotations

import json
from pathlib import Path

from alpha.self_operator.artifact_schema import (
    CURRENT_SCHEMA_VERSION,
    ArtifactFinding,
    OperatorConfirmation,
    SelfOperatorArtifact,
    validate_artifact,
)
from alpha.self_operator.artifact_store import dumps_artifact_json
from alpha.self_operator.redaction import REDACTION_TEXT


def artifact(**overrides):
    payload = {
        "schema_version": CURRENT_SCHEMA_VERSION,
        "lane_id": "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-11-SELF-OPERATOR-LOCAL-ARTIFACT-PREFLIGHT-FOUNDATION-001",
        "run_id": "unit-run-001",
        "created_at": "2026-06-08T00:00:00Z",
        "operator_confirmation": OperatorConfirmation(explicit=True),
        "input_summary": {"requested_action": "local foundation only"},
        "preflight_result": {"allowed": True, "stop_state": "passed"},
        "findings": (),
        "stop_state": "passed",
        "artifact_paths": ("artifact.json",),
        "evidence_boundary": "local-only; no source-artifact mutation; no evidence promotion",
        "redaction_status": "redacted",
    }
    payload.update(overrides)
    return SelfOperatorArtifact(**payload)


def finding_ids(result):
    return {finding.id for finding in result.findings}


def test_valid_artifact_passes(tmp_path: Path) -> None:
    result = artifact().validate(output_root=tmp_path)
    assert result.valid is True
    assert result.findings == ()


def test_missing_confirmation_fails(tmp_path: Path) -> None:
    result = artifact(operator_confirmation=OperatorConfirmation(explicit=False)).validate(output_root=tmp_path)
    assert "SELF_OPERATOR_APPROVAL_GATE_REQUIRED" in finding_ids(result)


def test_missing_stop_state_fails_when_required(tmp_path: Path) -> None:
    result = artifact(stop_state="").validate(output_root=tmp_path, require_stop_state=True)
    assert "SELF_OPERATOR_STOP_STATE_REQUIRED" in finding_ids(result)


def test_unsupported_schema_version_fails(tmp_path: Path) -> None:
    result = artifact(schema_version="self_operator.local_artifact.v0").validate(output_root=tmp_path)
    assert "SELF_OPERATOR_ARTIFACT_UNSUPPORTED_SCHEMA_VERSION" in finding_ids(result)


def test_unredacted_secret_marker_is_redacted_in_json_output(tmp_path: Path) -> None:
    model = artifact(input_summary={"api_key": "fake-api-key-for-redaction-only"})
    assert model.validate(output_root=tmp_path).valid is True
    rendered = model.to_json(redact=True)
    assert "fake-api-key" not in rendered
    assert REDACTION_TEXT in rendered


def test_unredacted_secret_marker_is_rejected_when_status_is_unredacted(tmp_path: Path) -> None:
    result = artifact(
        input_summary={"note": "token=fake-token-for-redaction-only"},
        redaction_status="unredacted",
    ).validate(output_root=tmp_path)
    assert "SELF_OPERATOR_UNREDACTED_SECRET_MARKER" in finding_ids(result)


def test_malformed_findings_fail_validation(tmp_path: Path) -> None:
    malformed = ArtifactFinding(id="", reason_code="", message="")
    result = artifact(findings=(malformed,)).validate(output_root=tmp_path)
    assert "SELF_OPERATOR_ARTIFACT_FINDING_MALFORMED" in finding_ids(result)


def test_artifact_path_outside_output_root_fails(tmp_path: Path) -> None:
    result = artifact(artifact_paths=("../outside.json",)).validate(output_root=tmp_path)
    assert "SELF_OPERATOR_ARTIFACT_PATH_OUTSIDE_OUTPUT_ROOT" in finding_ids(result)


def test_json_roundtrip_preserves_stable_structure(tmp_path: Path) -> None:
    model = artifact()
    rendered = dumps_artifact_json(model)
    loaded = json.loads(rendered)
    roundtrip = SelfOperatorArtifact.from_mapping(loaded)
    assert roundtrip.to_dict() == model.to_dict()
    assert rendered == dumps_artifact_json(roundtrip)
