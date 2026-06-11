"""Final closeout guardrails for the Self Operator release closeout lane.

Lane: ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-RELEASE-CLOSEOUT-AND-FINAL-GUARDRAILS-001

These tests are deterministic and local-only: they read repository files and
run the static release-gate evaluator. They never execute proposed commands
and never call providers or external systems.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from alpha.self_operator import execution_gate
from alpha.self_operator.preflight import ProposedTask
from alpha.self_operator.release_gate import (
    BOUNDARY_PACKET,
    CLOSEOUT_PACKET,
    EXECUTION_PACKET,
    IMPORT_PACKET,
    INTERPRETATION_PACKET,
    RUNBOOK_PACKET,
    evaluate_self_operator_release_gates,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET_DIR = REPO_ROOT / CLOSEOUT_PACKET
RUNBOOK_FILE = REPO_ROOT / RUNBOOK_PACKET / "mvp-operator-runbook.md"

ACCEPTED_IMPORT_DIR = (
    "alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import"
)
INTERPRETATION_APPLY_DIR = (
    "alpha-solver-post-level-3-level-13-to-level-14-self-operator-operator-decision-interpretation-apply"
)
RELEASE_GATE_APPLY_DIR = (
    "alpha-solver-post-level-3-level-14-self-operator-release-gate-apply"
)

REQUIRED_PACKET_FILES = (
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
    "duplicate-closeout-attempts-reviewed.md",
    "selected-next-lane.md",
    "blocker-fallback-lane.md",
)

ALLOWED_FINAL_STATUSES = (
    "eligible_for_operator_supervised_review",
    "blocked",
    "inconclusive",
)
ALLOWED_ELIGIBLE_WORDING = (
    "The narrow operator-only Self Operator path is eligible for the next "
    "operator-supervised review stage, based only on the accepted local "
    "evidence chain and completed closeout gates."
)

# Phrases blocked as project-status claims. They may appear only in
# forbidden-claim documentation files, never as status assertions.
FORBIDDEN_CLAIM_PHRASES = (
    "mvp ready",
    "release ready",
    "production ready",
    "runtime ready",
    "provider ready",
    "hosted ready",
    "benchmark validated",
    "benchmark superior",
    "autonomous ready",
    "broad user ready",
)
CLAIM_DOCUMENTATION_FILES = {
    "forbidden-claims.md",
    "forbidden-claim-scan-results.md",
    "checks-run.md",
}

# External runtime surface terms that closeout outputs may reference only in
# boundary/non-action/claim-documentation files (as negations or scan
# records), never in status or summary files.
SURFACE_TERMS = (
    "provider",
    "hosted model",
    "/v1/solve",
    "browser",
    "deployment",
    "billing",
    "credential",
    "secret",
)
BOUNDARY_DOCUMENTATION_FILES = {
    "evidence-boundary.md",
    "non-actions.md",
    "boundary-status.md",
    "forbidden-claims.md",
    "forbidden-claim-scan-results.md",
    "checks-run.md",
    "post-closeout-release-gate-report.md",
    "post-closeout-release-gate-report.json",
}


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def _packet_files() -> list[Path]:
    return sorted(item for item in PACKET_DIR.iterdir() if item.is_file())


def _runbook_section_5() -> str:
    text = RUNBOOK_FILE.read_text(encoding="utf-8")
    start = text.index("## 5. Approval identity behavior")
    end = text.index("## 6.")
    return " ".join(text[start:end].split())


def test_release_gate_closeout_path_aligned_with_this_packet() -> None:
    assert CLOSEOUT_PACKET.as_posix() == (
        "docs/evals/runs/"
        "alpha-solver-post-level-3-level-14-self-operator-release-closeout-and-final-guardrails"
    )
    assert PACKET_DIR.is_dir()


def test_closeout_packet_contains_all_required_files() -> None:
    missing = [name for name in REQUIRED_PACKET_FILES if not (PACKET_DIR / name).is_file()]
    assert missing == []


def test_prerequisites_exist_before_closeout() -> None:
    runs = REPO_ROOT / "docs/evals/runs"
    assert (runs / ACCEPTED_IMPORT_DIR).is_dir(), "accepted import evidence is required before closeout"
    assert (runs / INTERPRETATION_APPLY_DIR).is_dir(), "accepted interpretation is required before closeout"
    assert (runs / RELEASE_GATE_APPLY_DIR).is_dir(), "release-gate application is required before closeout"
    assert (REPO_ROOT / IMPORT_PACKET).is_dir()
    assert (REPO_ROOT / INTERPRETATION_PACKET).is_dir()
    assert RUNBOOK_FILE.is_file(), "the canonical runbook is required before closeout"
    assert (REPO_ROOT / BOUNDARY_PACKET).is_dir(), "the evidence-boundary review is required before closeout"


def test_evidence_chain_orders_import_before_interpretation_before_release_gate() -> None:
    chain = (PACKET_DIR / "evidence-chain.md").read_text(encoding="utf-8")
    import_at = chain.index(ACCEPTED_IMPORT_DIR)
    interpretation_at = chain.index(INTERPRETATION_APPLY_DIR)
    release_gate_at = chain.index(RELEASE_GATE_APPLY_DIR)
    assert import_at < interpretation_at < release_gate_at


def test_non_execution_proof_is_preserved_and_referenced() -> None:
    proof = REPO_ROOT / EXECUTION_PACKET / "non-execution-proof.md"
    assert proof.is_file(), "the #461 non-execution proof must be preserved"
    chain = (PACKET_DIR / "evidence-chain.md").read_text(encoding="utf-8")
    assert "non-execution-proof.md" in chain


def test_final_status_uses_bounded_vocabulary() -> None:
    text = (PACKET_DIR / "final-status.md").read_text(encoding="utf-8")
    match = re.search(r"`([a-z_]+)`", text)
    assert match is not None, "final-status.md must declare a backticked status token"
    assert match.group(1) in ALLOWED_FINAL_STATUSES
    if match.group(1) == "eligible_for_operator_supervised_review":
        normalized = " ".join(text.split())
        assert ALLOWED_ELIGIBLE_WORDING in normalized


def test_no_forbidden_readiness_claims_outside_claim_documentation() -> None:
    offenders: list[str] = []
    for path in _packet_files():
        if path.name in CLAIM_DOCUMENTATION_FILES:
            continue
        text = _normalized(path)
        for phrase in FORBIDDEN_CLAIM_PHRASES:
            if phrase in text:
                offenders.append(f"{path.name}: {phrase}")
    assert offenders == []


def test_no_surface_terms_outside_boundary_documentation() -> None:
    offenders: list[str] = []
    for path in _packet_files():
        if path.name in BOUNDARY_DOCUMENTATION_FILES:
            continue
        text = _normalized(path)
        for term in SURFACE_TERMS:
            if term in text:
                offenders.append(f"{path.name}: {term}")
    assert offenders == []


def test_full_root_release_gate_sees_closeout_complete() -> None:
    report = evaluate_self_operator_release_gates(REPO_ROOT)
    statuses = {gate.gate_id: gate.status for gate in report.gates}
    assert statuses["release_closeout_review_complete"] == "pass"
    assert report.final_status == "eligible_for_release_closeout_review"


def test_recorded_eligibility_is_backed_by_gate_report() -> None:
    final_text = (PACKET_DIR / "final-status.md").read_text(encoding="utf-8")
    claims_eligible = "eligible_for_operator_supervised_review" in final_text
    report = json.loads(
        (PACKET_DIR / "post-closeout-release-gate-report.json").read_text(encoding="utf-8")
    )
    gate_statuses = {gate["gate_id"]: gate["status"] for gate in report["gates"]}
    if claims_eligible:
        assert report["final_status"] == "eligible_for_release_closeout_review"
        assert gate_statuses["release_closeout_review_complete"] == "pass"
    else:
        assert "`blocked`" in final_text or "`inconclusive`" in final_text


def test_gate_report_remains_gate_result_not_readiness_claim() -> None:
    report = json.loads(
        (PACKET_DIR / "post-closeout-release-gate-report.json").read_text(encoding="utf-8")
    )
    assert "does not claim MVP readiness" in report["non_actions"]
    report_md = (PACKET_DIR / "post-closeout-release-gate-report.md").read_text(encoding="utf-8")
    assert "not a release-readiness claim" in report_md


def test_runbook_does_not_overstate_approval_identity_enforcement() -> None:
    section = _runbook_section_5()
    assert "only when both" in section
    assert "cannot be compared" in section
    assert "not an automatic" in section
    assert "`metadata.run_id`" in section
    assert "no `requested_action` fallback" in section
    assert "requires the approval record to match" not in section


def test_execution_gate_proposed_identity_matches_runbook_wording() -> None:
    bare = ProposedTask.from_mapping(
        {
            "lane_id": "LANE-GUARDRAIL-001",
            "requested_action": "a requested action that must not become identity",
            "metadata": {},
        }
    )
    assert execution_gate._proposed_scope_identity(bare) == ""
    assert execution_gate._proposed_run_id(bare) == ""

    explicit = ProposedTask.from_mapping(
        {
            "lane_id": "LANE-GUARDRAIL-001",
            "requested_action": "a requested action that must not become identity",
            "metadata": {"run_id": "run-guardrail-1", "scope_identity": "scope a"},
        }
    )
    assert execution_gate._proposed_scope_identity(explicit) == "scope a"
    assert execution_gate._proposed_run_id(explicit) == "run-guardrail-1"

    source = (REPO_ROOT / "alpha/self_operator/execution_gate.py").read_text(encoding="utf-8")
    proposed_identity_body = source.split("def _proposed_scope_identity", 1)[1].split("\ndef ", 1)[0]
    assert "requested_action" not in proposed_identity_body


def test_final_status_cli_remains_deferred_and_not_required() -> None:
    assert not (REPO_ROOT / "scripts/self_operator_status.py").exists()
    assert not (REPO_ROOT / "tests/test_self_operator_status_cli.py").exists()
    assert not (
        REPO_ROOT
        / "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-final-status-cli"
    ).exists()
    next_steps = (PACKET_DIR / "post-closeout-next-steps.md").read_text(encoding="utf-8")
    assert "deferred" in next_steps
