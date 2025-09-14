import copy
from pathlib import Path

import yaml

from service.scoring.decision_rules import load_weights
from service.scoring import tuning


# Sample dataset with deterministic behaviour
LARGE_SAMPLE = [
    {
        "id": f"case{i}",
        "plans": [
            {"id": "a", "confidence": 1.0, "risk": 0.5, "label_is_winner": False},
            {"id": "b", "confidence": 0.6, "risk": 0.0, "label_is_winner": True},
        ],
    }
    for i in range(10)
]


def test_grid_points_count_and_bounds():
    bounds = {"a": [0.0, 1.0], "b": [0.0, 0.5]}
    pts = tuning.grid_points(bounds, 3)
    assert len(pts) == 9
    vals_a = sorted({p["a"] for p in pts})
    vals_b = sorted({p["b"] for p in pts})
    assert vals_a == [0.0, 0.5, 1.0]
    assert vals_b == [0.0, 0.25, 0.5]


def test_evaluate_computes_accuracy_and_margin():
    sample = [
        {
            "id": "c1",
            "plans": [
                {"id": "p1", "confidence": 1.0, "label_is_winner": True},
                {"id": "p2", "confidence": 0.0, "label_is_winner": False},
            ],
        },
        {
            "id": "c2",
            "plans": [
                {"id": "p1", "confidence": 0.8, "label_is_winner": False},
                {"id": "p2", "confidence": 0.9, "label_is_winner": True},
            ],
        },
    ]
    weights = load_weights("config/decision_rules.yaml")
    metrics = tuning.evaluate(weights, sample)
    assert metrics["top1_accuracy"] == 1.0
    assert metrics["mean_margin"] == 0.55


def test_tune_finds_better_than_default_on_sample_ge_10pct():
    config = yaml.safe_load(Path("config/tuning.yaml").read_text())
    config["runtime"]["max_evals"] = 100
    default = load_weights("config/decision_rules.yaml")
    baseline = tuning.evaluate(default, LARGE_SAMPLE)
    result = tuning.tune(LARGE_SAMPLE, config=config, default_weights=default)
    assert result["metrics"]["top1_accuracy"] - baseline["top1_accuracy"] >= 0.1


def test_save_best_yaml_and_is_reproducible(tmp_path):
    path = tmp_path / "best.yaml"
    weights = {"confidence": 1.1, "risk": 0.9}
    tuning.save_best_yaml(path, weights)
    first = path.read_text()
    tuning.save_best_yaml(path, weights)
    second = path.read_text()
    assert first == second
    data = yaml.safe_load(first)
    assert data["weights"] == weights


def test_to_route_explain_includes_deltas_and_evals():
    default = load_weights("config/decision_rules.yaml")
    result: tuning.TuningResult = {
        "best_weights": {"confidence": 1.1},
        "metrics": {"top1_accuracy": 0.0, "mean_margin": 0.0},
        "evals": 12,
        "route_explain": {},
    }
    explain = tuning.to_route_explain(result, default)
    assert explain["tuning"] == "grid"
    assert explain["evals"] == 12
    assert "confidence" in explain["delta"]


def test_runtime_limit_respected_and_deterministic():
    config = yaml.safe_load(Path("config/tuning.yaml").read_text())
    config["runtime"]["max_evals"] = 10
    default = load_weights("config/decision_rules.yaml")
    r1 = tuning.tune(LARGE_SAMPLE, config=config, default_weights=default)
    r2 = tuning.tune(LARGE_SAMPLE, config=config, default_weights=default)
    assert r1["evals"] <= 10
    assert r1 == r2
