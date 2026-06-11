#!/usr/bin/env python3
"""CLI wrapper for deterministic Self Operator acceptance interpretation."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from alpha.self_operator.acceptance_interpretation import (  # noqa: E402
    READINESS_BLOCKED,
    interpret_acceptance_import_summary,
    write_acceptance_interpretation,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Interpret imported local Self Operator acceptance results without claiming readiness."
    )
    parser.add_argument("--import-summary", required=True, type=Path, help="Path to imported acceptance summary JSON.")
    parser.add_argument(
        "--operator-decision",
        type=Path,
        default=None,
        help=(
            "Optional path to an explicit operator-decision JSON artifact "
            "(self_operator.expected_safety_block_operator_review.v1)."
        ),
    )
    parser.add_argument("--output", required=True, type=Path, help="Path for deterministic interpretation JSON.")
    args = parser.parse_args(argv)

    try:
        import_summary = json.loads(args.import_summary.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"blocked: could not read import summary: {exc}", file=sys.stderr)
        return 2

    operator_decision = None
    if args.operator_decision is not None:
        try:
            operator_decision = json.loads(args.operator_decision.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"blocked: could not read operator decision: {exc}", file=sys.stderr)
            return 2

    interpretation = interpret_acceptance_import_summary(import_summary, operator_decision=operator_decision)
    write_acceptance_interpretation(interpretation, args.output)
    payload = interpretation.to_dict()
    p0 = payload["summary"]["p0_defect_count"]
    p1 = payload["summary"]["p1_defect_count"]
    consumption = payload["operator_decision_consumption"]
    if not consumption["provided"]:
        decision_state = "not_provided"
    elif consumption["consumed"]:
        decision_state = "consumed"
    else:
        decision_state = "invalid"
    print(
        "interpretation="
        f"{payload['readiness_implication']} "
        f"tasks={payload['summary']['task_count']} "
        f"defects={payload['summary']['defect_count']} "
        f"p0={p0} p1={p1} "
        f"operator_decision={decision_state} "
        f"confirmation_type={consumption['confirmation_type'] or 'none'} "
        "machine_readable_artifact_confirmation=false "
        "non_claim='does not claim MVP readiness'"
    )
    if consumption["provided"] and not consumption["consumed"]:
        print(
            "blocked: operator decision not consumed: " + "; ".join(consumption["validation_errors"]),
            file=sys.stderr,
        )
    if payload["readiness_implication"] == READINESS_BLOCKED:
        return 1
    if p0 or p1:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
