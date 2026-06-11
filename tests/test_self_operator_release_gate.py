from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from alpha.self_operator.release_gate import (
    BOUNDARY_PACKET,
    CLOSEOUT_PACKET,
    DRY_RUN_PACKET,
    EXECUTION_PACKET,
    FOUNDATION_PACKET,
    IMPORT_PACKET,
    INTERPRETATION_PACKET,
    MANUAL_PACKET,
    APPROVAL_PACKET,
    RUNBOOK_PACKET,
    evaluate_self_operator_release_gates,
    write_release_gate_report,
)

REQUIRED_PACKETS = (
    FOUNDATION_PACKET,
    APPROVAL_PACKET,
    DRY_RUN_PACKET,
    MANUAL_PACKET,
    EXECUTION_PACKET,
    IMPORT_PACKET,
    INTERPRETATION_PACKET,
    RUNBOOK_PACKET,
    BOUNDARY_PACKET,
    CLOSEOUT_PACKET,
)


def test_closeout_packet_path_matches_closeout_and_final_guardrails_lane() -> None:
    """The closeout gate must recognize the lane's actual closeout packet path.

    Guards against the #473/#474 mismatch where closeout packets were written
    under `...-release-closeout-and-final-guardrails/` while the gate checked
    the old `...-release-closeout/` path.
    """
    assert CLOSEOUT_PACKET.as_posix() == (
        "docs/evals/runs/"
        "alpha-solver-post-level-3-level-14-self-operator-release-closeout-and-final-guardrails"
    )


def _write_packet(root: Path, packet: Path, text: str = "# fixture\n") -> None:
    target = root / packet
    target.mkdir(parents=True, exist_ok=True)
    (target / "README.md").write_text(text, encoding="utf-8")


def _write_all_packets(root: Path, *, except_packets: set[Path] | None = None) -> None:
    excluded = except_packets or set()
    for packet in REQUIRED_PACKETS:
        if packet not in excluded:
            _write_packet(root, packet)


def _gate_statuses(root: Path) -> dict[str, str]:
    report = evaluate_self_operator_release_gates(root)
    return {gate.gate_id: gate.status for gate in report.gates}


def test_missing_execution_packet_blocks(tmp_path: Path) -> None:
    _write_all_packets(tmp_path, except_packets={EXECUTION_PACKET})

    report = evaluate_self_operator_release_gates(tmp_path)

    assert report.final_status == "blocked_missing_execution"
    assert report.ready is False
    assert _gate_statuses(tmp_path)["operator_supervised_acceptance_executed"] == "missing"


def test_missing_import_packet_blocks(tmp_path: Path) -> None:
    _write_all_packets(tmp_path, except_packets={IMPORT_PACKET})

    report = evaluate_self_operator_release_gates(tmp_path)

    assert report.final_status == "blocked_missing_import"
    assert report.earliest_missing_gate == "result_import_complete"


def test_missing_interpretation_packet_blocks(tmp_path: Path) -> None:
    _write_all_packets(tmp_path, except_packets={INTERPRETATION_PACKET})

    report = evaluate_self_operator_release_gates(tmp_path)

    assert report.final_status == "blocked_missing_interpretation"
    assert report.earliest_missing_gate == "acceptance_interpretation_complete"


def test_missing_runbook_finalization_blocks(tmp_path: Path) -> None:
    _write_all_packets(tmp_path, except_packets={RUNBOOK_PACKET})

    report = evaluate_self_operator_release_gates(tmp_path)

    assert report.final_status == "blocked_missing_runbook_finalization"
    assert report.earliest_missing_gate == "mvp_runbook_finalized_or_updated"


def test_missing_evidence_boundary_review_blocks(tmp_path: Path) -> None:
    _write_all_packets(tmp_path, except_packets={BOUNDARY_PACKET})

    report = evaluate_self_operator_release_gates(tmp_path)

    assert report.final_status == "blocked_missing_boundary_review"
    assert report.earliest_missing_gate == "evidence_boundary_review_complete"


def test_missing_release_closeout_blocks(tmp_path: Path) -> None:
    _write_all_packets(tmp_path, except_packets={CLOSEOUT_PACKET})

    report = evaluate_self_operator_release_gates(tmp_path)

    assert report.final_status == "blocked_release_closeout_not_reviewed"
    assert report.earliest_missing_gate == "release_closeout_review_complete"
    assert _gate_statuses(tmp_path)["release_closeout_review_complete"] == "missing"


def test_all_synthetic_gates_present_gives_eligible_for_release_closeout_review(tmp_path: Path) -> None:
    _write_all_packets(tmp_path)

    report = evaluate_self_operator_release_gates(tmp_path)

    assert report.final_status == "eligible_for_release_closeout_review"
    assert report.ready is True
    assert report.earliest_missing_gate is None
    assert _gate_statuses(tmp_path)["release_closeout_review_complete"] == "pass"


def test_p0_defect_blocks(tmp_path: Path) -> None:
    _write_all_packets(tmp_path)
    defect_file = tmp_path / INTERPRETATION_PACKET / "defects.md"
    defect_file.write_text("# Defects\n\n- P0 defect: open source mutation violation.\n", encoding="utf-8")

    report = evaluate_self_operator_release_gates(tmp_path)

    assert report.final_status == "blocked_release_closeout_not_reviewed"
    assert report.ready is False
    assert _gate_statuses(tmp_path)["p0_p1_defects_absent"] == "blocked"


