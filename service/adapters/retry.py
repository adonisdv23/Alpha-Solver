from __future__ import annotations

"""Generic retry helpers with exponential backoff and jitter."""

from typing import Callable, Tuple, TypeVar
import random
import time
import logging

from .base import AdapterError

T = TypeVar("T")

log = logging.getLogger("alpha.adapters.retry")

# default knobs
DEFAULT_MAX_RETRIES = 3
DEFAULT_BASE_MS = 100
DEFAULT_MAX_SLEEP_MS = 1000
DEFAULT_TIMEOUT_CEILING_MS = 2000

_TRANSIENT_HTTP = {408, 409, 425, 429}


def classify_error(err: Exception) -> bool:
    """Return True if the error is considered transient."""
    if isinstance(err, AdapterError):
        return bool(err.retryable)
    status = getattr(err, "status", None) or getattr(err, "status_code", None)
    if isinstance(status, int):
        if status >= 500 or status in _TRANSIENT_HTTP:
            return True
        if 400 <= status < 500:
            return False
    if isinstance(err, (TimeoutError, ConnectionError, OSError)):
        return True
    return False


def retry_call(
    fn: Callable[[], T],
    *,
    adapter: str,
    idempotent: bool = True,
    max_retries: int = DEFAULT_MAX_RETRIES,
    base_ms: int = DEFAULT_BASE_MS,
    max_sleep_ms: int = DEFAULT_MAX_SLEEP_MS,
    timeout_ceiling_ms: int = DEFAULT_TIMEOUT_CEILING_MS,
    budget_guard=None,
) -> Tuple[T, int, float]:
    """Call ``fn`` retrying transient failures.

    Returns a tuple ``(result, attempts, sleep_ms)``.
    On final failure the original exception is raised with ``_alpha_retry_attempts``
    and ``_alpha_retry_sleep_ms`` attributes populated for metrics.
    """

    attempts = 0
    total_sleep_ms = 0.0
    while True:
        try:
            attempts += 1
            return fn(), attempts, total_sleep_ms
        except Exception as err:  # pragma: no cover - transient path
            transient = classify_error(err)
            log.info(
                "adapter=%s attempt=%d err_class=%s transient=%s",
                adapter,
                attempts,
                err.__class__.__name__,
                str(transient).lower(),
            )
            if (not idempotent) or (not transient) or attempts > max_retries:
                setattr(err, "_alpha_retry_attempts", attempts)
                setattr(err, "_alpha_retry_sleep_ms", total_sleep_ms)
                raise
            sleep_ms = min(base_ms * (2 ** (attempts - 1)), max_sleep_ms)
            sleep_ms = random.uniform(0, sleep_ms)
            if total_sleep_ms + sleep_ms > timeout_ceiling_ms:
                setattr(err, "_alpha_retry_attempts", attempts)
                setattr(err, "_alpha_retry_sleep_ms", total_sleep_ms)
                raise
            if budget_guard and not budget_guard(sleep_ms):
                setattr(err, "_alpha_retry_attempts", attempts)
                setattr(err, "_alpha_retry_sleep_ms", total_sleep_ms)
                raise
            time.sleep(sleep_ms / 1000.0)
            total_sleep_ms += sleep_ms
