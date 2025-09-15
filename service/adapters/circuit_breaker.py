from __future__ import annotations

"""Simple circuit breaker implementation for tool adapters.

States:
- CLOSED: calls pass through. On failures over threshold -> OPEN.
- OPEN: calls short-circuit. After timeout -> HALF_OPEN.
- HALF_OPEN: allow limited trial calls. Success -> CLOSED, failure -> OPEN with backoff.
"""

from dataclasses import dataclass
from typing import Callable
import random
import time


@dataclass
class CircuitBreaker:
    """Per-adapter circuit breaker.

    Parameters mirror the spec defaults but are configurable so tests can tune
    thresholds/timeouts. ``time_func`` defaults to ``time.monotonic`` so tests
    can provide a fake time implementation.
    """

    failure_threshold: int = 5
    recovery_timeout_ms: int = 10_000
    half_open_max_calls: int = 1
    backoff_base_ms: int = 200
    backoff_jitter: float = 0.3
    time_func: Callable[[], float] | None = None

    def __post_init__(self) -> None:
        self._state = "closed"
        self._failure_count = 0
        self._half_open_calls = 0
        self._opened_at_ms: float | None = None
        self._current_timeout_ms = self.recovery_timeout_ms
        self._open_count = 0
        self._time = self.time_func or time.monotonic

    # ------------------------------------------------------------------
    @property
    def state(self) -> str:
        return self._state

    def allow_call(self) -> bool:
        """Return ``True`` if the call is allowed to proceed."""

        now_ms = self._time() * 1000
        if self._state == "open":
            assert self._opened_at_ms is not None
            if now_ms - self._opened_at_ms >= self._current_timeout_ms:
                # Move to half-open
                self._state = "half_open"
                self._half_open_calls = 0
            else:
                return False

        if self._state == "half_open":
            if self._half_open_calls >= self.half_open_max_calls:
                return False
            self._half_open_calls += 1
            return True

        return True  # closed

    # ------------------------------------------------------------------
    def record_success(self) -> None:
        if self._state == "half_open":
            self._state = "closed"
        self._failure_count = 0
        self._half_open_calls = 0
        self._opened_at_ms = None
        self._current_timeout_ms = self.recovery_timeout_ms
        self._open_count = 0

    def record_failure(self) -> None:
        if self._state == "half_open":
            self._trip()
            return

        self._failure_count += 1
        if self._failure_count >= self.failure_threshold:
            self._trip()

    # ------------------------------------------------------------------
    def _trip(self) -> None:
        """Transition to OPEN with jittered backoff."""

        self._state = "open"
        self._opened_at_ms = self._time() * 1000
        self._failure_count = 0
        self._half_open_calls = 0
        self._open_count += 1

        backoff = self.backoff_base_ms * (2 ** (self._open_count - 1))
        jitter = random.uniform(1 - self.backoff_jitter, 1 + self.backoff_jitter)
        self._current_timeout_ms = self.recovery_timeout_ms + backoff * jitter

