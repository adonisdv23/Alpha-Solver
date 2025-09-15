from __future__ import annotations

"""Utility helpers for normalising and freezing weight dictionaries."""

import math
from typing import Dict, Iterable, Tuple


def normalize(weights: Dict[str, float]) -> Dict[str, float]:
    """Return a new dictionary with non-negative values that sum to ``1.0``.

    ``NaN`` or ``inf`` values are treated as ``0.0``.  The returned dictionary has
    keys sorted alphabetically to guarantee deterministic ordering.
    """
    cleaned: list[Tuple[str, float]] = []
    for key in sorted(weights.keys()):
        value = float(weights.get(key, 0.0))
        if not math.isfinite(value) or value < 0.0:
            value = 0.0
        cleaned.append((key, value))
    total = sum(v for _, v in cleaned)
    if total <= 0.0:
        n = len(cleaned) or 1
        return {k: 1.0 / n for k, _ in cleaned}
    return {k: v / total for k, v in cleaned}


def freeze(weights: Dict[str, float]) -> Tuple[Tuple[str, float], ...]:
    """Return a deterministic tuple representation of ``weights``."""
    normed = normalize(weights)
    return tuple((k, normed[k]) for k in sorted(normed))
