from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Callable, Dict, Iterable

import resource

from .replay import ReplayHarness
from .telemetry import TelemetryExporter


async def _dummy_sender(batch: list[dict]) -> None:  # pragma: no cover - trivial sender
    return None


def benchmark(
    fn: Callable[[str], None],
    queries: Iterable[str],
    out_dir: str | Path = "artifacts/benchmarks",
    *,
    stress_replay: bool = False,
    stress_telemetry: bool = False,
) -> Dict[str, float]:
    out_p = Path(out_dir)
    out_p.mkdir(parents=True, exist_ok=True)
    results = []
    harness = ReplayHarness(out_p / "replay") if stress_replay else None
    exporter = TelemetryExporter(_dummy_sender) if stress_telemetry else None
    for q in queries:
        start = time.perf_counter()
        fn(q)
        elapsed = time.perf_counter() - start
        mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
        result = {"query": q, "elapsed": elapsed, "mem": mem}
        results.append(result)
        if harness:
            harness.record({"session_id": harness.session_id, "event": "benchmark", "timestamp": time.time(), "version": "1.0", "data": result})
        if exporter:
            import asyncio

            asyncio.run(exporter.emit({"session_id": "bench", "event": "benchmark", "timestamp": time.time(), "version": "1.0", "data": result}))
    summary = {
        "count": len(results),
        "total_time": sum(r["elapsed"] for r in results),
        "max_mem": max((r["mem"] for r in results), default=0),
    }
    with (out_p / "benchmark.json").open("w", encoding="utf-8") as f:
        json.dump({"results": results, **summary}, f, indent=2)
    with (out_p / "benchmark.md").open("w", encoding="utf-8") as f:
        f.write("|metric|value|\n|---|---|\n")
        for k, v in summary.items():
            f.write(f"{k}|{v}\n")
    if harness:
        harness.save()
    if exporter:
        import asyncio

        asyncio.run(exporter.close())
    return summary
