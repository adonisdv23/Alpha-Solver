from __future__ import annotations

"""Deterministic Chain-of-Thought guidance utilities."""

from typing import Any, Dict


def guidance_score(context: Dict[str, Any]) -> float:
    """Return a normalized guidance score based on ``context``.

    The score counts the presence of reasoning keywords inside the optional
    ``hint`` field of ``context`` and normalizes the result to ``[0, 1]``.
    """

    hint = context.get("hint", "").lower()
    keywords = ["therefore", "because", "thus"]
    matches = sum(1 for kw in keywords if kw in hint)
    return matches / len(keywords)
