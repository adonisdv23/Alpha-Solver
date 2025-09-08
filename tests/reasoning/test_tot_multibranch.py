from alpha.reasoning.tot import TreeOfThoughtSolver


def test_multi_branch_width_and_nodes():
    solver = TreeOfThoughtSolver(multi_branch=True, max_width=2, max_nodes=2, seed=42)
    result = solver.solve("test question")
    assert result["explored_nodes"] <= 2
    assert len(result["path"]) <= solver.max_depth + 1
