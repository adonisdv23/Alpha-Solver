from alpha.router import ProgressiveRouter, ProgressiveRouterConfig


def test_progressive_router_escalates():
    cfg = ProgressiveRouterConfig(enable_progressive_router=True, router_min_progress=0.5)
    router = ProgressiveRouter.from_config(cfg)
    assert router is not None
    assert router.route(0.6) == "basic"
    assert router.route(0.4) == "structured"
    assert router.route(0.2) == "constrained"
    assert router.route(0.1) == "constrained"


def test_progressive_router_disabled_returns_none():
    cfg = ProgressiveRouterConfig()
    assert ProgressiveRouter.from_config(cfg) is None
