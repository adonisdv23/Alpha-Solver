"""Execute plan steps with circuit breaker and audit logging"""
from __future__ import annotations
from typing import Dict, List

from .plan import Plan

from .governance import CircuitBreaker, AuditLogger
from .prompt_writer import PromptWriter
from alpha.adapters import ADAPTERS


def run(plan: Dict, *, execute: bool = False) -> List[Dict]:
    breaker_conf = plan.get("breaker", {})
    trip_count = breaker_conf.get("trip_count", 0)
    breaker = CircuitBreaker(trip_count=trip_count)
    audit = AuditLogger()
    writer = PromptWriter()
    trace: List[Dict] = []
    for idx, step in enumerate(plan.get("steps", [])):
        audit.log({"event": "step.start", "tool_id": step.get("tool_id")})
        if not breaker.allow():
            audit.log({"event": "breaker.tripped"})
            break
        adapter_name = step.get("adapter")
        if adapter_name in ADAPTERS and not execute:
            adapter = ADAPTERS[adapter_name]()
            prompt = adapter.render_prompt(step)
            path = writer.write(idx, prompt)
            trace.append({"tool_id": step.get("tool_id"), "prompt_path": str(path)})
        else:
            trace.append({"tool_id": step.get("tool_id"), "executed": True})
    plan["audit_log"] = str(audit.path)
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
