"""Tests for PR646 substantive-lift manual eval prep materials.

These checks validate local prep artifacts only. They perform no provider calls,
no hosted or local model calls, no network access, no scoring, no ranking, no
blinding, and no unblinding.
"""
from __future__ import annotations

import json
from pathlib import Path

from alpha.eval import operator_run_capture as orc

PACKET_PATH = Path(
    "tests/fixtures/operator_run_capture/pr646_substantive_lift_case_packet.json"
)
RUNBOOK_PATH = Path("docs/evals/runbooks/PR646_SUBSTANTIVE_LIFT_MANUAL_EVAL.md")
SPEC_PATH = Path(".specs/PR646-SUBSTANTIVE-LIFT-MANUAL-EVAL-PREP-001.md")
INDEX_PATH = Path(".specs/INDEX.md")

FORBIDDEN_FIELD_NAMES = {
    "score",
    "scores",
    "rank",
    "ranking",
    "winner",
    "blind_label",
    "source_map",
    "identity_map",
    "readiness",
    "benchmark",
    "superiority",
}

REPO_GROUNDING_TERMS = (
    "alpha_solver_portable.py",
    "operator_run_capture.py",
    "docs/OPERATOR_RUN_CAPTURE.md",
    "tests/test_alpha_substantive_lift_contract.py",
    "tests/test_alpha_local_runtime_honesty.py",
    ".specs/",
    "PR #646",
    "PR #647",
    "PR #648",
    "/v1/solve",
)

REQUIRED_LIFT_MOVES = (
    "intent diagnosis",
    "hidden assumption",
    "dominant tradeoff",
    "committed recommendation",
    "failure condition",
    "same-day next action",
)

REQUIRED_SOURCE_CONTEXT_FILES = (
    "alpha_solver_portable.py",
    ".specs/ALPHA-SOLVER-SUBSTANTIVE-LIFT-ANSWER-CONTRACT-001.md",
    ".specs/ALPHA-SOLVER-TOT-ECHO-HONESTY-HOTFIX-001.md",
    ".specs/ALPHA-SOLVER-SAFEOUT-CONFIDENCE-HONESTY-001.md",
    "alpha/eval/operator_run_capture.py",
    "docs/OPERATOR_RUN_CAPTURE.md",
    "tests/fixtures/operator_run_capture/pr646_substantive_lift_case_packet.json",
)


def _packet() -> dict:
    return json.loads(PACKET_PATH.read_text(encoding="utf-8"))


def _walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def test_pr646_case_packet_validates_under_existing_harness():
    assert orc.validate_case_packet(_packet()) == []
    capture = orc.scaffold_capture(_packet())
    assert orc.validate_capture(capture) == []


def test_packet_has_at_least_five_high_headroom_cases():
    cases = _packet()["cases"]
    assert len(cases) >= 5
    for case in cases:
        prompt = case["prompt"].lower()
        assert len(case["prompt"]) > 180
        for move in REQUIRED_LIFT_MOVES:
            assert move in prompt


def test_task_ids_are_unique_and_stable():
    task_ids = [case["task_id"] for case in _packet()["cases"]]
    assert len(task_ids) == len(set(task_ids))
    assert task_ids == [
        "pr646-case-001-next-bottleneck",
        "pr646-case-002-runtime-vs-manual",
        "pr646-case-003-route-persona-causality",
        "pr646-case-004-local-tot-honesty-boundary",
        "pr646-case-005-manual-eval-no-scoring",
        "pr646-case-006-implementation-lane-selection",
    ]


def test_prompts_are_repo_grounded_and_non_empty():
    for case in _packet()["cases"]:
        prompt = case["prompt"]
        assert prompt.strip()
        assert any(term in prompt for term in REPO_GROUNDING_TERMS), prompt
        assert "Alpha Solver" in prompt or "alpha" in prompt.lower()


def test_packet_fields_do_not_include_forbidden_scoring_or_blinding_keys():
    keys = set(_walk_keys(_packet()))
    assert keys.isdisjoint(FORBIDDEN_FIELD_NAMES)


def test_runbook_contains_required_boundary_statements():
    text = RUNBOOK_PATH.read_text(encoding="utf-8")
    required = (
        "Capture only",
        "No provider calls",
        "hosted model calls",
        "local model calls",
        "network calls",
        "Do not score",
        "rank",
        "assign a winner",
        "blind",
        "unblind",
        "blind_label",
        "source_map",
        "identity_map",
        "benchmark results",
        "readiness",
        "Alpha superiority",
        "/v1/solve",
    )
    for phrase in required:
        assert phrase in text


def test_runbook_references_existing_cli_flow_only():
    text = RUNBOOK_PATH.read_text(encoding="utf-8")
    assert "python scripts/operator_run_capture.py init" in text
    assert "python scripts/operator_run_capture.py validate" in text
    assert "python scripts/operator_run_capture.py export" in text
    assert "existing CLI only" in text
    assert "operator_run_capture.py" in text
    assert "score" not in text.lower().replace("do not score", "")


def test_runbook_requires_equal_source_context_for_baseline_and_alpha_threads():
    text = RUNBOOK_PATH.read_text(encoding="utf-8")
    normalized_text = " ".join(text.split())
    assert "same context to both the plain/baseline thread and the Alpha" in text
    assert "before asking any case-packet prompt" in text
    assert "provide the shared repo/source context from step 1" in normalized_text
    assert "provide the same shared repo/source context from step 1" in normalized_text
    assert "Record the context method in" in text
    assert "route_metadata" in text
    assert "paste the relevant excerpts" in text
    assert "equivalent repo-aware context source" in text


def test_runbook_names_required_source_context_files():
    text = RUNBOOK_PATH.read_text(encoding="utf-8")
    for source_file in REQUIRED_SOURCE_CONTEXT_FILES:
        assert source_file in text


def test_spec_is_indexed():
    index = INDEX_PATH.read_text(encoding="utf-8")
    spec_name = SPEC_PATH.name
    assert spec_name in index
    assert "PR646-SUBSTANTIVE-LIFT-MANUAL-EVAL-PREP-001" in index
