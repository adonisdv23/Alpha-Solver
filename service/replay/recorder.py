import hashlib
import json
import re
from typing import Any, Callable, Dict

from .snapshot import compute_snapshot


def redact(value: Any) -> Any:
    """Redact PII by removing digits from strings recursively."""
    if isinstance(value, str):
        return re.sub(r"\d", "X", value)
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


def canonical_json(data: Any) -> str:
    """Canonical JSON with sorted keys and stable float formatting."""
    def float_handler(obj: Any) -> Any:
        if isinstance(obj, float):
            return f"{obj:.6f}"
        raise TypeError()

    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=float_handler)


def stable_hash(data: Any) -> str:
    canonical = canonical_json(data)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class Recorder:
    """Simple deterministic recorder."""

    def __init__(self, snapshot_fn: Callable[[], Dict[str, Any]] | None = None) -> None:
        self.snapshot_fn = snapshot_fn or compute_snapshot

    def record(
        self,
        scenario: str,
        payload: Dict[str, Any],
        *,
        seed: int,
        run_func: Callable[[Dict[str, Any], int], tuple[str, Dict[str, Any]]],
        model_id: str = "model",
        provider_id: str = "provider",
        options: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Record a scenario using ``run_func``."""
        sanitized = redact(payload)
        opts = options or {}
        snapshot = self.snapshot_fn()
        output, route_explain = run_func(sanitized, seed)
        hash_input = {
            "snapshot": snapshot,
            "route_explain": {
                "scores": route_explain.get("scores"),
                "gate_decisions": route_explain.get("gate_decisions"),
                "plan_winner": route_explain.get("plan_winner"),
                "budget_verdict": route_explain.get("budget_verdict"),
            },
        }
        record_hash = stable_hash(hash_input)
        return {
            "scenario": scenario,
            "payload": sanitized,
            "options": opts,
            "seed": seed,
            "model_id": model_id,
            "provider_id": provider_id,
            "snapshot": snapshot,
            "route_explain": route_explain,
            "output": output,
            "hash": record_hash,
        }
