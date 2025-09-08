"""Deterministic path scoring utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Protocol, Callable


class PathScorer(Protocol):
    """Protocol for pluggable path scorers."""

    def score(self, *, node_text: str, context: Dict[str, object]) -> float:  # pragma: no cover - protocol
        ...


@dataclass
class LexicalScorer:
    """Simple lexical keyword based scorer.

    The score combines relevance of ``node_text`` to ``context['query_tokens']``
    and a depth based progress term.  The combined score is normalised to
    ``[0, 1]``.
    """

    def score(self, *, node_text: str, context: Dict[str, object]) -> float:
        tokens = set(str(node_text).lower().split())
        query_tokens = set(context.get("query_tokens", set()))
        relevance = len(tokens & query_tokens) / max(len(query_tokens), 1)
        depth = int(context.get("depth", 0))
        max_depth = int(context.get("max_depth", 1))
        progress = max(0.0, 1 - (depth / max(max_depth, 1)))
        raw = 0.4 * relevance + 0.3 * progress
        return round(max(0.0, min(1.0, raw / 0.7 if 0.7 else raw)), 3)


@dataclass
class ConstraintScorer:
    """Penalty scorer that checks for obvious contradictions."""

    negatives: tuple[str, ...] = ("contradiction", "inconsistent", "impossible")

    def score(self, *, node_text: str, context: Dict[str, object]) -> float:
        text = str(node_text).lower()
        return 0.0 if any(term in text for term in self.negatives) else 1.0


@dataclass
class CompositeScorer:
    """Weighted composite over registered scorers."""

    weights: Dict[str, float]

    def score(self, *, node_text: str, context: Dict[str, object]) -> float:
        total = 0.0
        for name, weight in self.weights.items():
            if name == "composite":
                continue
            factory = SCORERS.get(name)
            if not factory:
                continue
            scorer = factory() if callable(factory) else factory
            total += weight * scorer.score(node_text=node_text, context=context)
        return round(max(0.0, min(1.0, total)), 3)


# Registry of scorer factories
SCORERS: Dict[str, Callable[..., PathScorer]] = {
    "lexical": LexicalScorer,
    "constraint": ConstraintScorer,
    "composite": lambda weights=None: CompositeScorer(
        weights or {"lexical": 0.6, "constraint": 0.4}
    ),
}


__all__ = ["PathScorer", "SCORERS", "LexicalScorer", "ConstraintScorer", "CompositeScorer"]
