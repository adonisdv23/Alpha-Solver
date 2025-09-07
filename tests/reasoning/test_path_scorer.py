from alpha.reasoning.tot import TreeOfThoughtSolver, Node


def test_path_scorer_deterministic_normalized():
    solver = TreeOfThoughtSolver()
    node1 = Node(subquery="q", path=["q"], score=0.0, depth=0)
    node2 = Node(subquery="q", path=["q"], score=0.0, depth=0)
    score1 = solver.path_scorer(node1)
    score2 = solver.path_scorer(node2)
    assert 0 <= score1 <= 1
    assert score1 == score2
