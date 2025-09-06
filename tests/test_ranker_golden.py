from alpha.core.registry_provider import RegistryProvider


def test_golden_ranker_output_smoke():
    rp = RegistryProvider()
    res = rp.shortlist(query="golden smoke test", region="US", k=3)
    assert len(res) >= 1
    r0 = res[0]
    assert "tool_id" in r0 and "score" in r0 and "confidence" in r0
    assert "explain" in r0 and "total" in r0["explain"]
