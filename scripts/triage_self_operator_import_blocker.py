#!/usr/bin/env python3
"""CLI wrapper for deterministic Self Operator import-blocker triage."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from alpha.self_operator.import_blocker_triage import (
    DEFAULT_TASK_ID,
    FIX_CLASSIFICATIONS,
    triage_import_blocker,
    write_triage_result,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Triage a blocked_source_mutation_concern acceptance-import blocker without "
            "mutating source artifacts, fabricating artifacts, interpreting acceptance "
            "results, or claiming readiness."
        )
    )
    parser.add_argument("--packet-dir", required=True, type=Path, help="Local execution packet directory to triage.")
    parser.add_argument("--task-id", default=DEFAULT_TASK_ID, help=f"Task ID to triage. Defaults to {DEFAULT_TASK_ID}.")
    parser.add_argument(
        "--import-summary",
        type=Path,
        default=None,
        help="Optional path to the blocking acceptance-import-summary.json for cross-reference.",
    )
    parser.add_argument("--output-dir", type=Path, default=None, help="Optional directory for the triage result JSON.")
    parser.add_argument(
        "--output-name",
        default="import-blocker-triage-result.json",
        help="Output JSON filename. Defaults to import-blocker-triage-result.json.",
    )
    args = parser.parse_args()

    result = triage_import_blocker(args.packet_dir, args.task_id, args.import_summary)
    print(f"Self Operator import-blocker triage: task={result.task_id}; classification={result.classification}")
    for reason in result.classification_reasons:
        print(f"  - {reason}")
    print(f"Recommended follow-up: {result.recommended_followup}")
    if args.output_dir is not None:
        output_path = write_triage_result(result, args.output_dir / args.output_name)
        print(f"Triage result written to {output_path}")
    print("Evidence boundary: read-only triage; results are not interpreted; MVP readiness is not claimed.")
    return 0 if result.classification in FIX_CLASSIFICATIONS else 1


if __name__ == "__main__":
    raise SystemExit(main())
