"""Budget and resilience gates for MCP interactions."""
from __future__ import annotations

import time
from typing import Any, Callable, Tuple

LLM_ONLY_MAX_COST = 0.02


class CircuitBreaker:
    """Simple circuit breaker to protect against repeated MCP failures."""

    def __init__(
        self, failure_threshold: int = 3, recovery_time: float = 30.0
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self._opened_at: float | None = None

    @property
    def is_open(self) -> bool:
        if self._opened_at is None:
            return False
        if time.time() - self._opened_at >= self.recovery_time:
            self.reset()
            return False
        return True

    def record_failure(self) -> None:
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self._opened_at = time.time()

    def record_success(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.failure_count = 0
        self._opened_at = None


def apply_budget_gate(
    estimated_cost: float, max_cost: float = LLM_ONLY_MAX_COST
) -> Tuple[bool, str]:
    """Return whether the MCP path is allowed given the budget."""

    if estimated_cost > max_cost:
        return False, "budget_exceeded"
    return True, "within_budget"


def retry_with_backoff(
    func: Callable[[], Any], retries: int = 3, base_delay: float = 0.1, max_delay: float = 1.0
) -> Any:
    """Retry ``func`` with exponential backoff for transient failures."""

    attempt = 0
    while True:
        try:
            return func()
        except Exception:
            attempt += 1
            if attempt > retries:
                raise
            delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
            time.sleep(delay)


__all__ = ["LLM_ONLY_MAX_COST", "CircuitBreaker", "apply_budget_gate", "retry_with_backoff"]