def test_p1_defect_blocks(tmp_path: Path) -> None:
    _write_all_packets(tmp_path)
    defect_file = tmp_path / RUNBOOK_PACKET / "defects.md"
    defect_file.write_text("# Defects\n\n- P1 failure blocker remains unresolved.\n", encoding="utf-8")

    report = evaluate_self_operator_release_gates(tmp_path)

    assert report.final_status == "blocked_release_closeout_not_reviewed"
    assert report.ready is False
    assert _gate_statuses(tmp_path)["p0_p1_defects_absent"] == "blocked"


def test_backticked_severity_vocabulary_does_not_block(tmp_path: Path) -> None:
    _write_all_packets(tmp_path)
    taxonomy = tmp_path / INTERPRETATION_PACKET / "defect-taxonomy.md"
    taxonomy.write_text(
        "# Defect Taxonomy\n\n"
        "- `P0`: evidence boundary or source mutation violation\n"
        "- `P1`: approval, identity, stop-state, or non-execution safety failure\n"
        "\n`blocked` is emitted for any `P0` or `P1` defect.\n",
        encoding="utf-8",
    )

    report = evaluate_self_operator_release_gates(tmp_path)

    assert _gate_statuses(tmp_path)["p0_p1_defects_absent"] == "pass"
    assert report.final_status == "eligible_for_release_closeout_review"


def test_backticked_unresolved_p0_marker_blocks(tmp_path: Path) -> None:
    _write_all_packets(tmp_path)
    register = tmp_path / INTERPRETATION_PACKET / "defect-register.md"
    register.write_text(
        "# Defect register\n\n- `P0`: unresolved source mutation violation\n",
        encoding="utf-8",
    )

    report = evaluate_self_operator_release_gates(tmp_path)

    assert _gate_statuses(tmp_path)["p0_p1_defects_absent"] == "blocked"
    assert report.ready is False


def test_backticked_unresolved_p1_marker_blocks(tmp_path: Path) -> None:
    _write_all_packets(tmp_path)
    register = tmp_path / INTERPRETATION_PACKET / "defect-register.md"
    register.write_text(
        "# Defect register\n\n- `P1`: unresolved approval failure\n",
        encoding="utf-8",
    )

    report = evaluate_self_operator_release_gates(tmp_path)

    assert _gate_statuses(tmp_path)["p0_p1_defects_absent"] == "blocked"
    assert report.ready is False


def test_table_form_backticked_defect_rows_block(tmp_path: Path) -> None:
    _write_all_packets(tmp_path)
    register = tmp_path / INTERPRETATION_PACKET / "defect-register.md"
    register.write_text(
        "# Defect register\n\n"
        "| Severity | Defect |\n"
        "| --- | --- |\n"
        "| `P0` | source mutation violation |\n"
        "| `P1` | approval failure |\n",
        encoding="utf-8",
    )

    report = evaluate_self_operator_release_gates(tmp_path)

    assert _gate_statuses(tmp_path)["p0_p1_defects_absent"] == "blocked"
    assert report.ready is False


def test_resolved_backticked_references_allowed_only_when_marked_resolved(tmp_path: Path) -> None:
    _write_all_packets(tmp_path)
    register = tmp_path / INTERPRETATION_PACKET / "defect-register.md"

    register.write_text(
        "# Defect register\n\nNo `P0` or `P1` defects remain open; all are resolved.\n",
        encoding="utf-8",
    )
    assert _gate_statuses(tmp_path)["p0_p1_defects_absent"] == "pass"

    register.write_text(
        "# Defect register\n\n`P1` defect remains open.\n",
        encoding="utf-8",
    )
    assert _gate_statuses(tmp_path)["p0_p1_defects_absent"] == "blocked"


def test_deterministic_json_output(tmp_path: Path) -> None:
    _write_all_packets(tmp_path, except_packets={IMPORT_PACKET})
    report = evaluate_self_operator_release_gates(tmp_path)
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    write_release_gate_report(report, first)
    write_release_gate_report(report, second)

    assert first.read_text(encoding="utf-8") == second.read_text(encoding="utf-8")
    parsed = json.loads(first.read_text(encoding="utf-8"))
    assert parsed["final_status"] == "blocked_missing_import"


def test_cli_exits_nonzero_when_blocked(tmp_path: Path) -> None:
    _write_all_packets(tmp_path, except_packets={IMPORT_PACKET})
    output = tmp_path / "gate-report.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/check_self_operator_release_gate.py",
            "--repo-root",
            str(tmp_path),
            "--output",
            str(output),
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "blocked_missing_import" in result.stdout
    assert output.is_file()


def test_cli_does_not_claim_mvp_readiness(tmp_path: Path) -> None:
    _write_all_packets(tmp_path, except_packets={IMPORT_PACKET})

    result = subprocess.run(
        [
            sys.executable,
            "scripts/check_self_operator_release_gate.py",
            "--repo-root",
            str(tmp_path),
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
    )

    combined = result.stdout + result.stderr
    assert "MVP " + "ready" not in combined
    assert "does not claim MVP readiness" in combined
