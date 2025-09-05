from __future__ import annotations
import argparse
import sys
from pathlib import Path
from typing import List

from . import __version__
from .core import loader, selector, orchestrator, runner
from .core.determinism import apply_seed
from .core.paths import ensure_dir, write_json_atomic, timestamp_rfc3339z


def parse_queries(path: str) -> List[str]:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(path)
    return [line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Alpha Solver CLI",
        epilog=(
            "Examples:\n"
            "  python -m alpha.cli --plan-only --queries docs/queries.txt\n"
            "  python -m alpha.cli --execute --regions 'US' --queries docs/queries.txt\n"
            "  python -m alpha.cli --explain --regions 'EU' --queries docs/queries.txt"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--plan-only", "--dry-run", action="store_true", dest="plan_only", help="build plan only")
    modes.add_argument("--explain", action="store_true", help="build plan with explanations")
    modes.add_argument("--execute", action="store_true", help="build and execute plan")
    parser.add_argument("--regions", default="US", help="comma-separated regions")
    parser.add_argument("--k", type=int, default=5, help="top-N tools")
    parser.add_argument("--queries", default="docs/queries.txt", help="queries file")
    parser.add_argument("--outdir", default="artifacts", help="output directory")
    parser.add_argument("--seed", type=int, default=None, help="optional seed")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    parser.add_argument("--policy-dryrun", action="store_true", help="policy dry run (no enforcement)")
    parser.add_argument("--benchmark", action="store_true", help="run benchmark suite")
    parser.add_argument("--replay", help="replay a saved session id")
    args = parser.parse_args(argv)

    if args.version:
        print(f"Alpha Solver {__version__}")
        return 0

    if args.replay:
        from .core.replay import ReplayHarness

        harness = ReplayHarness()
        session = harness.load(args.replay)
        for ev in session.events:
            print(ev)
        return 0

    if args.benchmark:
        from .core.benchmark import benchmark

        queries = parse_queries(args.queries)
        benchmark(lambda q: None, queries)
        return 0

    seed = apply_seed(args.seed)
    print(f"Using seed: {seed}")

    loader.load_all("registries")

    from .core.observability import ObservabilityManager

    obs = ObservabilityManager()
    obs.log_event({"event": "start", "seed": seed})

    regions = [r.strip() for r in args.regions.split(',') if r.strip()]
    if not regions:
        print("No regions specified", file=sys.stderr)
        return 2
    try:
        queries = parse_queries(args.queries)
    except FileNotFoundError:
        print(f"Queries file not found: {args.queries}", file=sys.stderr)
        return 2
    if not queries:
        print("No queries found", file=sys.stderr)
        return 2

    artifact_dir = ensure_dir(args.outdir)

    exit_code = 0
    for region in regions:
        for query in queries:
            tools_raw = loader.REGISTRY_CACHE.get("tools", {})
            if isinstance(tools_raw, dict):
                tools_list = tools_raw.get("tools", [])
            elif isinstance(tools_raw, list):
                tools_list = tools_raw
            else:
                tools_list = []
            shortlist = selector.rank_region(
                tools_list,
                region,
                args.k,
                clusters=loader.REGISTRY_CACHE.get("clusters"),
            )
            plan = orchestrator.build_plan(
                query,
                region,
                args.k,
                shortlist,
                loader.REGISTRY_CACHE.get("budget_controls"),
                seed=seed,
                policy_dryrun=args.policy_dryrun,
            )
            obs.log_event({"event": "plan", "region": region, "query": query})

            ts = plan.run.get("timestamp") or timestamp_rfc3339z()
            plan_dir = ensure_dir(Path(artifact_dir) / "plans" / ts)
            shortlist_path = artifact_dir / "last_shortlist.json"
            write_json_atomic(shortlist_path, shortlist)
            plan.artifacts["shortlist_snapshot"] = str(shortlist_path)
            plan_path = plan_dir / "plan.json"
            plan.artifacts["plan_path"] = str(plan_path)
            write_json_atomic(plan_path, plan.to_dict())
            write_json_atomic(artifact_dir / "last_plan.json", plan.to_dict())

            if args.explain:
                for step in plan.steps:
                    reason_str = "; ".join(f"{k}:{v}" for k, v in step.reasons.items())
                    conf = step.confidence if step.confidence is not None else "n/a"
                    print(f"{step.tool_id} -> {reason_str} (confidence {conf})")
            elif args.plan_only or (not args.explain and not args.execute):
                print(plan.human_summary())

            if args.execute:
                trace = runner.run_plan(plan, local_only=True)
                trace_path = artifact_dir / f"trace_{ts}.json"
                write_json_atomic(trace_path, trace)
                # If any step indicates error, mark nonzero
                if any("error" in t for t in trace):
                    exit_code = 1

    session_id = obs.close()
    if session_id:
        print(f"Replay session saved: {session_id}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
