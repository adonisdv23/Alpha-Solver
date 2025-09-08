"""Deterministic benchmarks for reasoning strategies."""

from __future__ import annotations

import csv
import json
import os
import time
from typing import Dict, List

from alpha.reasoning.cot import run_cot
from alpha.reasoning.tot import TreeOfThoughtSolver
from alpha.router import ProgressiveRouter

PROMPTS = [
    "What is 2+2?",
    "Name three colors.",
]


def _bench() -> List[Dict[str, object]]:
    results: List[Dict[str, object]] = []
    for prompt in PROMPTS:
        # CoT
        start = time.time()
        cot = run_cot(prompt, seed=42, max_steps=2)
        elapsed = int((time.time() - start) * 1000)
        results.append(
            {
                "prompt": prompt,
                "method": "cot",
                "explored_nodes": 0,
                "top_score": cot.get("confidence", 0.0),
                "elapsed_ms": elapsed,
                "route": "cot",
            }
        )

        # ToT single
        solver = TreeOfThoughtSolver(seed=42)
        start = time.time()
        tot_single = solver.solve(prompt)
        elapsed = int((time.time() - start) * 1000)
        results.append(
            {
                "prompt": prompt,
                "method": "tot_single",
                "explored_nodes": tot_single["explored_nodes"],
                "top_score": tot_single["confidence"],
                "elapsed_ms": elapsed,
                "route": "tot",
            }
        )

        # ToT multi
        solver = TreeOfThoughtSolver(seed=42, multi_branch=True, max_width=2, max_nodes=10)
        start = time.time()
        tot_multi = solver.solve(prompt)
        elapsed = int((time.time() - start) * 1000)
        results.append(
            {
                "prompt": prompt,
                "method": "tot_multi",
                "explored_nodes": tot_multi["explored_nodes"],
                "top_score": tot_multi["confidence"],
                "elapsed_ms": elapsed,
                "route": "tot",
            }
        )

        # ToT + Router
        solver = TreeOfThoughtSolver(seed=42, multi_branch=True, max_width=2, max_nodes=10)
        router = ProgressiveRouter()
        start = time.time()
        tot_router = solver.solve(prompt, router=router)
        route = router.stage
        elapsed = int((time.time() - start) * 1000)
        results.append(
            {
                "prompt": prompt,
                "method": "tot_router",
                "explored_nodes": tot_router["explored_nodes"],
                "top_score": tot_router["confidence"],
                "elapsed_ms": elapsed,
                "route": route,
            }
        )
    return results


def main() -> None:
    rows = _bench()
    out_dir = os.path.join(os.path.dirname(__file__), "..", "bench_out")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "bench.csv")
    json_path = os.path.join(out_dir, "bench.json")
    with open(csv_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    with open(json_path, "w") as fh:
        json.dump(rows, fh, indent=2)


if __name__ == "__main__":
    main()
