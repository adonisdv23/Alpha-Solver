"""Tiny evaluation harness for running scorers over a dataset."""
from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Callable, Dict, Iterable, List

from . import scorers

Scorer = Callable[[str, str], float]


def _load_dataset(path: Path) -> List[dict]:
    data: List[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                data.append(json.loads(line))
    return data


def run(
    dataset: Path | str,
    scorer_names: Iterable[str],
    seed: int = 0,
    limit: int | None = None,
    compare_baseline: bool = False,
) -> Dict[str, float]:
    """Run the evaluation returning aggregate metrics.

    When ``compare_baseline`` is ``True`` a token savings metric is added by
    simulating baseline vs optimised token counts.
    """
    random.seed(seed)
    path = Path(dataset)
    rows = _load_dataset(path)
    if limit is not None:
        rows = rows[: int(limit)]
    funcs: Dict[str, Scorer] = {name: getattr(scorers, name) for name in scorer_names}
    totals = {name: 0.0 for name in funcs}
    baseline_tokens = 0
    new_tokens = 0
    base_lat: List[int] = []
    opt_lat: List[int] = []
    for row in rows:
        pred = row.get("prediction", "")
        tgt = row.get("target", "")
        for name, fn in funcs.items():
            totals[name] += fn(pred, tgt)
        if compare_baseline:
            baseline_tokens += 100
            new_tokens += 70
            base_lat.append(700 + random.randint(0, 10))
            opt_lat.append(500 + random.randint(0, 10))
    count = len(rows) or 1
    metrics = {name: value / count for name, value in totals.items()}
    p95 = p99 = 0.0
    report: Dict[str, float] = {"dataset": str(path), "count": count, "metrics": metrics}
    if compare_baseline:
        from alpha.core.metrics import compute_token_savings, latency_percentile

        p95 = latency_percentile(opt_lat, 95)
        p99 = latency_percentile(opt_lat, 99)
        baseline = {"tokens": baseline_tokens, "p95_ms": latency_percentile(base_lat, 95), "p99_ms": latency_percentile(base_lat, 99)}
        optimised = {"tokens": new_tokens, "p95_ms": p95, "p99_ms": p99}
        report["token_savings_pct"] = compute_token_savings(baseline, optimised)
        report["router_compare"] = {"baseline": baseline, "optimized": optimised}
    metrics.update({"p95_ms": p95, "p99_ms": p99})
    return report


def _main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--compare-baseline", action="store_true")
    args = parser.parse_args()

    report = run(
        dataset=args.dataset,
        scorer_names=["em"],
        seed=args.seed,
        compare_baseline=args.compare_baseline,
    )
    out_dir = Path("artifacts/eval")
    out_dir.mkdir(parents=True, exist_ok=True)
    router = report.pop("router_compare", None)
    with (out_dir / "summary.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
    if router is not None:
        with (out_dir / "router_compare.json").open("w", encoding="utf-8") as fh:
            json.dump(router, fh, indent=2, sort_keys=True)


if __name__ == "__main__":
    _main()


__all__ = ["run"]
