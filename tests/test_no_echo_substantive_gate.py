import json
from pathlib import Path

from alpha.eval.no_echo_substantive_gate import (
    EXACT_PROMPT_ECHO,
    NEAR_ECHO,
    PLACEHOLDER_STUB_CANNED,
    SAFE_OUT_REFUSAL_CLARIFICATION,
    SUBSTANTIVE_DERIVED_OUTPUT,
    classify_output,
    evaluate_fixture,
)

FIXTURES = Path(__file__).parent / "fixtures" / "no_echo_substantive_gate_cases.json"


def test_fixture_categories_match_expected_outcomes():
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))

    results = [evaluate_fixture(fixture) for fixture in fixtures]

    assert all(result["matched_expected_category"] for result in results)
    assert {result["category"] for result in results} == {
        EXACT_PROMPT_ECHO,
        NEAR_ECHO,
        PLACEHOLDER_STUB_CANNED,
        SAFE_OUT_REFUSAL_CLARIFICATION,
        SUBSTANTIVE_DERIVED_OUTPUT,
    }


def test_substantive_output_requires_configured_answer_fields():
    result = classify_output(
        "Explain photosynthesis in two plain-language sentences.",
        "Plants use sunlight, water, and carbon dioxide to make sugars for energy while releasing oxygen into the air for other organisms.",
        required_answer_fields=("Answer:",),
    )

    assert result.category == PLACEHOLDER_STUB_CANNED
    assert result.passed is False
    assert result.metrics.required_answer_fields_present is False


def test_safeout_is_not_misclassified_as_placeholder_or_echo():
    result = classify_output(
        "Summarize an unavailable source without inventing facts.",
        "SAFE-OUT: I cannot verify an unavailable source. Please provide the text to summarize.",
    )

    assert result.category == SAFE_OUT_REFUSAL_CLARIFICATION
    assert result.passed is True
    assert result.metrics.safe_refusal_detected is True
