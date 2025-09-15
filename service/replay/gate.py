from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .recorder import stable_hash


def _build_stable(route_explain: Dict[str, Any]) -> Dict[str, Any]:
    meta = route_explain.get("meta", {})
    subset = {
        "winner": route_explain.get("winner"),
        "scores_sorted": route_explain.get("scores_sorted", []),
        "gates": route_explain.get("gates", {}),
        "budget_verdict": route_explain.get("budget_verdict"),
        "meta": {
            "rules_sha": meta.get("rules_sha"),
            "gates_sha": meta.get("gates_sha"),
            "model_set": meta.get("model_set"),
        },
    }
    return subset


def _hash(route_explain: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    stable_obj = _build_stable(route_explain)
    return stable_hash(stable_obj), stable_obj


def _simulate_run(record: Dict[str, Any], seed: int, run_idx: int) -> Dict[str, Any]:
    base = record.get("result", 0)
    flap = record.get("flap")
    rnd_seed = seed if not flap else seed + run_idx
    rnd = random.Random(rnd_seed)
    noise = rnd.random() if record.get("noise", True) else 0.0
    winner = base + noise
    return {
        "winner": winner,
        "scores_sorted": [winner],
        "gates": {"g1": winner},
        "budget_verdict": "ok",
        "meta": {"rules_sha": "r", "gates_sha": "g", "model_set": "m"},
    }


def _diff_dict(expected: Dict[str, Any], actual: Dict[str, Any], prefix: str = "") -> List[Tuple[str, Any, Any]]:
    diffs: List[Tuple[str, Any, Any]] = []
    keys = set(expected) | set(actual)
    for key in keys:
        path = f"{prefix}.{key}" if prefix else key
        ev = expected.get(key)
        av = actual.get(key)
        if ev == av:
            continue
        if isinstance(ev, dict) and isinstance(av, dict):
            diffs.extend(_diff_dict(ev, av, path))
        else:
            diffs.append((path, ev, av))
    return diffs


def _format_diffs(diffs: List[Tuple[str, Any, Any]]) -> str:
    lines: List[str] = []
    for path, ev, av in diffs[:8]:
        if isinstance(ev, (int, float)) and isinstance(av, (int, float)):
            delta = av - ev
            lines.append(f"{path}: {ev:.6f}->{av:.6f} (\u0394={delta:+.6f})")
        else:
            lines.append(f"{path}: {ev}->{av}")
    return "; ".join(lines)


def determinism_gate(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Replay determinism gate")
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument(
        "--replay-file",
        default="data/datasets/replay/replay_small.jsonl",
    )
    parser.add_argument(
        "--skip-tags",
        default="known_flaky,external_tool_missing",
    )
    parser.add_argument("--timeout-ms", type=int, default=60000)
    parser.add_argument("--fast", action="store_true")
    args = parser.parse_args(argv)

    runs = args.runs
    if args.fast:
        runs = min(runs, 2)
    seed = args.seed
    start = time.time()
    replay_path = Path(args.replay_file)
    skip_tags = {t.strip() for t in args.skip_tags.split(",") if t.strip()}
    records: List[Dict[str, Any]] = []
    skipped = 0
    skipped_tags: set[str] = set()
    with replay_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            tags = rec.get("tags", [])
            if any(tag in skip_tags for tag in tags):
                skipped += 1
                for tag in tags:
                    if tag in skip_tags:
                        skipped_tags.add(tag)
                continue
            records.append(rec)

    print(
        f"determinism_gate: runs={runs} seed={seed} set={replay_path}",
        file=sys.stdout,
    )
    baseline_hashes: List[str] | None = None
    baseline_routes: List[Dict[str, Any]] | None = None
    for run_idx in range(runs):
        if (time.time() - start) * 1000 > args.timeout_ms:
            print("determinism_gate: TIMEOUT", file=sys.stdout)
            return 2
        hashes: List[str] = []
        routes: List[Dict[str, Any]] = []
        for rec in records:
            route = _simulate_run(rec, seed, run_idx)
            h, stable_obj = _hash(route)
            hashes.append(h)
            routes.append(stable_obj)
        if baseline_hashes is None:
            baseline_hashes = hashes
            baseline_routes = routes
            continue
        if hashes != baseline_hashes:
            assert baseline_routes is not None
            for i, (h0, h1) in enumerate(zip(baseline_hashes, hashes)):
                if h0 != h1:
                    diffs = _diff_dict(baseline_routes[i], routes[i])
                    diff_str = _format_diffs(diffs)
                    print(
                        f"determinism_gate: FAIL after run {run_idx + 1} — diffs: {diff_str}",
                        file=sys.stdout,
                    )
                    if skipped:
                        tags_list = ",".join(sorted(skipped_tags))
                        print(
                            f"skipped: {skipped} (tags=[{tags_list}])",
                            file=sys.stdout,
                        )
                    return 1
    print(
        f"determinism_gate: PASS ({runs}/{runs} stable)",
        file=sys.stdout,
    )
    if skipped:
        tags_list = ",".join(sorted(skipped_tags))
        print(
            f"skipped: {skipped} (tags=[{tags_list}])",
            file=sys.stdout,
        )
    return 0


if __name__ == "__main__":
    sys.exit(determinism_gate())
