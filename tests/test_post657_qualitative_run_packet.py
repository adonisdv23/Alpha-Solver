"""Tests for the post-#657 qualitative run packet prep artifacts.

These checks validate static docs, spec, and fixture shape only. They do not
execute a manual review, call providers, call hosted or local models, score,
rank, select winners, compare identities, or produce readiness evidence.
"""
from __future__ import annotations

import json
from pathlib import Path

from alpha.eval import operator_run_capture as orc

PACKET_PATH = Path(
    "tests/fixtures/operator_run_capture/post657_qualitative_case_packet.json"
)
RUNBOOK_PATH = Path("docs/evals/runbooks/POST657_QUALITATIVE_RUN_PACKET.md")
SPEC_PATH = Path(".specs/POST657-QUALITATIVE-RUN-PACKET-001.md")
INDEX_PATH = Path(".specs/INDEX.md")

REQUIRED_MOVES = ("Intent", "Assumes", "Tradeoff", "Recommendation", "Fails if", "Next")
ANCHOR_TERMS = (".md", ".py", ".json", ".specs/", "PR #", "Issue #")
FORBIDDEN_PACKET_KEYS = {
    "score",
    "scores",
    "rating",
    "ratings",
    "rank",
    "ranking",
    "winner",
    "benchmark",
    "readiness",
    "blind_label",
    "source_map",
    "identity_map",
    "ab_identity_key",
    "baseline_output",
    "routed_output",
    "expected_answer",
    "expected_answers",
}
FORBIDDEN_RUNBOOK_DIRECTIVES = (
    "score the",
    "rank the",
    "select a winner",
    "choose a winner",
    "compare identities",
    "a/b identity key",
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


def test_post657_case_packet_validates_under_existing_harness():
    packet = _packet()
    assert orc.validate_case_packet(packet) == []
    capture = orc.scaffold_capture(packet)
    assert orc.validate_capture(capture) == []


def test_packet_id_and_case_count_are_bounded():
    packet = _packet()
    assert packet["packet_id"] == "POST657-QUALITATIVE-RUN-PACKET-001"
    assert 4 <= len(packet["cases"]) <= 6


def test_cases_have_stable_non_empty_task_ids_and_prompts():
    cases = _packet()["cases"]
    task_ids = [case["task_id"] for case in cases]
    assert task_ids == [
        "post657-case-001-preflight-signal",
        "post657-case-002-safeout-lift-boundary",
        "post657-case-003-solution-envelope-capture",
        "post657-case-004-route-metadata-minimality",
        "post657-case-005-reviewer-instruction-boundary",
        "post657-case-006-next-fork-after-run",
    ]
    assert len(task_ids) == len(set(task_ids))
    for case in cases:
        assert case["task_id"].strip()
        assert case["prompt"].strip()


def test_each_prompt_requires_six_moves_and_repo_anchors():
    for case in _packet()["cases"]:
        prompt = case["prompt"]
        for move in REQUIRED_MOVES:
            assert move in prompt, case["task_id"]
        assert any(term in prompt for term in ANCHOR_TERMS), case["task_id"]


def test_packet_has_no_output_expected_answer_or_review_result_fields():
    keys = set(_walk_keys(_packet()))
    assert keys.isdisjoint(FORBIDDEN_PACKET_KEYS)


def test_runbook_contains_exact_command_sequence():
    text = RUNBOOK_PATH.read_text(encoding="utf-8")
    expected_commands = (
        "python scripts/operator_run_capture.py init \\\n  --case-packet tests/fixtures/operator_run_capture/post657_qualitative_case_packet.json \\\n  --out local/post657_qualitative_capture.json",
        "python scripts/operator_run_capture.py validate \\\n  --capture local/post657_qualitative_capture.json",
        "python scripts/operator_run_capture.py lift-preflight \\\n  --capture local/post657_qualitative_capture.json \\\n  --report-out local/post657_qualitative_lift_preflight_report.json",
        "python scripts/operator_run_capture.py validate \\\n  --capture local/post657_qualitative_capture.json \\\n  --for-export",
        "python scripts/operator_run_capture.py export \\\n  --capture local/post657_qualitative_capture.json \\\n  --out local/post657_qualitative_capture_packet.json",
    )
    cursor = 0
    for command in expected_commands:
        index = text.find(command, cursor)
        assert index != -1, command
        cursor = index + len(command)


def test_runbook_documents_manual_paste_and_preflight_boundaries():
    text = RUNBOOK_PATH.read_text(encoding="utf-8")
    required = (
        "baseline_output",
        "routed_output",
        "SOLUTION:",
        "route_metadata",
        "validation_status` to `captured`",
        "validation_status` to `excluded`",
        "structural_pass` means only",
        "structural_fail` means",
        "safe_out_not_applicable",
        "anchor_checks_vacuous",
        "not answer quality",
        "not scoring",
        "not a benchmark",
        "not readiness evidence",
        "not superiority evidence",
    )
    for phrase in required:
        assert phrase in text


def test_runbook_does_not_direct_scoring_ranking_winners_or_identity_comparison():
    text = RUNBOOK_PATH.read_text(encoding="utf-8").lower()
    normalized = " ".join(text.split())
    for phrase in FORBIDDEN_RUNBOOK_DIRECTIVES:
        assert phrase not in text
    assert "should not add score, rank, winner" in text
    assert "do not ask the operator or reviewer to score, rank, select winners" in normalized


def test_spec_is_indexed_and_names_static_scope():
    index = INDEX_PATH.read_text(encoding="utf-8")
    spec = SPEC_PATH.read_text(encoding="utf-8")
    assert SPEC_PATH.name in index
    assert "POST657-QUALITATIVE-RUN-PACKET-001" in index
    assert "No runtime behavior changes" in spec
    assert "No execution of the manual qualitative review" in spec
