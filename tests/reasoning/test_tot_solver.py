from alpha.reasoning.tot import TreeOfThoughtSolver


def test_tot_solver_end_to_end():
    solver = TreeOfThoughtSolver(branching_factor=2, max_depth=2, score_threshold=0.95)
    result = solver.solve("start")
    assert result["solution"] == "start.2.2"
    assert result["path"] == ["start", "start.2", "start.2.2"]
    assert 0 <= result["score"] <= 1
