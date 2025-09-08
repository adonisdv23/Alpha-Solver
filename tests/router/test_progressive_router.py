from alpha.router import ProgressiveRouter


def test_progressive_router_escalates():
    router = ProgressiveRouter(min_progress=0.5)
    assert router.route(0.6) == "basic"
    assert router.route(0.4) == "structured"
    assert router.route(0.2) == "constrained"
    assert router.route(0.1) == "constrained"
