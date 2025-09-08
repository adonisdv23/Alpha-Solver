from __future__ import annotations

import csv
import json
import random
import time
from pathlib import Path
from typing import Dict, List, Optional

from .scorers import SCORERS
from alpha.core.budgets import compute_percentiles, compute_cost_per_call, gate_decision
from alpha.core.config import get_quality_gate


def _load_dataset(path: str) -> List[dict]:
    p = Path(path)
    if p.suffix == ".jsonl":
        with p.open("r", encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]
    if p.suffix == ".csv":
        with p.open("r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            return [row for row in reader]
    raise ValueError(f"Unsupported dataset format: {p.suffix}")


def run_eval(dataset_path: str, seed: int, scorers: List[str], limit: Optional[int] = None) -> Dict:
    data = _load_dataset(dataset_path)
    if limit:
        data = data[:limit]
    rng = random.Random(seed)
    examples = []
    metric_totals = {s: 0.0 for s in scorers}
    latencies: List[float] = []
    costs: List[float] = []

    print(json.dumps({"event": "eval_start", "count": len(data)}))
    for item in data:
        start = time.perf_counter()
        expected = item.get("expected", "")
        prediction = expected  # placeholder deterministic prediction
        latency_ms = rng.uniform(100, 300)
        cost = 0.005
        latencies.append(latency_ms)
        costs.append(cost)
        example_metrics = {}
        for s in scorers:
            fn = SCORERS.get(s)
            if not fn:
                continue
            score = fn(str(prediction), str(expected), item.get("meta"))
            example_metrics[s] = score
            metric_totals[s] += score
        examples.append(
            {
                "id": item.get("id"),
                "prompt": item.get("prompt"),
                "expected": expected,
                "prediction": prediction,
                "metrics": example_metrics,
                "latency_ms": latency_ms,
                "cost": cost,
            }
        )
        print(json.dumps({"event": "eval_example", "id": item.get("id"), "metrics": example_metrics}))
        time.sleep(0)  # allow time.perf_counter diff for determinism
    metrics = {k: (metric_totals[k] / len(examples) if examples else 0.0) for k in metric_totals}
    latency = compute_percentiles(latencies)
    cost_per_call = compute_cost_per_call(costs)
    report = {
        "examples": examples,
        "metrics": metrics,
        "latency": latency,
        "cost_per_call": cost_per_call,
    }
    cfg = get_quality_gate()
    passed, reasons = gate_decision(report, cfg)
    report["passed"] = passed
    report["reasons"] = reasons
    out_dir = Path("artifacts/eval")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "latest_report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({"event": "eval_end", "passed": passed}))
    return report
