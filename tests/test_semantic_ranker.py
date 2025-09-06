from alpha.core.semantic import hybrid_score

def test_hybrid_score_basic():
    q = "zapier automation"
    a = "Zapier – automate your apps"
    b = "Completely unrelated tool"
    s_a = hybrid_score(q, a, lexical_score=0.4)
    s_b = hybrid_score(q, b, lexical_score=0.4)
    assert s_a > s_b

def test_hybrid_score_bounds():
    s = hybrid_score("x", "y", lexical_score=2.0)
    assert 0.0 <= s <= 1.0
