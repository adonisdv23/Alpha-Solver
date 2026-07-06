"""Offline structural tests for the substantive lift answer contract.

These checks validate the portable-surface contract text, its machine-readable
constants, the deterministic wording checker, and committed fixture examples.
They do not call providers or models, do not execute /v1/solve, and do not
score, rank, or compare outputs; a passing run makes no quality, benchmark,
readiness, or superiority claim.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import alpha_solver_portable as portable

FIXTURE = Path("tests/fixtures/alpha_substantive_lift_cases.json")
PORTABLE_CONTRACT = Path("alpha_solver_portable.py")
SPEC = Path(".specs/ALPHA-SOLVER-SUBSTANTIVE-LIFT-ANSWER-CONTRACT-001.md")

EXPECTED_LABELS = [
    "Intent:",
    "Assumes:",
    "Tradeoff:",
    "Recommendation:",
    "Fails if:",
    "Next:",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _cases() -> list[dict]:
    return json.loads(_read(FIXTURE))["cases"]


class TestContractText:
    def test_portable_docstring_contains_lift_contract_section(self):
        text = _read(PORTABLE_CONTRACT)
        assert "SUBSTANTIVE LIFT CONTRACT (HIGH-HEADROOM TASKS)" in text
        assert "ALPHA-SOLVER-SUBSTANTIVE-LIFT-ANSWER-CONTRACT-001" in text
        assert "ANTI-GENERIC RULES" in text
        for label in EXPECTED_LABELS:
            assert label in text

    def test_lift_section_comes_after_restraint_contract(self):
        text = _read(PORTABLE_CONTRACT)
        assert text.index("MINIMAL ALPHA BEHAVIOR CONTRACT") < text.index(
            "SUBSTANTIVE LIFT CONTRACT (HIGH-HEADROOM TASKS)"
        )

    def test_low_headroom_precedence_is_explicit(self):
        normalized = _normalize(_read(PORTABLE_CONTRACT))
        assert (
            "the compact-envelope exception and low-headroom restraint rules "
            "override this contract" in normalized
        )
        assert "never force the lift block" in normalized

    def test_contract_states_wording_only_boundary(self):
        normalized = _normalize(_read(PORTABLE_CONTRACT))
        assert (
            "this contract constrains solution wording on this portable surface "
            "only" in normalized
        )
        assert (
            "makes no benchmark, readiness, production, or superiority claims"
            in normalized
        )


class TestContractConstants:
    def test_moves_match_documented_labels_in_order(self):
        assert [label for label, _ in portable.SUBSTANTIVE_LIFT_MOVES] == (
            EXPECTED_LABELS
        )
        for _, requirement in portable.SUBSTANTIVE_LIFT_MOVES:
            assert requirement.strip()

    def test_triggers_and_exemptions_are_disjoint_and_nonempty(self):
        triggers = set(portable.SUBSTANTIVE_LIFT_TRIGGERS)
        exempt = set(portable.SUBSTANTIVE_LIFT_EXEMPT)
        assert triggers and exempt
        assert not triggers & exempt

    def test_summary_contains_moves_rules_and_boundary(self):
        summary = portable.substantive_lift_contract_summary()
        assert portable.SUBSTANTIVE_LIFT_LANE in summary
        for label in EXPECTED_LABELS:
            assert label in summary
        for rule in portable.SUBSTANTIVE_LIFT_ANTI_GENERIC_RULES:
            assert rule in summary
        assert "SOLUTION wording requirements only" in summary


class TestChecker:
    def test_compliant_fixture_solutions_pass(self):
        for case in _cases():
            if not case["lift_required"]:
                continue
            result = portable.check_substantive_lift(case["compliant_solution"])
            assert result["ok"], (case["case_id"], result)
            assert result["has_lift_block"]
            assert result["opens_with_intent"]
            assert result["order_ok"]
            assert result["generic_flags"] == []

    def test_non_compliant_fixture_solutions_fail(self):
        for case in _cases():
            if not case["lift_required"]:
                continue
            result = portable.check_substantive_lift(case["non_compliant_solution"])
            assert not result["ok"], (case["case_id"], result)
            assert result["missing_moves"], case["case_id"]

    def test_hedge_phrasing_is_flagged_even_with_lift_block(self):
        text = (
            "Intent: Decide between two databases for the new service.\n"
            "Assumes: Read-heavy workload with modest write volume.\n"
            "Tradeoff: Operational familiarity versus horizontal scale.\n"
            "Recommendation: It depends on your team, but Postgres is common.\n"
            "Fails if: Write volume exceeds a single primary's capacity.\n"
            "Next: Load-test the top three queries against Postgres today.\n"
        )
        result = portable.check_substantive_lift(text)
        assert not result["ok"]
        assert result["generic_flags"]

    def test_word_boundary_prevents_audit_depends_false_positive(self):
        text = (
            "Intent: Decide whether the audit depends on external counsel.\n"
            "Assumes: The audit scope is already fixed by the contract.\n"
            "Tradeoff: Internal speed versus external defensibility.\n"
            "Recommendation: Run the audit internally with counsel reviewing only findings.\n"
            "Fails if: The contract requires an independent third-party attestation.\n"
            "Next: Read the audit clause in the signed contract this morning.\n"
        )
        result = portable.check_substantive_lift(text)
        assert result["ok"], result

    def test_weak_next_action_is_flagged(self):
        text = (
            "Intent: Choose a queue technology for background jobs.\n"
            "Assumes: Throughput stays under 1k messages per second.\n"
            "Tradeoff: Operational simplicity versus delivery guarantees.\n"
            "Recommendation: Use the managed queue already in the platform account.\n"
            "Fails if: Jobs require strict ordering across partitions.\n"
            "Next: Consider evaluating several queue options with the team.\n"
        )
        result = portable.check_substantive_lift(text)
        assert not result["ok"]
        assert result["weak_next_action"]

    def test_out_of_order_block_is_rejected(self):
        text = (
            "Recommendation: Ship the migration behind a feature flag.\n"
            "Intent: Decide how to roll out the schema change safely.\n"
            "Assumes: The table has under ten million rows.\n"
            "Tradeoff: Rollout speed versus rollback safety.\n"
            "Fails if: The migration locks the table longer than five seconds.\n"
            "Next: Measure the migration lock time against a production-size copy.\n"
        )
        result = portable.check_substantive_lift(text)
        assert not result["ok"]
        assert not result["opens_with_intent"]
        assert not result["order_ok"]

    def test_low_headroom_answer_correctly_has_no_lift_block(self):
        low = [case for case in _cases() if not case["lift_required"]]
        assert low, "fixture must include a low-headroom precedence case"
        for case in low:
            result = portable.check_substantive_lift(case["compliant_solution"])
            assert not result["has_lift_block"]


class TestFixtureShape:
    def test_at_least_three_realistic_substantive_prompts(self):
        substantive = [case for case in _cases() if case["lift_required"]]
        assert len(substantive) >= 3
        for case in substantive:
            assert len(case["prompt"]) > 40
            assert case["non_compliant_reason"].strip()

    def test_compliance_example_solution_passes_checker(self):
        example = portable.COMPLIANCE_EXAMPLES["COMPLIANT"]
        start = example.index("SOLUTION:") + len("SOLUTION:")
        end = example.index("CONFIDENCE:")
        result = portable.check_substantive_lift(example[start:end])
        assert result["ok"], result

    def test_generic_compliance_example_fails_checker(self):
        example = portable.COMPLIANCE_EXAMPLES["NON_COMPLIANT_GENERIC"]
        start = example.index("SOLUTION:") + len("SOLUTION:")
        end = example.index("Why it fails")
        result = portable.check_substantive_lift(example[start:end])
        assert not result["ok"]
        assert result["generic_flags"]

    def test_spec_exists_and_names_planning_predecessor(self):
        text = _read(SPEC)
        assert "ALPHA-ANSWER-STRUCTURE-V2-001" in text
        assert "ALPHA-SOLVER-SUBSTANTIVE-LIFT-ANSWER-CONTRACT-001" in text
