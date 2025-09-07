from __future__ import annotations

"""Deterministic benchmarks for reasoning modes."""

import csv
import json
import time
from pathlib import Path
from typing import List, Dict

from alpha.reasoning.tot import TreeOfThoughtSolver
from alpha.router import ProgressiveRouter
from alpha.reasoning.cot import guidance_score

PROMPTS = ["simple math", "edge case"]
MODES = ["cot", "tot_single", "tot_multi", "tot_router"]


def _run_tot(query: str, multi: bool, router: bool) -> Dict[str, object]:
    pr = ProgressiveRouter(["basic", "structured", "constrained"]) if router else None
    solver = TreeOfThoughtSolver(multi_branch=multi, router=pr)
    start = time.perf_counter()
    result = solver.solve(query)
    elapsed = int((time.perf_counter() - start) * 1000)
    return {
        "explored_nodes": result.get("explored_nodes", 0),
        "score": result.get("confidence", 0.0),
        "elapsed_ms": elapsed,
        "route": "tot" if not router else "tot_router",
    }


def run() -> Dict[str, Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for prompt in PROMPTS:
        for mode in MODES:
            if mode == "cot":
                start = time.perf_counter()
                score = guidance_score({"hint": prompt})
                elapsed = int((time.perf_counter() - start) * 1000)
                rows.append({
                    "prompt": prompt,
                    "mode": mode,
                    "explored_nodes": 0,
                    "score": score,
                    "elapsed_ms": elapsed,
                    "route": "cot",
                })
            elif mode == "tot_single":
                res = _run_tot(prompt, False, False)
                rows.append({"prompt": prompt, "mode": mode, **res})
            elif mode == "tot_multi":
                res = _run_tot(prompt, True, False)
                rows.append({"prompt": prompt, "mode": mode, **res})
            else:
                res = _run_tot(prompt, True, True)
                rows.append({"prompt": prompt, "mode": mode, **res})
    out = Path("bench_out")
    out.mkdir(exist_ok=True)
    csv_path = out / "bench.csv"
    json_path = out / "summary.json"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["prompt", "mode", "explored_nodes", "score", "elapsed_ms", "route"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    with json_path.open("w") as f:
        json.dump(rows, f, indent=2)
    return {row["mode"] + ":" + row["prompt"]: row for row in rows}


if __name__ == "__main__":
    run()

