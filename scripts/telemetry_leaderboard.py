from __future__ import annotations

import argparse
import csv
import glob
import json
from collections import Counter
from io import StringIO
from pathlib import Path
from typing import Iterable, Iterator, Dict


SUCCESS_STATES = {"success", "ok", True, 1}


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


def build_leaderboard(rows: Iterable[dict], *, by_region: bool = False, by_family: bool = False) -> Dict[str, Counter] | Counter:
    if by_region:
        out: Dict[str, Counter] = {}
    else:
        out = Counter()
    for row in rows:
        solver = row.get("solver") or row.get("model") or row.get("id")
        if by_family and row.get("family"):
            solver = row.get("family")
        status = row.get("status")
        if not solver or status not in SUCCESS_STATES:
            continue
        if by_region:
            region = row.get("region") or "unknown"
            out.setdefault(region, Counter())[solver] += 1
        else:
            out[solver] += 1
    return out


def _markdown_table(counts: Counter, limit: int) -> str:
    lines = ["| solver | success |", "|---|---|"]
    for solver, cnt in counts.most_common(limit):
        lines.append(f"| {solver} | {cnt} |")
    lines.append("")
    return "\n".join(lines)


def to_markdown(counts: Dict[str, Counter] | Counter, limit: int) -> str:
    if isinstance(counts, Counter):
        return _markdown_table(counts, limit)
    lines = []
    for region in sorted(counts):
        lines.append(f"### {region}")
        lines.append(_markdown_table(counts[region], limit))
    return "\n".join(lines)


def to_csv(counts: Dict[str, Counter] | Counter, limit: int) -> str:
    buf = StringIO()
    writer = csv.writer(buf)
    if isinstance(counts, Counter):
        writer.writerow(["solver", "success"])
        for solver, cnt in counts.most_common(limit):
            writer.writerow([solver, cnt])
    else:
        writer.writerow(["region", "solver", "success"])
        for region in sorted(counts):
            for solver, cnt in counts[region].most_common(limit):
                writer.writerow([region, solver, cnt])
    return buf.getvalue()


def collect(paths: Iterable[str], **kwargs) -> Dict[str, Counter] | Counter:
    return build_leaderboard(iter_rows(paths), **kwargs)


def render_markdown(counts: Dict[str, Counter] | Counter, topk: int) -> str:
    header = ["# Telemetry Leaderboard", ""]
    if isinstance(counts, Counter):
        header.append("## Global Top Tools")
        header.append("")
    header.append(to_markdown(counts, topk))
    return "\n".join(header)


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline telemetry leaderboard")
    parser.add_argument("--paths", nargs="+", required=True, help="Glob(s) for telemetry jsonl files")
    parser.add_argument("--limit", type=int, default=5, help="Top N")
    parser.add_argument("--topk", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--format", choices=["md", "csv", "all"], default="md", help="Output format")
    parser.add_argument("--out", help="Output file path (or prefix if --format all)")
    parser.add_argument("--by-region", action="store_true", help="Group outputs per region")
    parser.add_argument("--by-family", action="store_true", help="Roll-up by tool family if present")
    args = parser.parse_args()

    counts = build_leaderboard(iter_rows(args.paths), by_region=args.by_region, by_family=args.by_family)

    limit = args.topk if args.topk is not None else args.limit

    out_md: Path | None = None
    out_csv: Path | None = None
    if args.out:
        base = Path(args.out)
        if args.format == "all":
            out_md = base.with_suffix(".md")
            out_csv = base.with_suffix(".csv")
        elif args.format == "md":
            out_md = base
        else:
            out_csv = base
    elif args.format == "all":
        base_dir = Path("artifacts")
        base_dir.mkdir(parents=True, exist_ok=True)
        out_md = base_dir / "telemetry_leaderboard.md"
        out_csv = base_dir / "telemetry_leaderboard.csv"

    if args.format in ("md", "all"):
        md = render_markdown(counts, limit)
        if out_md:
            out_md.parent.mkdir(parents=True, exist_ok=True)
            out_md.write_text(md, encoding="utf-8")
        else:
            print(md)
    if args.format in ("csv", "all"):
        csv_content = to_csv(counts, limit)
        if out_csv:
            out_csv.parent.mkdir(parents=True, exist_ok=True)
            out_csv.write_text(csv_content, encoding="utf-8")
        else:
            print(csv_content, end="")


if __name__ == "__main__":
    main()
