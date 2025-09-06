"""Execute plan steps with governance checks"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .plan import Plan
from .governance import (
    AuditLogger,
    BudgetCapGate,
    CircuitBreaker,
    GovernanceError,
    PolicyDryRun,
)
from .prompt_writer import PromptWriter
from alpha.adapters import ADAPTERS


def snapshot_shortlist(region: str, query_hash: str, shortlist: List[Dict[str, Any]]) -> str:
    """Persist top-k shortlist snapshot for audits; returns file path."""
    topk = int(os.getenv("ALPHA_SNAPSHOT_TOPK", "5"))
    art_root = os.getenv("ALPHA_ARTIFACTS_DIR", "artifacts")
    path = Path(art_root) / "shortlists" / str(region) / f"{query_hash}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    items = []
    for rank, item in enumerate(shortlist[:topk], 1):
        items.append({
            "rank": rank,
            "tool_id": str(item.get("id") or item.get("tool_id")),
            "score": float(item.get("score", 0.0)),
            "prior": float(item.get("prior", 0.0)),
        })
    rec = {
        "region": region,
        "query_hash": query_hash,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "items": items,
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False)
    return str(path)


class Runner:
    def __init__(self) -> None:
        self.budget_gate = BudgetCapGate(
            max_steps=int(os.getenv("ALPHA_BUDGET_STEPS", "100"))
        )
        self.circuit_breaker = CircuitBreaker(
            max_errors=int(os.getenv("ALPHA_MAX_ERRORS", "5"))
        )
        self.audit_logger = AuditLogger("logs/governance_audit.jsonl")
        self.dryrun = PolicyDryRun(
            enabled=os.getenv("ALPHA_POLICY_DRYRUN", "0") == "1"
        )
        self.writer = PromptWriter()

    def solve(self, plan: Dict, *, execute: bool = False) -> List[Dict]:
        trace: List[Dict] = []
        self.audit_logger.log_event("query", {"steps": len(plan.get("steps", []))})
        for idx, step in enumerate(plan.get("steps", []), 1):
            try:
                self.budget_gate.check(idx)
            except GovernanceError as err:
                self.audit_logger.log_event("budget.exceeded", {"step": idx})
                self.dryrun.handle(err)
                if not self.dryrun.enabled:
                    break
            self.audit_logger.log_event("step.start", {"tool_id": step.get("tool_id")})
            try:
                adapter_name = step.get("adapter")
                if adapter_name in ADAPTERS and not execute:
                    adapter = ADAPTERS[adapter_name]()
                    prompt = adapter.render_prompt(step)
                    path = self.writer.write(idx - 1, prompt)
                    trace.append({"tool_id": step.get("tool_id"), "prompt_path": str(path)})
                else:
                    trace.append({"tool_id": step.get("tool_id"), "executed": True})
            except Exception as e:
                try:
                    self.circuit_breaker.record_error()
                except GovernanceError as err:
                    self.audit_logger.log_event("breaker.tripped", {})
                    self.dryrun.handle(err)
                    if not self.dryrun.enabled:
                        break
                if not self.dryrun.enabled:
                    raise e
        return trace


def run(plan: Dict, *, execute: bool = False) -> List[Dict]:
    runner = Runner()
    trace = runner.solve(plan, execute=execute)
    plan["audit_log"] = str(runner.audit_logger.path)
    return trace


def run_plan(plan: Plan, local_only: bool = True) -> List[Dict]:
    """Execute a Plan dataclass; external steps skipped when local_only."""
    wrapper = {
        "steps": [s.to_dict() for s in plan.steps],
        "breaker": plan.guards.circuit_breakers,
    }
    trace = run(wrapper, execute=not local_only)
    plan.guards.audit = {"log_path": wrapper.get("audit_log")}
    return trace

