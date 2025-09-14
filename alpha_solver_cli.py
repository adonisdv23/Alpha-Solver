from __future__ import annotations

import argparse
import json
from typing import Iterable, Tuple

from alpha_solver_entry import _tree_of_thought


def _parse_escalation(value: str) -> Tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def main(argv: Iterable[str] | None = None) -> None:  # pragma: no cover - thin CLI
    """CLI entry point for Alpha Solver."""

    ap = argparse.ArgumentParser(description="Alpha Solver Tree-of-Thought CLI")
    ap.add_argument("query")
    ap.add_argument("--multi-branch", action="store_true", help="Enable beam search")
    ap.add_argument("--max-width", type=int, default=3)
    ap.add_argument("--max-nodes", type=int, default=100)
    ap.add_argument("--enable-progressive-router", action="store_true", help="Enable router")
    ap.add_argument(
        "--router-escalation",
        default="basic,structured,constrained",
        help="Comma separated escalation stages",
    )
    ap.add_argument("--low-conf-threshold", type=float, default=0.35)
    ap.add_argument("--clarify-conf-threshold", type=float, default=0.55)
    ap.add_argument("--min-budget-tokens", type=int, default=256)
    ap.add_argument("--no-cot-fallback", action="store_true", help="Disable CoT fallback")
    args = ap.parse_args(list(argv) if argv is not None else None)

    result = _tree_of_thought(
        args.query,
        multi_branch=args.multi_branch,
        max_width=args.max_width,
        max_nodes=args.max_nodes,
        enable_progressive_router=args.enable_progressive_router,
        router_escalation=_parse_escalation(args.router_escalation),
        low_conf_threshold=args.low_conf_threshold,
        clarify_conf_threshold=args.clarify_conf_threshold,
        min_budget_tokens=args.min_budget_tokens,
        enable_cot_fallback=not args.no_cot_fallback,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":  # pragma: no cover
    main()
