from alpha.reasoning.tot import TreeOfThoughtSolver, Node


def test_prune_threshold():
    solver = TreeOfThoughtSolver(prune_threshold=0.6)
    low = Node(subquery="a", path=["a"], score=0.5, depth=1)
    high = Node(subquery="b", path=["b"], score=0.7, depth=1)
    assert solver._retrace_and_prune(low) is True
    assert solver._retrace_and_prune(high) is False
