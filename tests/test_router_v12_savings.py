from pathlib import Path

from alpha.routing import RouterV12
from alpha.core.metrics import compute_token_savings


def test_router_v12_savings():
    dataset = Path("datasets/mvp_golden.jsonl")
    router = RouterV12()
    baseline = router.simulate(dataset, baseline=True)
    new = router.simulate(dataset, baseline=False)
    pct = compute_token_savings(baseline, new)
    assert pct >= 0.15
