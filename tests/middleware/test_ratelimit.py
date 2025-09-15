import sys
import time
from pathlib import Path

try:
    from fakeredis import FakeRedis
except Exception:  # pragma: no cover - fallback
    class FakeRedis:
        def __init__(self):
            self.store = {}
        def ping(self):
            return True
        def get(self, key):
            return self.store.get(key)
        def set(self, key, value):
            self.store[key] = value

sys.path.append(str(Path(__file__).resolve().parents[2]))
from alpha.middleware.ratelimit import RateLimiter, get_bucket_level, get_throttles_total


def test_ratelimiter_burst_and_refill():
    client = FakeRedis()
    rl = RateLimiter("bucket", rate_per_sec=1, capacity=3, redis_client=client)

    # Burst up to capacity
    for _ in range(3):
        assert rl.allow()
    assert not rl.allow(2)
    assert get_throttles_total() >= 1

    # Refill a token and allow again
    time.sleep(1)  # ~1 token
    assert rl.allow()
    level = get_bucket_level()
    assert 0 <= level <= 3

    start = time.perf_counter()
    rl.allow()
    assert (time.perf_counter() - start) * 1000 < 10
