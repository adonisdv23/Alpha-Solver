"""Plan assembly orchestrator"""
from __future__ import annotations
from typing import Dict, List, Any

from .loader import REGISTRY_CACHE
from .plan import Plan, PlanStep, Guardrails
from .paths import timestamp_rfc3339z
from .governance import BudgetControls


def _tool_cost(tool_id: str) -> float:
    tools = REGISTRY_CACHE.get("tools", [])
    if isinstance(tools, dict):
        tools = tools.get("tools", [])
    for t in tools:
        if t.get("id") == tool_id:
            try:
                return float(t.get("unit_cost", 0))
            except Exception:
                return 0.0
    return 0.0


def build_plan(query: str, region: str, k: int, shortlist: List[Dict[str, Any]], budget_cfg: Dict[str, Any] | None) -> Plan:
    """Construct a Plan from selector shortlist without executing."""
    timestamp = timestamp_rfc3339z()

    steps: List[PlanStep] = []
    adapters_cfg = REGISTRY_CACHE.get("adapters", {}).get("families", {"default": "openai"})
    default_adapter = adapters_cfg.get("default", "openai")
    for item in shortlist[:k]:
        tool_id = item.get("tool_id") or item.get("id")
        if tool_id is None:
            continue
        prompt = item.get("prompt", "")
        adapter = item.get("family") or default_adapter
        reasons = item.get("reasons", {})
        confidence = item.get("confidence")
        cost = _tool_cost(tool_id)
        steps.append(
            PlanStep(
                tool_id=tool_id,
                prompt=prompt,
                adapter=adapter,
                reasons=reasons,
                confidence=confidence,
                estimated_cost_usd=cost,
            )
        )

    total = sum(s.estimated_cost_usd for s in steps)
    guards = Guardrails(
        budget=budget_cfg or {},
        circuit_breakers=REGISTRY_CACHE.get("circuit_breakers", {}),
        audit={}
    )

    plan = Plan(
        version="1.0",
        run={"timestamp": timestamp, "region": region, "query": query, "seed": None},
        inputs={"k": k, "region": region, "query": query, "shortlist_ref": None},
        steps=steps,
        guards=guards,
        fallbacks=[],
        artifacts={"shortlist_snapshot": None, "plan_path": None},
        estimated_cost_usd=total,
    )
    return plan


def plan(playbook_id: str, shortlist: List[Dict[str, Any]], *, budget: BudgetControls | None = None) -> Dict[str, Any]:
    """Compatibility wrapper returning a dict as earlier versions did."""
    if budget is None:
        budget = BudgetControls.load()
    plan_obj = build_plan(playbook_id, "", len(shortlist), shortlist, None)
    total = plan_obj.estimated_cost_usd
    verdict = budget.check_plan_cost(total)
    instructions_only = False
    if not verdict["ok"]:
        if verdict["action"] == "instructions_only":
            instructions_only = True
        elif verdict["action"] == "abort":
            raise RuntimeError("budget exceeded")
    return {
        "steps": [s.to_dict() for s in plan_obj.steps],
        "estimated_cost_usd": total,
        "instructions_only": instructions_only,
        "breaker": plan_obj.guards.circuit_breakers,
    }
