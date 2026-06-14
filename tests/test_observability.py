import json
import time
from pathlib import Path

from service.observability.logger import JsonlLogger
from service.observability.replay import ReplayHarness


BASE_ROUTE = {"decision": "go", "confidence": 0.99, "budget_verdict": None}


def read_events(path: Path):
    h = ReplayHarness(str(path))
    return list(h.iter_events())


def test_jsonl_write_and_rotation(tmp_path):
    log_path = tmp_path / "events.log"
    logger = JsonlLogger(str(log_path), rotate_mb=0.0001)
    for i in range(2):
        logger.event(name="evt", route_explain=BASE_ROUTE, payload={"i": i})
    logger.close()

    assert log_path.exists()
    rotated = Path(str(log_path) + ".1")
    assert rotated.exists()

    events_base = read_events(log_path)
    assert len(events_base) == 2


def test_event_envelope_has_required_fields(tmp_path):
    log_path = tmp_path / "e.log"
    logger = JsonlLogger(str(log_path))
    logger.event(name="sample", route_explain=BASE_ROUTE, payload={"a": 1})
    logger.close()

    with open(log_path, encoding="utf-8") as fp:
        event = json.loads(fp.readline())

    for key in ["ts", "pid", "name", "route_explain", "payload", "meta"]:
        assert key in event


def test_policy_fields_passthrough_when_present(tmp_path):
    route = {
        **BASE_ROUTE,
        "policy_verdict": "allow",
        "redaction_stats": {"foo": 1},
        "extra": "drop-me",
    }
    log_path = tmp_path / "p.log"
    logger = JsonlLogger(str(log_path))
    logger.event(
        name="policy",
        route_explain=route,
        payload={"keep": 1, "pii_raw": "secret"},
    )
    logger.close()

    event = read_events(log_path)[0]
    assert "policy_verdict" in event["route_explain"]
    assert "redaction_stats" in event["route_explain"]
    # ensure unexpected fields are removed from route_explain
    assert "extra" not in event["route_explain"]
    assert "pii_raw" not in event["payload"]
    assert event["payload"]["keep"] == 1


def test_jsonl_logger_redacts_prompt_provider_secret_and_billing_like_fields(tmp_path):
    log_path = tmp_path / "redacted.log"
    logger = JsonlLogger(str(log_path))
    logger.event(
        name="provider-boundary",
        route_explain=BASE_ROUTE,
        payload={
            "query": "canonical query marker must not leak",
            "prompt": "raw prompt marker must not leak",
            "provider_response": "raw provider answer must not leak",
            "OPENAI_API_KEY": "sk-ABCDEF1234567890",
            "billing_account": "card 4242 4242 4242 4242",
            "input_tokens": 7,
            "output_tokens": 9,
            "total_tokens": 16,
            "prompt_tokens": 7,
            "completion_tokens": 9,
            "safe_metric": 3,
        },
        meta={
            "query": "meta query marker must not leak",
            "Authorization": "Bearer abcdef1234567890",
            "request_id": "req-1",
            "total_tokens": 16,
        },
    )
    logger.close()

    text = log_path.read_text(encoding="utf-8")
    event = json.loads(text)

    assert event["payload"]["safe_metric"] == 3
    assert event["payload"]["input_tokens"] == 7
    assert event["payload"]["output_tokens"] == 9
    assert event["payload"]["total_tokens"] == 16
    assert event["payload"]["prompt_tokens"] == 7
    assert event["payload"]["completion_tokens"] == 9
    assert event["meta"]["request_id"] == "req-1"
    assert event["meta"]["total_tokens"] == 16
    assert "canonical query marker" not in text
    assert "meta query marker" not in text
    assert "raw prompt marker" not in text
    assert "raw provider answer" not in text
    assert "sk-ABCDEF1234567890" not in text
    assert "4242 4242 4242 4242" not in text
    assert "Bearer abcdef1234567890" not in text


def test_replay_iter_and_filter(tmp_path):
    log_path = tmp_path / "r.log"
    logger = JsonlLogger(str(log_path))
    logger.event(name="a", route_explain=BASE_ROUTE, payload={"x": 1})
    logger.event(name="b", route_explain=BASE_ROUTE, payload={"x": 2})
    logger.event(name="a", route_explain=BASE_ROUTE, payload={"x": 1})
    logger.close()

    harness = ReplayHarness(str(log_path))
    events = list(harness.iter_events())
    assert [e["name"] for e in events] == ["a", "b", "a"]

    only_a = harness.filter(name="a")
    assert len(only_a) == 2

    x2 = harness.filter(where={"payload": {"x": 2}})
    assert len(x2) == 1 and x2[0]["name"] == "b"


def test_replay_to_requests_roundtrip_10_of_10(tmp_path):
    log_path = tmp_path / "req.log"
    logger = JsonlLogger(str(log_path))
    for i in range(10):
        logger.event(name="req", route_explain=BASE_ROUTE, payload={"n": i})
    logger.close()

    harness = ReplayHarness(str(log_path))
    requests = harness.to_requests(name="req", extractor=lambda e: e["payload"])
    echo = lambda x: x
    outputs = [echo(r) for r in requests]
    assert outputs == [{"n": i} for i in range(10)]


def test_trace_render_p95_under_2s(tmp_path):
    log_path = tmp_path / "perf.log"
    logger = JsonlLogger(str(log_path))
    for i in range(50):
        logger.event(name="perf", route_explain=BASE_ROUTE, payload={"i": i})
    logger.close()

    start = time.monotonic()
    events = list(ReplayHarness(str(log_path)).iter_events())
    duration = time.monotonic() - start
    assert len(events) == 50
    assert duration < 2.0
