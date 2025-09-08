"""Deterministic self-validation helpers for Chain-of-Thought outputs."""
from __future__ import annotations

import re
from typing import Iterable, List, Tuple


def _eval_simple_arithmetic(text: str) -> float | None:
    """Evaluate very small ``a op b`` expressions."""
    m = re.search(r"(\-?\d+(?:\.\d+)?)\s*([+\-*\/])\s*(\-?\d+(?:\.\d+)?)", text)
    if not m:
        return None
    a, op, b = m.groups()
    a_f = float(a)
    b_f = float(b)
    if op == "+":
        return a_f + b_f
    if op == "-":
        return a_f - b_f
    if op == "*":
        return a_f * b_f
    if op == "/":
        return a_f / b_f
    return None


def validate_answer(
    cot_steps: Iterable[str],
    final_answer: str,
    rules: List[str] | None = None,
) -> Tuple[bool, List[str]]:
    """Validate ``final_answer`` against ``cot_steps``.

    Two deterministic checks are performed:
    * numeric consistency via a tiny arithmetic evaluator
    * regex shape checks ensuring the answer matches at least one pattern
    """
    reasons: List[str] = []
    steps_text = "\n".join(cot_steps)

    expected = _eval_simple_arithmetic(steps_text)
    if expected is not None:
        try:
            provided = float(final_answer.strip())
        except ValueError:
            provided = None  # type: ignore[assignment]
        if provided is None or abs(provided - expected) > 1e-9:
            reasons.append("numeric_mismatch")

    patterns = [r"^.+$"] if not rules else list(rules)
    if not any(re.match(pat, final_answer) for pat in patterns):
        reasons.append("shape_mismatch")

    return (len(reasons) == 0, reasons)


__all__ = ["validate_answer"]
