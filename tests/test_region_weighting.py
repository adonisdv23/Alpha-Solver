from pathlib import Path
from alpha.core import selector
from alpha.core.determinism import apply_seed


def test_region_weights_change_order():
    Path('artifacts/tools_canon.csv').unlink(missing_ok=True)
    selector._CANON_CACHE = None
    base_tools = [
        {"id": "t1", "router_value": 0.4, "confidence": 1.0},
        {"id": "t2", "router_value": 0.5, "confidence": 0.0},
    ]
    apply_seed(0)
    us = selector.rank_region([dict(t) for t in base_tools], region="US", top_k=2)
    eu = selector.rank_region([dict(t) for t in base_tools], region="EU", top_k=2)
    assert us[0]["id"] == "t1"
    assert eu[0]["id"] == "t2"


def test_priors_cap():
    tools = [{"id": "p1", "router_value": 0.1, "tags": ["security", "analytics", "security"]}]
    ranked = selector.rank_region(tools, region="US", top_k=1)
    item = ranked[0]
    assert item["reasons"]["prior_boost"] <= 0.1
