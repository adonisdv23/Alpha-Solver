from __future__ import annotations

"""Command line interface for the budget simulator.

This tiny CLI is designed for tests.  It loads scenario decks, runs the
simulator and can emit JSON/CSV reports.  It also supports simple
before/after comparisons to help answer "what-if" questions about changing
model sets or budget caps.
"""

import argparse
import json
import pathlib
from glob import glob
from typing import Any, Dict, List
import yaml

from service.finops import simulator
from service.finops.simulator import Caps


def _load_scenarios(patterns: List[str]) -> List[Dict[str, Any]]:
    paths: List[str] = []
    for p in patterns:
        paths.extend(sorted(glob(p)))
    scenarios: List[Dict[str, Any]] = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    scenarios.append(json.loads(line))
    return scenarios


def _load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith(".json"):
            return json.load(f)
        return yaml.safe_load(f)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Budget simulator")
    parser.add_argument("--scenarios", nargs="+", required=True)
    parser.add_argument("--model-set", action="append")
    parser.add_argument("--max-cost-usd", type=float)
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--latency-budget-ms", type=float)
    parser.add_argument("--out-json")
    parser.add_argument("--out-csv")
    parser.add_argument("--before-config")
    parser.add_argument("--after-config")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)

    scenarios = _load_scenarios(args.scenarios)

    if args.before_config and args.after_config:
        before_cfg = _load_config(args.before_config)
        after_cfg = _load_config(args.after_config)
        result = simulator.compare(before_cfg, after_cfg, scenarios)
        summary = result["after"]["summary"]
        rows = result["after"]["scenarios"]
    else:
        model_set = (args.model_set or ["default"])[0]
        caps = Caps(
            max_cost_usd=args.max_cost_usd,
            max_tokens=args.max_tokens,
            latency_budget_ms=args.latency_budget_ms,
        )
        result = simulator.simulate(scenarios, model_set, caps=caps)
        summary = result["summary"]
        rows = result["scenarios"]

    if args.out_json:
        pathlib.Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

    if args.out_csv:
        import csv

        pathlib.Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
        with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "id",
                    "intent",
                    "model_set",
                    "route",
                    "est_tokens",
                    "est_cost_usd",
                    "est_latency_ms",
                    "verdict",
                ],
            )
            writer.writeheader()
            writer.writerows(rows)

    if args.summary_only:
        print(
            f"model_set={summary['model_set']} cost_usd={summary['total_cost_usd']:.4f} "
            f"tokens={summary['total_tokens']} p95_latency_ms={summary['p95_latency_ms']:.1f} "
            f"verdict={summary['budget_verdict']}"
        )

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(main())
