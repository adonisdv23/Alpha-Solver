import io
import logging
import time

import pytest

from service.logging import redactor
from service.logging.filters import install
from service import otel


FIXTURES = {
    "auth": "Authorization: Bearer abcdef1234567890",
    "api": "sk-ABCDEF1234567890",
    "slack": "xoxb-123456789012-ABCDEFG",
    "token": "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6",
    "email": "alice@example.com",
    "phone": "+1-415-555-2671",
}


def _contains_secret(s: str) -> bool:
    return any(v in s for v in FIXTURES.values())


@pytest.fixture(autouse=True)
def _reset_counters():
    redactor.reset_counters()
    yield


@pytest.fixture()
def logger():
    log = logging.getLogger("redact")
    log.setLevel(logging.INFO)
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    log.addHandler(handler)
    install(log)
    yield log, stream
    log.removeHandler(handler)


def test_detections():
    for kind, raw in FIXTURES.items():
        redacted = redactor.redact(raw)
        assert raw not in redacted
        assert "REDACTED" in redacted or kind in {"email", "phone"}
    assert redactor.redact(FIXTURES["auth"]) == "Authorization: Bearer ***REDACTED***"
    assert redactor.ERROR_TOTAL == 0


def test_allowlist():
    data = {"safe": FIXTURES["api"], "other": FIXTURES["api"]}
    out = redactor.redact(data, allowlist=["safe"])
    assert out["safe"] == FIXTURES["api"]
    assert out["other"] == "***REDACTED***"


def test_structured_logs(logger):
    log, stream = logger
    log.info(
        "testing",
        extra={"payload": {"email": FIXTURES["email"], "deep": {"phone": FIXTURES["phone"]}}},
    )
    text = stream.getvalue()
    assert FIXTURES["email"] not in text
    assert FIXTURES["phone"] not in text


def test_spans_redacted_and_dropped():
    otel.reset_exported_spans()
    otel.init_tracer()
    with otel.span("t", note=FIXTURES["api"], prompt="should drop"):
        pass
    spans = otel.get_exported_spans()
    attrs = spans[0].attributes
    assert attrs["note"] == "***REDACTED***"
    assert "prompt" not in attrs


def test_performance_and_no_leak(logger):
    log, stream = logger
    start = time.perf_counter()
    messages = list(FIXTURES.values()) + ["normal message"]
    for i in range(1000):
        log.info(messages[i % len(messages)])
    duration = time.perf_counter() - start
    avg_ms = (duration / 1000) * 1000
    assert avg_ms <= 1.0
    output = stream.getvalue()
    assert not _contains_secret(output)
    for sp in otel.get_exported_spans():
        assert not _contains_secret(str(sp.attributes))
    assert redactor.ERROR_TOTAL == 0
    expected = (len(messages) - 1) * (1000 // len(messages)) + min(
        1000 % len(messages), len(messages) - 1
    )
    assert redactor.APPLIED_TOTAL == expected
