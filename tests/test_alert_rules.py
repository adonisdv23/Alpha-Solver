"""Tests for the alert manager."""

from __future__ import annotations

from service.alerts import AlertManager


def test_p95_latency_alert_and_budget_over():
    events = []
    mgr = AlertManager(p95_target_ms=100, window_seconds=60, callback=events.append)

    # First feed latencies below threshold
    for i in range(95):
        mgr.record_latency(50, now=float(i))

    assert not events

    # Now push p95 above threshold
    for i in range(95, 100):
        mgr.record_latency(500, now=float(i))

    assert any(e["type"] == "p95_latency" for e in events)

    mgr.record_budget_over(now=101.0)
    assert any(e["type"] == "budget_over" for e in events)


def test_no_alert_under_thresholds():
    events = []
    mgr = AlertManager(p95_target_ms=100, window_seconds=60, callback=events.append)

    for i in range(100):
        mgr.record_latency(50, now=float(i))

    assert events == []

