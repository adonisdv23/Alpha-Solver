import json
import logging

from alpha.reasoning.logging import SCHEMA_VERSION, log_event, validate_event


def test_schema_version_and_validation(caplog) -> None:
    caplog.set_level(logging.INFO)
    log_event(
        "run_summary",
        layer="run",
        counts={"n": 1},
        final_route="tot",
        final_confidence=0.9,
    )
    record = caplog.records[0]
    payload = json.loads(record.msg)
    assert payload["schema_version"] == SCHEMA_VERSION
    assert validate_event(payload)


def test_validate_event_missing_fields() -> None:
    assert not validate_event({"event": "run_summary"})
