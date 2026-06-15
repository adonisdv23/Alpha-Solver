"""Deterministic no-echo/substantive-generation gate helpers.

This module is intentionally local-only and text-only. It does not call models,
providers, credentials, external APIs, dashboards, or `/v1/solve`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

EXACT_PROMPT_ECHO = "exact_prompt_echo"
NEAR_ECHO = "near_echo"
PLACEHOLDER_STUB_CANNED = "placeholder_stub_canned_output"
SAFE_OUT_REFUSAL_CLARIFICATION = "safe_out_refusal_or_clarification"
SUBSTANTIVE_DERIVED_OUTPUT = "substantive_derived_output"

_WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")
_PLACEHOLDER_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bplaceholder\b",
        r"\bstub\b",
        r"\btodo\b",
        r"\btbd\b",
        r"\bn/?a\b",
        r"\blorem ipsum\b",
        r"\bcoming soon\b",
        r"\bwork in progress\b",
        r"\bnot implemented\b",
        r"\bfill (?:this|in) later\b",
        r"\bexample answer\b",
        r"\bgeneric answer\b",
        r"\blocal deterministic answer: break the request\b",
    )
)
_SAFE_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"^\s*SAFE-OUT\s*:",
        r"\bi (?:can'?t|cannot|won't|will not)\b.*\b(?:answer|help|comply|substantiate|verify)\b",
        r"\bneed (?:more|additional) (?:context|information)\b",
        r"\bplease (?:clarify|provide)\b",
        r"\bunsupported\b.*\b(?:request|fixture|context|local)\b",
    )
)


@dataclass(frozen=True)
class GateMetrics:
    normalized_overlap_ratio: float
    longest_copied_span_ratio: float
    novelty_ratio: float
    output_token_count: int
    required_answer_fields_present: bool
    placeholder_stub_phrase_detected: bool
    safe_refusal_detected: bool


@dataclass(frozen=True)
class GateResult:
    category: str
    passed: bool
    reason: str
    metrics: GateMetrics


def normalize_text(text: str) -> str:
    return " ".join(_tokens(text))


def _tokens(text: str) -> list[str]:
    return _WORD_RE.findall(text.lower())


def _overlap_ratio(prompt_tokens: Sequence[str], output_tokens: Sequence[str]) -> float:
    if not output_tokens:
        return 0.0
    prompt_set = set(prompt_tokens)
    return sum(1 for token in output_tokens if token in prompt_set) / len(output_tokens)


def _longest_copied_span(prompt_tokens: Sequence[str], output_tokens: Sequence[str]) -> int:
    if not prompt_tokens or not output_tokens:
        return 0
    best = 0
    previous = [0] * (len(output_tokens) + 1)
    for prompt_token in prompt_tokens:
        current = [0] * (len(output_tokens) + 1)
        for index, output_token in enumerate(output_tokens, start=1):
            if prompt_token == output_token:
                current[index] = previous[index - 1] + 1
                best = max(best, current[index])
        previous = current
    return best


def _contains_any(patterns: Iterable[re.Pattern[str]], text: str) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def classify_output(
    prompt: str,
    output: str,
    *,
    required_answer_fields: Sequence[str] = (),
    min_derived_tokens: int = 16,
    near_echo_overlap_threshold: float = 0.80,
    near_echo_span_threshold: float = 0.55,
    min_novelty_ratio: float = 0.35,
) -> GateResult:
    """Classify an output against a prompt using deterministic text heuristics."""

    prompt_tokens = _tokens(prompt)
    output_tokens = _tokens(output)
    normalized_prompt = " ".join(prompt_tokens)
    normalized_output = " ".join(output_tokens)
    overlap = _overlap_ratio(prompt_tokens, output_tokens)
    span = _longest_copied_span(prompt_tokens, output_tokens)
    span_ratio = span / max(1, len(output_tokens))
    novelty = 1.0 - overlap if output_tokens else 0.0
    required_present = all(field.lower() in output.lower() for field in required_answer_fields)
    placeholder = _contains_any(_PLACEHOLDER_PATTERNS, output)
    safe = _contains_any(_SAFE_PATTERNS, output)

    metrics = GateMetrics(
        normalized_overlap_ratio=round(overlap, 4),
        longest_copied_span_ratio=round(span_ratio, 4),
        novelty_ratio=round(novelty, 4),
        output_token_count=len(output_tokens),
        required_answer_fields_present=required_present,
        placeholder_stub_phrase_detected=placeholder,
        safe_refusal_detected=safe,
    )

    if normalized_output and normalized_output == normalized_prompt:
        return GateResult(EXACT_PROMPT_ECHO, False, "normalized output exactly equals normalized prompt", metrics)
    if overlap >= near_echo_overlap_threshold or span_ratio >= near_echo_span_threshold:
        return GateResult(NEAR_ECHO, False, "output copies too much prompt text", metrics)
    if placeholder:
        return GateResult(PLACEHOLDER_STUB_CANNED, False, "placeholder, stub, or canned phrase detected", metrics)
    if safe:
        return GateResult(SAFE_OUT_REFUSAL_CLARIFICATION, True, "bounded safe-out/refusal/clarification detected", metrics)
    if len(output_tokens) < min_derived_tokens:
        return GateResult(PLACEHOLDER_STUB_CANNED, False, "output is too short for a derived answer", metrics)
    if novelty < min_novelty_ratio:
        return GateResult(NEAR_ECHO, False, "output has insufficient novelty from prompt", metrics)
    if not required_present:
        return GateResult(PLACEHOLDER_STUB_CANNED, False, "required answer field is missing", metrics)
    return GateResult(SUBSTANTIVE_DERIVED_OUTPUT, True, "output is bounded, novel, and field-complete", metrics)


def evaluate_fixture(fixture: Mapping[str, Any]) -> dict[str, Any]:
    result = classify_output(
        str(fixture["prompt"]),
        str(fixture["output"]),
        required_answer_fields=tuple(fixture.get("required_answer_fields", ())),
    )
    payload = asdict(result)
    payload["id"] = fixture.get("id")
    payload["expected_category"] = fixture.get("expected_category")
    payload["matched_expected_category"] = result.category == fixture.get("expected_category")
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic no-echo/substantive fixture gate.")
    parser.add_argument("fixtures", type=Path)
    args = parser.parse_args(argv)
    fixtures = json.loads(args.fixtures.read_text(encoding="utf-8"))
    results = [evaluate_fixture(fixture) for fixture in fixtures]
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if all(result["matched_expected_category"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
