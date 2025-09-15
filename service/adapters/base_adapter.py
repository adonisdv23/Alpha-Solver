from __future__ import annotations

"""Adapter retry wrapper with metrics and logging."""

from typing import Callable, Dict, Any

from .retry import retry_call
from service.metrics.exporter import Counter, _REGISTRY

_RETRY_TOTAL = Counter(
    "alpha_adapter_retry_total",
    "adapter retries",
    ["adapter", "outcome", "attempts"],
    registry=_REGISTRY,
)
_RETRY_SLEEP = Counter(
    "alpha_adapter_retry_sleep_ms_sum",
    "total retry sleep ms",
    ["adapter"],
    registry=_REGISTRY,
)


def with_retry(
    fn: Callable[[], Dict[str, Any]],
    *,
    adapter: str,
    idempotent: bool,
    budget_guard=None,
) -> Dict[str, Any]:
    """Execute ``fn`` with retry semantics and record metrics."""

    try:
        res, attempts, sleep_ms = retry_call(
            fn,
            adapter=adapter,
            idempotent=idempotent,
            budget_guard=budget_guard,
        )
    except Exception as err:  # pragma: no cover - error path
        attempts = getattr(err, "_alpha_retry_attempts", 1)
        sleep_ms = getattr(err, "_alpha_retry_sleep_ms", 0.0)
        _RETRY_TOTAL.labels(adapter=adapter, outcome="giveup", attempts=str(attempts)).inc()
        if sleep_ms:
            _RETRY_SLEEP.labels(adapter=adapter).inc(sleep_ms)
        raise
    _RETRY_TOTAL.labels(adapter=adapter, outcome="success", attempts=str(attempts)).inc()
    if sleep_ms:
        _RETRY_SLEEP.labels(adapter=adapter).inc(sleep_ms)
    if isinstance(res, dict) and isinstance(res.get("meta"), dict):
        res["meta"]["attempts"] = attempts
    return res
