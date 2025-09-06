import json
from pathlib import Path

from alpha.core.registry_provider import RegistryProvider
from alpha.core.freshness import blend


def final_score(lex, jw, sr, prior, rec, weights, rec_w):
    w1, w2, w3 = weights
    hybrid = max(0.0, min(1.0, w1 * lex + w2 * jw + w3 * sr))
    base = hybrid * prior
    return blend(base, rec, rec_w)


def test_aggregator_output_matches_golden():
    rp = RegistryProvider()
    rp.load()
    res = rp.shortlist("analytics", region="US", k=3)
    golden = json.loads(Path("tests/golden/aggregator_output.json").read_text())
    assert res == golden


def test_hybrid_ranker_monotonic():
    a = dict(lex=1.0, jw=0.0, sr=0.0, prior=0.2, rec=0.2)
    b = dict(lex=0.0, jw=1.0, sr=1.0, prior=0.8, rec=0.8)

    # lexical emphasis
    sa = final_score(**a, weights=(1.0, 0.0, 0.0), rec_w=0.0)
    sb = final_score(**b, weights=(1.0, 0.0, 0.0), rec_w=0.0)
    assert sa > sb

    # semantic emphasis
    sa = final_score(**a, weights=(0.0, 0.5, 0.5), rec_w=0.0)
    sb = final_score(**b, weights=(0.0, 0.5, 0.5), rec_w=0.0)
    assert sb > sa

    # recency emphasis
    sa = final_score(**a, weights=(0.6, 0.25, 0.15), rec_w=1.0)
    sb = final_score(**b, weights=(0.6, 0.25, 0.15), rec_w=1.0)
    assert sb > sa

    # priors influence
    low = final_score(1, 1, 1, 0.2, 0.0, weights=(0.6, 0.25, 0.15), rec_w=0.0)
    high = final_score(1, 1, 1, 0.8, 0.0, weights=(0.6, 0.25, 0.15), rec_w=0.0)
    assert high > low
