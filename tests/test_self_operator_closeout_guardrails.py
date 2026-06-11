from __future__ import annotations

import json
from pathlib import Path

from alpha.self_operator.release_gate import (
    BOUNDARY_PACKET,
    CLOSEOUT_PACKET as GATE_CLOSEOUT_PACKET,
    IMPORT_PACKET,
    INTERPRETATION_PACKET,
    RUNBOOK_PACKET,
    evaluate_self_operator_release_gates,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
CLOSEOUT_PACKET = REPO_ROOT / "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-closeout-and-final-guardrails"
RUNBOOK = REPO_ROOT / "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization/mvp-operator-runbook.md"
EXECUTION_GATE = REPO_ROOT / "alpha/self_operator/execution_gate.py"

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
    "post-closeout-release-gate-report.json",
    "post-closeout-release-gate-report.md",
}

ALLOWED_FINAL_STATUSES = {
    "eligible_for_operator_supervised_review",
    "blocked",
    "inconclusive",
}

ALLOWED_ELIGIBLE_WORDING = (
    "The narrow operator-only Self Operator path is eligible for the next "
    "operator-supervised review stage, based only on the accepted local "
    "evidence chain and completed closeout gates."
)

FORBIDDEN_STATUS_CLAIMS = (
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

FORBIDDEN_CLOSEOUT_SURFACE_TERMS = (
    "provider call",
    "hosted model",
    "external API",
    "browser automation",
    "deployment",
    "billing",
    "credential",
    "secret",
    "/v1/solve",
)


def _read(name: str) -> str:
    return (CLOSEOUT_PACKET / name).read_text(encoding="utf-8")


def _section(text: str, header: str) -> str:
    start = text.index(header)
    next_header = text.find("\n## ", start + len(header))
    return text[start:] if next_header == -1 else text[start:next_header]


def test_closeout_packet_has_required_files() -> None:
    assert CLOSEOUT_PACKET.is_dir()
    present = {path.name for path in CLOSEOUT_PACKET.iterdir() if path.is_file()}
    assert REQUIRED_CLOSEOUT_FILES <= present


def test_final_status_uses_only_operator_approved_vocabulary_and_wording() -> None:
    text = _read("final-status.md")
    status_line = next(line for line in text.splitlines() if line.startswith("final_status:"))
    final_status = status_line.split(":", 1)[1].strip()

    assert final_status in ALLOWED_FINAL_STATUSES
    if final_status == "eligible_for_operator_supervised_review":
        assert ALLOWED_ELIGIBLE_WORDING in text
    for phrase in FORBIDDEN_STATUS_CLAIMS:
        assert phrase not in text


def test_approved_claims_avoid_readiness_and_forbidden_surface_references() -> None:
    text = _read("approved-claims.md")

    assert ALLOWED_ELIGIBLE_WORDING in text
    for phrase in FORBIDDEN_STATUS_CLAIMS:
        assert phrase not in text
    for term in FORBIDDEN_CLOSEOUT_SURFACE_TERMS:
        assert term not in text


def test_evidence_chain_requires_import_before_interpretation() -> None:
    text = _read("evidence-chain.md")

    import_pos = text.index("accepted result import")
    interpretation_pos = text.index("accepted interpretation")
    assert import_pos < interpretation_pos
    assert str(IMPORT_PACKET) in text
    assert str(INTERPRETATION_PACKET) in text


def test_gate_status_requires_interpretation_before_release_gate_pass() -> None:
    text = _read("gate-status.md")

    interpretation_pos = text.index("acceptance_interpretation_complete")
    gate_pos = text.index("release gate application")
    assert interpretation_pos < gate_pos
    assert "`p0_p1_defects_absent`" in text and "| pass |" in text
    assert "`release_closeout_review_complete`" in text and "| pass |" in text


def test_closeout_requires_runbook_and_boundary_review() -> None:
    runbook_status = _read("runbook-status.md")
    boundary_status = _read("boundary-status.md")
    final_status = _read("final-status.md")

    assert str(RUNBOOK_PACKET) in runbook_status
    assert "mvp-operator-runbook.md" in runbook_status
    assert str(BOUNDARY_PACKET) in boundary_status
    assert "evidence-boundary review exists" in boundary_status
    assert "runbook_finalized: true" in final_status
    assert "evidence_boundary_review_complete: true" in final_status


def test_non_execution_proof_is_required_for_closeout() -> None:
    text = _read("evidence-chain.md") + _read("gate-status.md")

    assert "non-execution proof" in text
    assert "non_execution" in text


def test_closeout_does_not_claim_release_readiness() -> None:
    text = _read("release-closeout-summary.md") + _read("final-status.md")

    assert "final_status: eligible_for_operator_supervised_review" in text
    assert "release ready" not in text
    assert "release readiness" not in text


def test_forbidden_claim_scan_passed_without_remaining_forbidden_claims() -> None:
    text = _read("forbidden-claim-scan-results.md")

    assert "final scan decision: pass" in text
    assert "forbidden_claim | 0" in text
    assert "No forbidden claim remains." in text


def test_release_gate_closeout_path_aligned_with_this_packet() -> None:
    """The deterministic gate's CLOSEOUT_PACKET must be this packet's directory.

    Guards against the merged-#474 state where this packet existed but the
    deterministic release gate still checked the old `...-release-closeout/`
    path and therefore reported closeout as missing.
    """
    assert GATE_CLOSEOUT_PACKET.as_posix() == (
        "docs/evals/runs/"
        "alpha-solver-post-level-3-level-14-self-operator-release-closeout-and-final-guardrails"
    )
    assert (REPO_ROOT / GATE_CLOSEOUT_PACKET) == CLOSEOUT_PACKET
    assert CLOSEOUT_PACKET.is_dir()


def test_full_root_release_gate_sees_closeout_complete() -> None:
    report = evaluate_self_operator_release_gates(REPO_ROOT)
    statuses = {gate.gate_id: gate.status for gate in report.gates}
    assert statuses["release_closeout_review_complete"] == "pass"
    assert report.final_status == "eligible_for_release_closeout_review"


def test_recorded_eligibility_is_backed_by_full_root_gate_report() -> None:
    """Final closeout eligibility may be recorded only with full-root gate proof."""
    final_text = _read("final-status.md")
    claims_eligible = "eligible_for_operator_supervised_review" in final_text
    report = json.loads(_read("post-closeout-release-gate-report.json"))
    gate_statuses = {gate["gate_id"]: gate["status"] for gate in report["gates"]}
    if claims_eligible:
        assert report["final_status"] == "eligible_for_release_closeout_review"
        assert gate_statuses["release_closeout_review_complete"] == "pass"
    else:
        assert "blocked" in final_text or "inconclusive" in final_text


def test_runbook_approval_identity_wording_matches_current_gate_behavior() -> None:
    runbook_text = RUNBOOK.read_text(encoding="utf-8")
    gate_text = EXECUTION_GATE.read_text(encoding="utf-8")
    runbook_section = _section(runbook_text, "## 5. Approval identity behavior")

    assert "if approval_run_id and proposed_run_id" in gate_text
    assert "if approval_scope_identity and proposed_scope_identity" in gate_text
    assert 'for key in ("task_identity", "scope_identity", "scope_summary")' in gate_text
    assert "requested_action" not in gate_text[gate_text.index("def _proposed_scope_identity") : gate_text.index("def _normalize_identity")]

    assert "only when comparable values are present on both sides" in runbook_section
    assert "Operators should provide explicit proposed-task\n  `metadata.run_id`" in runbook_section
    assert "Operators should provide explicit proposed-task metadata\n  scope identity" in runbook_section
    assert "that dimension cannot be compared by the current gate" in runbook_section
    assert "requested_action`" in runbook_section
    assert "Proposed-task scope identity is\n  read only from proposed-task metadata `task_identity`, `scope_identity`, or\n  `scope_summary`" in runbook_section
    assert "must equal the proposed task's metadata `run_id`" not in runbook_section
    assert "else `scope_summary`) must match" not in runbook_section
