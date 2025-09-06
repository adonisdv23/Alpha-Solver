from __future__ import annotations

import argparse
import csv
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List

try:
    import resource  # type: ignore
except Exception:  # pragma: no cover
    resource = None  # type: ignore


def parse_queries(args: argparse.Namespace) -> List[str]:
    queries: List[str] = []
    if args.queries:
        queries.extend(args.queries)
    if args.queries_file:
        path = Path(args.queries_file)
        if path.exists():
            queries.extend(q.strip() for q in path.read_text(encoding="utf-8").splitlines() if q.strip())
    return queries


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark queries")
    parser.add_argument("--queries", nargs="*", help="Inline queries")
    parser.add_argument("--queries-file", help="Path to queries file")
    parser.add_argument("--regions", nargs="+", required=True, help="Regions")
    parser.add_argument("--seed", type=int, default=0, help="Seed")
    parser.add_argument("--repeat", type=int, default=3, help="Repeats per query")
    args = parser.parse_args()

    queries = parse_queries(args)
    if not queries:
        parser.error("No queries provided")

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path("artifacts") / "bench"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"bench_{ts}.csv"

    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["query", "region", "repeat", "duration_ms", "maxrss_kb"])
        for query in queries:
            for region in args.regions:
                for r in range(args.repeat):
                    start = time.perf_counter()
                    cmd = [
                        sys.executable,
                        "-m",
                        "alpha.cli",
                        "run",
                        "--queries",
                        query,
                        "--regions",
                        region,
                        "--seed",
                        str(args.seed),
                        "--plan-only",
                    ]
                    try:
                        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                    except Exception:
                        pass
                    end = time.perf_counter()
                    duration_ms = int((end - start) * 1000)
                    if resource:
                        rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
                    else:
                        rss = float("nan")
                    writer.writerow([query, region, r, duration_ms, rss])


if __name__ == "__main__":
    main()
