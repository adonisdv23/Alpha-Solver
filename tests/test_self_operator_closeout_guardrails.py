from __future__ import annotations

from pathlib import Path

import pytest

from alpha.self_operator.release_gate import evaluate_self_operator_release_gates

ROOT = Path(__file__).resolve().parents[1]
CLOSEOUT_PACKET = ROOT / (
    "docs/evals/runs/"
    "alpha-solver-post-level-3-level-14-self-operator-release-closeout-and-final-guardrails"
)
RUNBOOK = ROOT / (
    "docs/evals/runs/"
    "alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization/"
    "mvp-operator-runbook.md"
)
EXECUTION_GATE = ROOT / "alpha/self_operator/execution_gate.py"

REQUIRED_CLOSEOUT_FILES = {
    "README.md",
    "release-closeout-summary.md",
    "evidence-chain.md",
    "gate-status.md",
    "defect-status.md",
    "runbook-status.md",
    "boundary-status.md",
    "runbook-approval-identity-correction.md",
    "approved-claims.md",
    "forbidden-claims.md",
    "forbidden-claim-scan-results.md",
    "guardrails-added.md",
    "checks-run.md",
    "final-status.md",
    "post-closeout-next-steps.md",
}

ALLOWED_FINAL_STATUSES = {
    "eligible_for_operator_supervised_review",
    "blocked",
    "inconclusive",
}
APPROVED_ELIGIBLE_WORDING = (
    "The narrow operator-only Self Operator path is eligible for the next "
    "operator-supervised review stage, based only on the accepted local "
    "evidence chain and completed closeout gates."
)
FORBIDDEN_READINESS_PHRASES = (
    "MVP ready",
    "release ready",
    "production ready",
    "runtime ready",
    "provider ready",
    "hosted ready",
    "benchmark validated",
    "autonomous ready",
    "broad user ready",
)
FORBIDDEN_REFERENCE_TERMS = (
    "provider",
    "model",
    "api",
    "browser",
    "deployment",
    "billing",
    "credential",
)


def _packet_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(CLOSEOUT_PACKET.glob("*.md"), key=lambda item: item.name)
    )


def _read(name: str) -> str:
    return (CLOSEOUT_PACKET / name).read_text(encoding="utf-8")


def test_closeout_packet_contains_required_files() -> None:
    assert CLOSEOUT_PACKET.is_dir()
    present = {path.name for path in CLOSEOUT_PACKET.iterdir() if path.is_file()}
    assert REQUIRED_CLOSEOUT_FILES <= present


@pytest.mark.parametrize("missing", ["result_import_complete", "acceptance_interpretation_complete"])
def test_release_gate_blocks_missing_accepted_evidence_before_closeout(
    tmp_path: Path, missing: str
) -> None:
    report = evaluate_self_operator_release_gates(tmp_path)

    assert report.ready is False
    statuses = {gate.gate_id: gate.status for gate in report.gates}
    assert statuses[missing] == "missing"
    assert report.final_status != "eligible_for_release_closeout_review"


def test_final_status_uses_only_operator_approved_vocabulary() -> None:
    text = _read("final-status.md")

    assert "final_status: eligible_for_operator_supervised_review" in text
    assert any(f"final_status: {status}" in text for status in ALLOWED_FINAL_STATUSES)
    assert APPROVED_ELIGIBLE_WORDING in text
    assert "eligible_for_release_closeout_review" not in text


def test_closeout_outputs_do_not_make_forbidden_readiness_claims() -> None:
    allowed_files = {"forbidden-claims.md", "forbidden-claim-scan-results.md", "checks-run.md"}

    for path in sorted(CLOSEOUT_PACKET.glob("*.md"), key=lambda item: item.name):
        if path.name in allowed_files:
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_READINESS_PHRASES:
            hits = [
                line
                for line in text.splitlines()
                if phrase in line
                and "not claim" not in line
                and "does not claim" not in line
                and "must not" not in line
                and "No " not in line
            ]
            assert hits == [], f"unexpected project-status claim for {phrase!r} in {path.name}: {hits}"


def test_closeout_outputs_keep_boundary_terms_in_allowed_files_only() -> None:
    allowed_files = {
        "boundary-status.md",
        "checks-run.md",
        "forbidden-claim-scan-results.md",
        "forbidden-claims.md",
        "runbook-approval-identity-correction.md",
    }

    for path in sorted(CLOSEOUT_PACKET.glob("*.md"), key=lambda item: item.name):
        if path.name in allowed_files:
            continue
        lower = path.read_text(encoding="utf-8").lower()
        for term in FORBIDDEN_REFERENCE_TERMS:
            assert term not in lower, f"{term!r} appears in {path.name}"


def test_non_execution_proof_is_recorded() -> None:
    text = _packet_text().lower()

    assert "no runtime behavior was changed" in text
    assert "no source evidence was mutated" in text
    assert "non-execution proof" in text
    assert "offline" in text


def test_evidence_chain_order_is_enforced_in_closeout_packet() -> None:
    text = _read("evidence-chain.md")

    import_pos = text.index("| 1 | accepted import")
    interpretation_pos = text.index("| 2 | accepted interpretation")
    gate_pos = text.index("| 3 | release gate")
    runbook_pos = text.index("| 4 | runbook finalization")
    boundary_pos = text.index("| 5 | evidence-boundary review")
    closeout_pos = text.index("| 6 | closeout")
    assert import_pos < interpretation_pos < gate_pos < runbook_pos < boundary_pos < closeout_pos


def test_prerequisite_statuses_are_recorded_before_closeout() -> None:
    text = _read("gate-status.md") + _read("defect-status.md")

    for phrase in (
        "accepted result import exists: yes",
        "accepted interpretation exists: yes",
        "release gate apply exists: yes",
        "runbook finalization exists: yes",
        "evidence-boundary review exists: yes",
        "no unresolved P0: yes",
        "no unresolved P1: yes",
        "P2/P3 defects either resolved or explicitly deferred: yes",
        "operator-approved closeout wording is used: yes",
    ):
        assert phrase in text


def test_runbook_approval_identity_wording_matches_current_gate_behavior() -> None:
    runbook_text = RUNBOOK.read_text(encoding="utf-8")
    gate_text = EXECUTION_GATE.read_text(encoding="utf-8")

    assert 'for key in ("task_identity", "scope_identity", "scope_summary")' in gate_text
    assert 'for key in ("task_identity", "scope_identity", "scope_summary", "requested_action")' in gate_text
    assert "when both are present" in runbook_text
    assert "metadata.run_id" in runbook_text
    assert "Proposed task scope identity is drawn only from proposed task metadata" in runbook_text
    normalized_runbook = " ".join(runbook_text.split())
    assert "it does not fall back to `requested_action`" in normalized_runbook
    assert "will not itself produce an approval identity mismatch finding" in normalized_runbook
    assert "Do not treat missing proposed identity fields as an automatic identity mismatch" in normalized_runbook
