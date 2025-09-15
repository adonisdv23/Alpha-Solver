"""Router integration hooks for clarifier."""
from __future__ import annotations

from typing import Any, Dict, Tuple

from .clarifier import Clarifier
from . import trigger


def maybe_clarify(payload: Dict[str, Any], config: Any, templates: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Apply clarifier if confidence below threshold.

    Returns updated payload and route_explain metadata.
    """
    clarifier = Clarifier(templates)
    confidence = float(payload.get("confidence", 1.0))
    # consult trigger helper for decision
    clarify_flag, reason = trigger.should_clarify(
        decision=payload.get("decision", ""),
        confidence=confidence,
        budget_tokens=payload.get("budget_tokens", 0),
        policy_flags={},
    )
    # honour runtime config threshold
    threshold = getattr(config, "clarify_conf_threshold", trigger.CLARIFY_CONF_THRESHOLD)
    if confidence >= threshold:
        clarify_flag = False
        reason = "high_confidence"

    explain = {
        "clarify": {
            "triggered": clarify_flag,
            "reason": reason,
            "question": None,
            "answer_used": False,
            "deck_sha": clarifier.deck_sha,
        }
    }
    if not clarify_flag:
        return payload, explain

    question = clarifier.generate_question(payload)
    if not question:
        return payload, explain

    answer = payload.get("clarify_answer")
    new_payload = clarifier.merge_answer(payload, answer)
    explain["clarify"].update({"question": question, "answer_used": bool(answer)})
    return new_payload, explain
