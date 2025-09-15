from __future__ import annotations

import time
from typing import MutableMapping, Protocol

try:  # pragma: no cover - fallback for minimal prometheus stubs
    from prometheus_client import Counter, Gauge  # type: ignore
except ImportError:  # pragma: no cover - minimal Gauge implementation
    from prometheus_client import Counter  # type: ignore

    class Gauge(Counter):
        def set(self, value: float) -> None:  # simple gauge behaviour
            self.value = value


class RedisLike(Protocol):
    """Minimal Redis interface used by :class:`RateLimiter`."""

    def hgetall(self, key: str) -> MutableMapping[str, float]:
        ...

    def hmset(self, key: str, mapping: MutableMapping[str, float]) -> None:
        ...

    def expire(self, key: str, ttl: int) -> None:
        ...


_THROTTLES = Counter(
    "alpha_ratelimiter_throttles_total", "Requests throttled", ["scope"]
)
_BUCKET_LEVEL = Gauge(
    "alpha_ratelimiter_bucket_level", "Token bucket level", ["scope", "bucket"]
)


class RateLimiter:
    """Redis-backed token bucket rate limiter.

    Parameters
    ----------
    redis:
        Redis client or compatible object.
    tenant_rate:
        Max tokens per interval for a tenant bucket.
    global_rate:
        Max tokens per interval for the global bucket.
    interval:
        Refill interval in seconds (default 60).
    """

    def __init__(
        self,
        redis: RedisLike,
        tenant_rate: int,
        global_rate: int,
        interval: int = 60,
    ) -> None:
        self.redis = redis
        self.tenant_rate = tenant_rate
        self.global_rate = global_rate
        self.interval = interval

    # public API ---------------------------------------------------------
    def allow(self, tenant: str) -> bool:
        """Check if a request for ``tenant`` should be allowed."""
        if not self._consume(f"{tenant}:tenant", self.tenant_rate, "tenant"):
            return False
        if not self._consume("global:global", self.global_rate, "global"):
            return False
        return True

    # internal -----------------------------------------------------------
    def _consume(self, key: str, rate: int, scope: str) -> bool:
        now = time.time()
        data = self.redis.hgetall(key) or {}
        tokens = float(data.get("tokens", rate))  # bucket capacity equals rate
        ts = float(data.get("ts", now))

        # refill based on elapsed time
        elapsed = max(0.0, now - ts)
        tokens = min(rate, tokens + elapsed * rate / self.interval)

        allowed = tokens >= 1
        if allowed:
            tokens -= 1
        self.redis.hmset(key, {"tokens": tokens, "ts": now})
        try:
            self.redis.expire(key, self.interval)
        except Exception:
            # allow fake backends without expire support
            pass

        _BUCKET_LEVEL.labels(scope=scope, bucket=key).set(tokens)
        if not allowed:
            _THROTTLES.labels(scope=scope).inc()
        return allowed
