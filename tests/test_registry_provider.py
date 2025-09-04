from alpha.core.registry_provider import RegistryProvider

def rp():
    r = RegistryProvider('registries/registry_seed_v0_7_0.jsonl','schemas/registry_schema_v1.json')
    r.load()
    return r

def test_legal_surfaces():
    top = rp().rank("legal contract review", 5)
    assert top and any(x["id"].startswith("tool.legal.") for x in top)

def test_region_weighting():
    r = rp()
    us = r.rank("procurement workflow", 10, region="US")
    ap = r.rank("procurement workflow", 10, region="APAC")
    zu = next(x for x in us if x["id"]=="tool.automation.zapier")
    za = next(x for x in ap if x["id"]=="tool.automation.zapier")
    assert zu["score"] >= za["score"]
