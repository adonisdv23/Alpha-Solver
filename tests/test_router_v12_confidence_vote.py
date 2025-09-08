from alpha.routing import RouterV12
from alpha.core.config import RouterConfig, VoteConfig


def test_router_v12_basic_vote_deterministic():
    cfg = RouterConfig(vote=VoteConfig(enabled=True, k=3))
    router = RouterV12(cfg)
    ans1 = router.basic_vote(["A", "B", "A"])
    ans2 = router.basic_vote(["A", "B", "A"])
    assert ans1 == ans2 == "A"
