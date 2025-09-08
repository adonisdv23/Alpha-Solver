from __future__ import annotations

"""Deterministic Chain-of-Thought guidance utilities."""

from typing import Any, Dict, List


def guidance_score(context: Dict[str, Any]) -> float:
    """Return a normalized guidance score based on ``context``.

    The score counts the presence of reasoning keywords inside the optional
    ``hint`` field of ``context`` and normalizes the result to ``[0, 1]``.
    """

    hint = context.get("hint", "").lower()
    keywords = ["therefore", "because", "thus"]
    matches = sum(1 for kw in keywords if kw in hint)
    return matches / len(keywords)


def run_cot(query: str, seed: int, max_steps: int) -> Dict[str, Any]:
    """Return a deterministic Chain-of-Thought fallback response.

    Parameters
    ----------
    query:
        Original user query.
    seed:
        Unused seed maintained for deterministic signature.
    max_steps:
        Maximum number of reasoning steps to emit.
    """

    steps: List[str] = [f"step_{i}: {query}" for i in range(1, max_steps + 1)]
    return {
        "answer": f"To proceed, consider: {query}",
        "confidence": 0.50,
        "steps": steps,
    }
