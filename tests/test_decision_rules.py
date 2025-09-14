import time

import pytest

from service.scoring.decision_rules import (
    load_weights,
    validate_weights,
    score_plan,
    rank_plans,
)


def test_load_and_validate_weights_ok():
    weights = load_weights("config/decision_rules.yaml")
    validate_weights(weights)


def test_validate_weights_rejects_bad_shape():
    bad = {"weights": {}, "norms": {}, "tiebreak": []}
    with pytest.raises(ValueError):
        validate_weights(bad)


def test_score_is_deterministic():
    weights = load_weights()
    plan = {
        "id": "p",
        "confidence": 0.5,
        "tool_first": True,
        "cost_tokens": 100,
        "steps": 1,
        "risk": 0.1,
        "latency_ms": 200,
    }
    scores = [score_plan(plan, weights)[0] for _ in range(5)]
    assert all(s == scores[0] for s in scores)


def test_rank_orders_expected_top1_on_sample():
    weights = load_weights()
    plans = [
        {
            "id": "plan_tool_confident",
            "confidence": 0.9,
            "tool_first": True,
            "cost_tokens": 100,
            "steps": 2,
            "risk": 0.1,
            "latency_ms": 100,
        },
        {
            "id": "plan_confident_no_tool",
            "confidence": 0.9,
            "tool_first": False,
            "cost_tokens": 50,
            "steps": 1,
            "risk": 0.1,
            "latency_ms": 100,
        },
        {
            "id": "plan_tool_low_conf",
            "confidence": 0.2,
            "tool_first": True,
            "cost_tokens": 50,
            "steps": 1,
            "risk": 0.1,
            "latency_ms": 100,
        },
    ]
    ranked = rank_plans(plans, weights)
    assert ranked[0]["id"] == "plan_tool_confident"


def test_ties_are_broken_deterministically():
    weights = load_weights()
    plan1 = {
        "id": "p1",
        "confidence": 0.9,
        "cost_tokens": 500,
        "tool_first": False,
        "risk": 0,
        "steps": 0,
        "latency_ms": 0,
    }
    plan2 = {
        "id": "p2",
        "confidence": 0.85,
        "tool_first": True,
        "risk": 0.21464285714285714,
        "cost_tokens": 0,
        "steps": 0,
        "latency_ms": 0,
    }
    plan3 = dict(plan2, id="p3")
    ranked = rank_plans([plan3, plan2, plan1], weights)
    ids = [p["id"] for p in ranked]
    assert ids == ["p1", "p2", "p3"]


def test_p95_ranking_under_50ms_for_50_plans():
    weights = load_weights()

    def make_plan(i: int) -> dict:
        return {
            "id": f"p{i}",
            "confidence": (i % 10) / 10,
            "cost_tokens": i * 10,
            "steps": i % 5,
            "risk": (i % 3) / 3,
            "tool_first": i % 2 == 0,
            "latency_ms": i * 5,
        }

    plans = [make_plan(i) for i in range(50)]
    durations = []
    for _ in range(20):
        start = time.monotonic()
        rank_plans(plans, weights)
        durations.append(time.monotonic() - start)
    durations.sort()
    idx = int(len(durations) * 0.95)
    if idx == len(durations):
        idx -= 1
    assert durations[idx] < 0.05


def test_explain_contains_expected_fields():
    weights = load_weights()
    plan = {
        "id": "p",
        "confidence": 0.5,
        "tool_first": True,
        "cost_tokens": 100,
        "steps": 1,
        "risk": 0.1,
        "latency_ms": 200,
    }
    ranked = rank_plans([plan], weights)
    expl = ranked[0]["_explain"]
    assert set(expl.keys()) == {"score", "components", "tiebreak_chain"}
    components = expl["components"]
    assert {"confidence", "tool_first", "cost_tokens", "steps", "risk", "latency_ms"} <= set(
        components.keys()
    )
    assert expl["tiebreak_chain"] == ["confidence", "latency_ms", "cost_tokens", "id"]
