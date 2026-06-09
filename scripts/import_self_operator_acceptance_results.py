#!/usr/bin/env python3
"""CLI wrapper for deterministic local Self Operator acceptance result imports."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from alpha.self_operator.result_import import BLOCKED_STATUSES, import_acceptance_execution_packet, write_acceptance_import_summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Import and validate local Self Operator acceptance artifacts without interpreting "
            "results, updating Google Sheets, or mutating source artifacts."
        )
    )
    parser.add_argument("--packet-dir", required=True, type=Path, help="Local execution packet directory to import.")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for the deterministic import summary JSON.")
    parser.add_argument(
        "--output-name",
        default="acceptance-import-summary.json",
        help="Output JSON filename. Defaults to acceptance-import-summary.json.",
    )
    args = parser.parse_args()

    summary = import_acceptance_execution_packet(args.packet_dir, args.output_dir)
    output_path = write_acceptance_import_summary(summary, args.output_dir / args.output_name)
    print(
        "Self Operator acceptance import: "
        f"status={summary.status}; tasks={len(summary.task_records)}; artifacts={len(summary.artifacts)}; "
        f"output={output_path}"
    )
    print("Evidence boundary: results are not interpreted; MVP readiness is not claimed.")
    return 1 if summary.status in BLOCKED_STATUSES else 0


if __name__ == "__main__":
    raise SystemExit(main())
