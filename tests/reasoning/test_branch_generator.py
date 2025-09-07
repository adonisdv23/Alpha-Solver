from alpha.reasoning.tot import TreeOfThoughtSolver, Node


def test_branch_generator():
    solver = TreeOfThoughtSolver(branching_factor=2)
    root = Node(subquery="q", path=["q"], score=0.0, depth=0)
    branches = solver.branch_generator(root)
    assert [b.subquery for b in branches] == ["q.1", "q.2"]
    assert all(b.depth == 1 for b in branches)
