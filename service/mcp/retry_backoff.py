from __future__ import annotations

import asyncio
import random
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

from .error_taxonomy import map_exception, is_retryable


async def _call_maybe_async(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Invoke ``func`` which may be sync or async."""
    result = func(*args, **kwargs)
    if asyncio.iscoroutine(result) or isinstance(result, Awaitable):
        return await result  # type: ignore[arg-type]
    return result


async def call_with_retries(
    func: Callable[..., Any],
    *args: Any,
    timeout: float,
    base: float = 0.2,
    factor: float = 2.0,
    jitter: float = 0.2,
    max_retries: int = 2,
    max_delay: float = 2.0,
    seed: Optional[int] = None,
    idempotency_key: Optional[str] = None,
    **kwargs: Any,
) -> Tuple[Any, Dict[str, Any]]:
    """Execute ``func`` with retries and backoff.

    Returns a tuple of ``(result, retry_metadata)``. ``retry_metadata`` contains
    the number of attempts, the list of delays between attempts, and the error
    classification for the last encountered error if any.
    """

    rng = random.Random(seed)
    attempts = 0
    delays: List[float] = []
    last_err = None

    delay = base
    loop = asyncio.get_event_loop()
    deadline = loop.time() + timeout if timeout is not None else None

    while True:
        attempts += 1
        try:
            call_kwargs = dict(kwargs)
            if idempotency_key is not None:
                call_kwargs.setdefault("idempotency_key", idempotency_key)

            if deadline is not None:
                remaining = deadline - loop.time()
                if remaining <= 0:
                    raise TimeoutError("timeout budget exceeded")
                result = await asyncio.wait_for(
                    _call_maybe_async(func, *args, **call_kwargs),
                    timeout=remaining,
                )
            else:
                result = await _call_maybe_async(func, *args, **call_kwargs)

            meta = {
                "attempts": attempts,
                "delays": delays,
                "last_error_class": last_err.cls.value if last_err else None,
                "last_error_code": last_err.code if last_err else None,
            }
            return result, meta
        except Exception as exc:  # pragma: no cover - broad for mapping
            last_err = map_exception(exc)
            retryable = is_retryable(last_err)
            if attempts > max_retries or not retryable:
                meta = {
                    "attempts": attempts,
                    "delays": delays,
                    "last_error_class": last_err.cls.value,
                    "last_error_code": last_err.code,
                }
                setattr(exc, "retry_meta", meta)
                raise

            candidate = min(max_delay, delay * factor)
            jitter_range = candidate * jitter
            next_delay = rng.uniform(
                max(base, candidate - jitter_range),
                min(max_delay, candidate + jitter_range),
            )

            if deadline is not None:
                remaining = deadline - loop.time()
                if next_delay > remaining:
                    meta = {
                        "attempts": attempts,
                        "delays": delays,
                        "last_error_class": last_err.cls.value,
                        "last_error_code": last_err.code,
                    }
                    setattr(exc, "retry_meta", meta)
                    raise

            delays.append(next_delay)
            delay = next_delay
            await asyncio.sleep(next_delay)
