from __future__ import annotations

from typing import Any, Callable, Dict

from .recorder import canonical_json, stable_hash
from .snapshot import compute_snapshot


class ReplayMismatch(AssertionError):
    """Raised when replay differs from recorded state."""


def _diff(expected: Dict[str, Any], actual: Dict[str, Any]) -> Dict[str, Any]:
    diff: Dict[str, Any] = {}
    keys = set(expected) | set(actual)
    for key in keys:
        ev = expected.get(key)
        av = actual.get(key)
        if ev == av:
            continue
        if isinstance(ev, dict) and isinstance(av, dict):
            nested = _diff(ev, av)
            if nested:
                diff[key] = nested
        else:
            diff[key] = {"expected": ev, "actual": av}
    return diff


class Player:
    def __init__(self, snapshot_fn: Callable[[], Dict[str, Any]] | None = None) -> None:
        self.snapshot_fn = snapshot_fn or compute_snapshot

    def replay(
        self,
        record: Dict[str, Any],
        run_func: Callable[[Dict[str, Any], int], tuple[str, Dict[str, Any]]],
    ) -> Dict[str, Any]:
        seed = record["seed"]
        payload = record["payload"]
        current_snapshot = self.snapshot_fn()
        output, route_explain = run_func(payload, seed)
        hash_input = {
            "snapshot": current_snapshot,
            "route_explain": {
                "scores": route_explain.get("scores"),
                "gate_decisions": route_explain.get("gate_decisions"),
                "plan_winner": route_explain.get("plan_winner"),
                "budget_verdict": route_explain.get("budget_verdict"),
            },
        }
        current_hash = stable_hash(hash_input)

        diffs: Dict[str, Any] = {}
        if current_snapshot != record["snapshot"]:
            diffs["snapshot"] = _diff(record["snapshot"], current_snapshot)
        if route_explain != record["route_explain"]:
            diffs["route_explain"] = _diff(record["route_explain"], route_explain)
        if current_hash != record["hash"]:
            diffs["hash"] = {"expected": record["hash"], "actual": current_hash}

        if diffs:
            raise ReplayMismatch(canonical_json(diffs))

        return {"output": output, "hash": current_hash, "route_explain": route_explain}
