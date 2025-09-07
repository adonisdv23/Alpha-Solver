from alpha.reasoning.tot import TreeOfThoughtSolver


def _run():
    solver = TreeOfThoughtSolver(seed=42)
    return solver.solve("solve x")


def test_tot_solver_deterministic_and_confident():
    r1, r2, r3 = _run(), _run(), _run()
    assert r1["answer"] == r2["answer"] == r3["answer"]
    assert r1["confidence"] == r2["confidence"] == r3["confidence"]
    assert len(r1["path"]) == len(r2["path"]) == len(r3["path"])
    assert r1["confidence"] >= 0.70
    assert r1["reason"] == "ok"


def test_tot_solver_below_threshold():
    solver = TreeOfThoughtSolver(seed=42, score_threshold=0.9)
    result = solver.solve("impossible question")
    assert result["reason"] == "below_threshold"
    assert result["confidence"] < 0.9
