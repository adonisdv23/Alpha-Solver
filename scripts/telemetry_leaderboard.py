from __future__ import annotations

import argparse
import glob
import json
from collections import Counter
from pathlib import Path
from typing import Iterable, Iterator


def iter_rows(paths: Iterable[str]) -> Iterator[dict]:
    """Yield JSON objects from provided path globs."""
    for pattern in paths:
        for path in glob.glob(pattern):
            p = Path(path)
            if not p.exists():
                continue
            with p.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except Exception:
                        continue


def build_leaderboard(rows: Iterable[dict]) -> Counter:
    counts: Counter[str] = Counter()
    for row in rows:
        solver = row.get("solver") or row.get("model") or row.get("id")
        status = row.get("status")
        if not solver:
            continue
        if status in ("success", "ok", True, 1):
            counts[solver] += 1
    return counts


def to_markdown(counts: Counter[str], topk: int) -> str:
    lines = ["| solver | success |", "|---|---|"]
    for solver, cnt in counts.most_common(topk):
        lines.append(f"| {solver} | {cnt} |")
    lines.append("")
    return "\n".join(lines)


def to_csv(counts: Counter[str], topk: int) -> str:
    rows = [("solver", "success")]
    rows.extend(counts.most_common(topk))
    out_lines: list[str] = []
    for solver, cnt in rows:
        out_lines.append(f"{solver},{cnt}")
    out_lines.append("")
    return "\n".join(out_lines)


def collect(paths: Iterable[str]) -> Counter:
    """Convenience wrapper for building a leaderboard from paths."""
    return build_leaderboard(iter_rows(paths))


def render_markdown(counts: Counter[str], topk: int) -> str:
    """Render markdown with a small header for regression locking."""
    header = ["# Telemetry Leaderboard", "", "## Global Top Tools", ""]
    header.append(to_markdown(counts, topk))
    return "\n".join(header)


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline telemetry leaderboard")
    parser.add_argument("--paths", nargs="+", required=True, help="Glob(s) for telemetry jsonl files")
    parser.add_argument("--topk", type=int, default=5, help="Top K solvers")
    parser.add_argument("--format", choices=["md", "csv"], default="md", help="Output format")
    parser.add_argument("--out", help="Output file path")
    args = parser.parse_args()

    counts = build_leaderboard(iter_rows(args.paths))
    content = to_markdown(counts, args.topk) if args.format == "md" else to_csv(counts, args.topk)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
