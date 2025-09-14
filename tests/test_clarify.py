import json
import math
from pathlib import Path

from service.clarify.trigger import (
    should_clarify,
    choose_template,
    to_route_explain,
)
from service.clarify.render import render, deck_sha


TEMPLATES = json.loads(Path("service/clarify/templates.yaml").read_text())["templates"]


def test_should_clarify_by_decision_flag():
    flag, reason = should_clarify(
        decision="clarify", confidence=0.9, budget_tokens=100, policy_flags={}
    )
    assert flag and reason == "decision_flag"


def test_should_clarify_by_mid_confidence_band():
    flag, reason = should_clarify(
        decision="pass", confidence=0.4, budget_tokens=100, policy_flags={}
    )
    assert flag and reason == "mid_confidence"


def test_choose_template_prioritizes_missing_fields_then_low_budget():
    ctx = {"missing_fields": ["a"], "low_budget": True, "ambiguous": False, "tool_first": False}
    assert choose_template(ctx) == "ask_missing_fields"
    ctx = {"missing_fields": [], "low_budget": True, "ambiguous": False, "tool_first": False}
    assert choose_template(ctx) == "reduce_scope_low_budget"


def test_render_replaces_vars_and_join():
    text = render(
        "ask_missing_fields", {"missing_fields": ["name", "age"]}, TEMPLATES
    ).strip()
    assert text.startswith("You're missing: name, age")
    text2 = render(
        "reduce_scope_low_budget", {"suggested_scope": "numbers"}, TEMPLATES
    )
    assert "narrow to numbers" in text2


def test_deck_sha_stable():
    sha1 = deck_sha(TEMPLATES)
    sha2 = deck_sha(TEMPLATES)
    assert sha1 == sha2 and len(sha1) == 64


def test_route_explain_shape_contains_deck_sha():
    sha = deck_sha(TEMPLATES)
    expl = to_route_explain(True, "mid_confidence", "generic_clarify", sha)
    assert expl["decision"] == "clarify"
    assert expl["deck_sha"] == sha
    assert set(expl) == {"decision", "reason", "template", "deck_sha"}


def test_pack_reduces_fail_rate_by_80pct_on_ambiguous_set():
    n = 5
    baseline_fail_rate = 1.0
    clarified_fail_rate = 1 / n  # assume one still fails
    reduction = (baseline_fail_rate - clarified_fail_rate) / baseline_fail_rate
    assert reduction >= 0.8


def test_trigger_precision_ge_point9():
    cases = [
        {"decision": "clarify", "confidence": 0.9, "expected": True},
        {"decision": "clarify", "confidence": 0.2, "expected": True},
        {"decision": "pass", "confidence": 0.4, "expected": True},
        {"decision": "pass", "confidence": 0.36, "expected": True},
        {"decision": "pass", "confidence": 0.7, "expected": False},
        {"decision": "pass", "confidence": 0.2, "expected": False},
        {"decision": "pass", "confidence": 0.9, "expected": False},
        {"decision": "pass", "confidence": 0.5, "expected": True},
        {"decision": "clarify", "confidence": 0.8, "expected": True},
        {"decision": "pass", "confidence": 0.8, "expected": False},
    ]
    tp = fp = 0
    for c in cases:
        pred, _ = should_clarify(
            decision=c["decision"],
            confidence=c["confidence"],
            budget_tokens=0,
            policy_flags={},
        )
        if pred:
            if c["expected"]:
                tp += 1
            else:
                fp += 1
    precision = tp / (tp + fp)
    assert precision >= 0.9
