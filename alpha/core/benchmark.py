from __future__ import annotations

"""Simple performance benchmarking utilities."""

import json
import resource
import time
from pathlib import Path
from typing import Callable, Dict, Iterable


def benchmark(
    fn: Callable[[str], None],
    queries: Iterable[str],
    out_dir: str | Path = "artifacts/benchmarks",
    *,
    with_replay: bool = False,
    with_telemetry: bool = False,
) -> Dict[str, float]:
    """Run ``fn`` over ``queries`` and export JSON/Markdown summaries."""

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
    data = {"results": results, **summary, "replay": with_replay, "telemetry": with_telemetry}
    (out_p / "benchmark.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    md = ["|query|elapsed|mem|", "|---|---|---|"]
    for r in results:
        md.append(f"|{r['query']}|{r['elapsed']:.4f}|{r['mem']}|")
    md.append(f"\nTotal time: {summary['total_time']:.4f}s  Max mem: {summary['max_mem']}")
    (out_p / "benchmark.md").write_text("\n".join(md), encoding="utf-8")
    return summary


__all__ = ["benchmark"]
