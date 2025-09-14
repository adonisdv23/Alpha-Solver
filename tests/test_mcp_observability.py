import time

import pytest

from service.mcp import observability as obs
from service.mcp.error_taxonomy import ErrorClass


FIXED_TS = "2023-01-01T00:00:00+00:00"


@pytest.fixture(autouse=True)
def fixed_ts(monkeypatch):
    monkeypatch.setattr(obs, "_iso_utc", lambda: FIXED_TS)


def test_success_event_shape_and_redaction():
    with obs.start_call("toolA", "req1", idempotency_key="idem") as ctx:
        pass
    event = obs.record_success(
        ctx,
        confidence=0.9,
        extra={"pii_raw": "x", "api_token": "y", "foo": 1, "db_secret": "z"},
    )

    assert event["name"] == "mcp.call"
    assert event["payload"] == {
        "tool": "toolA",
        "request_id": "req1",
        "idempotency_key": "idem",
    }
    route = event["route_explain"]
    assert route["decision"] == "success"
    assert route["confidence"] == 0.9
    assert route["budget_verdict"] == "ok"
    assert "foo" in route
    assert "pii_raw" not in route and "api_token" not in route and "db_secret" not in route
    assert event["meta"]["error_class"] is None


def test_error_event_includes_error_class_and_retryable_meta():
    with obs.start_call("toolB", "req2") as ctx:
        pass
    event = obs.record_error(ctx, TimeoutError("boom"))

    assert event["route_explain"]["decision"] == "error"
    assert event["meta"]["error_class"] == ErrorClass.TIMEOUT.value
    assert event["meta"]["retryable"] is True
    assert event["route_explain"]["cls"] == ErrorClass.TIMEOUT.value


def test_context_manager_measures_latency():
    with obs.start_call("toolC", "req3") as ctx:
        time.sleep(0.01)
    event = obs.record_success(ctx, confidence=0.5)
    assert event["meta"]["latency_ms"] >= 10


def test_jsonl_roundtrip():
    with obs.start_call("toolD", "req4") as ctx:
        pass
    event = obs.record_success(ctx, confidence=1.0)
    line = obs.to_jsonl(event)
    out = obs.from_jsonl(line)
    assert out == event


def test_overhead_p95_under_2ms():
    times = []
    for _ in range(100):
        t0 = time.monotonic()
        with obs.start_call("t", "r") as ctx:
            pass
        obs.record_success(ctx, confidence=0.1)
        times.append((time.monotonic() - t0) * 1000)
    times.sort()
    p95 = times[int(len(times) * 0.95)]
    assert p95 < 2.0


def test_replay_10_of_10_identical(monkeypatch):
    seq = iter(range(20))
    monkeypatch.setattr(obs.time, "monotonic", lambda: next(seq))

    lines = []
    for _ in range(10):
        with obs.start_call("tool", "req") as ctx:
            pass
        line = obs.to_jsonl(obs.record_success(ctx, confidence=1.0))
        lines.append(line)
    assert len(set(lines)) == 1
