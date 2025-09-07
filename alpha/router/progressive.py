from __future__ import annotations

"""Deterministic progressive complexity router."""

from dataclasses import dataclass
from typing import List

from alpha.reasoning.logging import log_event


@dataclass
class ProgressiveRouter:
    """Route between prompt profiles based on observed progress."""

    escalation: List[str]
    min_progress: float = 0.55
    _current: int = 0

    def profile(self) -> str:
        return self.escalation[self._current]

    def observe(self, depth: int, best_score: float) -> None:
        if depth <= len(self.escalation) - 1 and best_score < self.min_progress and self._current < depth:
            prev = self.escalation[self._current]
            self._current += 1
            new = self.escalation[self._current]
            log_event("router_escalate", **{"from": prev, "to": new, "reason": "low_progress"})

