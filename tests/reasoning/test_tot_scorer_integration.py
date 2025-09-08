from alpha.reasoning.tot import TreeOfThoughtSolver


def test_tot_default_composite():
    solver = TreeOfThoughtSolver()
    res = solver.solve("solve x")
    assert res["answer"] == "solve x"
    assert res["confidence"] == 1.0


def test_tot_lexical_only():
    solver = TreeOfThoughtSolver(scorer="lexical")
    res = solver.solve("impossible question")
    assert res["confidence"] <= 1.0
