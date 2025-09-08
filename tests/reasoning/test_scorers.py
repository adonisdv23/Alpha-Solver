from alpha.reasoning.scoring import SCORERS, CompositeScorer


def test_lexical_scorer_deterministic():
    scorer = SCORERS["lexical"]()
    ctx = {"query_tokens": {"solve", "x"}, "depth": 1, "max_depth": 5}
    s1 = scorer.score(node_text="solve x", context=ctx)
    s2 = scorer.score(node_text="solve x", context=ctx)
    assert 0 <= s1 <= 1
    assert s1 == s2


def test_constraint_scorer_penalty():
    scorer = SCORERS["constraint"]()
    ctx = {}
    ok = scorer.score(node_text="all good", context=ctx)
    bad = scorer.score(node_text="impossible case", context=ctx)
    assert ok == 1.0 and bad == 0.0


def test_composite_weights_and_rounding():
    comp = CompositeScorer({"lexical": 0.5, "constraint": 0.5})
    ctx = {"query_tokens": {"a"}, "depth": 0, "max_depth": 1}
    score = comp.score(node_text="a", context=ctx)
    assert isinstance(score, float)
    assert round(score, 3) == score
