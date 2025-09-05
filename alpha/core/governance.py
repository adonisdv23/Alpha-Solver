"""Governance helpers: budget controls, circuit breakers, audit logging"""
from __future__ import annotations
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

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
