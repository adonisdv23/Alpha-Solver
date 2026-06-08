from __future__ import annotations

import json
from pathlib import Path

from alpha.self_operator.preflight import ProposedTask, run_local_preflight

LANE_ID = "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-11-SELF-OPERATOR-LOCAL-ARTIFACT-PREFLIGHT-FOUNDATION-001"


def task(tmp_path: Path, **overrides) -> ProposedTask:
    payload = {
        "lane_id": LANE_ID,
        "requested_action": "classify local-only foundation changes without executing them",
        "candidate_changed_files": (
            "alpha/self_operator/preflight.py",
            "tests/test_self_operator_preflight.py",
            "docs/evals/runs/alpha-solver-post-level-3-level-11-self-operator-local-artifact-preflight-foundation/README.md",
        ),
        "proposed_commands": ("git status --short", "python -m pytest -q tests/test_self_operator_preflight.py"),
        "operator_confirmation": True,
        "output_root": str(tmp_path),
        "evidence_boundary": "local-only; no provider/API/dashboard/CLI/credential/deployment/billing/browser/Google Sheets/source-artifact mutation/evidence promotion/acceptance",
        "artifact_paths": ("preflight/result.json",),
    }
    payload.update(overrides)
    return ProposedTask.from_mapping(payload)


def ids(result):
    return {finding.id for finding in result.findings}


def test_missing_operator_confirmation_blocks(tmp_path: Path) -> None:
    result = run_local_preflight(task(tmp_path, operator_confirmation=False))
    assert result.allowed is False
    assert "SELF_OPERATOR_APPROVAL_GATE_REQUIRED" in ids(result)


def test_unclear_scope_blocks(tmp_path: Path) -> None:
    result = run_local_preflight(task(tmp_path, requested_action=""))
    assert "SELF_OPERATOR_SCOPE_UNCLEAR" in ids(result)


def test_forbidden_command_blocks(tmp_path: Path) -> None:
    result = run_local_preflight(task(tmp_path, proposed_commands=("curl https://example.invalid",)))
    assert "SELF_OPERATOR_EXTERNAL_API_BLOCKED" in ids(result)
    assert result.command_classifications[0].allowed is False


def test_out_of_scope_changed_files_block(tmp_path: Path) -> None:
    result = run_local_preflight(task(tmp_path, candidate_changed_files=("alpha/providers/openai.py",)))
    assert "SELF_OPERATOR_FORBIDDEN_SURFACE_CHANGED_FILE" in ids(result)


def test_unsafe_artifact_path_blocks(tmp_path: Path) -> None:
    result = run_local_preflight(task(tmp_path, artifact_paths=("../unsafe.json",)))
    assert "SELF_OPERATOR_ARTIFACT_PATH_OUTSIDE_OUTPUT_ROOT" in ids(result)


def test_missing_evidence_boundary_blocks(tmp_path: Path) -> None:
    result = run_local_preflight(task(tmp_path, evidence_boundary=""))
    assert "SELF_OPERATOR_EVIDENCE_BOUNDARY_REQUIRED" in ids(result)


def test_valid_local_only_proposal_passes(tmp_path: Path) -> None:
    result = run_local_preflight(task(tmp_path))
    assert result.allowed is True
    assert result.stop_state == "passed"
    assert result.findings == ()


def test_result_is_json_serializable(tmp_path: Path) -> None:
    result = run_local_preflight(task(tmp_path))
    rendered = json.dumps(result.to_dict(), sort_keys=True)
    assert LANE_ID in rendered


def test_tests_use_inert_command_strings_only(tmp_path: Path) -> None:
    result = run_local_preflight(task(tmp_path, proposed_commands=("playwright test", "gcloud deploy")))
    assert {classification.reason_code for classification in result.command_classifications} == {
        "browser_automation",
        "deployment",
    }
