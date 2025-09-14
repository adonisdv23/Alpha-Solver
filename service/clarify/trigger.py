"""Clarify trigger helpers."""
from __future__ import annotations

from typing import Tuple, Optional, Dict, Any

# confidence thresholds mirror gating defaults
LOW_CONF_THRESHOLD: float = 0.35
CLARIFY_CONF_THRESHOLD: float = 0.55


def should_clarify(*, decision: str, confidence: float, budget_tokens: int, policy_flags: Dict[str, Any]) -> Tuple[bool, str]:
    """Decide whether to clarify.

    Parameters
    ----------
    decision: str
        Upstream decision flag. If set to ``"clarify"`` we always clarify.
    confidence: float
        Model confidence score between 0 and 1.
    budget_tokens: int
        Current token budget (unused, placeholder for future logic).
    policy_flags: dict
        Additional policy flags (unused).

    Returns
    -------
    tuple(bool, str)
        Clarify flag and reason code.
    """
    if decision == "clarify":
        return True, "decision_flag"
    if LOW_CONF_THRESHOLD <= confidence < CLARIFY_CONF_THRESHOLD:
        return True, "mid_confidence"
    return False, "pass"


def choose_template(context: Dict[str, Any]) -> str:
    """Choose a clarification template key based on context flags."""
    if context.get("missing_fields"):
        return "ask_missing_fields"
    if context.get("ambiguous"):
        return "disambiguate_intent"
    if context.get("tool_first"):
        return "pick_tool_first"
    if context.get("low_budget"):
        return "reduce_scope_low_budget"
    return "generic_clarify"


def to_route_explain(clarify: bool, reason: str, template_key: Optional[str], deck_sha_str: str) -> Dict[str, Any]:
    """Build route explanation payload."""
    return {
        "decision": "clarify" if clarify else "pass",
        "reason": reason,
        "template": template_key,
        "deck_sha": deck_sha_str,
    }
