import random
from alpha.core.determinism import apply_seed
from alpha.core import loader, selector, orchestrator


def build(seed: int):
    apply_seed(seed)
    loader.load_all('registries')
    tools = [{"id": "a", "router_value": 0.5}, {"id": "b", "router_value": 0.4}]
    shortlist = selector.rank_region(tools, region="US", top_k=2)
    return orchestrator.build_plan("q", "US", 2, shortlist, None, seed=seed)


def test_same_seed_stable():
    p1 = build(42)
    p2 = build(42)
    assert p1.run["seed"] == 42
    assert p1.steps[0].to_dict() == p2.steps[0].to_dict()


def test_different_seeds_differ():
    p1 = build(1)
    p2 = build(2)
    assert p1.run["seed"] != p2.run["seed"]
    apply_seed(1)
    r1 = random.random()
    apply_seed(2)
    r2 = random.random()
    assert r1 != r2
