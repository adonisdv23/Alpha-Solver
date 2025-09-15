from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from .recorder import stable_hash, redact


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _round_floats(obj: Any) -> Any:
    """Round floats recursively to 6 decimals for stability."""

    if isinstance(obj, float):
        return round(obj, 6)
    if isinstance(obj, list):
        return [_round_floats(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _round_floats(v) for k, v in obj.items()}
    return obj


def _stable_subset(route_explain: Dict[str, Any]) -> Dict[str, Any]:
    """Return canonical subset used for hashing."""

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
    return _round_floats(subset)


def _hash(route_explain: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    stable_obj = _stable_subset(route_explain)
    return stable_hash(stable_obj), stable_obj


def _simulate_run(record: Dict[str, Any], seed: int, run_idx: int) -> Dict[str, Any]:
    """Simulate a routing run.

    ``record`` may contain ``flap: true`` to introduce non determinism
    across runs which is useful in tests.
    """

    base = record.get("result", 0)
    flap = record.get("flap")
    rnd_seed = seed if not flap else seed + run_idx
    rnd = random.Random(rnd_seed)
    noise = rnd.random() if record.get("noise", True) else 0.0
    winner_val = base + noise
    return {
        "winner": f"model{int(winner_val * 1000)}",
        "scores_sorted": [winner_val],
        "gates": {"g1": winner_val},
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


def _format_diff(diffs: Sequence[Tuple[str, Any, Any]]) -> List[str]:
    lines: List[str] = []
    for path, ev, av in list(diffs)[:8]:
        ev_r = redact(ev)
        av_r = redact(av)
        lines.append(f"{path}: {ev_r}->{av_r}")
    return lines


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------

def run_file(
    replay_file: str,
    *,
    runs: int,
    seed: int,
    skip_tags: Iterable[str] | None = None,
) -> Dict[str, Any]:
    """Run determinism harness on ``replay_file``.

    Returns a summary dictionary with ``stable``, ``pass_pct`` and
    ``mismatches`` (first mismatch per record with diff tuples).
    """

    path = Path(replay_file)
    records: List[Dict[str, Any]] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            reason = rec.get("skip_reason", "")
            if skip_tags and any(tag in reason for tag in skip_tags):
                continue
            records.append(rec)

    mismatches: List[Dict[str, Any]] = []
    total = 0
    for rec in records:
        total += 1
        base_route = _simulate_run(rec, seed, 0)
        base_hash, base_subset = _hash(base_route)
        mismatch: List[Tuple[str, Any, Any]] | None = None
        for run_idx in range(1, runs):
            route = _simulate_run(rec, seed, run_idx)
            run_hash, run_subset = _hash(route)
            if run_hash != base_hash and mismatch is None:
                mismatch = _diff_dict(base_subset, run_subset)
        if mismatch:
            mismatches.append({"id": rec.get("id"), "diff": mismatch})

    pass_pct = 100.0
    if total:
        pass_pct = 100.0 * (total - len(mismatches)) / total

    return {
        "seed": seed,
        "runs": runs,
        "set": str(path),
        "stable": not mismatches,
        "pass_pct": round(pass_pct, 2),
        "mismatches": mismatches,
    }


def format_mismatch(mismatch: Dict[str, Any]) -> List[str]:
    """Return formatted diff lines for a mismatch entry."""

    return _format_diff(mismatch.get("diff", []))
