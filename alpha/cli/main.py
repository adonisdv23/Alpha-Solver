"""Minimal CLI wrapping evaluation, gate checks and budget display."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from alpha.eval import harness
from alpha.core.config import get_quality_gate
from alpha.core import budgets as budgets_module
from alpha.routing import RouterV12
from alpha.core.metrics import compute_token_savings


def _cmd_eval_run(args: argparse.Namespace) -> None:
    report = harness.run(
        dataset=args.dataset,
        scorer_names=args.scorers.split(","),
        seed=args.seed,
        limit=args.limit,
    )
    out_dir = Path("artifacts/eval")
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "latest_report.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")
    print(report_path)


def _cmd_gate_check(args: argparse.Namespace) -> int:
    cfg = get_quality_gate()
    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    metrics = report.get("metrics", {})
    ok = True
    if metrics.get(cfg.primary_metric, 0.0) < cfg.min_accuracy:
        ok = False
    if metrics.get("p95_ms", 0) > cfg.max_p95_ms:
        ok = False
    if metrics.get("p99_ms", 0) > cfg.max_p99_ms:
        ok = False
    if metrics.get("cost_per_call", 0.0) > cfg.max_cost_per_call:
        ok = False
    if not ok:
        raise SystemExit(1)
    print("quality gate passed")
    return 0


def _cmd_budgets_show(args: argparse.Namespace) -> None:
    info = budgets_module.to_dict()
    for k, v in info.items():
        print(f"{k}: {v}")


def _cmd_router_simulate(args: argparse.Namespace) -> None:
    router = RouterV12()
    baseline = router.simulate(args.dataset, baseline=True)
    new = router.simulate(args.dataset, baseline=False)
    pct = compute_token_savings(baseline, new)
    report = {
        "token_savings_pct": pct,
        "pruned_branches": new["pruned_count"],
        "deterministic": True,
    }
    out_dir = Path("artifacts/eval")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "router_compare.json").write_text(json.dumps(report), encoding="utf-8")
    print(json.dumps(report))


def _cmd_solve(args: argparse.Namespace) -> None:
    if args.strategy == "react":
        from alpha.reasoning.react_lite import run_react_lite

        result = run_react_lite(args.prompt, seed=args.seed)
        print(f"{result['final_answer']} {result['confidence']}")
    else:
        from alpha_solver_entry import _tree_of_thought

        result = _tree_of_thought(args.prompt, seed=args.seed)
        print(result.get("final_answer"), result.get("confidence"))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="alpha.cli.main")
    sub = parser.add_subparsers(dest="command")

    # eval run
    eval_parser = sub.add_parser("eval")
    eval_sub = eval_parser.add_subparsers(dest="action")
    run_parser = eval_sub.add_parser("run")
    run_parser.add_argument("--dataset", required=True)
    run_parser.add_argument("--scorers", default="em")
    run_parser.add_argument("--seed", type=int, default=0)
    run_parser.add_argument("--limit", type=int, default=None)
    run_parser.set_defaults(func=_cmd_eval_run)

    # gate check
    gate_parser = sub.add_parser("gate")
    gate_sub = gate_parser.add_subparsers(dest="action")
    check_parser = gate_sub.add_parser("check")
    check_parser.add_argument("--report", required=True)
    check_parser.set_defaults(func=_cmd_gate_check)

    # budgets show
    budgets_parser = sub.add_parser("budgets")
    budgets_sub = budgets_parser.add_subparsers(dest="action")
    show_parser = budgets_sub.add_parser("show")
    show_parser.set_defaults(func=_cmd_budgets_show)

    # router simulate
    router_parser = sub.add_parser("router")
    router_sub = router_parser.add_subparsers(dest="action")
    sim_parser = router_sub.add_parser("simulate")
    sim_parser.add_argument("--dataset", required=True)
    sim_parser.add_argument("--seed", type=int, default=42)
    sim_parser.add_argument("--compare-baseline", action="store_true")
    sim_parser.set_defaults(func=_cmd_router_simulate)

    # solve
    solve_parser = sub.add_parser("solve")
    solve_parser.add_argument("--prompt", required=True)
    solve_parser.add_argument("--strategy", choices=["cot", "react", "tot"], default="cot")
    solve_parser.add_argument("--seed", type=int, default=0)
    solve_parser.set_defaults(func=_cmd_solve)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    return args.func(args) or 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
