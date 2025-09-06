"""Governance helpers: budget controls, policy gates, audit logging"""
from __future__ import annotations
import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List
import uuid

from .loader import parse_yaml_lite


class GovernanceError(RuntimeError):
    """Raised when a governance policy blocks execution."""


# ---------------- Budget Controls ----------------

@dataclass
class BudgetControls:
    limit: float
    action: str

    @classmethod
    def load(cls, path: str = "config/budget_controls.yaml") -> "BudgetControls":
        p = Path(path)
        data = {}
        if p.exists():
            data = parse_yaml_lite(p.read_text(encoding="utf-8"))
        conf = data.get("budgets", {}).get("default", {})
        limit = float(conf.get("limit", float("inf")))
        action = conf.get("over_budget_action", "abort")
        return cls(limit=limit, action=action)

    def check_plan_cost(self, cost: float) -> Dict[str, object]:
        ok = cost <= self.limit
        result = {
            "ok": ok,
            "limit": self.limit,
            "actual": cost,
            "action": "allow" if ok else self.action,
        }
        return result


class BudgetCapGate:
    """Enforce a maximum number of steps in a run."""

    def __init__(self, max_steps: int):
        self.max_steps = int(max_steps)

    def check(self, step_count: int) -> None:
        if step_count > self.max_steps:
            raise GovernanceError(f"budget exceeded: {step_count} > {self.max_steps}")


class CircuitBreaker:
    """Trip after too many errors within a time window."""

    def __init__(self, max_errors: int, window: int = 60):
        self.max_errors = int(max_errors)
        self.window = int(window)
        self._errors: List[datetime] = []

    def record_error(self) -> None:
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(seconds=self.window)
        self._errors = [t for t in self._errors if t >= cutoff]
        self._errors.append(now)
        if self.max_errors and len(self._errors) > self.max_errors:
            raise GovernanceError("circuit breaker tripped")


class AuditLogger:
    """Append governance audit events as JSON lines."""

    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.session_id = str(uuid.uuid4())

    def log_event(self, event: str, data: Dict[str, object] | None = None) -> None:
        rec = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "session_id": self.session_id,
            "event": event,
            "data": data or {},
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


class PolicyDryRun:
    """When enabled, governance errors are logged but not raised."""

    def __init__(self, enabled: bool = False):
        self.enabled = bool(enabled)

    def handle(self, err: GovernanceError) -> None:
        if self.enabled:
            logging.warning("policy dry-run: %s", err)
        else:
            raise err


# ---------------- Data Classification ----------------


@dataclass
class EnforcementReport:
    downgraded: List[int] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


class DataClassifier:
    def __init__(self, rules: List[Dict[str, str]]):
        self.rules = rules

    @staticmethod
    def load(path: str = "config/data_classification.yaml") -> "DataClassifier":
        p = Path(path)
        rules: List[Dict[str, str]] = []
        if p.exists():
            data = parse_yaml_lite(p.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                rules = data.get("rules", []) or []
        return DataClassifier(rules)

    def enforce(self, plan, *, dryrun: bool = False) -> EnforcementReport:
        report = EnforcementReport()
        for idx, step in enumerate(plan.steps):
            prompt = step.prompt.lower()
            for rule in self.rules:
                pattern = rule.get("match", "")
                action = rule.get("action", "")
                if pattern and re.search(pattern, prompt):
                    note = f"step{idx}:{action}:{pattern}"
                    report.notes.append(note)
                    if action == "instructions_only" and not dryrun:
                        step.mode = "instructions_only"
                        report.downgraded.append(idx)
                    break
        return report
