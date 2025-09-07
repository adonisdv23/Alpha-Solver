from alpha.reasoning.tot import TreeOfThoughtSolver, Node


def test_default_prune_threshold():
    solver = TreeOfThoughtSolver()
    best = 0.9
    low = Node(id=1, subquery="a", path=("a",), score=0.6, depth=1)
    high = Node(id=2, subquery="b", path=("b",), score=0.8, depth=1)
    assert solver._retrace_and_prune(low, best) is True
    assert solver._retrace_and_prune(high, best) is False


def test_custom_prune_threshold():
    solver = TreeOfThoughtSolver()
    best = 0.9
    node = Node(id=3, subquery="c", path=("c",), score=0.7, depth=1)
    assert solver._retrace_and_prune(node, best, threshold=0.9) is True
    node2 = Node(id=4, subquery="d", path=("d",), score=0.7, depth=1)
    assert solver._retrace_and_prune(node2, best, threshold=0.5) is False
