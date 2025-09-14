"""Simple deterministic weight tuning for RES-03 decision rules.

This module provides a tiny grid search utility for tuning the weight
parameters used by :mod:`service.scoring.decision_rules`.  The search is
fully deterministic and does not rely on any third party optimisation
libraries.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import random
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, TypedDict

import yaml

from .decision_rules import rank_plans


class TuningResult(TypedDict):
    """Result from :func:`tune`.

    Attributes
    ----------
    best_weights:
        Mapping of weight name to tuned value.
    metrics:
        Dictionary with ``top1_accuracy`` and ``mean_margin``.
    evals:
        Number of weight combinations evaluated.
    route_explain:
        Small summary suitable for routing telemetry.
    """

    best_weights: Dict[str, float]
    metrics: Dict[str, float]
    evals: int
    route_explain: Dict[str, Any]


# ---------------------------------------------------------------------------
# Loading utilities
# ---------------------------------------------------------------------------

def load_labeled_sample(path: str) -> List[Dict[str, Any]]:
    """Load a labelled sample from ``path``.

    ``path`` may point to a JSON or JSON Lines file.  Each entry is expected
    to contain an ``id`` and a list of ``plans`` where each plan includes a
    boolean ``label_is_winner``.
    """
    p = Path(path)
    with p.open("r", encoding="utf-8") as fh:
        if p.suffix == ".jsonl":
            data = [json.loads(line) for line in fh if line.strip()]
        else:
            data = json.load(fh)

    cleaned: List[Dict[str, Any]] = []
    for case in data:
        new_case = dict(case)
        new_case.pop("pii_raw", None)
        plans = []
        for plan in new_case.get("plans", []):
            new_plan = dict(plan)
            new_plan.pop("pii_raw", None)
            plans.append(new_plan)
        new_case["plans"] = plans
        cleaned.append(new_case)
    return cleaned


# ---------------------------------------------------------------------------
# Search space helpers
# ---------------------------------------------------------------------------

def _linspace(start: float, stop: float, steps: int) -> List[float]:
    if steps < 2:
        raise ValueError("steps must be >=2")
    step = (stop - start) / (steps - 1)
    return [start + i * step for i in range(steps)]


def grid_points(bounds: Dict[str, List[float]], steps_per_weight: int) -> List[Dict[str, float]]:
    """Return all combinations within ``bounds``.

    The order of points is deterministic and follows the order of keys in
    ``bounds``.
    """
    keys = list(bounds.keys())
    value_lists: List[List[float]] = [
        _linspace(v[0], v[1], steps_per_weight) for v in bounds.values()
    ]

    points: List[Dict[str, float]] = []
    # Cartesian product implemented iteratively for clarity and determinism
    def _product(idx: int, current: Dict[str, float]) -> None:
        if idx == len(keys):
            points.append(dict(current))
            return
        key = keys[idx]
        for val in value_lists[idx]:
            current[key] = val
            _product(idx + 1, current)
    _product(0, {})
    return points


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate(weights: Dict[str, Any], labeled: List[Dict[str, Any]]) -> Dict[str, float]:
    """Evaluate ``weights`` against ``labeled`` sample.

    ``weights`` is a full configuration dictionary compatible with
    :func:`rank_plans`.
    """
    if not labeled:
        return {"top1_accuracy": 0.0, "mean_margin": 0.0}

    correct = 0
    margins: List[float] = []
    for case in labeled:
        plans = [dict(p) for p in case.get("plans", [])]
        ranked = rank_plans(plans, weights)
        if not ranked:
            continue
        top1 = ranked[0]
        if top1.get("label_is_winner"):
            correct += 1
        if len(ranked) > 1:
            margin = ranked[0]["_score"] - ranked[1]["_score"]
        else:
            margin = ranked[0]["_score"]
        margins.append(margin)

    accuracy = correct / len(labeled)
    mean_margin = sum(margins) / len(margins) if margins else 0.0
    return {"top1_accuracy": accuracy, "mean_margin": mean_margin}


# ---------------------------------------------------------------------------
# Tuning
# ---------------------------------------------------------------------------

def _apply_jitter(point: Dict[str, float], pct: float, rng: random.Random) -> Dict[str, float]:
    if pct <= 0:
        return dict(point)
    return {k: v * (1 + rng.uniform(-pct, pct)) for k, v in point.items()}


def tune(
    labeled: List[Dict[str, Any]], *, config: Dict[str, Any], default_weights: Dict[str, Any]
) -> TuningResult:
    """Grid search for best weights.

    The best combination is chosen by the primary metric and then the
    secondary metric as defined in ``config``.
    """
    search = config.get("search", {})
    bounds = config.get("bounds", {})
    metrics_cfg = config.get("metrics", {})
    runtime = config.get("runtime", {})

    steps = int(search.get("steps_per_weight", 2))
    jitter = float(search.get("jitter_pct", 0.0))
    max_evals = int(runtime.get("max_evals", 0))
    seed = int(runtime.get("seed", 0))
    primary = metrics_cfg.get("primary", "top1_accuracy")
    secondary = metrics_cfg.get("secondary", "mean_margin")

    rng = random.Random(seed)
    points = grid_points(bounds, steps)

    best_point: Dict[str, float] | None = None
    best_metrics: Dict[str, float] | None = None
    evals = 0

    for point in points:
        if max_evals and evals >= max_evals:
            break
        candidate_weights = _apply_jitter(point, jitter, rng)
        cfg = yaml.safe_load(yaml.safe_dump(default_weights))
        cfg["weights"].update(candidate_weights)
        metrics = evaluate(cfg, labeled)
        evals += 1

        if best_metrics is None:
            best_point, best_metrics = candidate_weights, metrics
            continue
        if metrics[primary] > best_metrics[primary] or (
            metrics[primary] == best_metrics[primary]
            and metrics[secondary] > best_metrics[secondary]
        ):
            best_point, best_metrics = candidate_weights, metrics

    result: TuningResult = {
        "best_weights": best_point or {},
        "metrics": best_metrics or {"top1_accuracy": 0.0, "mean_margin": 0.0},
        "evals": evals,
        "route_explain": {},
    }
    result["route_explain"] = to_route_explain(result, default_weights)
    return result


# ---------------------------------------------------------------------------
# Saving helpers
# ---------------------------------------------------------------------------

def save_best_yaml(path: str, best_weights: Dict[str, float]) -> None:
    """Persist ``best_weights`` to ``path`` in YAML format."""
    data = {"weights": best_weights}
    with open(Path(path), "w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, sort_keys=True)


# ---------------------------------------------------------------------------
# Route explain helpers
# ---------------------------------------------------------------------------

def to_route_explain(result: TuningResult, default_weights: Dict[str, Any]) -> Dict[str, Any]:
    """Create a small explanation dictionary for routing telemetry."""
    deltas: Dict[str, float] = {}
    base = default_weights.get("weights", {})
    tuned = result.get("best_weights", {})
    for key, base_val in base.items():
        tuned_val = tuned.get(key, base_val)
        deltas[key] = tuned_val - float(base_val)
    return {"tuning": "grid", "evals": result.get("evals", 0), "delta": deltas}

