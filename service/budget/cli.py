from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from .guard import BudgetGuard
from .simulator import load_cost_models, simulate


def _read_items(path: Path) -> List[Dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        items: List[Dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                items.append(json.loads(line))
        return items
    if suffix == ".json":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("JSON must be a list of items")
        return data
    raise ValueError(f"Unsupported file extension: {suffix}")


def _scrub(obj: Any) -> Any:
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            if k == "pii_raw" or k.endswith("_token") or k.endswith("_secret"):
                continue
            result[k] = _scrub(v)
        return result
    if isinstance(obj, list):
        return [_scrub(v) for v in obj]
    return obj


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Budget simulation and guard")
    parser.add_argument("--provider", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--items", required=True)
    parser.add_argument("--max-cost", type=float, required=True)
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--jsonl-out")

    args = parser.parse_args(argv)

    try:
        items = _read_items(Path(args.items))
        cost_models = load_cost_models()
        sim_result = simulate(items, cost_models, provider=args.provider, model=args.model)
        guard = BudgetGuard(max_cost_usd=args.max_cost, max_tokens=args.max_tokens)
        verdict = guard.check(sim_result)
    except Exception as exc:  # invalid input
        print(f"error: {exc}", file=sys.stderr)
        final = {
            "provider": args.provider,
            "model": args.model,
            "budget_verdict": "error",
            "totals": {},
        }
        print(json.dumps(final, sort_keys=True))
        return 1

    if args.jsonl_out:
        out_path = Path(args.jsonl_out)
        with out_path.open("w", encoding="utf-8") as f:
            for item in sim_result["items"]:
                f.write(json.dumps(_scrub(item), sort_keys=True) + "\n")

    totals = sim_result["totals"]
    summary = (
        f"cost_usd={totals['cost_usd']:.4f} "
        f"tokens={totals['tokens']} "
        f"verdict={verdict['budget_verdict']}"
    )
    print(summary)
    final = {
        "provider": sim_result["provider"],
        "model": sim_result["model"],
        "budget_verdict": verdict["budget_verdict"],
        "totals": totals,
    }
    print(json.dumps(final, sort_keys=True))
    return 0 if verdict["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
