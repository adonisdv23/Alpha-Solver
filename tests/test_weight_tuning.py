from __future__ import annotations

from service.tuning.weight_harness import tune
from service.tuning.weights_normalize import normalize, freeze


def _make_dataset(n: int = 50):
    scenarios = []
    for i in range(n):
        plans = [
            {
                "id": "a",
                "factors": {"good": 0.7 + (i % 3) * 0.01, "bad": 0.0},
                "label": True,
            },
            {
                "id": "b",
                "factors": {"good": 0.6 + (i % 3) * 0.01, "bad": 0.4},
                "label": False,
            },
        ]
        scenarios.append({"id": str(i), "plans": plans})
    return scenarios


def test_harness_improves_accuracy_and_normalises():
    scenarios = _make_dataset()
    default = {"good": 0.5, "bad": 0.5}
    result = tune(scenarios, default, seed=123, samples=200)
    assert result["after"]["accuracy"] - result["before"]["accuracy"] >= 0.05
    weights = result["weights"]
    assert abs(sum(weights.values()) - 1.0) < 1e-6
    assert all(v >= 0 for v in weights.values())
    assert list(weights.keys()) == sorted(weights.keys())


def test_determinism_same_seed_same_result():
    scenarios = _make_dataset()
    default = {"good": 0.5, "bad": 0.5}
    r1 = tune(scenarios, default, seed=42, samples=100)
    r2 = tune(scenarios, default, seed=42, samples=100)
    assert r1 == r2


def test_normalize_invariants_and_freeze():
    raw = {"b": float("nan"), "a": -1.0, "c": float("inf")}
    norm = normalize(raw)
    assert abs(sum(norm.values()) - 1.0) < 1e-6
    assert all(v >= 0 for v in norm.values())
    assert list(norm.keys()) == sorted(norm.keys())
    frozen = freeze(raw)
    assert frozen == tuple(sorted(norm.items()))


def test_no_gain_path_returns_flag():
    # Dataset where default weights already optimal
    scenarios = []
    for i in range(10):
        plans = [
            {"id": "a", "factors": {"good": 1.0}, "label": True},
            {"id": "b", "factors": {"good": 0.5}, "label": False},
        ]
        scenarios.append({"id": str(i), "plans": plans})
    default = {"good": 1.0}
    result = tune(scenarios, default, seed=0, samples=50)
    assert result["no_gain"] is True
