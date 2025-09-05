from __future__ import annotations
import argparse
import sys
from pathlib import Path
from typing import List

from .core import loader, selector, orchestrator, runner
from .core.paths import ensure_dir, write_json_atomic, timestamp_rfc3339z


def parse_queries(path: str) -> List[str]:
    p = Path(path)
    if p.is_file():
        return [line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    return []


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Alpha Solver CLI")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--plan-only", action="store_true", help="build plan only")
    modes.add_argument("--explain", action="store_true", help="build plan with explanations")
    modes.add_argument("--execute", action="store_true", help="build and execute plan")
    parser.add_argument("--regions", default="US", help="comma-separated regions")
    parser.add_argument("--k", type=int, default=5, help="top-N tools")
    parser.add_argument("--queries", default="docs/queries.txt", help="queries file")
    parser.add_argument("--seed", type=int, default=None, help="optional seed")
    args = parser.parse_args(argv)

    loader.load_all("registries")

    regions = [r.strip() for r in args.regions.split(',') if r.strip()]
    if not regions:
        regions = [""]
    queries = parse_queries(args.queries)

    artifact_dir = ensure_dir("artifacts")

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
            plan = orchestrator.build_plan(query, region, args.k, shortlist, loader.REGISTRY_CACHE.get("budget_controls"))
            if args.seed is not None:
                plan.run["seed"] = args.seed

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

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
