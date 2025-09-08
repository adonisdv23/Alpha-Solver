"""Lightweight deterministic accounting utilities."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

_DETERMINISTIC = os.getenv("ALPHA_DETERMINISM") == "1"


@dataclass
class Accountant:
    """Track expansions and simulated token counts."""

    expansions: int = 0
    sim_tokens: int = 0
    start: float = 0.0 if _DETERMINISTIC else time.time()

    def record(self, text: str) -> None:
        """Record an expansion for ``text``."""

        self.expansions += 1
        self.sim_tokens += len(text.split())

    def summary(self) -> dict:
        """Return a summary dictionary."""

        elapsed = 0.0 if _DETERMINISTIC else time.time() - self.start
        return {
            "expansions": self.expansions,
            "sim_tokens": self.sim_tokens,
            "elapsed_ms": int(elapsed * 1000),
        }


__all__ = ["Accountant"]
