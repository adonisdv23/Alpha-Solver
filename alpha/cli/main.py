from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from importlib import metadata
from typing import List

from alpha.core import runner
from alpha.core.replay import ReplayHarness
from alpha.core.accessibility import AccessibilityChecker
from alpha.core.errors import UserInputError, hint
from alpha.core.queries_loader import load_queries
from alpha.eval import harness as eval_harness
from alpha.core.config import get_quality_gate
from alpha.core.budgets import load_budgets


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
    commands = {"run", "sweep", "telemetry", "quick-audit", "version", "replay", "bench", "a11y-check", "eval", "gate", "budgets"}
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

    p_replay = sp.add_parser("replay", help="Replay a recorded observability session.")
    p_replay.add_argument("--session", required=True, help="Replay session id.")

    p_bench = sp.add_parser("bench", help="Run benchmark harness.")
    p_bench.add_argument("--quick", action="store_true", help="Run quick benchmark suite.")

    p_a11y = sp.add_parser("a11y-check", help="Run accessibility checks over JSONL events.")
    p_a11y.add_argument("--input", required=True, help="Input JSONL file to scan.")

    p_eval = sp.add_parser("eval", help="Evaluation harness commands.")
    sp_eval = p_eval.add_subparsers(dest="eval_cmd", required=True)
    p_eval_run = sp_eval.add_parser("run", help="Run evaluation harness")
    p_eval_run.add_argument("--dataset", required=True, help="Path to dataset JSONL")
    p_eval_run.add_argument("--scorers", default="em", help="Comma separated scorers")
    p_eval_run.add_argument("--seed", type=int, default=0)
    p_eval_run.add_argument("--limit", type=int, default=0)

    p_gate = sp.add_parser("gate", help="Quality gate commands.")
    sp_gate = p_gate.add_subparsers(dest="gate_cmd", required=True)
    p_gate_check = sp_gate.add_parser("check", help="Check evaluation report against gate")
    p_gate_check.add_argument("--report", required=True, help="Path to evaluation report")

    p_bud = sp.add_parser("budgets", help="Budget configuration commands.")
    sp_bud = p_bud.add_subparsers(dest="bud_cmd", required=True)
    sp_bud.add_parser("show", help="Show budget configuration")

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
            import sys as _sys

            cmd = [_sys.executable, "scripts/telemetry_leaderboard.py"]
            if args.paths:
                cmd += ["--paths", *args.paths]
            cmd += ["--topk", str(args.topk), "--format", args.format]
            return subprocess.run(cmd, check=True).returncode
        if args.cmd == "quick-audit":
            from . import run_quick_audit as _run
            return _run()
        if args.cmd == "version":
            print("alpha-solver", _resolve_version())
            return 0
        if args.cmd == "replay":
            harness = ReplayHarness("artifacts/replays")
            session = harness.load(args.session)
            for ev in harness.replay(session):
                print(json.dumps(ev))
            return 0
        if args.cmd == "bench":
            if args.quick:
                root = Path(__file__).resolve().parent.parent.parent
                env = os.environ.copy()
                existing = env.get("PYTHONPATH", "")
                env["PYTHONPATH"] = (
                    f"{existing}{os.pathsep}{root}" if existing else str(root)
                )
                cmd = [sys.executable, "scripts/bench_reasoners.py"]
                return subprocess.run(cmd, check=True, env=env, cwd=root).returncode
            return 0
        if args.cmd == "a11y-check":
            checker = AccessibilityChecker.from_config()
            path = Path(args.input)
            results = []
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    text = obj.get("text") or obj.get("content")
                    if isinstance(text, str):
                        results.append(checker.check_text(text))
            summary = {
                "count": len(results),
                "fail": sum(1 for r in results if not r["ok"]),
                "avg_readability": round(
                    sum(r["readability"] for r in results) / len(results), 3
                )
                if results
                else 0.0,
            }
            out_dir = Path("artifacts/a11y")
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "summary.json").write_text(
                json.dumps(summary, ensure_ascii=False), encoding="utf-8"
            )
            return 0
        if args.cmd == "eval" and args.eval_cmd == "run":
            scorers = [s.strip() for s in args.scorers.split(",") if s.strip()]
            res = eval_harness.run(args.dataset, scorers, seed=args.seed, limit=args.limit or None)
            print(json.dumps({"metrics": res.metrics, "latency": res.latency, "cost_per_call": res.cost_per_call}, indent=2))
            return 0
        if args.cmd == "gate" and args.gate_cmd == "check":
            cfg = get_quality_gate()
            report = json.loads(Path(args.report).read_text(encoding="utf-8"))
            metrics = report.get("metrics", {})
            latency = report.get("latency", {})
            cost = float(report.get("cost_per_call", 0.0))
            if metrics.get(cfg.primary_metric, 0.0) < cfg.min_accuracy:
                print("primary metric below threshold", file=sys.stderr)
                return 1
            if latency.get("p95_ms", 0) > cfg.max_p95_ms:
                print("p95 latency above threshold", file=sys.stderr)
                return 1
            if latency.get("p99_ms", 0) > cfg.max_p99_ms:
                print("p99 latency above threshold", file=sys.stderr)
                return 1
            if cost > cfg.max_cost_per_call:
                print("cost per call above threshold", file=sys.stderr)
                return 1
            print("quality gate passed")
            return 0
        if args.cmd == "budgets" and args.bud_cmd == "show":
            data = load_budgets()
            print(json.dumps(data, indent=2))
            return 0
    except UserInputError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    main()

