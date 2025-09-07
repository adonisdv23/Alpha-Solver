import heapq

from alpha.reasoning.tot import TreeOfThoughtSolver, Node


def test_best_path_selector():
    solver = TreeOfThoughtSolver()
    frontier = []
    nodes = [
        Node(id=1, subquery="a", path=("a",), score=0.2, depth=1),
        Node(id=2, subquery="b", path=("b",), score=0.8, depth=1),
        Node(id=3, subquery="c", path=("c",), score=0.5, depth=1),
    ]
    for node in nodes:
        heapq.heappush(frontier, (-node.score, node.path, node.id, node))

    best = solver.best_path_selector(frontier)
    assert best.subquery == "b"
