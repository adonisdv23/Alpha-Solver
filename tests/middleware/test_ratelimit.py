import time
from pathlib import Path
import sys

try:
    from fakeredis import FakeRedis
except Exception:  # pragma: no cover
    class FakeRedis:  # minimal stub
        def incrby(self, key, n):
            self.store[key] = self.store.get(key, 0) + n
            return self.store[key]
        def pexpire(self, key, ttl):
            return True
        def __init__(self):
            self.store = {}

sys.path.append(str(Path(__file__).resolve().parents[2]))
from alpha.middleware.ratelimit import RateLimiter


def test_ratelimiter_redis_and_speed():
    client = FakeRedis()
    rl = RateLimiter(bucket="b1", tenant="t1", rate_per_sec=100, capacity=100, redis_client=client)

    results = [rl.allow() for _ in range(120)]
    assert not all(results)
    assert rl.get_throttles_total() > 0
    assert rl.get_bucket_level() >= 0

    start = time.perf_counter()
    rl.allow()
    assert (time.perf_counter() - start) < 0.01
