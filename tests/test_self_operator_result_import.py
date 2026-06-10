from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from alpha.self_operator.result_import import (
    BLOCKED_STATUSES,
    TASK_IDS,
    import_acceptance_execution_packet,
    write_acceptance_import_summary,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
ACTUAL_PACKET = REPO_ROOT / "docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-operator-supervised-local-acceptance-execution"


def _payload(task_id: str, artifact: str, *, stop: bool = False, **overrides):
    base = {
        "schema_version": (
            "self_operator.stop_state_record.v1"
            if stop
            else "self_operator.dry_run_result.v1"
            if artifact == "dry-run-result.json"
            else "self_operator.execution_gate_result.v1"
        ),
        "lane_id": "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-12-SELF-OPERATOR-LOCAL-HARNESS-DRY-RUN-WRAPPER-001",
        "run_id": f"{task_id.lower()}-run-001",
        "redaction_status": "redacted",
        "evidence_boundary": "local-only; operator-supervised; no execution; no evidence promotion",
        "metadata": {"acceptance_status": "not_interpreted", "mvp_readiness": "unclaimed"},
    }
    if artifact == "dry-run-result.json":
        base["non_execution_confirmation"] = "wrapper does not execute proposed commands; it only classifies proposed command text"
        base["proposed_task_summary"] = {
            "metadata": {
                "execution_lane_id": "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-OPERATOR-SUPERVISED-LOCAL-ACCEPTANCE-EXECUTION-001",
                "mla_task_id": task_id,
                "run_id": f"{task_id.lower()}-run-001",
            }
        }
    if stop:
        base.update({"stop_state": "blocked", "reason_code": "expected_safety_block", "findings": []})
    base.update(overrides)
    return base


def _write_packet(root: Path, *, stop_tasks: set[str] | None = None, missing: tuple[str, str] | None = None) -> Path:
    stop_tasks = stop_tasks or set()
    root.mkdir(parents=True)
    (root / "raw-artifacts").mkdir()
    (root / "README.md").write_text(
        "# Packet\n\nlocal-only raw evidence. It does not interpret results. It does not claim MVP readiness.\n",
        encoding="utf-8",
    )
    (root / "evidence-boundary.md").write_text(
        "# Evidence boundary\n\nlocal-only; no execution; does not interpret results; does not claim MVP readiness.\n",
        encoding="utf-8",
    )
    (root / "evidence-boundary-review.md").write_text("local-only no execution present\n", encoding="utf-8")
    (root / "non-execution-proof.md").write_text(
        "Proposed task commands were not executed. The wrapper does not execute proposed commands.\n",
        encoding="utf-8",
    )
    (root / "redaction-review.md").write_text(
        "- Redaction status: PASS\n- Real credentials or production secrets used: none.\n",
        encoding="utf-8",
    )
    (root / "non-actions.md").write_text("No source artifact mutation.\n", encoding="utf-8")
    raw_rows = ["| Task ID | Expected copied artifacts | Missing expected artifacts | Status |", "| --- | --- | --- | --- |"]
    ledger_rows = [
        "| Task ID | Artifact | Path | Checksum | Schema version | Artifact lane ID | Run ID | Redaction status | Evidence-boundary status | Non-execution marker |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for task_id in TASK_IDS:
        artifacts = ["dry-run-result.json", "execution-gate-result.json"]
        if task_id in stop_tasks:
            artifacts.append("stop-state.json")
        task_dir = root / "raw-artifacts" / task_id
        task_dir.mkdir()
        expected_cell = "; ".join(artifacts)
        raw_rows.append(f"| {task_id} | {expected_cell} | None | PASS |")
        for artifact in artifacts:
            if missing == (task_id, artifact):
                continue
            stop = artifact == "stop-state.json"
            path = task_dir / artifact
            path.write_text(json.dumps(_payload(task_id, artifact, stop=stop), sort_keys=True, indent=2) + "\n", encoding="utf-8")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            payload = json.loads(path.read_text(encoding="utf-8"))
            marker = payload.get("non_execution_confirmation", "not present")
            ledger_rows.append(
                f"| {task_id} | {artifact} | raw-artifacts/{task_id}/{artifact} | {digest} | "
                f"{payload['schema_version']} | {payload['lane_id']} | {payload['run_id']} | redacted | present | {marker} |"
            )
    (root / "raw-artifacts-index.md").write_text("\n".join(raw_rows) + "\n", encoding="utf-8")
    (root / "artifact-ledger.md").write_text("\n".join(ledger_rows) + "\n", encoding="utf-8")
    return root


def test_imports_complete_synthetic_acceptance_packet(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert summary.status == "import_ready"
    assert summary.coverage == TASK_IDS
    assert len(summary.task_records) == 10
    assert all(artifact.sha256 for artifact in summary.artifacts)


def test_detects_missing_dry_run_result_artifact(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet", missing=("MLA-001", "dry-run-result.json"))
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert summary.status == "blocked_missing_artifact"
    assert summary.blocked


def test_detects_malformed_json(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    (packet / "raw-artifacts/MLA-001/dry-run-result.json").write_text("{bad", encoding="utf-8")
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert summary.status == "blocked_malformed_artifact"


def test_detects_artifact_path_traversal(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    text = (packet / "artifact-ledger.md").read_text(encoding="utf-8")
    text = text.replace("raw-artifacts/MLA-001/dry-run-result.json", "../outside/dry-run-result.json", 1)
    (packet / "artifact-ledger.md").write_text(text, encoding="utf-8")
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert summary.status == "blocked_malformed_artifact"


def test_detects_missing_non_execution_confirmation(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    path = packet / "raw-artifacts/MLA-001/dry-run-result.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.pop("non_execution_confirmation")
    path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert summary.status == "blocked_non_execution_missing"


def test_detects_missing_evidence_boundary(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    (packet / "evidence-boundary.md").write_text("# Evidence boundary\n", encoding="utf-8")
    (packet / "evidence-boundary-review.md").write_text("", encoding="utf-8")
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert summary.status == "blocked_evidence_boundary_failure"


def test_detects_redaction_failure_marker(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    path = packet / "raw-artifacts/MLA-001/execution-gate-result.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["redaction_status"] = "failed"
    path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert summary.status == "blocked_redaction_failure"


def test_preserves_expected_safety_blocked_task_as_import_ready_when_stop_state_exists(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet", stop_tasks={"MLA-002"})
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    task = next(record for record in summary.task_records if record.task_id == "MLA-002")
    assert task.status == "import_ready_with_expected_blocks"
    assert summary.status == "import_ready_with_expected_blocks"


def test_produces_deterministic_json_output(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    first = write_acceptance_import_summary(summary, tmp_path / "out/one.json").read_text(encoding="utf-8")
    second = write_acceptance_import_summary(summary, tmp_path / "out/two.json").read_text(encoding="utf-8")
    assert first == second


def test_never_interprets_results_as_mvp_readiness(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    data = summary.to_dict()
    assert data["readiness_interpretation"] == "not_interpreted"
    assert data["mvp_readiness"] == "unclaimed"
    assert "ready" not in data["mvp_readiness"]


MUTATION_BLOCKED_FINDING = {
    "id": "SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED",
    "message": "forbidden source-artifact mutation",
    "reason_code": "source_artifact_mutation",
    "severity": "error",
    "stop_state": "blocked",
    "surface": "command_classification",
}


def _install_canonical_mla_010_blocked_mutation(packet: Path, dry_run_extra: dict | None = None) -> None:
    """Replace MLA-010 with the exact artifact shapes the #461 packet records for the blocked mutation fixture."""

    payloads = {
        "dry-run-result.json": _payload(
            "MLA-010",
            "dry-run-result.json",
            allowed=False,
            dry_run_status="blocked_by_failed_preflight",
            reason_code="failed_preflight",
            execution_gate_summary={
                "allowed_for_local_dry_run": False,
                "finding_ids": ["SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED"],
                "gate_status": "blocked_by_failed_preflight",
                "reason_code": "failed_preflight",
            },
            preflight_summary={
                "allowed": False,
                "command_reason_codes": ["source_artifact_mutation"],
                "finding_ids": ["SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED"],
                "stop_state": "blocked",
            },
            stop_state_summary={
                "finding_ids": ["SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED"],
                "reason_code": "failed_preflight",
                "stop_state": "blocked",
            },
            **(dry_run_extra or {}),
        ),
        "execution-gate-result.json": _payload(
            "MLA-010",
            "execution-gate-result.json",
            allowed_for_local_dry_run=False,
            findings=[dict(MUTATION_BLOCKED_FINDING)],
            gate_status="blocked_by_failed_preflight",
            reason_code="failed_preflight",
        ),
        "stop-state.json": _payload(
            "MLA-010",
            "stop-state.json",
            stop=True,
            blocked_surfaces=["command_classification"],
            findings=[dict(MUTATION_BLOCKED_FINDING)],
            reason_code="failed_preflight",
        ),
    }
    task_dir = packet / "raw-artifacts/MLA-010"
    raw_index = packet / "raw-artifacts-index.md"
    raw_index.write_text(
        raw_index.read_text(encoding="utf-8").replace(
            "| MLA-010 | dry-run-result.json; execution-gate-result.json |",
            "| MLA-010 | dry-run-result.json; execution-gate-result.json; stop-state.json |",
        ),
        encoding="utf-8",
    )
    ledger = packet / "artifact-ledger.md"
    ledger_rows = [line for line in ledger.read_text(encoding="utf-8").splitlines() if "| MLA-010 |" not in line]
    for artifact_name, payload in sorted(payloads.items()):
        path = task_dir / artifact_name
        path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        marker = payload.get("non_execution_confirmation", "not present")
        ledger_rows.append(
            f"| MLA-010 | {artifact_name} | raw-artifacts/MLA-010/{artifact_name} | {digest} | "
            f"{payload['schema_version']} | {payload['lane_id']} | {payload['run_id']} | redacted | present | {marker} |"
        )
    ledger.write_text("\n".join(ledger_rows) + "\n", encoding="utf-8")


def test_accepts_exact_mla_010_blocked_mutation_marker_shapes(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    _install_canonical_mla_010_blocked_mutation(packet)
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert summary.status == "import_ready_with_expected_blocks"
    assert summary.source_artifact_mutation_status == "not_present"
    task = next(record for record in summary.task_records if record.task_id == "MLA-010")
    assert task.status == "import_ready_with_expected_blocks"
    assert all(not artifact.findings for artifact in task.artifact_records)


def test_blocks_mutation_marker_outside_blocked_finding_context(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    _install_canonical_mla_010_blocked_mutation(
        packet,
        dry_run_extra={"notes": "operator note mentioning source_artifact_mutation outside findings"},
    )
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert summary.status == "blocked_source_mutation_concern"
    assert summary.source_artifact_mutation_status == "blocked_source_mutation_concern"


def test_accepts_boundary_non_execution_phrase_from_proof_file(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    (packet / "evidence-boundary.md").write_text(
        "# Evidence boundary\n\nThis packet records local-only artifacts. It does not interpret results, "
        "does not claim MVP readiness, and does not mutate source artifacts.\n",
        encoding="utf-8",
    )
    (packet / "evidence-boundary-review.md").write_text("- No source-artifact mutation: CONFIRMED.\n", encoding="utf-8")
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert summary.evidence_boundary_status == "present"
    assert summary.status == "import_ready"


def test_blocks_boundary_missing_local_only_despite_proof_file(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    (packet / "evidence-boundary.md").write_text(
        "# Evidence boundary\n\nThis packet does not mutate source artifacts.\n",
        encoding="utf-8",
    )
    (packet / "evidence-boundary-review.md").write_text("- No source-artifact mutation: CONFIRMED.\n", encoding="utf-8")
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert summary.status == "blocked_evidence_boundary_failure"


def test_actual_461_packet_imports_with_expected_blocks(tmp_path: Path):
    if not ACTUAL_PACKET.exists():
        return
    summary = import_acceptance_execution_packet(ACTUAL_PACKET, tmp_path / "out")
    assert summary.status == "import_ready_with_expected_blocks"
    assert summary.source_artifact_mutation_status == "not_present"
    assert summary.evidence_boundary_status == "present"
    task = next(record for record in summary.task_records if record.task_id == "MLA-010")
    assert task.status == "import_ready_with_expected_blocks"
    assert all(not artifact.findings for artifact in task.artifact_records)


def test_rejects_source_artifact_mutation_markers(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    path = packet / "raw-artifacts/MLA-010/stop-state.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(
        json.dumps(_payload("MLA-010", "stop-state.json", stop=True, reason_code="source_artifact_mutation"), sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    raw_index = packet / "raw-artifacts-index.md"
    raw_index.write_text(
        raw_index.read_text(encoding="utf-8").replace(
            "MLA-010 | dry-run-result.json; execution-gate-result.json",
            "MLA-010 | dry-run-result.json; execution-gate-result.json; stop-state.json",
        ),
        encoding="utf-8",
    )
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    ledger = packet / "artifact-ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + f"| MLA-010 | stop-state.json | raw-artifacts/MLA-010/stop-state.json | {digest} | self_operator.stop_state_record.v1 | ALPHA-SOLVER-POST-LEVEL-3-LEVEL-12-SELF-OPERATOR-LOCAL-HARNESS-DRY-RUN-WRAPPER-001 | mla-010-run-001 | redacted | present | not present |\n",
        encoding="utf-8",
    )
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert summary.status == "blocked_source_mutation_concern"


def test_validates_mla_001_through_mla_010_coverage(tmp_path: Path):
    packet = _write_packet(tmp_path / "packet")
    text = (packet / "raw-artifacts-index.md").read_text(encoding="utf-8")
    (packet / "raw-artifacts-index.md").write_text("\n".join(line for line in text.splitlines() if "MLA-010" not in line), encoding="utf-8")
    summary = import_acceptance_execution_packet(packet, tmp_path / "out")
    assert "MLA-010" in summary.missing_tasks
    assert summary.status == "blocked_missing_artifact"


def test_handles_actual_461_packet_if_present_without_mutating_it(tmp_path: Path):
    if not ACTUAL_PACKET.exists():
        return
    before = {path.relative_to(ACTUAL_PACKET): hashlib.sha256(path.read_bytes()).hexdigest() for path in ACTUAL_PACKET.rglob("*") if path.is_file()}
    summary = import_acceptance_execution_packet(ACTUAL_PACKET, tmp_path / "out")
    after = {path.relative_to(ACTUAL_PACKET): hashlib.sha256(path.read_bytes()).hexdigest() for path in ACTUAL_PACKET.rglob("*") if path.is_file()}
    assert before == after
    assert summary.coverage == TASK_IDS
    assert summary.status in BLOCKED_STATUSES | {"import_ready", "import_ready_with_expected_blocks"}


def test_cli_help():
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts/import_self_operator_acceptance_results.py"), "--help"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "--packet-dir" in result.stdout
