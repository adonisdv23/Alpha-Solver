"""Offline telemetry leaderboard generator (stdlib-only)."""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path
from typing import Dict, Iterable, Iterator, List


def _iter_events(paths: Iterable[str]) -> Iterator[dict]:
    for name in paths:
        p = Path(name)
        if not p.exists():
            continue
        with p.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue


def _summaries(events: Iterable[dict]) -> List[dict]:
    out: Dict[str, dict] = {}
    for ev in events:
        if ev.get("event") != "run_summary":
            continue
        run_id = ev.get("run_id", "")
        task = ev.get("task", "")
        out[run_id] = {
            "run_id": run_id,
            "task": task,
            "final_confidence": float(ev.get("final_confidence", 0.0)),
            "final_route": ev.get("final_route", ""),
        }
    rows = list(out.values())
    rows.sort(key=lambda r: (-r["final_confidence"], r["run_id"]))
    return rows


def _group_by_task(rows: List[dict]) -> List[dict]:
    best: Dict[str, dict] = {}
    for row in rows:
        task = row["task"]
        current = best.get(task)
        if current is None or (
            row["final_confidence"], row["run_id"]
        ) > (current["final_confidence"], current["run_id"]):
            best[task] = row
    grouped = list(best.values())
    grouped.sort(key=lambda r: (-r["final_confidence"], r["task"]))
    return grouped


def _to_markdown(rows: List[dict], topk: int) -> str:
    lines = ["| run_id | task | final_confidence | final_route |", "|---|---|---|---|"]
    for row in rows[:topk]:
        lines.append(
            f"| {row['run_id']} | {row['task']} | {row['final_confidence']:.3f} | {row['final_route']} |"
        )
    lines.append("")
    lines.append("")
    return "\n".join(lines)


def _to_csv(rows: List[dict], topk: int) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["run_id", "task", "final_confidence", "final_route"])
    for row in rows[:topk]:
        writer.writerow(
            [row["run_id"], row["task"], f"{row['final_confidence']:.3f}", row["final_route"]]
        )
    value = buf.getvalue()
    if not value.endswith("\n"):
        value += "\n"
    return value


def main() -> None:  # pragma: no cover - CLI wrapper
    ap = argparse.ArgumentParser(description="Telemetry leaderboard")
    ap.add_argument("--paths", nargs="+", required=True)
    ap.add_argument("--topk", type=int, default=5)
    ap.add_argument("--format", choices=["md", "csv"], default="md")
    ap.add_argument("--by", choices=["run", "task"], default="run")
    ap.add_argument("--out")
    args = ap.parse_args()

    rows = _summaries(_iter_events(args.paths))
    if args.by == "task":
        rows = _group_by_task(rows)

    content = _to_markdown(rows, args.topk) if args.format == "md" else _to_csv(rows, args.topk)

    if args.out:
        Path(args.out).write_text(content, encoding="utf-8")
    else:
        print(content, end="")


def collect(paths: Iterable[str]) -> List[dict]:
    """Collect run summaries from ``paths`` for backward compatibility."""

    return _summaries(_iter_events(paths))


def render_markdown(rows: List[dict], topk: int) -> str:
    """Render Markdown leaderboard for ``rows``."""

    return _to_markdown(rows, topk)


if __name__ == "__main__":  # pragma: no cover
    main()
