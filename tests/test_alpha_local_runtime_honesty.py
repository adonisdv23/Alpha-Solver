"""Local-output honesty tests (ALPHA-SOLVER-TOT-ECHO-HONESTY-HOTFIX-001).

Unsupported local deterministic prompts must never surface prompt echo or
ToT/CoT template artifacts as final answers; they must return a bounded
SAFE-OUT-style response with diagnostics. These tests call only the local
deterministic paths: no providers, no hosted or local models, no network.
They assert honesty, not intelligence — a passing run makes no quality,
benchmark, readiness, or superiority claim.
"""
from __future__ import annotations

import alpha_solver_portable as portable
from alpha.reasoning.cache import make_key
from alpha.solver import observability as solver_obs
from alpha_solver_entry import AlphaSolver, _tree_of_thought

BLOCKED_TEMPLATE_PREFIXES = (
    "Rephrase:",
    "Decompose:",
    "Edge cases:",
    "Counterpoints:",
    "Summarize:",
)
COT_ARTIFACT_PREFIXES = ("To proceed, consider:", "To proceed, clarify:")
LIFT_LABELS = ("Intent:", "Assumes:", "Tradeoff:", "Recommendation:", "Fails if:", "Next:")

# Contains "impossible", which the constraint scorer zeroes, dropping the
# composite root score to 0.6 so a 0.7 threshold deterministically routes to
# the CoT fallback — the live template-echo leak path this lane closes.
UNSUPPORTED_HIGH_HEADROOM = (
    "Our team says zero-downtime auth migration is impossible; "
    "design a rollout plan anyway."
)

UNSUPPORTED_CONFIGS = (
    {},
    {"low_conf_threshold": 0.7},
    {"multi_branch": True},
)

SUPPORTED_FIXTURE_PROMPTS = {
    "photosynthesis": "Explain photosynthesis in two plain-language sentences.",
    "checklist": "Give a three-item checklist for packing for a one-night work trip.",
    "database": (
        "Help me choose a database for my app; I have not decided traffic, "
        "budget, or data model."
    ),
    "false_premise": (
        'Summarize the main claims of the 2025 paper "Quantum Bananas Cure '
        'Insomnia" without inventing facts.'
    ),
}


def _normalized(text: str) -> str:
    return " ".join(text.strip().lower().split())


def _section(rendered: str, header: str, next_marker: str) -> str:
    start = rendered.index(f"{header}:\n") + len(f"{header}:\n")
    end = rendered.index(next_marker, start)
    return rendered[start:end]


def _solve_unsupported(**kwargs) -> dict:
    return _tree_of_thought(
        UNSUPPORTED_HIGH_HEADROOM, cache_path=None, enable_cache=False, **kwargs
    )


def test_unsupported_prompt_never_echoes_the_prompt():
    for config in UNSUPPORTED_CONFIGS:
        result = _solve_unsupported(**config)
        assert _normalized(result["final_answer"]) != _normalized(
            UNSUPPORTED_HIGH_HEADROOM
        ), config
        assert _normalized(result["solution"]) != _normalized(
            UNSUPPORTED_HIGH_HEADROOM
        ), config


def test_unsupported_prompt_never_starts_with_template_prefixes():
    for config in UNSUPPORTED_CONFIGS:
        result = _solve_unsupported(**config)
        answer = result["final_answer"].strip()
        for prefix in BLOCKED_TEMPLATE_PREFIXES + COT_ARTIFACT_PREFIXES:
            assert not answer.lower().startswith(prefix.lower()), (config, answer)


def test_unsupported_prompt_returns_bounded_safeout_text():
    for config in UNSUPPORTED_CONFIGS:
        result = _solve_unsupported(**config)
        answer = result["final_answer"]
        assert answer.startswith("SAFE-OUT:"), (config, answer)
        lowered = answer.lower()
        assert (
            "synthesis is unavailable" in lowered
            or "could not derive a substantive answer" in lowered
        ), (config, answer)
        assert result["solution"] == result["final_answer"]


