#!/usr/bin/env python3
"""CLI wrapper for the deterministic Self Operator release-gate checker."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from alpha.self_operator.release_gate import (  # noqa: E402
    evaluate_self_operator_release_gates,
    write_release_gate_report,
)

BLOCKED_PREFIX = "blocked_"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check deterministic Self Operator MVP release gates. The checker "
            "writes JSON, never mutates source artifacts, and does not claim MVP readiness."
        )
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."), help="Repository root to inspect.")
    parser.add_argument("--output", type=Path, help="Optional deterministic JSON output path.")
    args = parser.parse_args(argv)

    report = evaluate_self_operator_release_gates(args.repo_root)
    if args.output:
        write_release_gate_report(report, args.output)

    print(f"Self Operator release gate final_status: {report.final_status}")
    print(f"ready: {str(report.ready).lower()} (does not claim MVP readiness)")
    print(f"earliest_missing_gate: {report.earliest_missing_gate or 'none'}")
    for gate in report.gates:
        print(f"- {gate.gate_id}: {gate.status} ({gate.reason})")

    return 1 if report.final_status.startswith(BLOCKED_PREFIX) else 0


if __name__ == "__main__":
    raise SystemExit(main())
