import heapq

from alpha.reasoning.tot import TreeOfThoughtSolver, Node


def test_best_path_selector():
    solver = TreeOfThoughtSolver()
    frontier = []
    nodes = [
        Node(subquery="a", path=["a"], score=0.2, depth=1),
        Node(subquery="b", path=["b"], score=0.8, depth=1),
        Node(subquery="c", path=["c"], score=0.5, depth=1),
    ]
    for node in nodes:
        heapq.heappush(frontier, (-node.score, node))

    best = solver.best_path_selector(frontier)
    assert best.subquery == "b"
