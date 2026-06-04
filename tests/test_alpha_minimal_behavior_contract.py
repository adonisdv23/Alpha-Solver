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
    r"\bmvp (?:is )?validated\b",
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


def test_protected_runtime_contract_file_is_unchanged_by_this_lane():
    assert PORTABLE_CONTRACT.exists()
    assert "Alpha Solver v2.3.0-P3" in _read(PORTABLE_CONTRACT)
