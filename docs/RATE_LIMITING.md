# Rate Limiting

`alpha.middleware.ratelimit.RateLimiter` provides a small token‑bucket limiter.
It can operate against Redis using `INCRBY`/`PEXPIRE` or fall back to an
in‑memory store protected by a lock. No external service is required for tests.

```python
from fakeredis import FakeRedis
from alpha.middleware.ratelimit import RateLimiter

rl = RateLimiter(bucket="chat", rate_per_sec=5, capacity=10, redis_client=FakeRedis())
rl.allow()
```

Metrics helpers are exposed via instance methods:
`get_bucket_level()` returns remaining tokens and `get_throttles_total()` counts
rejected requests.
