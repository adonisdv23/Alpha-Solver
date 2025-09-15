# Rate Limiting

Redis-backed token bucket limiter with per-tenant and global scopes.  Each
request consumes one token from both the tenant bucket (`{tenant}:tenant`) and
the global bucket (`global:global`).  Buckets refill linearly over the
configured interval.

## Example

```python
from alpha.middleware.ratelimit import RateLimiter

# simple in-memory stand-in for Redis
class InMemoryRedis:
    def __init__(self):
        self.store = {}
    def hgetall(self, key):
        return self.store.get(key, {}).copy()
    def hmset(self, key, mapping):
        self.store.setdefault(key, {}).update(mapping)
    def expire(self, key, ttl):
        pass

backend = InMemoryRedis()
limiter = RateLimiter(backend, tenant_rate=5, global_rate=10, interval=60)
assert limiter.allow("tenant-123")
```

Prometheus metrics are exported for throttled requests and current bucket level
(`alpha_ratelimiter_throttles_total` and `alpha_ratelimiter_bucket_level`).
