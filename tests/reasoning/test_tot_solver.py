from alpha.reasoning.tot import TreeOfThoughtSolver


def test_tot_solver_end_to_end():
    solver = TreeOfThoughtSolver(branching_factor=2, max_depth=2, score_threshold=0.95)
    result = solver.solve("start")
    assert result["solution"] == "start.2.1"
    assert result["path"] == ["start", "start.2", "start.2.1"]
    assert 0 <= result["score"] <= 1


def test_timeout_abort(caplog):
    solver = TreeOfThoughtSolver(timeout=0.0)
    with caplog.at_level("WARNING"):
        result = solver.solve("start")
    assert result["path"] == ["start"]
    assert any(rec.msg.get("reason") == "timeout" for rec in caplog.records)


def test_max_nodes_abort(caplog):
    solver = TreeOfThoughtSolver(max_nodes=0)
    with caplog.at_level("WARNING"):
        result = solver.solve("start")
    assert result["path"] == ["start"]
    assert any(rec.msg.get("reason") == "max_nodes" for rec in caplog.records)
