from __future__ import annotations

import argparse
import subprocess
import sys
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


def main(argv: List[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    ap = argparse.ArgumentParser(prog="alpha-solver", description="Alpha Solver CLI")
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
            )
        if args.cmd == "telemetry":
            import subprocess, sys as _sys

            cmd = [_sys.executable, "scripts/telemetry_leaderboard.py"]
            if args.paths:
                cmd += ["--paths", *args.paths]
            cmd += ["--topk", str(args.topk), "--format", args.format]
            return subprocess.run(cmd, check=True).returncode
        if args.cmd == "quick-audit":
            from . import cli as _self  # reuse our earlier helper if present

            return run_quick_audit()
        if args.cmd == "version":
            from importlib.metadata import PackageNotFoundError, version

            try:
                print("alpha-solver", version("alpha-solver"))
            except PackageNotFoundError:
                print("alpha-solver (dev)")
            return 0
    except UserInputError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

