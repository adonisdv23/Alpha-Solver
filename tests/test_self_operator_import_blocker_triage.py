from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from alpha.self_operator.import_blocker_triage import (
    FIX_CLASSIFICATIONS,
    triage_import_blocker,
    write_triage_result,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
ACTUAL_PACKET = REPO_ROOT / "docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-operator-supervised-local-acceptance-execution"
LANE = "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-12-SELF-OPERATOR-LOCAL-HARNESS-DRY-RUN-WRAPPER-001"
RUN = "mla-010-local-acceptance-001"
BOUNDARY = "local-only; operator-supervised; no execution; no source-artifact mutation; no evidence promotion"
FINDING = {
    "id": "SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED",
    "message": "forbidden source-artifact mutation",
    "reason_code": "source_artifact_mutation",
    "severity": "error",
    "stop_state": "blocked",
    "surface": "command_classification",
}
LEDGER_ROW = (
    "| MLA-010 | non-execution proof | Synthetic proposed touch command targets a temp sentinel file. | "
    "Wrapper does not execute proposed command; unsafe source mutation command is blocked. | "
    "dry_run_status=blocked_by_failed_preflight; allowed=False; reason_code=failed_preflight | PASS | "
    "raw-artifacts/MLA-010 | None | Raw local evidence only. |"
)
PROOF = (
    "# Non-execution proof\n\n"
    "- MLA-010 proposed `touch` command was classified as source-mutation command text and blocked "
    "by preflight/execution-gate summaries instead of being executed; the sentinel remained absent.\n"
    "- Proposed task commands were not executed.\n"
)


def _canonical_payloads() -> dict[str, dict]:
    return {
        "dry-run-result.json": {
            "allowed": False,
            "dry_run_status": "blocked_by_failed_preflight",
            "evidence_boundary": BOUNDARY,
            "execution_gate_summary": {
                "allowed_for_local_dry_run": False,
                "finding_ids": ["SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED"],
                "gate_status": "blocked_by_failed_preflight",
                "reason_code": "failed_preflight",
            },
            "lane_id": LANE,
            "non_execution_confirmation": "wrapper does not execute proposed commands; it only classifies proposed command text",
            "preflight_summary": {
                "allowed": False,
                "command_reason_codes": ["source_artifact_mutation"],
                "finding_ids": ["SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED"],
                "stop_state": "blocked",
            },
            "proposed_task_summary": {
                "metadata": {
                    "execution_lane_id": "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-OPERATOR-SUPERVISED-LOCAL-ACCEPTANCE-EXECUTION-001",
                    "mla_task_id": "MLA-010",
                    "run_id": RUN,
                }
            },
            "reason_code": "failed_preflight",
            "redaction_status": "redacted",
            "run_id": RUN,
            "schema_version": "self_operator.dry_run_result.v1",
            "stop_state_summary": {
                "finding_ids": ["SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED"],
                "reason_code": "failed_preflight",
                "stop_state": "blocked",
            },
        },
        "execution-gate-result.json": {
            "allowed_for_local_dry_run": False,
            "evidence_boundary": BOUNDARY,
            "findings": [dict(FINDING)],
            "gate_status": "blocked_by_failed_preflight",
            "lane_id": LANE,
            "reason_code": "failed_preflight",
            "redaction_status": "redacted",
            "run_id": RUN,
            "schema_version": "self_operator.execution_gate_result.v1",
        },
        "stop-state.json": {
            "blocked_surfaces": ["command_classification"],
            "evidence_boundary": BOUNDARY,
            "findings": [dict(FINDING)],
            "lane_id": LANE,
            "message": "execution gate blocked: failed_preflight",
            "reason_code": "failed_preflight",
            "redaction_status": "redacted",
            "run_id": RUN,
            "schema_version": "self_operator.stop_state_record.v1",
            "stop_state": "blocked",
        },
    }


def _write_packet(
    root: Path,
    payloads: dict[str, dict] | None = None,
    *,
    ledger_row: str = LEDGER_ROW,
    proof: str = PROOF,
    drop: tuple[str, ...] = (),
    checksum_override: dict[str, str] | None = None,
) -> Path:
    payloads = payloads if payloads is not None else _canonical_payloads()
    checksum_override = checksum_override or {}
    root.mkdir(parents=True)
    task_dir = root / "raw-artifacts" / "MLA-010"
    task_dir.mkdir(parents=True)
    (root / "README.md").write_text("# Synthetic packet\n\nlocal-only raw evidence.\n", encoding="utf-8")
    (root / "non-execution-proof.md").write_text(proof, encoding="utf-8")
    expected_cell = "; ".join(sorted(payloads))
    (root / "raw-artifacts-index.md").write_text(
        "| Task ID | Expected copied artifacts | Missing expected artifacts | Status |\n"
        "| --- | --- | --- | --- |\n"
        f"| MLA-010 | {expected_cell} | None | PASS |\n",
        encoding="utf-8",
    )
    ledger_rows = [
        "| Task ID | Artifact | Path | Checksum | Schema version | Artifact lane ID | Run ID | Redaction status | Evidence-boundary status | Non-execution marker |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for artifact_name in sorted(payloads):
        payload = payloads[artifact_name]
        if artifact_name not in drop:
            path = task_dir / artifact_name
            path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            digest = "0" * 64
        digest = checksum_override.get(artifact_name, digest)
        ledger_rows.append(
            f"| MLA-010 | {artifact_name} | raw-artifacts/MLA-010/{artifact_name} | {digest} | "
            f"{payload['schema_version']} | {payload['lane_id']} | {payload['run_id']} | redacted | present | not present |"
        )
    (root / "artifact-ledger.md").write_text("\n".join(ledger_rows) + "\n", encoding="utf-8")
    (root / "task-execution-ledger.md").write_text(
        "| Task ID | Objective | Input fixture summary | Expected result | Observed result | Status | Raw artifact paths | Defect reference | Reviewer note |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        f"{ledger_row}\n",
        encoding="utf-8",
    )
    return root


def test_canonical_blocked_marker_packet_classifies_expected_synthetic_marker(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    result = triage_import_blocker(packet)
    assert result.classification == "expected_synthetic_marker"
    assert result.contract_expects_blocked_source_mutation
    assert result.non_execution_proof_confirms_blocked
    assert all(record.unexpected_marker_count == 0 for record in result.artifacts)
    assert sum(len(record.marker_occurrences) for record in result.artifacts) > 0


def test_marker_outside_blocked_context_defaults_to_inconclusive(tmp_path: Path):
    payloads = _canonical_payloads()
    payloads["dry-run-result.json"]["notes"] = "operator note mentioning source_artifact_mutation outside findings"
    packet = _write_packet(tmp_path / "packet", payloads)
    result = triage_import_blocker(packet)
    assert result.classification == "inconclusive"


def test_missing_contract_expectation_defaults_to_inconclusive(tmp_path: Path):
    row = "| MLA-010 | non-execution proof | safe fixture | Wrapper does not execute proposed command. | observed | PASS | paths | None | note |"
    packet = _write_packet(tmp_path / "packet", ledger_row=row, proof="# Non-execution proof\n\nProposed task commands were not executed.\n")
    result = triage_import_blocker(packet)
    assert result.classification == "inconclusive"
    assert not result.contract_expects_blocked_source_mutation


def test_malformed_artifact_classification(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    (packet / "raw-artifacts/MLA-010/stop-state.json").write_text("{bad", encoding="utf-8")
    result = triage_import_blocker(packet)
    assert result.classification == "malformed_artifact"


def test_checksum_mismatch_defaults_to_inconclusive(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet", checksum_override={"stop-state.json": "f" * 64})
    result = triage_import_blocker(packet)
    assert result.classification == "inconclusive"
    assert any(record.checksum_status == "mismatched" for record in result.artifacts)


def test_allowed_mutation_record_classifies_true_violation(tmp_path: Path):
    payloads = _canonical_payloads()
    payloads["dry-run-result.json"]["mutation_record"] = {
        "allowed": True,
        "reason_code": "source_artifact_mutation",
    }
    packet = _write_packet(tmp_path / "packet", payloads)
    result = triage_import_blocker(packet)
    assert result.classification == "true_violation"
    assert result.recommended_followup == "do_not_patch_importer_create_blocker_review_packet"


def test_missing_artifact_defaults_to_inconclusive(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet", drop=("stop-state.json",))
    result = triage_import_blocker(packet)
    assert result.classification == "inconclusive"


def test_packet_without_markers_classifies_importer_false_positive(tmp_path: Path):
    payloads = _canonical_payloads()
    safe_finding = {
        "id": "SELF_OPERATOR_APPROVAL_GATE_REQUIRED",
        "message": "missing approval",
        "reason_code": "missing_approval",
        "severity": "error",
        "stop_state": "blocked",
        "surface": "approval",
    }
    payloads["dry-run-result.json"]["execution_gate_summary"]["finding_ids"] = ["SELF_OPERATOR_APPROVAL_GATE_REQUIRED"]
    payloads["dry-run-result.json"]["preflight_summary"]["command_reason_codes"] = ["missing_approval"]
    payloads["dry-run-result.json"]["preflight_summary"]["finding_ids"] = ["SELF_OPERATOR_APPROVAL_GATE_REQUIRED"]
    payloads["dry-run-result.json"]["stop_state_summary"]["finding_ids"] = ["SELF_OPERATOR_APPROVAL_GATE_REQUIRED"]
    payloads["execution-gate-result.json"]["findings"] = [dict(safe_finding)]
    payloads["stop-state.json"]["findings"] = [dict(safe_finding)]
    packet = _write_packet(tmp_path / "packet", payloads)
    result = triage_import_blocker(packet)
    assert result.classification == "importer_false_positive"


def test_triage_is_read_only_and_deterministic(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in packet.rglob("*") if path.is_file()}
    result = triage_import_blocker(packet)
    after = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in packet.rglob("*") if path.is_file()}
    assert before == after
    first = write_triage_result(result, tmp_path / "out/one.json").read_text(encoding="utf-8")
    second = write_triage_result(result, tmp_path / "out/two.json").read_text(encoding="utf-8")
    assert first == second
    data = json.loads(first)
    assert data["mvp_readiness"] == "unclaimed"
    assert data["readiness_interpretation"] == "not_interpreted"


def test_actual_461_packet_classifies_expected_synthetic_marker_without_mutation(tmp_path: Path):
    if not ACTUAL_PACKET.exists():
        return
    before = {path.relative_to(ACTUAL_PACKET): hashlib.sha256(path.read_bytes()).hexdigest() for path in ACTUAL_PACKET.rglob("*") if path.is_file()}
    result = triage_import_blocker(ACTUAL_PACKET)
    after = {path.relative_to(ACTUAL_PACKET): hashlib.sha256(path.read_bytes()).hexdigest() for path in ACTUAL_PACKET.rglob("*") if path.is_file()}
    assert before == after
    assert result.classification == "expected_synthetic_marker"
    assert result.classification in FIX_CLASSIFICATIONS
    assert result.contract_expects_blocked_source_mutation
    assert result.non_execution_proof_confirms_blocked


def test_cli_help():
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts/triage_self_operator_import_blocker.py"), "--help"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "--packet-dir" in result.stdout
