from alpha.reasoning.tot import TreeOfThoughtSolver, Node


def test_best_path_selector_greedy_and_max_depth():
    solver = TreeOfThoughtSolver(branching_factor=2, max_depth=1, seed=42)
    solver._query_tokens = set()

    def custom_branch(parent: Node) -> list[Node]:
        return [
            Node(content="high", path=parent.path + ("high",), depth=parent.depth + 1, score=0.6, id=solver._next_id()),
            Node(content="low", path=parent.path + ("low",), depth=parent.depth + 1, score=0.5, id=solver._next_id()),
        ]

    solver.branch_generator = custom_branch  # type: ignore

    root = Node(content="root", path=("root",), depth=0, score=0.4, id=solver._next_id())
    best = solver.best_path_selector(root)
    assert best.content == "high"
    assert best.depth == 1


def test_best_path_selector_tiebreak():
    solver = TreeOfThoughtSolver(branching_factor=2, max_depth=1, seed=42)
    solver._query_tokens = set()

    def custom_branch(parent: Node) -> list[Node]:
        return [
            Node(content="b", path=parent.path + ("b",), depth=parent.depth + 1, score=0.6, id=solver._next_id()),
            Node(content="a", path=parent.path + ("a",), depth=parent.depth + 1, score=0.6, id=solver._next_id()),
        ]

    solver.branch_generator = custom_branch  # type: ignore

    root = Node(content="root", path=("root",), depth=0, score=0.4, id=solver._next_id())
    best = solver.best_path_selector(root)
    assert best.content == "a"