def test_diagnostics_identify_unsupported_local_cause():
    for config in UNSUPPORTED_CONFIGS:
        result = _solve_unsupported(**config)
        tot_diag = result["diagnostics"]["tot"]
        assert tot_diag.get("answer_kind") == "local_unsupported_safeout", config
        assert tot_diag.get("synthesis_available") is False, config
        assert (
            tot_diag.get("echo_detected") is True
            or tot_diag.get("template_branch_detected") is True
        ), config
        assert result["reason"] in (
            "prompt_echo_replaced_with_unsupported_local_safeout",
            "template_artifact_replaced_with_unsupported_local_safeout",
        ), config


def test_cot_fallback_template_artifact_is_bounded():
    result = _solve_unsupported(low_conf_threshold=0.7)
    assert result["route"] == "cot_fallback"
    assert not result["final_answer"].lower().startswith("to proceed, consider:")
    assert result["final_answer"].startswith("SAFE-OUT:")
    tot_diag = result["diagnostics"]["tot"]
    assert tot_diag.get("template_branch_detected") is True
    assert tot_diag.get("raw_template_answer", "").lower().startswith(
        "to proceed, consider:"
    )


def test_cot_fallback_records_visible_confidence_before_adjustment():
    result = _solve_unsupported(low_conf_threshold=0.7)
    tot_diag = result["diagnostics"]["tot"]

    assert result["route"] == "cot_fallback"
    assert result["confidence"] == 0.20
    assert tot_diag["confidence"] == 0.20
    assert result["confidence_before_adjustment"] == 0.50
    assert tot_diag["confidence_before_adjustment"] == 0.50


def test_cached_template_answer_is_bounded():
    query = "Design a sharding plan for our multi-tenant Postgres cluster."
    key = make_key(query, 0, (), "0")
    poisoned = {
        key: {
            "answer": f"Rephrase: {query}",
            "score": 0.99,
            "path": [query, f"Rephrase: {query}"],
            "hash": "stale",
            "ts": 0,
        }
    }
    envelope = AlphaSolver().solve(query, cache=poisoned)
    assert not envelope["final_answer"].startswith("Rephrase:")
    assert envelope["final_answer"].startswith("SAFE-OUT:")
    assert envelope["diagnostics"]["tot"].get("template_branch_detected") is True


def test_supported_fixture_prompts_preserve_prior_behavior():
    answers = {
        name: _tree_of_thought(prompt, cache_path=None, enable_cache=False)
        for name, prompt in SUPPORTED_FIXTURE_PROMPTS.items()
    }
    for name, result in answers.items():
        assert result["reason"] == "prompt_echo_replaced_with_local_derived_answer", name
        assert result["diagnostics"]["tot"]["echo_detected"] is True
        assert result["diagnostics"]["tot"].get("answer_kind") == "derived_local_fixture"
    assert "sunlight" in answers["photosynthesis"]["final_answer"].lower()
    assert "1." in answers["checklist"]["final_answer"]
    assert "3." in answers["checklist"]["final_answer"]
    assert "clarify" in answers["database"]["final_answer"].lower()
    assert "cannot substantiate" in answers["false_premise"]["final_answer"].lower()



def test_unsupported_safeout_confidence_is_low_and_diagnostic():
    result = _solve_unsupported()
    tot_diag = result["diagnostics"]["tot"]

    assert result["final_answer"].startswith("SAFE-OUT:")
    assert result["confidence"] == 0.20
    assert tot_diag["confidence"] == 0.20
    assert result["confidence_before_adjustment"] > result["confidence"]
    assert tot_diag["confidence_before_adjustment"] > tot_diag["confidence"]
    assert (
        result["confidence_adjustment_reason"]
        == "confidence_adjusted_due_to_unsupported_local_synthesis"
    )
    assert (
        tot_diag["confidence_adjustment_reason"]
        == "confidence_adjusted_due_to_unsupported_local_synthesis"
    )
    assert "confidence adjusted" in result["notes"]


