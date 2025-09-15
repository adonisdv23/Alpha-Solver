"""Prompt/Template clarifier core."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from . import render, trigger

MAX_QUESTION_CHARS = 120
MAX_USER_ECHO = 256


@dataclass
class Clarifier:
    """Generate and merge clarification questions."""

    templates: Dict[str, Any]

    def __post_init__(self) -> None:
        # Build a mapping of clarifier templates for quick rendering.
        mapping: Dict[str, str] = {}
        for tpl in self.templates.get("templates", []):
            if tpl.get("intent") == "clarify":
                mapping[tpl["id"]] = tpl.get("user", "")
        self._templates = mapping
        self.deck_sha = render.deck_sha(mapping)
        self.last_template: Optional[str] = None

    # ------------------------------------------------------------------
    def detect(self, payload: Dict[str, Any]) -> Tuple[bool, str]:
        """Detect if clarification is required and return (flag, reason)."""
        reasons = []
        confidence = float(payload.get("confidence", 1.0))
        if confidence < trigger.CLARIFY_CONF_THRESHOLD:
            reasons.append("low_confidence")
        if payload.get("missing_fields"):
            reasons.append("missing_fields")
        if payload.get("ambiguous"):
            reasons.append("ambiguous")
        if payload.get("contradictory"):
            reasons.append("contradictory_intent")
        triggered = bool(reasons)
        return triggered, reasons[0] if triggered else "pass"

    # ------------------------------------------------------------------
    def generate_question(self, payload: Dict[str, Any]) -> str:
        """Generate a concise clarification question."""
        template_key = trigger.choose_template(payload)
        question = render.render(template_key, payload, self._templates).strip()
        if len(question) > MAX_QUESTION_CHARS:
            question = question[:MAX_QUESTION_CHARS]
        self.last_template = template_key
        return question

    # ------------------------------------------------------------------
    def merge_answer(self, payload: Dict[str, Any], answer: Optional[str]) -> Dict[str, Any]:
        """Merge the user clarification answer into the payload."""
        merged = dict(payload)
        if answer:
            merged["intent"] = answer.strip()[:MAX_USER_ECHO]
            merged["clarify_answer"] = merged["intent"]
        return merged
