import pytest
from alpha.core import orchestrator
from alpha.core.governance import BudgetControls
from alpha.core.loader import REGISTRY_CACHE


def setup_module(_):
    REGISTRY_CACHE.clear()
    REGISTRY_CACHE["tools"] = [
        {"id": "tool.mock", "unit_cost": 1.0}
    ]
    REGISTRY_CACHE["adapters"] = {"families": {"default": "openai"}}


def test_under_budget():
    budget = BudgetControls(limit=5, action="instructions_only")
    plan = orchestrator.plan("pb", [{"tool_id": "tool.mock"}], budget=budget)
    assert plan["estimated_cost_usd"] == 1.0
    assert not plan.get("instructions_only")


def test_over_budget_downgrade():
    budget = BudgetControls(limit=0.5, action="instructions_only")
    plan = orchestrator.plan("pb", [{"tool_id": "tool.mock"}], budget=budget)
    assert plan["instructions_only"]


def test_over_budget_abort():
    budget = BudgetControls(limit=0.5, action="abort")
    with pytest.raises(RuntimeError):
        orchestrator.plan("pb", [{"tool_id": "tool.mock"}], budget=budget)
