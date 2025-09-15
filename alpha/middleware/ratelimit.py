from __future__ import annotations

import threading
import time
from typing import Any, Optional, Tuple, Dict

try:  # optional dependency
    import redis  # type: ignore
except Exception:  # pragma: no cover - best effort
    redis = None  # type: ignore


class RateLimiter:
    """Token bucket limiter with Redis or in-memory storage."""

    _state: Dict[Tuple[str, str], Tuple[float, float]] = {}
    _state_lock = threading.Lock()

    def __init__(
        self,
        *,
        bucket: str = "default",
        tenant: str = "global",
        rate_per_sec: float = 10.0,
        capacity: int = 20,
        redis_client: Optional[Any] = None,
    ) -> None:
        self.bucket = bucket
        self.tenant = tenant
        self.rate = float(rate_per_sec)
        self.capacity = int(capacity)
        self.redis_client = redis_client
        self._bucket_level = self.capacity
        self._throttles_total = 0

    # ------------------------------------------------------------------
    def _refill(self, tokens: float, last: float, now: float) -> float:
        tokens = min(self.capacity, tokens + (now - last) * self.rate)
        return tokens

    # ------------------------------------------------------------------
    def allow(self, n: int = 1) -> bool:
        """Attempt to consume *n* tokens."""
        now = time.time()
        if self.redis_client is not None:
            key = f"ratelimit:{self.tenant}:{self.bucket}"
            ttl_ms = int(1000 * self.capacity / self.rate)
            try:
                new_val = self.redis_client.incrby(key, n)
                if new_val == n:
                    self.redis_client.pexpire(key, ttl_ms)
                allowed = new_val <= self.capacity
                if not allowed:
                    self._throttles_total += 1
                self._bucket_level = max(0, self.capacity - new_val)
                return allowed
            except Exception:
                pass  # fall back to memory

        key = (self.tenant, self.bucket)
        with self._state_lock:
            tokens, last = self._state.get(key, (float(self.capacity), now))
            tokens = self._refill(tokens, last, now)
            allowed = tokens >= n
            if allowed:
                tokens -= n
            else:
                self._throttles_total += 1
            self._state[key] = (tokens, now)
            self._bucket_level = int(tokens)
            return allowed

    # ------------------------------------------------------------------
    def get_bucket_level(self) -> int:
        """Current tokens remaining in the bucket."""
        return int(self._bucket_level)

    # ------------------------------------------------------------------
    def get_throttles_total(self) -> int:
        """Total number of refused requests."""
        return self._throttles_total
