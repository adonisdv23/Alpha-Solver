from alpha.routing import RouterV12
from alpha.core.config import RouterConfig


def test_router_v12_determinism():
    cfg = RouterConfig(seed=42)
    branches = [
        {"id": "b", "score": 0.5, "tokens": 10},
        {"id": "a", "score": 0.5, "tokens": 10},
    ]
    orders = [RouterV12(cfg).score_branches(branches) for _ in range(3)]
    assert orders[0] == orders[1] == orders[2]
    tel = RouterV12(cfg).route_example(branches)
    tel2 = RouterV12(cfg).route_example(branches)
    assert tel == tel2
