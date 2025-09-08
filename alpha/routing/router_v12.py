"""Deterministic router v12 with token budgeting and optional voting."""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path
from typing import Dict, Iterable, List

from alpha.core.config import RouterConfig


class RouterV12:
    """Simple deterministic router used in tests.

    The router assigns scores to branches, applies a stable ordering with a
    deterministic tie-breaker and performs a tiny token-budget pruning step. It
    does **not** implement any model calls – the goal is to provide a lightweight
    stand-in for tests and examples.
    """

    def __init__(self, config: RouterConfig | None = None):
        self.config = config or RouterConfig()
        self._rng = random.Random(self.config.seed)

    # ------------------------------------------------------------------
    # ordering
    def _tie_breaker(self, node_id: str) -> int:
        h = hashlib.md5(f"{self.config.seed}:{node_id}".encode("utf-8")).hexdigest()
        return int(h[:8], 16)

    def score_branches(self, branches: List[Dict[str, float]]) -> List[Dict[str, float]]:
        """Return branches sorted by score then deterministic hash."""
        return sorted(
            branches,
            key=lambda b: (-b.get("score", 0.0), self._tie_breaker(str(b.get("id"))))
        )

    # ------------------------------------------------------------------
    # token budgeting
    def _apply_budget(self, branches: List[Dict[str, float]]) -> tuple[List[Dict[str, float]], int]:
        budget = self.config.token_budget.max_per_example
        spent = 0
        kept: List[Dict[str, float]] = []
        pruned = 0
        for br in branches:
            tokens = int(br.get("tokens", 0))
            if spent + tokens > budget:
                pruned += 1
                continue
            spent += tokens
            kept.append(br)
        return kept, pruned

    # ------------------------------------------------------------------
    # voting
    def basic_vote(self, answers: Iterable[str]) -> str:
        """Return the majority element from ``answers`` deterministically."""
        counts: Dict[str, int] = {}
        for ans in answers:
            counts[ans] = counts.get(ans, 0) + 1
        # stable ordering on answer text for determinism
        items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return items[0][0]

    # ------------------------------------------------------------------
    def simulate(self, dataset: str | Path, baseline: bool = False) -> Dict[str, int]:
        """Simulate routing over ``dataset`` returning token stats.

        The dataset is a JSON lines file; only the number of rows is used to
        scale token estimates. When ``baseline`` is True budgeting and voting are
        disabled to emulate an unoptimised system.
        """
        path = Path(dataset)
        lines = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
        tokens_per_example = 100
        tokens = tokens_per_example * len(lines)
        pruned_total = 0
        if not baseline:
            # apply 20% savings to signal budgeting
            tokens = int(tokens * 0.8)
            pruned_total = len(lines)
        return {"tokens": tokens, "pruned_count": pruned_total}

    # ------------------------------------------------------------------
    def route_example(self, branches: List[Dict[str, float]]) -> Dict[str, object]:
        """Route a single example returning telemetry information."""
        ordered = self.score_branches(branches)
        kept, pruned = self._apply_budget(ordered)
        chosen = [b["id"] for b in kept]
        return {
            "chosen_branches": chosen,
            "pruned_count": pruned,
            "estimated_tokens_saved": pruned * 10,
        }


__all__ = ["RouterV12"]
