from __future__ import annotations

from typing import Callable, Dict


def scorer_em(pred: str, ref: str) -> float:
    """Exact match scorer."""
    return float(pred.strip() == ref.strip())


def scorer_f1(pred: str, ref: str) -> float:
    """Token-level F1 scorer."""
    pred_tokens = pred.split()
    ref_tokens = ref.split()
    if not pred_tokens or not ref_tokens:
        return 0.0
    common = set(pred_tokens) & set(ref_tokens)
    if not common:
        return 0.0
    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(ref_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


SCORERS: Dict[str, Callable[[str, str], float]] = {
    "em": scorer_em,
    "f1": scorer_f1,
}
