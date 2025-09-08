"""Simplified governance engine with budget caps and audit logging.

This module mirrors :mod:`alpha.policy.engine` but emits audit records with an
``event_type`` field for easier downstream analytics.  It purposely keeps the
implementation small and deterministic to remain suitable for offline tests.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Decision:
    """Policy decision returned by :class:`GovernanceEngine`."""

    decision: str  # "allow" | "block" | "warn"
    reason: str


class GovernanceEngine:
    """Minimal governance engine with budgets and a circuit breaker."""

    def __init__(
        self,
        *,
        max_steps: int = 0,
        max_seconds: float = 0.0,
        breaker_max_fails: int = 0,
        dry_run: bool = False,
        audit_path: str = "artifacts/policy_audit.jsonl",
    ) -> None:
        self.max_steps = int(max_steps)
        self.max_seconds = float(max_seconds)
        self.breaker_max_fails = int(breaker_max_fails)
        self.dry_run = bool(dry_run)
        self.audit_path = Path(audit_path)
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)

        self.run_id = uuid.uuid4().hex
        self.start = time.time()
        self.steps = 0
        self.fails = 0

    # ------------------------------------------------------------------
    def _log(self, rec: Dict[str, object]) -> None:
        rec = dict(rec)
        rec.setdefault("event_type", "policy_audit")
        rec.setdefault("run_id", self.run_id)
        rec["timestamp"] = datetime.now(timezone.utc).isoformat().replace(
            "+00:00", "Z"
        )
        with self.audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # ------------------------------------------------------------------
    def decide(
        self,
        *,
        query: str = "",
        region: str = "",
        tool_id: str = "",
        family: str = "",
        tags: Optional[List[str]] = None,
    ) -> Decision:
        """Return policy decision for the next step and audit it."""

        tags = tags or []
        step_index = self.steps + 1
        elapsed = time.time() - self.start

        budget = {
            "steps": step_index,
            "max_steps": self.max_steps,
            "elapsed_s": round(elapsed, 3),
            "max_seconds": self.max_seconds,
        }
        breaker = {
            "fails": self.fails,
            "max_fails": self.breaker_max_fails,
            "tripped": self.breaker_max_fails > 0
            and self.fails >= self.breaker_max_fails,
        }

        decision = "allow"
        reason = ""
        if self.max_steps and step_index > self.max_steps:
            decision, reason = "block", "max_steps exceeded"
        elif self.max_seconds and elapsed > self.max_seconds:
            decision, reason = "block", "max_seconds exceeded"
        elif breaker["tripped"]:
            decision, reason = "block", "circuit breaker tripped"

        audit_decision = decision
        if self.dry_run and decision == "block":
            audit_decision = "warn"
            decision = "allow"

        self._log(
            {
                "decision": audit_decision,
                "reason": reason,
                "query": query,
                "region": region,
                "tool_id": tool_id,
                "family": family,
                "tags": tags,
                "budget": budget,
                "breaker": breaker,
            }
        )
        return Decision(audit_decision if self.dry_run else decision, reason)

    def record_step_result(self, success: bool) -> None:
        """Update counters after step execution."""

        if success:
            self.fails = 0
        else:
            self.fails += 1
        self.steps += 1


__all__ = ["Decision", "GovernanceEngine"]

