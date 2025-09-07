from alpha.reasoning.tot import TreeOfThoughtSolver, Node


def test_path_scorer_context_and_normalization():
    solver = TreeOfThoughtSolver()
    base = Node(id=0, subquery="q", path=("q",), score=0.0, depth=0)
    hinted = Node(
        id=1,
        subquery="q",
        path=("q",),
        score=0.0,
        depth=0,
        context={"hint": "because"},
    )
    base_score = solver.path_scorer(base)
    hinted_score = solver.path_scorer(hinted)
    assert 0 <= base_score <= 1
    assert 0 <= hinted_score <= 1
    assert hinted_score > base_score


def test_path_scorer_deterministic_with_context():
    solver = TreeOfThoughtSolver()
    node1 = Node(id=0, subquery="q", path=("q",), score=0.0, depth=0, context={"hint": "thus"})
    node2 = Node(id=1, subquery="q", path=("q",), score=0.0, depth=0, context={"hint": "thus"})
    assert solver.path_scorer(node1) == solver.path_scorer(node2)
