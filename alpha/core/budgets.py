"""Helpers for displaying evaluation budgets."""
from __future__ import annotations

from dataclasses import dataclass, asdict

from .config import get_quality_gate


@dataclass
class Budgets:
    min_accuracy: float
    max_p95_ms: int
    max_p99_ms: int
    max_cost_per_call: float


def get_budgets() -> Budgets:
    cfg = get_quality_gate()
    return Budgets(
        cfg.min_accuracy,
        cfg.max_p95_ms,
        cfg.max_p99_ms,
        cfg.max_cost_per_call,
    )


def to_dict() -> dict:
    return asdict(get_budgets())


__all__ = ["Budgets", "get_budgets", "to_dict"]
