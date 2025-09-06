from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any


def _load_run_trace(root: Path) -> tuple[str, Dict[str, Any]] | None:
    run_dir = root / "run"
    if not run_dir.exists():
        return None
    traces = sorted(run_dir.glob("run_*.json"))
    if not traces:
        return None
    path = traces[-1]
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    return path.stem, data


def _load_shortlists(root: Path, paths: List[str]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for p in sorted(paths):
        sp = Path(p)
        if not sp.is_absolute():
            sp = root / sp
        if not sp.exists():
            continue
        try:
            with sp.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            out.append(data)
        except Exception:
            continue
    out.sort(key=lambda x: (x.get("region", ""), x.get("query", "")))
    return out


def main() -> None:
    art_root = Path("artifacts")
    art_root.mkdir(parents=True, exist_ok=True)

    run_info = _load_run_trace(art_root)
    if not run_info:
        return
    run_id, trace = run_info
    seed = trace.get("seed")
    regions = trace.get("regions", [])
    shortlist_paths = trace.get("shortlist_paths", [])
    shortlists = _load_shortlists(art_root, shortlist_paths)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines: List[str] = ["# Run Overview", ""]
    lines.append(f"- run_id: {run_id}")
    lines.append(f"- seed: {seed}")
    lines.append(f"- now_utc: {now}")
    if regions:
        lines.append(f"- regions: {', '.join(sorted(regions))}")
    lines.append(f"- queries: {len(shortlists)}")
    lines.append("")

    for sl in shortlists:
        query = sl.get("query", "")
        region = sl.get("region", "")
        items = sorted(sl.get("items", []), key=lambda x: (-x.get("score", 0), x.get("tool_id", "")))
        lines.append(f"## {query} ({region})")
        lines.append("| rank | tool_id | score | confidence | reason |")
        lines.append("|---|---|---|---|---|")
        for idx, item in enumerate(items, 1):
            tool = item.get("tool_id", "")
            score = item.get("score", "")
            conf = item.get("confidence", "")
            reason = item.get("reason", "")
            lines.append(f"| {idx} | {tool} | {score} | {conf} | {reason} |")
        lines.append("")

    md_path = art_root / "overview.md"
    telemetry_md = art_root / "telemetry_leaderboard.md"
    telemetry_csv = art_root / "telemetry_leaderboard.csv"
    if telemetry_md.exists() or telemetry_csv.exists():
        lines.append("## Telemetry Leaderboard")
        if telemetry_md.exists():
            lines.append(f"- [Markdown]({telemetry_md.as_posix()})")
        if telemetry_csv.exists():
            lines.append(f"- [CSV]({telemetry_csv.as_posix()})")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
