from __future__ import annotations

"""Light‑weight deterministic weight tuning harness.

This module provides a minimal search utility used in tests.  It loads a
labeled scenario set, evaluates candidate weight vectors and returns the best
normalised weights together with BEFORE/AFTER metrics.

The implementation intentionally avoids heavy dependencies so that it can run
quickly inside the unit test suite.  The search strategy is a simple random
search over the unit simplex with a deterministic seed.
"""

import json
from pathlib import Path
import random
from typing import Dict, Iterable, List, Tuple, Any

from .weights_normalize import normalize
from . import reporters


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_scenarios(path: str | Path) -> List[Dict[str, Any]]:
    """Load labelled scenarios from a JSON Lines file."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


# ---------------------------------------------------------------------------
# Scoring and evaluation
# ---------------------------------------------------------------------------


def _score_plan(plan: Dict[str, float], weights: Dict[str, float]) -> float:
    return sum(weights.get(k, 0.0) * plan.get(k, 0.0) for k in weights)


def evaluate(weights: Dict[str, float], scenarios: Iterable[Dict[str, Any]] ) -> Dict[str, Any]:
    """Evaluate *weights* against *scenarios*.

    ``scenarios`` is expected to contain a ``plans`` list.  Each plan must
    contain a mapping of numeric ``factors`` and a boolean ``label`` that marks
    the winning plan.
    """
    scenarios = list(scenarios)
    total = len(scenarios)
    if not total:
        return {"accuracy": 0.0, "confusion": {}}

    confusion: Dict[Tuple[str, str], int] = {}
    correct = 0
    for case in scenarios:
        plans = case.get("plans", [])
        scored = sorted(
            plans,
            key=lambda p: _score_plan(p.get("factors", {}), weights),
            reverse=True,
        )
        if not scored:
            continue
        predicted = scored[0]["id"]
        actual = next((p["id"] for p in plans if p.get("label")), None)
        confusion[(predicted, actual)] = confusion.get((predicted, actual), 0) + 1
        if predicted == actual:
            correct += 1
    accuracy = correct / total
    return {"accuracy": accuracy, "confusion": confusion}


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------


def tune(
    scenarios: List[Dict[str, Any]],
    default_weights: Dict[str, float],
    *,
    seed: int = 0,
    samples: int = 500,
) -> Dict[str, Any]:
    """Search for better weights.

    The search samples random weight vectors on the unit simplex.  The result
    dictionary contains ``weights`` (normalised), BEFORE/AFTER metrics and a
    ``no_gain`` flag which is ``True`` when the best candidate does not improve
    accuracy by at least five percentage points.
    """
    norm_default = normalize(default_weights)
    before = evaluate(norm_default, scenarios)
    factors = list(norm_default.keys())

    rng = random.Random(seed)
    best_weights = dict(norm_default)
    best_metrics = before

    for _ in range(int(samples)):
        candidate = {f: rng.random() for f in factors}
        candidate = normalize(candidate)
        metrics = evaluate(candidate, scenarios)
        if metrics["accuracy"] > best_metrics["accuracy"]:
            best_weights = candidate
            best_metrics = metrics

    improvement = best_metrics["accuracy"] - before["accuracy"]
    no_gain = improvement < 0.05
    final_weights = norm_default if no_gain else best_weights

    report = reporters.build_report(before, best_metrics, norm_default, final_weights)

    return {
        "weights": final_weights,
        "before": before,
        "after": best_metrics,
        "no_gain": no_gain,
        "report": report,
    }


# ---------------------------------------------------------------------------
# Command line interface
# ---------------------------------------------------------------------------


def main(argv: List[str] | None = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Tune decision weights")
    parser.add_argument("--scenarios", required=True, help="Path to scenarios JSONL")
    parser.add_argument("--out", required=True, help="Where to write best weights JSON")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--samples", type=int, default=500)
    args = parser.parse_args(argv)

    scenarios = load_scenarios(args.scenarios)
    default = {f: 1.0 / 3 for f in {"confidence", "risk", "latency"}}  # placeholder
    result = tune(scenarios, default, seed=args.seed, samples=args.samples)

    out_path = Path(args.out)
    out_path.write_text(json.dumps(result["weights"], indent=2))
    text = reporters.to_text(result["report"])
    print(text)


if __name__ == "__main__":  # pragma: no cover
    main()
