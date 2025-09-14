"""Prompt deck selector."""
from __future__ import annotations

from typing import Any, Dict, Tuple


# Mapping from deck names to required context keys
_DECK_KEYS = {
    "generic": ["task"],
    "web_extract": ["url", "goal", "fields"],
    "sheets_ops": ["op", "sheet", "values"],
    "policy_clarify": ["missing_fields"],
}


def _normalize_value(value: Any) -> Any:
    """Strip whitespace from strings and items inside lists."""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return [_normalize_value(v) for v in value]
    return value


def choose_deck(context: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """Choose a prompt deck and minimal render context.

    Deterministic rules:
      - if context.get("intent") == "browse" -> "web_extract"
      - elif context.get("intent") == "sheet" -> "sheets_ops"
      - elif context.get("clarify", False) -> "policy_clarify"
      - else -> "generic"
    """

    intent = (context.get("intent") or "").strip()
    deck = "generic"
    if intent == "browse":
        deck = "web_extract"
    elif intent == "sheet":
        deck = "sheets_ops"
    elif bool(context.get("clarify", False)):
        deck = "policy_clarify"

    keys = _DECK_KEYS[deck]
    render_ctx: Dict[str, Any] = {}
    for k in keys:
        if k in context:
            render_ctx[k] = _normalize_value(context[k])
        else:
            # ensure key exists for template substitution
            if k in ("fields", "values", "missing_fields"):
                render_ctx[k] = []
            else:
                render_ctx[k] = ""
    return deck, render_ctx