def test_supported_fixture_confidence_stays_inherited_without_adjustment():
    result = _tree_of_thought(
        SUPPORTED_FIXTURE_PROMPTS["photosynthesis"],
        cache_path=None,
        enable_cache=False,
    )

    assert result["reason"] == "prompt_echo_replaced_with_local_derived_answer"
    assert result["confidence"] == 1.0
    assert result["diagnostics"]["tot"]["confidence"] == 1.0
    assert "confidence_adjustment_reason" not in result
    assert "confidence_adjustment_reason" not in result["diagnostics"]["tot"]

def test_honesty_guard_does_not_inject_lift_block():
    # Low-headroom/compact behavior stays outside the PR #646 lift contract:
    # the bounded SAFE-OUT replacement must not fabricate lift-block labels.
    for config in UNSUPPORTED_CONFIGS:
        result = _solve_unsupported(**config)
        for label in LIFT_LABELS:
            assert not result["final_answer"].strip().startswith(label), config
    rewrite = _tree_of_thought(
        "Rewrite this sentence to be shorter: 'We are currently in the process "
        "of conducting an evaluation of the proposal.'",
        cache_path=None,
        enable_cache=False,
    )
    for label in LIFT_LABELS:
        assert not rewrite["final_answer"].strip().startswith(label)


def test_classifier_flags_chained_and_single_artifacts():
    query = "Compare event sourcing versus CRUD for an audit ledger."
    cases = {
        f"Rephrase: {query}": "template_branch",
        f"Summarize: Decompose: {query}": "template_branch",
        f"Edge cases: {query}": "template_branch",
        f"To proceed, consider: {query}": "cot_template",
        query: "prompt_echo",
        query.upper(): "prompt_echo",
    }
    for answer, expected in cases.items():
        assert (
            solver_obs._classify_local_artifact(answer, query) == expected
        ), answer
    legit = "Use event sourcing only if replay and audit lineage justify it."
    assert solver_obs._classify_local_artifact(legit, query) is None
    assert solver_obs._classify_local_artifact(None, query) is None


def test_portable_local_path_never_surfaces_artifacts():
    prompts = (
        UNSUPPORTED_HIGH_HEADROOM,
        "Compare event sourcing versus CRUD for an audit-heavy fintech ledger.",
    )
    for seed in (7, 42, 99):
        for prompt in prompts:
            envelope = portable.PortableAlphaSolver(seed=seed).solve(prompt)
            answer = envelope.solution.strip()
            assert envelope.confidence == 0.20
            assert (
                envelope.safe_out_state["confidence_adjustment_reason"]
                == "confidence_adjusted_due_to_unsupported_local_synthesis"
            )
            assert "confidence adjusted" in envelope.safe_out_state["notes"]
            assert _normalized(answer) != _normalized(prompt), (seed, prompt)
            for prefix in BLOCKED_TEMPLATE_PREFIXES + ("Clarify and refine:",):
                assert not answer.lower().startswith(prefix.lower()), (
                    seed,
                    prompt,
                    answer,
                )


