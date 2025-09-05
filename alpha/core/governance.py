"""Governance helpers: budget controls, circuit breakers, audit logging"""
from __future__ import annotations
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, List

from .loader import parse_yaml_lite

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

# ---------------- Circuit Breaker ----------------

@dataclass
class CircuitBreaker:
    trip_count: int
    count: int = 0
    tripped: bool = False

    @classmethod
    def load(cls, path: str = "config/circuit_breakers.yaml") -> "CircuitBreaker":
        p = Path(path)
        data = {}
        if p.exists():
            data = parse_yaml_lite(p.read_text(encoding="utf-8"))
        conf = data.get("breakers", {}).get("default", {})
        return cls(trip_count=int(conf.get("trip_count", 0)))

    def allow(self) -> bool:
        if self.tripped:
            return False
        self.count += 1
        if self.trip_count and self.count > self.trip_count:
            self.tripped = True
            return False
        return True

# ---------------- Audit Logger ----------------

class AuditLogger:
    """Write audit events as JSON lines"""

    def __init__(self, base_dir: str = "artifacts/audit"):
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.path = Path(base_dir) / f"run_{ts}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event: Dict[str, object]):
        event = dict(event)
        event["ts"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


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
