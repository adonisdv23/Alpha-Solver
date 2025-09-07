from alpha.reasoning.tot import TreeOfThoughtSolver, Node


def test_path_scorer_deterministic_and_bounds():
    solver = TreeOfThoughtSolver()
    solver._query_tokens = {"solve", "x"}
    node = Node(content="Rephrase: solve x", path=("solve x", "Rephrase: solve x"), depth=1)
    score1 = solver.path_scorer(node)
    score2 = solver.path_scorer(node)
    assert 0 <= score1 <= 1
    assert score1 == score2 == round(score1, 3)


def test_path_scorer_penalizes_irrelevant_and_contradiction():
    solver = TreeOfThoughtSolver()
    solver._query_tokens = {"solve", "x"}
    relevant = Node(content="Rephrase: solve x", path=("solve x", "Rephrase: solve x"), depth=1)
    irrelevant = Node(content="unrelated", path=("solve x", "unrelated"), depth=1)
    contradiction = Node(content="This is impossible", path=("solve x", "This is impossible"), depth=1)
    score_rel = solver.path_scorer(relevant)
    score_irrel = solver.path_scorer(irrelevant)
    score_contra = solver.path_scorer(contradiction)
    assert score_rel > score_irrel
    assert score_contra < score_rel
