from __future__ import annotations

"""Simple per-adapter circuit breaker with jittered backoff."""

from dataclasses import dataclass, field
import random
import time
from typing import Literal

State = Literal["closed", "open", "half_open"]


@dataclass
class CircuitBreaker:
    adapter: str
    failure_threshold: int = 5
    recovery_timeout_ms: int = 10_000
    half_open_max_calls: int = 1
    backoff_base_ms: int = 200
    backoff_jitter: float = 0.30

    state: State = field(default="closed", init=False)
    _failure_count: int = field(default=0, init=False)
    _open_until: float = field(default=0.0, init=False)  # epoch seconds
    _half_open_calls: int = field(default=0, init=False)

    def allow_call(self) -> bool:
        """Return True if call is allowed under breaker state."""
        now = time.time()
        if self.state == "open":
            if now >= self._open_until:
                self.state = "half_open"
                self._half_open_calls = 0
            else:
                return False
        if self.state == "half_open":
            if self._half_open_calls >= self.half_open_max_calls:
                return False
            self._half_open_calls += 1
        return True

    def record_success(self) -> None:
        self._failure_count = 0
        if self.state in {"half_open", "open"}:
            self.state = "closed"
            self._open_until = 0.0

    def record_failure(self) -> bool:
        """Record a failure and return True if breaker moved to open."""
        if self.state == "half_open":
            self._trip(open_with_backoff=True)
            return True
        self._failure_count += 1
        if self._failure_count >= self.failure_threshold:
            self._trip(open_with_backoff=False)
            return True
        return False

    # Internal ---------------------------------------------------------------
    def _trip(self, *, open_with_backoff: bool) -> None:
        self.state = "open"
        self._failure_count = 0
        base = self.recovery_timeout_ms
        if open_with_backoff:
            jitter = 1 + random.uniform(-self.backoff_jitter, self.backoff_jitter)
            base += self.backoff_base_ms * jitter
        self._open_until = time.time() + base / 1000.0

    @property
    def opened_until(self) -> float:
        return self._open_until
