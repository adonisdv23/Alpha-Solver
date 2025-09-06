from __future__ import annotations
import re
from difflib import SequenceMatcher
from typing import Iterable, Tuple

_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")

def _tokens(s: str) -> set[str]:
    return set(t.lower() for t in _TOKEN_RE.findall(s))

def jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    A, B = set(a), set(b)
    if not A and not B:
        return 1.0
    if not A or not B:
        return 0.0
    return len(A & B) / float(len(A | B))

def seq_ratio(a: str, b: str) -> float:
    a = " ".join(_TOKEN_RE.findall(a.lower()))
    b = " ".join(_TOKEN_RE.findall(b.lower()))
    return SequenceMatcher(None, a, b).ratio()

def hybrid_score(
    query: str,
    candidate_text: str,
    lexical_score: float,
    weights: Tuple[float, float, float] = (0.60, 0.25, 0.15),
) -> float:
    """Compose lexical score with two cheap semantic-ish signals.
    Returns a value in [0,1] (clamped), deterministic for given inputs.
    """
    jw = jaccard(_tokens(query), _tokens(candidate_text))
    sr = seq_ratio(query, candidate_text)
    w1, w2, w3 = weights
    total = w1 * float(lexical_score) + w2 * jw + w3 * sr
    if total < 0.0:
        return 0.0
    if total > 1.0:
        return 1.0
    return total