def test_portable_rendered_solution_and_shortlist_scrub_honesty_artifacts():
    envelope = portable.PortableAlphaSolver(seed=7).solve(UNSUPPORTED_HIGH_HEADROOM)
    rendered = envelope.to_llm_response()
    solution = _section(rendered, "SOLUTION", "\n\nCONFIDENCE:")
    shortlist = _section(rendered, "SHORTLIST", "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    for answer_like_section in (solution, shortlist):
        assert _normalized(UNSUPPORTED_HIGH_HEADROOM) not in _normalized(
            answer_like_section
        )
        for artifact in (
            "Rephrase:",
            "Decompose:",
            "Edge cases:",
            "Counterpoints:",
            "Summarize:",
            "To proceed, consider:",
            "Clarify and refine:",
        ):
            assert artifact not in answer_like_section


def test_portable_honesty_helper_is_standalone_and_explicit():
    query = "Plan a zero-downtime database migration."
    flagged = portable.portable_local_output_honesty(f"Rephrase: {query}", query)
    assert flagged["artifact_detected"] is True
    assert flagged["artifact_kind"] == "template_branch"
    assert flagged["bounded_answer"].startswith("SAFE-OUT:")

    echo = portable.portable_local_output_honesty(query, query)
    assert echo["artifact_detected"] is True
    assert echo["artifact_kind"] == "prompt_echo"

    fallback = portable.portable_local_output_honesty(
        f"Clarify and refine: {query}", query
    )
    assert fallback["artifact_detected"] is True
    assert fallback["artifact_kind"] == "template_branch"

    clean = portable.portable_local_output_honesty(
        "Run the migration in three phases behind a read-proxy.", query
    )
    assert clean["artifact_detected"] is False
    assert clean["bounded_answer"] is None


def test_portable_diagnostics_tot_matches_safeout_honesty_adjustment():
    envelope = portable.PortableAlphaSolver(seed=7).solve(UNSUPPORTED_HIGH_HEADROOM)
    diagnostics_tot = envelope.diagnostics.tot

    assert envelope.solution.startswith("SAFE-OUT:")
    assert diagnostics_tot["answer_kind"] == "local_unsupported_safeout"
    assert diagnostics_tot["synthesis_available"] is False
    assert diagnostics_tot["confidence"] == envelope.safe_out_state["confidence"]
    assert (
        diagnostics_tot["confidence_before_adjustment"]
        == envelope.safe_out_state["confidence_before_adjustment"]
    )
    assert (
        diagnostics_tot["confidence_adjustment_reason"]
        == envelope.safe_out_state["confidence_adjustment_reason"]
    )
    assert diagnostics_tot["artifact_kind"] in {"prompt_echo", "template_branch"}


def test_unsupported_local_safeout_is_not_lift_cosplay_for_anchored_prompt():
    prompt = (
        "For alpha_solver_portable.py after PR #652, decide whether "
        "ALPHA-SOLVER-SUBSTANTIVE-LIFT-CASE-ANCHOR-HARDENING-001 proves "
        "local deterministic synthesis can produce a case-anchored Substantive "
        "Lift answer. Include concrete file and PR anchors."
    )

    envelope = portable.PortableAlphaSolver(seed=7).solve(prompt)

    assert envelope.solution.startswith("SAFE-OUT:"), envelope.solution
    assert envelope.confidence == 0.20
    assert envelope.safe_out_state["answer_kind"] == "local_unsupported_safeout"
    assert envelope.safe_out_state["synthesis_available"] is False
    assert (
        envelope.safe_out_state["confidence_adjustment_reason"]
        == "confidence_adjusted_due_to_unsupported_local_synthesis"
    )
    assert envelope.diagnostics.tot["answer_kind"] == "local_unsupported_safeout"
    assert envelope.diagnostics.tot["synthesis_available"] is False
    assert _normalized(envelope.solution) != _normalized(prompt)
    for prefix in BLOCKED_TEMPLATE_PREFIXES + COT_ARTIFACT_PREFIXES:
        assert not envelope.solution.lower().startswith(prefix.lower())
    for label in LIFT_LABELS:
        assert not envelope.solution.startswith(label)
    assert "Recommendation:" not in envelope.solution
    assert "Fails if:" not in envelope.solution
    assert "Next:" not in envelope.solution

    generic_lift_block = "\n".join(
        [
            "Intent: Address the request with a thoughtful approach.",
            "Assumes: The team wants a robust solution for the situation.",
            "Tradeoff: Balance quality against speed for the best outcome.",
            "Recommendation: Use best practices and carefully consider options.",
            "Fails if: Various stakeholders disagree with the approach.",
            "Next: Consider the available choices and decide how to proceed.",
        ]
    )
    lift_check = portable.check_substantive_lift(generic_lift_block, prompt=prompt)

    assert lift_check["ok"] is False
    assert lift_check["unanchored_lift"] is True
    assert lift_check["weak_anchor_distribution"] is True
    assert lift_check["filler_flags"]
    assert lift_check["weak_next_action"] is True
