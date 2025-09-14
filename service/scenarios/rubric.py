from __future__ import annotations

"""Rubric for judging step expectations."""

import re
from typing import Any, Dict, Tuple


class Rubric:
    """Deterministic judging of adapter values against expectations."""

    def judge(self, expect: Dict[str, Any], value: Any) -> Tuple[bool, str]:
        """Return verdict and reason for value against expectations."""
        if not expect:
            return True, ""

        # equality -------------------------------------------------------
        if "equals" in expect:
            if value != expect["equals"]:
                return False, f"expected {expect['equals']!r} got {value!r}"

        if "contains" in expect:
            target = expect["contains"]
            if isinstance(value, (str, list, tuple)):
                if target not in value:
                    return False, f"{target!r} not in {value!r}"
            else:
                return False, f"value {value!r} has no containment"

        if "regex" in expect:
            pattern = expect["regex"]
            if not isinstance(value, str) or re.search(pattern, value) is None:
                return False, f"{value!r} does not match {pattern!r}"

        if "type" in expect:
            t = expect["type"]
            if t == "number":
                if not isinstance(value, (int, float)):
                    return False, f"{value!r} is not number"
            elif t == "string":
                if not isinstance(value, str):
                    return False, f"{value!r} is not string"

        if "approx" in expect:
            try:
                target = float(expect["approx"])
                epsilon = float(expect.get("epsilon", 1e-6))
                if not isinstance(value, (int, float)) or abs(value - target) > epsilon:
                    return False, f"{value!r} not within {epsilon} of {target}"
            except Exception:
                return False, "approx expects numeric value"

        return True, ""

    def to_route_explain(self, verdict: bool, reason: str) -> Dict[str, Any]:
        data = {"judged": bool(verdict)}
        if not verdict and reason:
            data["policy_verdict"] = reason
        return data
