from __future__ import annotations

import os
import threading
import time
from typing import Any, Optional

try:  # optional dependency
    import redis  # type: ignore
except Exception:  # pragma: no cover - best effort
    redis = None  # type: ignore

__all__ = ["RateLimiter", "get_bucket_level", "get_throttles_total"]

_bucket_level = 0
_throttles_total = 0


def get_bucket_level() -> int:
    """Return the most recent bucket level."""
    return _bucket_level


def get_throttles_total() -> int:
    """Return the number of rejected requests."""
    return _throttles_total


class RateLimiter:
    """Token bucket rate limiter backed by Redis or in-memory fallback."""

    def __init__(
        self,
        bucket: str,
        rate_per_sec: float,
        capacity: int,
        *,
        tenant: str = "global",
        redis_url: Optional[str] = None,
        redis_client: Optional[Any] = None,
    ) -> None:
        self.bucket = bucket
        self.rate = float(rate_per_sec)
        self.capacity = int(capacity)
        self.tenant = tenant
        self.redis_url = redis_url or os.getenv("REDIS_URL")
        self.redis_client = redis_client
        if self.redis_client is None and self.redis_url and redis is not None:
            try:
                self.redis_client = redis.from_url(self.redis_url)
            except Exception:
                self.redis_client = None
        # In-memory fallback state
        self._tokens = float(self.capacity)
        self._last = time.time()
        self._lock = threading.Lock()

    def _refill(self, tokens: float, now: float, last: float) -> float:
        elapsed = max(0.0, now - last)
        tokens = min(self.capacity, tokens + elapsed * self.rate)
        return tokens

    def allow(self, n: int = 1) -> bool:
        """Return True if *n* tokens can be consumed."""
        global _bucket_level, _throttles_total
        now = time.time()
        if self.redis_client is not None:
            key = f"ratelimit:{self.tenant}:{self.bucket}"
            try:
                data = self.redis_client.get(key)
                if data:
                    tokens, last = map(float, data.decode().split(":"))
                else:
                    tokens, last = float(self.capacity), now
                tokens = self._refill(tokens, now, last)
                allowed = tokens >= n
                if allowed:
                    tokens -= n
                else:
                    _throttles_total += 1
                _bucket_level = int(tokens)
                self.redis_client.set(key, f"{tokens}:{now}")
                return allowed
            except Exception:
                # fall back to in-memory if redis errors
                pass
        # In-memory path
        with self._lock:
            tokens = self._refill(self._tokens, now, self._last)
            allowed = tokens >= n
            if allowed:
                tokens -= n
            else:
                _throttles_total += 1
            self._tokens = tokens
            self._last = now
            _bucket_level = int(tokens)
            return allowed
