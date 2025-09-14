import time
import pytest

from service.budget.simulator import load_cost_models, simulate


@pytest.fixture
def sample_items():
    return [
        {"id": "a", "prompt_tokens": 100, "completion_tokens": 50, "latency_ms": 100.0},
        {"id": "b", "prompt_tokens": 200, "completion_tokens": 100, "latency_ms": 200.0},
    ]


def test_load_cost_models():
    models = load_cost_models()
    assert models["providers"]["openai"]["gpt-4o"]["input_price_per_1k"] == 5.0


def test_deterministic_costs_within_tolerance(sample_items):
    models = load_cost_models()
    sim1 = simulate(sample_items, models, provider="openai", model="gpt-4o-mini")
    sim2 = simulate(sample_items, models, provider="openai", model="gpt-4o-mini")
    assert sim1["totals"]["cost_usd"] == pytest.approx(sim2["totals"]["cost_usd"], rel=0.001)


def test_totals_and_tokens(sample_items):
    models = load_cost_models()
    sim = simulate(sample_items, models, provider="openai", model="gpt-4o")
    assert sim["totals"]["tokens"] == sum(
        i["prompt_tokens"] + i["completion_tokens"] for i in sample_items
    )
    assert sim["totals"]["latency_ms"] == sum(i["latency_ms"] for i in sample_items)
    assert len(sim["items"]) == len(sample_items)
    for item, original in zip(sim["items"], sample_items):
        assert item["tokens"] == original["prompt_tokens"] + original["completion_tokens"]


def test_per_item_route_explain_shape(sample_items):
    models = load_cost_models()
    sim = simulate(sample_items, models, provider="openai", model="gpt-4o")
    for item in sim["items"]:
        rex = item["route_explain"]
        assert rex["decision"] == "simulate"
        assert set(rex) == {"decision", "cost_usd", "tokens", "latency_ms"}


def test_p95_under_2s_for_200_items():
    models = load_cost_models()
    items = [
        {"id": str(i), "prompt_tokens": 100, "completion_tokens": 100, "latency_ms": 50.0}
        for i in range(200)
    ]
    start = time.perf_counter()
    simulate(items, models, provider="openai", model="gpt-4o")
    duration = time.perf_counter() - start
    assert duration < 2.0
