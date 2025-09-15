from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

from service.replay.harness import run_file, format_mismatch


DEFAULT_REPLAY = "data/datasets/replay/replay_small.jsonl"
DEFAULT_SKIP = "known_flaky,external_tool_missing"


def _parse_skip_tags(raw: str | None) -> set[str]:
    if not raw:
        return set()
    return {t.strip() for t in raw.split(",") if t.strip()}


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Routing determinism harness")
    parser.add_argument("--replay-file", default=DEFAULT_REPLAY)
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--skip-tags", default=DEFAULT_SKIP)
    parser.add_argument("--out-json", dest="out_json")
    parser.add_argument("--out")
    parser.add_argument("--fast", action="store_true", help="reduce runs for quick smoke")
    args = parser.parse_args(list(argv) if argv is not None else None)

    runs = args.runs
    if args.fast:
        runs = min(runs, 3)
    skip_tags = _parse_skip_tags(args.skip_tags)

    try:
        summary = run_file(
            args.replay_file,
            runs=runs,
            seed=args.seed,
            skip_tags=skip_tags,
        )
    except FileNotFoundError:
        print(f"replay file not found: {args.replay_file}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - unexpected
        print(f"internal error: {exc}", file=sys.stderr)
        return 5

    # Console output
    print(f"seed={summary['seed']} runs={summary['runs']} file={summary['set']}")
    print(f"pass_pct={summary['pass_pct']:.1f}")
    if summary["mismatches"]:
        first = summary["mismatches"][0]
        print(f"first_mismatch_id={first['id']}")
        for line in format_mismatch(first):
            print(line)

    # JSON report
    if args.out_json:
        path = Path(args.out_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, sort_keys=True)

    # TXT report
    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            f"seed={summary['seed']} runs={summary['runs']} file={summary['set']}",
            f"pass_pct={summary['pass_pct']:.1f}",
        ]
        if summary["mismatches"]:
            first = summary["mismatches"][0]
            lines.append(f"first_mismatch_id={first['id']}")
            lines.extend(format_mismatch(first))
        else:
            lines.append("stable=yes")
        with path.open("w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    return 0 if summary["stable"] else 4


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
