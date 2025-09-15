import time
import logging

import pytest

from service.adapters.circuit_breaker import CircuitBreaker
from service.adapters.base_adapter import call_adapter, _BREAKERS
from service.metrics.exporter import MetricsExporter


def _metrics_text() -> str:
    client = MetricsExporter().test_client()
    return client.get("/metrics").text


def test_open_and_fallback_metrics():
    _BREAKERS["dummy"] = CircuitBreaker("dummy", failure_threshold=2, recovery_timeout_ms=50, backoff_base_ms=10)

    def fail():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        call_adapter(fail, adapter="dummy", idempotent=False)
    with pytest.raises(RuntimeError):
        call_adapter(fail, adapter="dummy", idempotent=False)
    res = call_adapter(fail, adapter="dummy", idempotent=False)
    assert res == {"adapter_skipped": True, "reason": "circuit_open"}

    metrics = _metrics_text()
    assert 'alpha_adapter_calls_total{adapter="dummy",result="failure"} 2.0' in metrics
    assert 'alpha_adapter_calls_total{adapter="dummy",result="fallback"} 1.0' in metrics
    assert 'alpha_adapter_breaker_state{adapter="dummy",state="open"} 1.0' in metrics
    assert 'alpha_adapter_open_total{adapter="dummy"} 1.0' in metrics


def test_half_open_recovery_and_failure_backoff():
    breaker = CircuitBreaker("dummy2", failure_threshold=1, recovery_timeout_ms=20, backoff_base_ms=10)
    _BREAKERS["dummy2"] = breaker

    def fail():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        call_adapter(fail, adapter="dummy2", idempotent=False)
    assert call_adapter(fail, adapter="dummy2", idempotent=False) == {"adapter_skipped": True, "reason": "circuit_open"}
    first_open = breaker.opened_until
    time.sleep(0.03)  # allow transition to half-open

    def succeed():
        return {"ok": True}

    res = call_adapter(succeed, adapter="dummy2", idempotent=False)
    assert res["ok"] is True
    metrics = _metrics_text()
    assert 'alpha_adapter_breaker_state{adapter="dummy2",state="closed"} 1.0' in metrics

    # trip again and fail during half-open
    with pytest.raises(RuntimeError):
        call_adapter(fail, adapter="dummy2", idempotent=False)
    assert call_adapter(fail, adapter="dummy2", idempotent=False) == {"adapter_skipped": True, "reason": "circuit_open"}
    time.sleep(0.03)
    with pytest.raises(RuntimeError):
        call_adapter(fail, adapter="dummy2", idempotent=False)
    assert call_adapter(fail, adapter="dummy2", idempotent=False) == {"adapter_skipped": True, "reason": "circuit_open"}
    second_open = breaker.opened_until
    assert second_open - time.time() > (breaker.recovery_timeout_ms + breaker.backoff_base_ms * 0.5) / 1000.0
    assert second_open > first_open


def test_failure_storm_latency_p95():
    _BREAKERS["storm"] = CircuitBreaker("storm", failure_threshold=1, recovery_timeout_ms=1000)

    def fail():
        raise RuntimeError("boom")

    lat = []
    for _ in range(20):
        start = time.time()
        try:
            call_adapter(fail, adapter="storm", idempotent=False)
        except RuntimeError:
            pass
        lat.append(time.time() - start)
    lat.sort()
    p95 = lat[int(len(lat) * 0.95) - 1]
    assert p95 < 5.0


def test_no_secrets_in_logs(caplog):
    _BREAKERS["log"] = CircuitBreaker("log", failure_threshold=1, recovery_timeout_ms=50)
    secret = "super_secret_token"

    def fail():
        raise RuntimeError(secret)

    with caplog.at_level(logging.INFO):
        with pytest.raises(RuntimeError):
            call_adapter(fail, adapter="log", idempotent=False)
    for rec in caplog.records:
        assert secret not in rec.getMessage()
