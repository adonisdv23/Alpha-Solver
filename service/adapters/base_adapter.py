from __future__ import annotations

"""Adapter wrapper that adds circuit breaker behaviour and metrics."""

from typing import Any, Dict
import logging

from .circuit_breaker import CircuitBreaker
from .base import IToolAdapter
from service.metrics import client as mclient


# ---------------------------------------------------------------------------
# Metrics
CALLS_TOTAL: mclient.Counter
BREAKER_STATE: mclient.Gauge
OPEN_TOTAL: mclient.Counter


def _init_metrics() -> None:
    """(Re)initialize metrics on the current registry."""
    global CALLS_TOTAL, BREAKER_STATE, OPEN_TOTAL
    CALLS_TOTAL = mclient.counter(
        "alpha_adapter_calls_total",
        "adapter calls",
        labelnames=("adapter", "result"),
    )
    BREAKER_STATE = mclient.gauge(
        "alpha_adapter_breaker_state",
        "breaker state",
        labelnames=("adapter", "state"),
    )
    OPEN_TOTAL = mclient.counter(
        "alpha_adapter_open_total",
        "breaker opened",
        labelnames=("adapter",),
    )


_init_metrics()


class BaseAdapter(IToolAdapter):
    """Shared adapter wrapper implementing circuit breaker logic."""

    def __init__(self, *, name: str, breaker: CircuitBreaker | None = None) -> None:
        self._name = name
        self._breaker = breaker or CircuitBreaker()
        self._update_state_metrics()

    # ------------------------------------------------------------------
    def name(self) -> str:  # pragma: no cover - trivial
        return self._name

    def _update_state_metrics(self) -> None:
        for state in ("closed", "open", "half_open"):
            value = 1 if self._breaker.state == state else 0
            BREAKER_STATE.labels(adapter=self._name, state=state).set(value)

    # ------------------------------------------------------------------
    def _run(
        self,
        payload: Dict[str, Any],
        *,
        idempotency_key: str | None,
        timeout_s: float,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    def run(
        self,
        payload: Dict[str, Any],
        *,
        idempotency_key: str | None = None,
        timeout_s: float = 5.0,
    ) -> Dict[str, Any]:
        old_state = self._breaker.state
        allowed = self._breaker.allow_call()
        if self._breaker.state != old_state:
            self._update_state_metrics()
        if not allowed:
            CALLS_TOTAL.labels(adapter=self._name, result="fallback").inc()
            return {"adapter_skipped": True, "reason": "circuit_open"}

        try:
            res = self._run(payload, idempotency_key=idempotency_key, timeout_s=timeout_s)
        except Exception:
            prev_state = self._breaker.state
            self._breaker.record_failure()
            CALLS_TOTAL.labels(adapter=self._name, result="failure").inc()
            if self._breaker.state == "open" and prev_state != "open":
                OPEN_TOTAL.labels(adapter=self._name).inc()
                logging.getLogger(__name__).warning(
                    "adapter %s circuit opened", self._name
                )
            if prev_state != self._breaker.state:
                self._update_state_metrics()
            raise
        else:
            self._breaker.record_success()
            CALLS_TOTAL.labels(adapter=self._name, result="success").inc()
            if old_state != self._breaker.state:
                self._update_state_metrics()
            return res

    # simple delegator; subclasses may override
    def to_route_explain(self, meta: Dict[str, Any]) -> Dict[str, Any]:  # pragma: no cover - simple
        return {"adapter": self._name, **meta}

