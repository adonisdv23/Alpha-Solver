"""Deterministic helper agents for router v12."""

from __future__ import annotations

import re
from typing import Dict, List, Tuple


def decomposer(query: str) -> List[str]:
    """Split ``query`` into ordered deterministic subgoals.

    The splitter uses simple comma/``and`` rules so the output is predictable
    and requires no external models.
    """

    parts = [p.strip() for p in re.split(r",|and", query) if p.strip()]
    return parts or [query]


def checker(step_text: str) -> Dict[str, bool]:
    """Return deterministic rule checks for ``step_text``.

    The current implementation exposes a tiny set of boolean features used by
    higher-level scoring logic.
    """

    return {
        "has_numbers": bool(re.search(r"\d", step_text)),
        "has_operator": bool(re.search(r"[+\-*/]", step_text)),
        "is_question": step_text.strip().endswith("?"),
    }


def calculator(expr: str) -> Tuple[bool, str]:
    """Parse and evaluate a small arithmetic subset.

    Only binary ``+``, ``-``, ``*`` and ``/`` expressions are supported.  The
    function returns a ``(ok, result_str)`` tuple where ``ok`` is ``True`` when
    the expression parsed and executed successfully.  Division by zero and
    malformed expressions return ``False``.
    """

    match = re.fullmatch(
        r"\s*([-+]?\d+(?:\.\d+)?)\s*([+\-*/])\s*([-+]?\d+(?:\.\d+)?)\s*",
        expr,
    )
    if not match:
        return False, "unsupported"
    a, op, b = match.groups()
    a_f, b_f = float(a), float(b)
    try:
        if op == "+":
            res = a_f + b_f
        elif op == "-":
            res = a_f - b_f
        elif op == "*":
            res = a_f * b_f
        else:  # division
            if b_f == 0:
                return False, "division_by_zero"
            res = a_f / b_f
    except Exception:
        return False, "error"

    if res.is_integer():
        return True, str(int(res))
    return True, str(res)


AGENTS_V12 = {
    "decomposer": decomposer,
    "checker": checker,
    "calculator": calculator,
}


__all__ = ["AGENTS_V12", "decomposer", "checker", "calculator"]
