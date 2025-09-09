from __future__ import annotations

"""Seed-stable minimal ReAct executor without external tools."""

import hashlib
import re
from typing import Dict, List, Tuple, Any

from .logging import log_safe_out_decision


def _derive_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def _step_hash(seed: int, step: int, prompt_hash: str) -> str:
    data = f"{seed}:{step}:{prompt_hash}".encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _confidence(prompt_hash: str, seed: int) -> float:
    h = hashlib.sha256(f"{prompt_hash}:{seed}".encode("utf-8")).hexdigest()
    # map to [0.70, 0.99]
    frac = int(h[:8], 16) / 0xFFFFFFFF
    return round(0.70 + 0.29 * frac, 2)


def _validate(answer: str, rules: Dict[str, str] | None) -> Tuple[bool, str]:
    if not rules:
        return True, ""
    for name, pattern in rules.items():
        if not re.match(pattern, answer):
            return False, f"rule {name} failed"
    return True, ""


def run_react_lite(
    prompt: str,
    seed: int,
    max_steps: int = 2,
    rules: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    """Run a deterministic ReAct-style loop without tools."""

    prompt_hash = _derive_hash(prompt)
    trace: List[Dict[str, str]] = []
    for idx in range(1, max_steps + 1):
        h = _step_hash(seed, idx, prompt_hash)[:8]
        trace.append(
            {
                "thought": f"t{idx}:{h}",
                "action": "self-check",
                "observation": "deterministic reflection",
            }
        )
    final_answer = f"{prompt_hash[:8]}"
    ok, rationale = _validate(final_answer, rules)
    confidence = _confidence(prompt_hash, seed)
    result: Dict[str, Any] = {
        "final_answer": final_answer if ok else "",
        "trace": trace,
        "confidence": confidence if ok else 0.0,
        "meta": {"strategy": "react", "seed": seed},
    }
    if not ok:
        log_safe_out_decision(
            route="halt", conf=0.0, threshold=1.0, reason="halt_validation_failed"
        )
        result["safe_out"] = {
            "code": "halt_validation_failed",
            "rationale": rationale,
        }
    return result


__all__ = ["run_react_lite"]
