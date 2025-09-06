from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Callable, Iterable, Dict

import resource


def benchmark(
    fn: Callable[[str], None], queries: Iterable[str], out_dir: str | Path = "artifacts/benchmarks"
) -> Dict[str, float]:
    out_p = Path(out_dir)
    out_p.mkdir(parents=True, exist_ok=True)
    results = []
    for q in queries:
        start = time.perf_counter()
        fn(q)
        elapsed = time.perf_counter() - start
        mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
        results.append({"query": q, "elapsed": elapsed, "mem": mem})
    summary = {
        "count": len(results),
        "total_time": sum(r["elapsed"] for r in results),
        "max_mem": max((r["mem"] for r in results), default=0),
    }
    with (out_p / "benchmark.json").open("w", encoding="utf-8") as f:
        json.dump({"results": results, **summary}, f, indent=2)
    return summary
