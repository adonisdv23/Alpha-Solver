from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from .diff import DEFAULT_FIELDS, diff_lists, normalize


def _parse_filter(expr: Optional[str]) -> Optional[Tuple[str, str]]:
    if not expr:
        return None
    if "=" not in expr:
        raise ValueError("filter must be of form key=value")
    k, v = expr.split("=", 1)
    return k, v


def _load_events(
    path: Path, *, flt: Optional[Tuple[str, str]] = None, limit: Optional[int] = None
) -> List[Dict]:
    events: List[Dict] = []
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            event = json.loads(line)
            if flt is not None:
                key, value = flt
                if str(event.get(key)) != value:
                    continue
            events.append(event)
            if limit is not None and len(events) >= limit:
                break
    return events


def _percentile(values: List[float], pct: float) -> float:
    if not values:
        return 0.0
    values_sorted = sorted(values)
    k = int((len(values_sorted) - 1) * (pct / 100.0))
    return values_sorted[k]


# ---------------------------------------------------------------------------
def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", required=True, help="JSONL event log")
    parser.add_argument("--compare", help="Second JSONL log to diff against")
    parser.add_argument("--filter", dest="filter_expr")
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--out")
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        filt = _parse_filter(args.filter_expr)
        events_a = _load_events(Path(args.events), flt=filt, limit=args.limit)
    except Exception:
        return 1

    durations: List[float] = []
    for e in events_a:
        start = time.monotonic()
        normalize(e, keep_keys=DEFAULT_FIELDS)
        durations.append((time.monotonic() - start) * 1000)

    diff_lines: List[str] = []
    mismatches = 0
    if args.compare:
        try:
            events_b = _load_events(Path(args.compare), flt=filt, limit=args.limit)
        except Exception:
            return 1
        diff_lines = diff_lists(events_a, events_b, id_key="id", keys=DEFAULT_FIELDS)
        mismatches = len([l for l in diff_lines if l != "... (truncated)"])

    summary = {
        "total": len(events_a),
        "mismatches": mismatches,
        "p95_ms": round(_percentile(durations, 95), 3),
    }
    print(json.dumps(summary))

    if args.out:
        Path(args.out).write_text("\n".join(diff_lines), encoding="utf-8")

    return 2 if mismatches > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
