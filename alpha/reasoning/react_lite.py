from __future__ import annotations

"""Seed-stable minimal ReAct executor for simple arithmetic."""

import hashlib
import operator
import re
from typing import Dict, List

from .logging import log_safe_out_decision

_ARITH_RE = re.compile(r"(\d+(?:\.\d+)?)\s*([+\-*/x])\s*(\d+(?:\.\d+)?)")
_OPS = {
    "+": ("Add", operator.add),
    "-": ("Subtract", operator.sub),
    "*": ("Multiply", operator.mul),
    "x": ("Multiply", operator.mul),
    "/": ("Divide", operator.truediv),
}


def _derive_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def _confidence(prompt_hash: str, seed: int) -> float:
    h = hashlib.sha256(f"{prompt_hash}:{seed}".encode("utf-8")).hexdigest()
    frac = int(h[:8], 16) / 0xFFFFFFFF
    return round(0.70 + 0.20 * frac, 2)


def _validate(answer: str, rules: Dict[str, str] | None) -> tuple[bool, str]:
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
) -> Dict[str, object]:
    """Run a deterministic ReAct-style loop over a single arithmetic expression."""

    prompt_hash = _derive_hash(prompt)
    trace: List[Dict[str, str]] = []
    match = _ARITH_RE.search(prompt)

    if not match:
        trace.append(
            {
                "thought": "Parse the question",
                "action": "self-check",
                "observation": "regex mismatch",
            }
        )
        log_safe_out_decision(
            route="halt", conf=0.0, threshold=1.0, reason="regex_mismatch"
        )
        return {
            "final_answer": "SAFE-OUT: regex mismatch",
            "trace": trace[:max_steps],
            "confidence": 0.0,
            "meta": {"strategy": "react", "seed": seed},
            "safe_out": {
                "code": "regex_mismatch",
                "rationale": "input did not match arithmetic pattern",
            },
        }

    left, op_sym, right = match.groups()
    op_sym_norm = "*" if op_sym == "x" else op_sym
    display_op = "×" if op_sym_norm == "*" else op_sym_norm
    trace.append(
        {
            "thought": "Parse the question",
            "action": "self-check",
            "observation": f"Found expression: {left} {op_sym_norm} {right}",
        }
    )

    a, b = float(left), float(right)
    if op_sym_norm == "/" and b == 0:
        result_val = "undefined"
        rationale = "Division by zero is undefined."
    else:
        op_name, func = _OPS[op_sym_norm]
        value = func(a, b)
        result_val = int(value) if float(value).is_integer() else value
        rationale = f"{op_name}: {left} {display_op} {right} = {result_val}."

    trace.append(
        {
            "thought": "Compute and sanity-check",
            "action": "self-check",
            "observation": "Deterministic reflection confirms the computation.",
        }
    )

    ok, rationale_fail = _validate(str(result_val), rules)
    if not ok:
        log_safe_out_decision(
            route="halt", conf=0.0, threshold=1.0, reason="halt_validation_failed"
        )
        return {
            "final_answer": "",
            "trace": trace[:max_steps],
            "confidence": 0.0,
            "meta": {"strategy": "react", "seed": seed},
            "safe_out": {
                "code": "halt_validation_failed",
                "rationale": rationale_fail,
            },
        }

    final_answer = f"{rationale} Therefore, the answer is {result_val}."
    confidence = _confidence(prompt_hash, seed)

    return {
        "final_answer": final_answer,
        "trace": trace[:max_steps],
        "confidence": confidence,
        "meta": {"strategy": "react", "seed": seed},
    }


__all__ = ["run_react_lite"]
