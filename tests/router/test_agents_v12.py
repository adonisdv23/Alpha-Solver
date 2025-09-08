from alpha.router.agents_v12 import AGENTS_V12, calculator, checker, decomposer


def test_decomposer_splits() -> None:
    assert decomposer("1+1 and 2+2") == ["1+1", "2+2"]


def test_checker_features() -> None:
    res = checker("2 + 2")
    assert res["has_numbers"] is True
    assert res["has_operator"] is True
    assert res["is_question"] is False


def test_calculator_eval() -> None:
    ok, val = calculator("2+2")
    assert ok and val == "4"
    ok2, _ = calculator("2/0")
    assert ok2 is False


def test_integration_order_and_score() -> None:
    q = "1+1 and 2+2"
    baseline = [q]
    base_score = sum(1 for s in baseline if calculator(s)[0])
    with_agents = decomposer(q)
    agent_score = sum(1 for s in with_agents if calculator(s)[0])
    assert with_agents != baseline
    assert agent_score > base_score
    # registry exposes deterministic ordering
    assert list(AGENTS_V12.keys()) == ["decomposer", "checker", "calculator"]
