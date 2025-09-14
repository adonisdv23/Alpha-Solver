"""Decision rules for scoring and ranking plans.

This module provides small, deterministic helpers for scoring candidate
plans and ranking them with a deterministic tiebreak chain.  The weights
and normalisation factors are loaded from a YAML configuration file.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import yaml


# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def load_weights(path: str = "config/decision_rules.yaml") -> Dict[str, Any]:
    """Load weights configuration from *path*.

    Parameters
    ----------
    path:
        Path to a YAML file containing the weights, normalisation factors and
        tiebreak configuration.
    """
    with open(Path(path), "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    validate_weights(data)
    return data


def validate_weights(weights: Dict[str, Any]) -> None:
    """Validate the shape of a weights configuration.

    Raises
    ------
    ValueError
        If required keys are missing or malformed.
    """
    if not isinstance(weights, dict):
        raise ValueError("weights must be a dict")

    required_top = {"weights", "norms", "tiebreak"}
    if not required_top.issubset(weights):
        raise ValueError("weights config missing sections")

    w = weights["weights"]
    n = weights["norms"]
    tb = weights["tiebreak"]

    required_weights = {
        "confidence",
        "tool_first",
        "cost_tokens",
        "steps",
        "risk",
        "latency_ms",
    }
    required_norms = {"cost_tokens_div", "steps_div", "latency_ms_div"}

    if not required_weights.issubset(w):
        raise ValueError("weights section missing fields")
    if not required_norms.issubset(n):
        raise ValueError("norms section missing fields")
    if not isinstance(tb, list) or not tb:
        raise ValueError("tiebreak must be a non-empty list")
    for rule in tb:
        if not isinstance(rule, str) or ":" not in rule:
            raise ValueError("invalid tiebreak rule")
        field, direction = rule.split(":", 1)
        if direction not in {"asc", "desc"} or not field:
            raise ValueError("invalid tiebreak rule")


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _normalise(value: float, div: float) -> float:
    """Simple min/div normalisation capped at 1.0."""
    if div <= 0:
        return 0.0
    return min(value / div, 1.0)


def score_plan(plan: Dict[str, Any], weights: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
    """Score a plan according to configured weights.

    Returns the numeric score and an explanation dictionary.
    """
    w = weights["weights"]
    n = weights["norms"]
    tiebreak_fields = [rule.split(":", 1)[0] for rule in weights["tiebreak"]]

    confidence = float(plan.get("confidence", 0.0))
    tool_first = 1.0 if plan.get("tool_first") else 0.0
    cost_norm = _normalise(float(plan.get("cost_tokens", 0)), float(n["cost_tokens_div"]))
    steps_norm = _normalise(float(plan.get("steps", 0)), float(n["steps_div"]))
    risk = float(plan.get("risk", 0.0))
    latency_norm = _normalise(float(plan.get("latency_ms", 0)), float(n["latency_ms_div"]))

    components = {
        "confidence": w["confidence"] * confidence,
        "tool_first": w["tool_first"] * tool_first,
        "cost_tokens": -w["cost_tokens"] * cost_norm,
        "steps": -w["steps"] * steps_norm,
        "risk": -w["risk"] * risk,
        "latency_ms": -w["latency_ms"] * latency_norm,
    }

    score = sum(components.values())
    explain = {
        "score": score,
        "components": components,
        "tiebreak_chain": tiebreak_fields,
    }
    return score, explain


# ---------------------------------------------------------------------------
# Ranking
# ---------------------------------------------------------------------------

def _tiebreak_key(plan: Dict[str, Any], tiebreak: Iterable[str]) -> Tuple[Any, ...]:
    key: List[Any] = [-plan["_score"]]
    for rule in tiebreak:
        field, direction = rule.split(":", 1)
        value = plan.get(field)
        if isinstance(value, bool):
            value = 1 if value else 0
        if isinstance(value, (int, float)):
            key.append(-value if direction == "desc" else value)
        else:
            value = "" if value is None else str(value)
            if direction == "desc":
                # Simple string inversion for descending order
                value = "".join(chr(255 - ord(c)) for c in value)
            key.append(value)
    return tuple(key)


def rank_plans(plans: List[Dict[str, Any]], weights: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return a new list of plans sorted by score and tiebreak chain."""
    ranked: List[Dict[str, Any]] = []
    for plan in plans:
        score, explain = score_plan(plan, weights)
        new_plan = dict(plan)
        new_plan["_score"] = score
        new_plan["_explain"] = explain
        ranked.append(new_plan)

    tiebreak = weights["tiebreak"]
    ranked.sort(key=lambda p: _tiebreak_key(p, tiebreak))
    return ranked

