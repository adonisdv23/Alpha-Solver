from __future__ import annotations

import logging
import random
import re
import time

import pytest

from service.adapters.base import AdapterError
from service.adapters.base_adapter import with_retry
from service.metrics.exporter import _REGISTRY


class FlakyAdapter:
    def __init__(self, p_fail: float = 0.5) -> None:
        self.p_fail = p_fail

    def run(self, payload):
        if random.random() < self.p_fail:
            raise AdapterError(code="TRANSIENT", retryable=True)
        return {"ok": True, "value": 1, "meta": {"attempts": 1}}


def test_success_lift_and_metrics():
    random.seed(0)
    n = 200
    baseline = 0
    for _ in range(n):
        ad = FlakyAdapter()
        try:
            ad.run({})
            baseline += 1
        except AdapterError:
            pass
    baseline_rate = baseline / n

    random.seed(0)
    success = 0
    for _ in range(n):
        ad = FlakyAdapter()
        try:
            with_retry(lambda: ad.run({}), adapter="flaky", idempotent=True)
            success += 1
        except AdapterError:
            pass
    retry_rate = success / n
    assert retry_rate >= baseline_rate + 0.10

    # force giveup case for metrics
    def always_fail():
        raise AdapterError(code="TRANSIENT", retryable=True)

    with pytest.raises(AdapterError):
        with_retry(always_fail, adapter="flaky", idempotent=True)

    metrics = {
        (s.labels.get("adapter"), s.labels.get("outcome")): s.value
        for m in _REGISTRY.collect()
        if m.name == "alpha_adapter_retry"
        for s in m.samples
        if s.name == "alpha_adapter_retry_total"
    }
    assert ("flaky", "success") in metrics
    assert ("flaky", "giveup") in metrics

    sleep_metric = {
        s.labels.get("adapter"): s.value
        for m in _REGISTRY.collect()
        if m.name == "alpha_adapter_retry_sleep_ms_sum"
        for s in m.samples
        if s.name == "alpha_adapter_retry_sleep_ms_sum_total"
    }
    assert "flaky" in sleep_metric


def test_fatal_short_circuit():
    calls = 0

    def fatal():
        nonlocal calls
        calls += 1
        raise AdapterError(code="SCHEMA", retryable=False)

    with pytest.raises(AdapterError):
        with_retry(fatal, adapter="fatal", idempotent=True)
    assert calls == 1


def test_latency_bounds():
    def always_transient():
        raise AdapterError(code="TRANSIENT", retryable=True)

    start = time.perf_counter()
    with pytest.raises(AdapterError):
        with_retry(always_transient, adapter="slow", idempotent=True)
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert elapsed_ms <= 2000


def test_idempotency_guard():
    calls = 0

    def transient():
        nonlocal calls
        calls += 1
        raise AdapterError(code="TRANSIENT", retryable=True)

    with pytest.raises(AdapterError):
        with_retry(transient, adapter="guard", idempotent=False)
    assert calls == 1


def test_no_secrets_in_logs(caplog):
    caplog.set_level(logging.INFO)

    def transient():
        raise AdapterError(code="TRANSIENT", retryable=True)

    with pytest.raises(AdapterError):
        with_retry(transient, adapter="log", idempotent=True)

    assert not re.search("token|secret", caplog.text)
