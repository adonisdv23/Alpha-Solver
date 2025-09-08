"""Simple scoring functions used by the evaluation harness."""
from __future__ import annotations

from typing import List


def _tokens(text: str) -> List[str]:
    return text.strip().split()


def em(prediction: str, target: str) -> float:
    """Exact match scorer."""
    return float(prediction.strip() == target.strip())


def f1(prediction: str, target: str) -> float:
    """Token level F1 scorer."""
    p_tokens = _tokens(prediction)
    t_tokens = _tokens(target)
    if not p_tokens or not t_tokens:
        return 0.0
    common = set(p_tokens) & set(t_tokens)
    if not common:
        return 0.0
    precision = len(common) / len(p_tokens)
    recall = len(common) / len(t_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


__all__ = ["em", "f1"]
