"""Alpha Solver v91 entrypoints."""

from alpha.reasoning.tot import TreeOfThoughtSolver
from alpha.policy.safe_out import SafeOutPolicy
from alpha.reasoning.logging import (
    log_safe_out_decision,
    set_replay_harness,
    set_session_id,
)
from alpha.core.replay import ReplayHarness
from alpha.core.accessibility import AccessibilityChecker

import argparse
import logging
import os
import json
from pathlib import Path


def _tree_of_thought(
    query: str,
    *,
    seed: int = 42,
    branching_factor: int = 3,
    score_threshold: float = 0.70,
    max_depth: int = 5,
    timeout_s: int = 10,
    dynamic_prune_margin: float = 0.15,
    low_conf_threshold: float = 0.60,
    enable_cot_fallback: bool = True,
    replay_harness: ReplayHarness | None = None,
) -> dict:
    """Solve ``query`` via deterministic Tree-of-Thought reasoning."""
    if replay_harness is not None:
        set_replay_harness(replay_harness)
        set_session_id(replay_harness.session_id)
    solver = TreeOfThoughtSolver(
        seed=seed,
        branching_factor=branching_factor,
        score_threshold=score_threshold,
        max_depth=max_depth,
        timeout_s=timeout_s,
        dynamic_prune_margin=dynamic_prune_margin,
    )
    tot_result = solver.solve(query)
    policy = SafeOutPolicy(
        low_conf_threshold=low_conf_threshold,
        enable_cot_fallback=enable_cot_fallback,
    )
    decision = policy.apply(tot_result, query)
    log_safe_out_decision(
        route=decision["route"],
        conf=float(tot_result.get("confidence", 0.0)),
        threshold=low_conf_threshold,
        reason=decision["reason"],
    )
    set_replay_harness(None)
    return decision


def main() -> None:  # pragma: no cover - CLI glue
    parser = argparse.ArgumentParser(description="Alpha Solver v91")
    parser.add_argument("query")
    parser.add_argument("--record", metavar="SESSION")
    parser.add_argument("--replay", metavar="SESSION")
    parser.add_argument("--telemetry-endpoint")
    parser.add_argument("--log-path")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--strict-accessibility", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        filename=args.log_path or os.getenv("LOG_PATH"),
        level=logging.DEBUG if args.verbose or os.getenv("VERBOSE") else logging.INFO,
    )

    harness: ReplayHarness | None = None
    session_to_validate = None
    if args.record:
        harness = ReplayHarness(session_id=args.record)
    elif args.replay:
        harness = ReplayHarness()
        session_to_validate = harness.load(args.replay)
    if harness:
        set_replay_harness(harness)
        set_session_id(harness.session_id)

    decision = _tree_of_thought(args.query, replay_harness=harness)

    if args.strict_accessibility:
        checker = AccessibilityChecker.from_config()
        report = checker.check_text(decision["final_answer"])
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        (reports_dir / "accessibility.json").write_text(json.dumps(report), encoding="utf-8")
        (reports_dir / "accessibility.csv").write_text(
            "readability,ok\n" f"{report['readability']},{int(report['ok'])}\n", encoding="utf-8"
        )
        if not report["ok"]:
            raise SystemExit("Accessibility score below target")

    if args.record and harness:
        session_id = harness.save()
        print(session_id)
    if args.replay and harness and session_to_validate is not None:
        harness.save()
        if harness.events != session_to_validate.events:
            raise SystemExit("Replay mismatch")


if __name__ == "__main__":  # pragma: no cover
    main()
