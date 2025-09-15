# Rate Limiting

`alpha.middleware.ratelimit.RateLimiter` implements a simple token bucket using
Redis when available and an in-memory fallback otherwise.

```python
from fakeredis import FakeRedis
from alpha.middleware.ratelimit import RateLimiter

rl = RateLimiter("chat", rate_per_sec=5, capacity=10, redis_client=FakeRedis())
rl.allow()
```

Helper functions `get_bucket_level()` and `get_throttles_total()` expose the
current state for metrics collection.
