"""Offline golden tests for the minimal Alpha behavior contract.

These checks validate committed fixture examples, static documentation, and score
arithmetic only. They do not execute Alpha runtime paths, call providers, require
secrets, rerun capture, rescore outputs, or mutate scored artifacts.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

FIXTURE = Path("tests/fixtures/alpha_minimal_behavior_cases.json")
TEST_PLAN = Path(
    "docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/"
    "minimal-behavior-contract-test-plan.md"
)
BATCH_B_SCORE_TABLE = Path(
    "docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/score-table.csv"
)
A3_1_SCORE_TABLE = Path(
    "docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/"
    "score-table.csv"
)
IMPLEMENTATION_READINESS_REVIEW = Path(
    "docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/"
    "implementation-readiness-review.md"
)
DECISION_MATRIX = Path(
    "docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/"
    "minimal-implementation-decision-matrix.csv"
)
PORTABLE_CONTRACT = Path("alpha_solver_portable.py")

REQUIRED_GROUPS = {
    "short_answer_first",
    "no_invented_scaffolding",
    "claim_boundary_safe_wording",
    "evidence_boundary_behavior",
    "artifact_stop_condition_behavior",
    "answer_structure_mode_examples",
}
REQUIRED_MODES = {
    "direct_answer",
    "reviewer_comment",
    "safe_rewrite",
    "evidence_boundary_answer",
    "artifact_stop_condition_answer",
    "protocol_checklist",
}
INVENTED_SCAFFOLDING_PATTERNS = (
    r"\bowner\s*:",
    r"\bowners?\s*=",
    r"\bdue date\b",
    r"\b20\d\d-\d\d-\d\d\b",
    r"(?:^|\s)/(?:workspace|tmp|home|src|app)/",
    r"\b(?:python -m pytest|pytest|git diff|curl)\b",
    r"\b\d+(?:\.\d+)?%\b",
    r"\bacceptance criteria\b",
    r"\bimplemented\b",
)
UNSAFE_CLAIM_PATTERNS = (
    r"\bmvp validation (?:is )?(?:confirmed|achieved|established)\b",
    r"\bvalidates alpha for mvp\b",
    r"\balpha (?:solver )?(?:is )?superior\b",
    r"\bplain providers? (?:are|is) inferior\b",
    r"\bproduction[- ]ready\b",
    r"\bproduction readiness (?:is )?(?:confirmed|achieved|established)\b",
    r"\bbenchmark success (?:is )?(?:confirmed|achieved|established)\b",
    r"\bexact billing (?:is )?accurate\b",
    r"\bprovider orchestration (?:is )?(?:implemented|confirmed|proven)\b",
    r"\bbroad runtime readiness (?:is )?(?:confirmed|achieved|established)\b",
)
STOP_CONDITION_CASES = {
    "artifact-stop-missing-score-table": "score table is missing",
    "artifact-stop-missing-capture-packet": "capture packet is missing",
    "artifact-stop-missing-raw-provider-payloads": "raw provider payloads are unavailable",
}
REQUIRED_TEST_PLAN_SECTIONS = (
    "## 1. Purpose",
    "## 2. Evidence basis",
    "## 3. What this PR tests",
    "## 4. What this PR does not implement",
    "## 5. Test groups",
    "## 6. Future implementation path",
    "## 7. Protected surfaces",
    "## 8. Non-claims",
)


def _read(path: Path) -> str:
    assert path.exists(), f"missing required artifact: {path}"
    return path.read_text(encoding="utf-8")


def _fixture() -> dict[str, Any]:
    return json.loads(_read(FIXTURE))


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _compact_envelope_block() -> str:
    text = _read(PORTABLE_CONTRACT)
    start = text.index("COMPACT-ENVELOPE EXCEPTION FOR LOW-HEADROOM TASKS")
    end = text.index("MINIMAL ALPHA BEHAVIOR CONTRACT")
    return text[start:end]


def _strict_output_requirements_block() -> str:
    text = _read(PORTABLE_CONTRACT)
    start = text.index("STRICT OUTPUT REQUIREMENTS")
    end = text.index("COMPACT-ENVELOPE EXCEPTION FOR LOW-HEADROOM TASKS")
    return text[start:end]


def _sentences(text: str) -> list[str]:
    return [part for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part]


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_pr_261_readiness_artifacts_exist_and_recommend_this_lane():
    review = _read(IMPLEMENTATION_READINESS_REVIEW)
    matrix = _read(DECISION_MATRIX)

    assert "ALPHA-MINIMAL-BEHAVIOR-CONTRACT-AND-TESTS-001" in review
    assert "offline golden tests" in review
    assert "no implementation is included" in review
    assert "B,offline golden tests first" in matrix
    assert "Make this the first implementation step" in matrix


def test_a3_1_and_batch_b_score_math_matches_committed_tables():
    a3_rows = _rows(A3_1_SCORE_TABLE)
    assert sum(int(row["plain_total"]) for row in a3_rows) == 237
    assert sum(int(row["alpha_total"]) for row in a3_rows) == 228
    assert sum(int(row["total_delta"]) for row in a3_rows) == -9

    batch_rows = _rows(BATCH_B_SCORE_TABLE)
    aggregate = next(row for row in batch_rows if row["comparison_id"] == "AGGREGATE")
    assert aggregate["plain_total"] == "405"
    assert aggregate["alpha_total"] == "455"
    assert aggregate["alpha_delta"] == "50"
    assert aggregate["notes"] == "limited 12-comparison Batch B pilot"


def test_fixture_declares_contract_only_not_runtime_enforcement():
    data = _fixture()

    assert data["schema_version"] == "alpha-minimal-behavior-contract-fixtures-v1"
    assert data["runtime_enforcement_status"] == "not_implemented_in_this_pr"
    assert (
        data["portable_prompt_protocol_status"]
        == "implemented_in_alpha_solver_portable_prompt_protocol"
    )
    assert set(data["required_safe_wording"]) == {
        "limited pilot favored Alpha",
        "does not establish broad superiority",
        "planning evidence, not validation",
        "repo evidence overrides planning ledger",
    }
    assert {case["group"] for case in data["cases"]} == REQUIRED_GROUPS
    assert REQUIRED_MODES <= {case["mode"] for case in data["cases"]}


def test_short_answer_first_examples_are_direct_and_not_memos():
    cases = [
        case for case in _fixture()["cases"] if case["group"] == "short_answer_first"
    ]
    assert {case["id"] for case in cases} == {
        "direct-answer-yes-no",
        "reviewer-comment-brief",
        "one-sentence-no-extra-sections",
    }

    yes_no = next(case for case in cases if case["id"] == "direct-answer-yes-no")
    assert yes_no["expected_output"].startswith(tuple(yes_no["starts_with_any"]))

    for case in cases:
        output = case["expected_output"]
        if "max_sentences" in case:
            assert len(_sentences(output)) <= case["max_sentences"]
        for forbidden in case.get("must_not_contain", []):
            assert forbidden.lower() not in output.lower()
        assert "##" not in output


def test_contract_examples_do_not_invent_scaffolding_when_not_supplied():
    for case in _fixture()["cases"]:
        output = case["expected_output"]
        if case["mode"] == "protocol_checklist":
            continue
        for pattern in INVENTED_SCAFFOLDING_PATTERNS:
            assert not re.search(pattern, output, flags=re.IGNORECASE), (
                f"{case['id']} invented scaffolding matching {pattern!r}"
            )


def test_claim_boundary_examples_avoid_forbidden_positive_claims():
    for case in _fixture()["cases"]:
        normalized_output = _normalize(case["expected_output"])
        for pattern in UNSAFE_CLAIM_PATTERNS:
            assert not re.search(pattern, normalized_output, flags=re.IGNORECASE), (
                f"{case['id']} used unsafe claim pattern {pattern!r}"
            )
        for forbidden in case.get("must_not_contain", []):
            assert forbidden.lower() not in normalized_output


def test_evidence_boundary_example_uses_required_safe_wording():
    case = next(
        case
        for case in _fixture()["cases"]
        if case["id"] == "evidence-boundary-answer"
    )
    output = case["expected_output"]

    for phrase in _fixture()["required_safe_wording"]:
        assert phrase in output
    for phrase in case["must_contain"]:
        assert phrase in output


def test_artifact_stop_condition_examples_stop_instead_of_reconstructing():
    cases = {case["id"]: case for case in _fixture()["cases"]}

    for case_id, stop_phrase in STOP_CONDITION_CASES.items():
        output = cases[case_id]["expected_output"]
        assert output.startswith("Stop:")
        assert stop_phrase in output
        assert "Do not" in output
        for forbidden in cases[case_id].get("must_not_contain", []):
            assert forbidden.lower() not in output.lower()


def test_answer_structure_modes_have_synthetic_examples():
    cases = _fixture()["cases"]
    mode_to_ids: dict[str, set[str]] = {}
    for case in cases:
        mode_to_ids.setdefault(case["mode"], set()).add(case["id"])

    assert "direct-answer-yes-no" in mode_to_ids["direct_answer"]
    assert "reviewer-comment-brief" in mode_to_ids["reviewer_comment"]
    assert "claim-boundary-safe-rewrite" in mode_to_ids["safe_rewrite"]
    assert "evidence-boundary-answer" in mode_to_ids["evidence_boundary_answer"]
    assert STOP_CONDITION_CASES.keys() <= mode_to_ids["artifact_stop_condition_answer"]
    assert "protocol-checklist" in mode_to_ids["protocol_checklist"]


def test_portable_minimal_behavior_summary_is_offline_and_bounded():
    from alpha_solver_portable import minimal_behavior_contract_summary

    summary = minimal_behavior_contract_summary()
    normalized = _normalize(summary)

    for phrase in (
        "direct answer first",
        "mode discipline",
        "low headroom restraint",
        "compact envelope mode",
        "no invented scaffolding",
        "compact caveats",
        "task relevant risk",
        "safe claim wording",
        "evidence boundary",
        "artifact stop conditions",
        "limited pilot favored alpha",
        "planning evidence, not validation",
        "repo evidence overrides planning ledger",
        "start with 'stop:'",
        "direct extractions",
        "short confirmations",
        "requested deliverable",
        "do not open with process labels",
        "keep the answer short",
        "do not force heavy solver framing",
        "keep solverenvelope labels",
        "non-essential sections minimal",
        "not expanded for low-headroom task",
        "not applicable / no useful alternatives",
        "do not turn every uncertainty into a long risk block",
        "suppress generic risk boilerplate",
    ):
        assert phrase in normalized
    for forbidden in (
        "provider orchestration is implemented",
        "mvp validation is established",
        "production-ready",
        "live providers were called",
        "capture was rerun",
        "sheets were updated",
    ):
        assert forbidden not in normalized


def test_portable_summary_preserves_boundary_and_no_runtime_implication():
    from alpha_solver_portable import minimal_behavior_contract_summary

    summary = minimal_behavior_contract_summary()
    normalized = _normalize(summary)

    assert "minimal alpha behavior contract" in normalized
    assert "does not alter provider, model, routing, safe-out, or /v1/solve behavior" in normalized
    for phrase in (
        "provider orchestration is implemented",
        "routing behavior changed",
        "model routing behavior changed",
        "runtime api behavior changed",
        "provider-side behavior changed",
        "production readiness is confirmed",
    ):
        assert phrase not in normalized


def test_portable_summary_requires_answer_first_low_headroom_and_compact_caveats():
    from alpha_solver_portable import minimal_behavior_contract_summary

    normalized = _normalize(minimal_behavior_contract_summary())

    for phrase in (
        "begin yes/no decisions",
        "requested deliverable",
        "put necessary rationale or caveats after the direct answer",
        "do not open with process labels unless they materially help the user",
        "for simple rewrites, formatting, direct extraction",
        "one-step admin tasks",
        "keep the answer short",
        "do not force heavy solver framing",
        "shortest wording that remains truthful",
        "do not turn every uncertainty into a long risk block",
    ):
        assert phrase in normalized


def test_portable_contract_resolves_envelope_low_headroom_conflict():
    text = _read(PORTABLE_CONTRACT)
    strict_block = _normalize(_strict_output_requirements_block())
    compact_block = _normalize(_compact_envelope_block())

    assert "every response must include all of these labels" in strict_block
    assert "every response must include all of these sections" not in strict_block
    assert "default full mode: 5 selected experts" in strict_block
    assert "default full mode: 2+ alternative answers" in strict_block
    assert text.index("default full mode: 5 selected experts") < text.index(
        "COMPACT-ENVELOPE EXCEPTION FOR LOW-HEADROOM TASKS"
    )
    assert text.index("COMPACT-ENVELOPE EXCEPTION FOR LOW-HEADROOM TASKS") < text.index(
        "MINIMAL ALPHA BEHAVIOR CONTRACT"
    )
    assert "default expert team and shortlist counts apply only outside" in compact_block
    assert "overrides those default counts for low-headroom tasks" in compact_block
    assert "does not remove the envelope labels" in compact_block


def test_low_headroom_envelope_sections_may_be_minimal_not_expanded():
    compact_block = _normalize(_compact_envelope_block())

    assert "keep the solverenvelope labels" in compact_block
    assert "make non-essential sections minimal" in compact_block
    assert "solution must contain the direct answer first" in compact_block
    assert (
        "confidence, route, and safe-out state should be one concise line each"
        in compact_block
    )
    assert "not expanded for low-headroom task" in compact_block
    assert "do not force 5 full expert insights" in compact_block
    assert "not applicable / no useful alternatives" in compact_block
    assert "do not force 2 expanded alternatives" in compact_block
    assert "do not add broad risk analysis" in compact_block
    assert "multi-pass narration" in compact_block
    assert "full memo" in compact_block


def test_portable_summary_exposes_compact_envelope_exception():
    from alpha_solver_portable import minimal_behavior_contract_summary

    normalized = _normalize(minimal_behavior_contract_summary())

    for phrase in (
        "compact envelope mode",
        "keep solverenvelope labels",
        "non-essential sections minimal",
        "solution contains the direct answer first",
        "instead of 5 full expert insights",
        "not applicable / no useful alternatives",
        "instead of forcing 2 expanded alternatives",
    ):
        assert phrase in normalized


def test_portable_summary_preserves_broad_non_claims():
    from alpha_solver_portable import minimal_behavior_contract_summary

    normalized = _normalize(minimal_behavior_contract_summary())

    for phrase in (
        "do not claim mvp validation",
        "broad superiority",
        "production readiness",
        "benchmark success",
        "exact billing accuracy",
        "broad runtime readiness",
        "provider orchestration",
    ):
        assert phrase in normalized


def test_output_format_refinement_examples_are_answer_shape_first():
    from alpha_solver_portable import OUTPUT_FORMAT_REFINEMENT_EXAMPLES

    reviewer = OUTPUT_FORMAT_REFINEMENT_EXAMPLES["concise_reviewer_comment"]
    replacement = OUTPUT_FORMAT_REFINEMENT_EXAMPLES["replacement_wording"]
    checklist = OUTPUT_FORMAT_REFINEMENT_EXAMPLES["preservation_checklist"]
    status = OUTPUT_FORMAT_REFINEMENT_EXAMPLES["two_sentence_status_update"]
    template = OUTPUT_FORMAT_REFINEMENT_EXAMPLES["compact_template"]

    assert reviewer.startswith("Please tighten")
    assert not re.match(r"^(analysis|process|reasoning|draft|comment|standard|replacement):", reviewer, re.IGNORECASE)

    assert replacement.startswith("The post-improvement run is limited")
    assert "standard:" not in replacement.lower()
    assert "Replacement:" not in replacement

    assert checklist.startswith("- [ ] Preserve")
    assert not checklist.lower().startswith(("analysis:", "process:", "here is", "standard:"))

    assert len(_sentences(status)) <= 2
    assert status.startswith("The portable-contract follow-up")
    assert template.startswith("Decision:")


def test_output_format_refinement_contract_suppresses_visible_process_and_wrappers():
    from alpha_solver_portable import minimal_behavior_contract_summary

    normalized = _normalize(minimal_behavior_contract_summary())

    for phrase in (
        "output format contamination guard",
        "suppress visible process-style text",
        "suppress wrapper labels",
        "do not emit accidental literal-label artifacts such as 'standard:'",
        "concise rewrite, reviewer-comment, replacement wording, checklist",
        "status update, and compact prompt/template tasks",
        "requested answer shape before any caveat",
        "avoid unnecessary memo framing",
        "start with checklist bullets",
        "start with the template or prompt",
    ):
        assert phrase in normalized


def test_refinement_examples_preserve_missing_results_batch_c_and_boundaries():
    from alpha_solver_portable import (
        OUTPUT_FORMAT_REFINEMENT_EXAMPLES,
        minimal_behavior_contract_summary,
    )

    summary = minimal_behavior_contract_summary()
    normalized = _normalize(summary)
    checklist = OUTPUT_FORMAT_REFINEMENT_EXAMPLES["preservation_checklist"]
    replacement = OUTPUT_FORMAT_REFINEMENT_EXAMPLES["replacement_wording"]

    assert "start with 'stop:'" in normalized
    assert "do not reconstruct" in normalized
    assert "do not reconstruct missing results" in checklist.lower()
    assert "keep batch c blocked" in checklist.lower()
    assert "batch c readiness" in replacement.lower()
    assert "planning evidence, not validation" in replacement
    assert "does not establish broad superiority" in replacement
    assert "repo evidence overrides planning ledger" in normalized
    assert "limited pilot favored alpha" in normalized



def test_test_plan_contains_required_sections_and_boundaries():
    text = _read(TEST_PLAN)
    normalized = _normalize(text)

    for section in REQUIRED_TEST_PLAN_SECTIONS:
        assert section in text
    for phrase in (
        "offline deterministic tests",
        "does not implement runtime enforcement",
        "does not call live providers",
        "does not require openai_api_key",
        "does not change provider/model/routing behavior",
        "does not change /v1/solve",
        "does not rerun capture",
        "does not rescore outputs",
        "does not update google sheets",
        "does not start batch c",
    ):
        assert phrase in normalized


def test_portable_contract_contains_minimal_behavior_protocol_wording():
    assert PORTABLE_CONTRACT.exists()
    text = _read(PORTABLE_CONTRACT)
    normalized = _normalize(text)

    for marker in ("LLM_PERSONA_PROTOCOL", "SAFE-OUT", "SolverEnvelope"):
        assert marker in text
    for phrase in (
        "MINIMAL ALPHA BEHAVIOR CONTRACT",
        "Direct answer first",
        "Mode discipline",
        "Low-headroom restraint",
        "COMPACT-ENVELOPE EXCEPTION",
        "No invented scaffolding",
        "Compact caveats",
        "Task-relevant risk",
        "Safe claim wording",
        "Evidence boundary",
        "Artifact stop conditions",
        "MINIMAL_BEHAVIOR_CONTRACT",
        "minimal_behavior_contract_summary",
    ):
        assert phrase in text
    for phrase in (
        "without changing providers, models, routing, safe-out, or the solverenvelope shape",
        "limited pilot favored alpha",
        "planning evidence, not validation",
        "repo evidence overrides planning ledger",
        "start with \"stop:\"",
        "does not alter provider, model, routing, safe-out, or /v1/solve behavior",
    ):
        assert phrase in normalized
