import pytest
from service.budget.guard import BudgetGuard


@pytest.mark.budget
def test_budget_guard_over_and_under_thresholds():
    guard = BudgetGuard(max_cost_usd=1.0, max_tokens=100)

    below = {"totals": {"cost_usd": 0.9, "tokens": 90}}
    res = guard.check(below)
    assert res["ok"]
    assert res["budget_verdict"] == "ok"
    assert res["route_explain"]["decision"] == "allow"

    near = {"totals": {"cost_usd": 1.0, "tokens": 100}}
    res_near = guard.check(near)
    assert res_near["ok"]
    assert res_near["budget_verdict"] == "ok"

    over_cost = {"totals": {"cost_usd": 1.01, "tokens": 90}}
    res_over_cost = guard.check(over_cost)
    assert not res_over_cost["ok"]
    assert res_over_cost["budget_verdict"] == "over_cost"
    assert res_over_cost["route_explain"]["budget_verdict"] == "over_cost"
    assert res_over_cost["route_explain"]["decision"] == "block"

    over_tokens = {"totals": {"cost_usd": 0.5, "tokens": 101}}
    res_over_tokens = guard.check(over_tokens)
    assert not res_over_tokens["ok"]
    assert res_over_tokens["budget_verdict"] == "over_tokens"
    assert res_over_tokens["route_explain"]["budget_verdict"] == "over_tokens"
    assert res_over_tokens["route_explain"]["decision"] == "block"
