import re
import time
from pathlib import Path

from alpha.middleware.ratelimit import RateLimiter


class FakeRedis:
    def __init__(self) -> None:
        self.store: dict[str, dict[str, float]] = {}

    def hgetall(self, key: str) -> dict[str, float]:
        return self.store.get(key, {}).copy()

    def hmset(self, key: str, mapping: dict[str, float]) -> None:
        self.store.setdefault(key, {}).update(mapping)

    def expire(self, key: str, ttl: int) -> None:  # pragma: no cover - noop
        return None


def test_burst_then_steady_and_perf():
    backend = FakeRedis()
    limiter = RateLimiter(backend, tenant_rate=5, global_rate=100, interval=1)

    latencies = []
    for _ in range(5):
        t0 = time.perf_counter()
        assert limiter.allow("t1")
        latencies.append(time.perf_counter() - t0)

    t0 = time.perf_counter()
    assert not limiter.allow("t1")
    latencies.append(time.perf_counter() - t0)

    time.sleep(1.05)
    t0 = time.perf_counter()
    assert limiter.allow("t1")  # refill allows again
    latencies.append(time.perf_counter() - t0)
    for _ in range(19):  # collect more samples without asserting outcome
        t0 = time.perf_counter()
        limiter.allow("t1")
        latencies.append(time.perf_counter() - t0)

    sorted_lat = sorted(latencies)
    p95 = sorted_lat[min(len(sorted_lat) - 1, int(len(sorted_lat) * 0.95))]
    assert p95 < 0.01


def test_per_tenant_isolation():
    backend = FakeRedis()
    limiter = RateLimiter(backend, tenant_rate=2, global_rate=100, interval=60)

    for _ in range(2):
        assert limiter.allow("a")
    assert not limiter.allow("a")

    for _ in range(2):
        assert limiter.allow("b")
    assert not limiter.allow("b")


def test_docs_example_runs():
    content = Path("docs/RATE_LIMITING.md").read_text()
    code = re.search(r"```python\n(.*?)\n```", content, re.S).group(1)
    ns: dict[str, object] = {}
    exec(code, ns)
