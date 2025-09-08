"""Helper utilities for basic evaluation metrics."""
from __future__ import annotations

from typing import Dict


def compute_token_savings(baseline_stats: Dict[str, int], new_stats: Dict[str, int]) -> float:
    """Return percentage token savings between two runs.

    ``baseline_stats`` and ``new_stats`` must contain a ``tokens`` integer.
    The result is a fraction in ``[0, 1]``.
    """
    base = int(baseline_stats.get("tokens", 0))
    new = int(new_stats.get("tokens", 0))
    if base <= 0:
        return 0.0
    return max(0.0, (base - new) / base)


__all__ = ["compute_token_savings"]
