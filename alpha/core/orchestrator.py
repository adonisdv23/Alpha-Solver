"""Simple orchestrator with budget and adapter selection"""
from __future__ import annotations
from typing import Dict, List

from .loader import REGISTRY_CACHE
from .governance import BudgetControls

from .plan import Plan, PlanStep


def _tool_cost(tool_id: str) -> float:
    tools = REGISTRY_CACHE.get("tools", [])
    if isinstance(tools, dict):
        tools = tools.get("tools", [])
    for t in tools:
        if t.get("id") == tool_id:
            return float(t.get("unit_cost", 0))
    return 0.0


def plan(playbook_id: str, shortlist: List[Dict], *, budget: BudgetControls | None = None) -> Dict:
    if budget is None:
        budget = BudgetControls.load()
    steps: List[PlanStep] = []
    adapters_cfg = REGISTRY_CACHE.get("adapters", {}).get("families", {"default": "openai"})
    default_adapter = adapters_cfg.get("default", "openai")
    breaker_cfg = REGISTRY_CACHE.get("circuit_breakers", {}).get("breakers", {}).get("default", {})
    for item in shortlist:
        tool_id = item.get("tool_id") or item.get("id")
        if tool_id is None:
            raise KeyError("tool_id")
        prompt = item.get("prompt", "")
        adapter = item.get("family") or default_adapter
        cost = _tool_cost(tool_id)
        steps.append(PlanStep(tool_id=tool_id, prompt=prompt, adapter=adapter, estimated_cost_usd=cost))
    total = sum(s.estimated_cost_usd for s in steps)
    result = Plan(steps=steps, estimated_cost_usd=total, breaker=breaker_cfg)
    verdict = budget.check_plan_cost(total)
    if not verdict["ok"]:
        if verdict["action"] == "instructions_only":
            result.instructions_only = True
        elif verdict["action"] == "abort":
            raise RuntimeError("budget exceeded")
    return {
        "steps": [s.__dict__ for s in result.steps],
        "estimated_cost_usd": result.estimated_cost_usd,
        "instructions_only": result.instructions_only,
        "breaker": result.breaker,
    }
