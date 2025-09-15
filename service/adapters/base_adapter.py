from __future__ import annotations

"""Adapter retry wrapper with circuit breaker and metrics."""

from typing import Callable, Dict, Any
import logging

from .retry import retry_call
from .circuit_breaker import CircuitBreaker
from service.metrics.exporter import Counter, _REGISTRY, prom

log = logging.getLogger(__name__)

# Retry metrics ---------------------------------------------------------------
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

# Circuit breaker metrics ----------------------------------------------------
_CALLS = Counter(
    "alpha_adapter_calls_total",
    "adapter calls",
    ["adapter", "result"],
    registry=_REGISTRY,
)
_OPEN_TOTAL = Counter(
    "alpha_adapter_open_total",
    "breaker opened",
    ["adapter"],
    registry=_REGISTRY,
)
_BREAKER_STATE = prom.Gauge(
    "alpha_adapter_breaker_state",
    "breaker state",
    ["adapter", "state"],
    registry=_REGISTRY,
)

_BREAKERS: dict[str, CircuitBreaker] = {}


def _state_metrics(adapter: str, state: str) -> None:
    for s in ("closed", "open", "half_open"):
        _BREAKER_STATE.labels(adapter=adapter, state=s).set(1 if s == state else 0)


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


def call_adapter(
    fn: Callable[[], Dict[str, Any]],
    *,
    adapter: str,
    idempotent: bool,
    budget_guard=None,
) -> Dict[str, Any]:
    """Execute ``fn`` guarded by a per-adapter circuit breaker."""

    breaker = _BREAKERS.setdefault(adapter, CircuitBreaker(adapter))
    if not breaker.allow_call():
        _CALLS.labels(adapter=adapter, result="fallback").inc()
        _state_metrics(adapter, breaker.state)
        return {"adapter_skipped": True, "reason": "circuit_open"}

    try:
        res = with_retry(
            fn,
            adapter=adapter,
            idempotent=idempotent,
            budget_guard=budget_guard,
        )
    except Exception:
        opened = breaker.record_failure()
        _CALLS.labels(adapter=adapter, result="failure").inc()
        _state_metrics(adapter, breaker.state)
        if opened:
            _OPEN_TOTAL.labels(adapter=adapter).inc()
        raise

    breaker.record_success()
    _CALLS.labels(adapter=adapter, result="success").inc()
    _state_metrics(adapter, breaker.state)
    return res

