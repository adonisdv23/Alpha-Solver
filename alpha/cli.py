from __future__ import annotations

import argparse
import subprocess
import sys
from importlib import metadata
from typing import List

from alpha.core import runner
from alpha.core.errors import UserInputError, hint
from alpha.core.queries_loader import load_queries


def run_quick_audit() -> int:
    """Invoke quick audit script in repo or installed mode."""
    try:
        return subprocess.run([sys.executable, "-m", "scripts.quick_audit"], check=True).returncode
    except Exception:
        return subprocess.run([sys.executable, "scripts/quick_audit.py"], check=True).returncode


EXAMPLES = """
alpha-solver run --queries "demo query" --regions US --plan-only --seed 1234
alpha-solver run --queries-file docs/queries.sample.txt --regions US EU --explain
alpha-solver telemetry --paths telemetry/*.jsonl --topk 5 --format md
"""


def _add_common_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--queries", nargs="*", default=[], help="Inline queries (space-separated).")
    p.add_argument(
        "--queries-file",
        help="Path to a queries file supporting # comments and @file includes.",
    )
    p.add_argument("--regions", nargs="*", default=["US"], help="Target regions (default: US).")
    p.add_argument("--seed", type=int, default=1234, help="Deterministic seed (default: 1234).")
    p.add_argument("--topk", type=int, default=5, help="Top-K shortlist size (default: 5).")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--plan-only", action="store_true", help="Emit plan and exit (no execution).")
    mode.add_argument("--explain", action="store_true", help="Emit plan + explanations, no execution.")
    mode.add_argument("--execute", action="store_true", help="Execute actions (default).")
    p.add_argument("--policy-dry-run", action="store_true", help="Log policy warnings but never block.")
    p.add_argument(
        "--budget-max-steps",
        type=int,
        default=0,
        help="Maximum allowed steps (0 = unlimited).",
    )
    p.add_argument(
        "--budget-max-seconds",
        type=float,
        default=0.0,
        help="Maximum wall-clock seconds (0 = unlimited).",
    )
    p.add_argument(
        "--breaker-max-fails",
        type=int,
        default=0,
        help="Consecutive failures before breaker trips (0 = disabled).",
    )
    p.add_argument(
        "--data-policy",
        help="Path to data_policy.json controlling family/tag allow/deny.",
    )


def _resolve_version() -> str:
    try:
        return metadata.version("alpha-solver")
    except metadata.PackageNotFoundError:
        from alpha import __version__

        return __version__


def main(argv: List[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    commands = {"run", "sweep", "telemetry", "quick-audit", "version"}
    if argv and not argv[0].startswith("-") and argv[0] not in commands:
        print(f"error: unknown command '{argv[0]}'", file=sys.stderr)
        return 2
    if "--examples" in argv:
        print(EXAMPLES)
        return 0

    ap = argparse.ArgumentParser(
        prog="alpha-solver",
        description="Alpha Solver command-line interface",
        epilog="Use --examples to see sample commands.",
    )
    ap.add_argument("--examples", action="store_true", help="Show usage examples and exit.")
    sp = ap.add_subparsers(dest="cmd", required=True)

    p_run = sp.add_parser("run", help="Run a single pass over queries and regions.")
    _add_common_args(p_run)

    p_sweep = sp.add_parser("sweep", help="Run a broader sweep (multiple regions/queries).")
    _add_common_args(p_sweep)

    p_tel = sp.add_parser("telemetry", help="Summarize telemetry / leaderboard.")
    p_tel.add_argument("--paths", nargs="+", required=False, help="Telemetry JSONL globs.")
    p_tel.add_argument("--topk", type=int, default=5)
    p_tel.add_argument("--format", choices=["md", "csv"], default="md")

    sp.add_parser("quick-audit", help="Run repository quick audit.")
    sp.add_parser("version", help="Show version and exit.")

    args = ap.parse_args(argv)
    try:
        if args.cmd in ("run", "sweep"):
            inline = [q for q in (args.queries or []) if q.strip()]
            loaded = load_queries(args.queries_file) if args.queries_file else []
            queries = loaded + inline
            if not queries:
                raise hint(
                    UserInputError("No queries provided."),
                    "Use --queries 'foo' or --queries-file docs/queries.sample.txt",
                )
            mode = "execute"
            if args.plan_only:
                mode = "plan-only"
            elif args.explain:
                mode = "explain"
            return runner.run_cli(
                queries=queries,
                regions=args.regions,
                seed=args.seed,
                topk=args.topk,
                mode=mode,
                policy_dry_run=args.policy_dry_run,
                budget_max_steps=args.budget_max_steps,
                budget_max_seconds=args.budget_max_seconds,
                breaker_max_fails=args.breaker_max_fails,
                data_policy=args.data_policy,
            )
        if args.cmd == "telemetry":
            import subprocess, sys as _sys

            cmd = [_sys.executable, "scripts/telemetry_leaderboard.py"]
            if args.paths:
                cmd += ["--paths", *args.paths]
            cmd += ["--topk", str(args.topk), "--format", args.format]
            return subprocess.run(cmd, check=True).returncode
        if args.cmd == "quick-audit":
            return run_quick_audit()
        if args.cmd == "version":
            print("alpha-solver", _resolve_version())
            return 0
    except UserInputError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    main()

