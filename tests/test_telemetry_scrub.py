import os
from scripts import telemetry_tools as tt


def test_scrub_helper(monkeypatch):
    monkeypatch.setenv("ALPHA_TELEMETRY_SCRUB", "1")
    rec = {
        "region": "US",
        "query_hash": "q1",
        "rank": 1,
        "query_text": "keep me private",
        "input_tokens": 2,
        "output_tokens": 3,
        "total_tokens": 5,
        "tool_id": "x",
    }
    out = tt._scrub_record(rec)
    assert out["query_text"] in ("***SCRUBBED***", None)
    assert out["input_tokens"] == 2
    assert out["output_tokens"] == 3
    assert out["total_tokens"] == 5
    assert out["tool_id"] == "x"
    assert out["region"] == "US"
