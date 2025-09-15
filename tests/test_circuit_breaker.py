import re
import statistics
import time
from typing import Any, Dict

import pytest

from service.adapters.base import AdapterError
from service.adapters.base_adapter import BaseAdapter
from service.adapters.circuit_breaker import CircuitBreaker
from service.metrics.exporter import MetricsExporter


class ManualTime:
    def __init__(self) -> None:
        self.now = 0.0

    def time(self) -> float:
        return self.now

    def advance_ms(self, ms: float) -> None:
        self.now += ms / 1000.0


class FlakyAdapter(BaseAdapter):
    """Adapter that fails until told otherwise."""

    def __init__(self, breaker: CircuitBreaker) -> None:
        super().__init__(name="flaky", breaker=breaker)
        self.payloads: list[Dict[str, Any]] = []

    def _run(self, payload: Dict[str, Any], *, idempotency_key: str | None = None, timeout_s: float = 5.0):
        self.payloads.append(payload)
        if payload.get("fail", True):
            raise AdapterError(code="BOOM", retryable=True)
        return {"ok": True}


@pytest.fixture
def manual_time() -> ManualTime:
    return ManualTime()


@pytest.fixture
def breaker(manual_time: ManualTime) -> CircuitBreaker:
    return CircuitBreaker(failure_threshold=2, recovery_timeout_ms=1000, backoff_base_ms=100, time_func=manual_time.time)


@pytest.fixture
def adapter(breaker: CircuitBreaker) -> FlakyAdapter:
    return FlakyAdapter(breaker)


def test_open_on_failures(adapter: FlakyAdapter, breaker: CircuitBreaker):
    for _ in range(2):
        with pytest.raises(AdapterError):
            adapter.run({"fail": True})
    assert breaker.state == "open"

    res = adapter.run({"fail": True})
    assert res == {"adapter_skipped": True, "reason": "circuit_open"}


def test_half_open_and_backoff(adapter: FlakyAdapter, breaker: CircuitBreaker, manual_time: ManualTime):
    # Open breaker with consecutive failures
    with pytest.raises(AdapterError):
        adapter.run({"fail": True})
    with pytest.raises(AdapterError):
        adapter.run({"fail": True})
    first_timeout = breaker._current_timeout_ms

    # Half-open success closes breaker
    manual_time.advance_ms(first_timeout + 1)
    res = adapter.run({"fail": False})
    assert res["ok"]
    assert breaker.state == "closed"

    # Open again
    with pytest.raises(AdapterError):
        adapter.run({"fail": True})
    with pytest.raises(AdapterError):
        adapter.run({"fail": True})
    timeout_before = breaker._current_timeout_ms

    # Half-open failure causes backoff
    manual_time.advance_ms(timeout_before + 1)
    with pytest.raises(AdapterError):
        adapter.run({"fail": True})
    assert breaker.state == "open"
    new_timeout = breaker._current_timeout_ms
    assert new_timeout > timeout_before


def test_metrics_and_fallback(adapter: FlakyAdapter, breaker: CircuitBreaker, manual_time: ManualTime):
    # cause open
    for _ in range(2):
        with pytest.raises(AdapterError):
            adapter.run({"fail": True})
    adapter.run({"fail": True})

    client = MetricsExporter().test_client()
    data = client.get("/metrics").text

    assert 'alpha_adapter_open_total{adapter="flaky"}' in data
    def _get(metric):
        m = re.search(metric + r" (\d+(?:\.\d+)?)", data)
        assert m
        return float(m.group(1))

    assert _get(r'alpha_adapter_calls_total{adapter="flaky",result="failure"}') >= 2
    assert _get(r'alpha_adapter_calls_total{adapter="flaky",result="fallback"}') >= 1
    assert _get(r'alpha_adapter_breaker_state{adapter="flaky",state="open"}') == 1


def test_performance_fallback(adapter: FlakyAdapter, breaker: CircuitBreaker, manual_time: ManualTime):
    with pytest.raises(AdapterError):
        adapter.run({"fail": True})
    with pytest.raises(AdapterError):
        adapter.run({"fail": True})
    assert breaker.state == "open"

    times = []
    for _ in range(50):
        start = time.perf_counter()
        adapter.run({"fail": True})
        times.append(time.perf_counter() - start)
    p95 = statistics.quantiles(times, n=20)[18]
    assert p95 < 5


def test_no_secrets_in_logs(adapter: FlakyAdapter, breaker: CircuitBreaker, caplog):
    secret_payload = {"fail": True, "api_key": "SECRET123"}
    for _ in range(2):
        with pytest.raises(AdapterError):
            adapter.run(secret_payload)
    # breaker now open -> log emitted
    adapter.run(secret_payload)
    log_text = "".join(record.message for record in caplog.records)
    assert "SECRET123" not in log_text
    assert not re.search(r"token|secret", log_text, re.IGNORECASE)
