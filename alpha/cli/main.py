"""Minimal CLI wrapping evaluation, gate checks and budget display."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from alpha.eval import harness
from alpha.core.config import get_quality_gate
from alpha.core import budgets as budgets_module


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
