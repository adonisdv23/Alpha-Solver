from service.adapters.gsheets_adapter import GSheetsAdapter
from service.adapters.playwright_adapter import PlaywrightAdapter
from service.adapters.base import AdapterError


def test_append_idempotent_by_range_and_key() -> None:
    adapter = GSheetsAdapter()
    payload = {
        "sheet": "s1",
        "range": "A1:A2",
        "op": "append",
        "values": [["1"], ["2"]],
        "idempotency_key": "k1",
    }
    r1 = adapter.run(payload)
    r2 = adapter.run(payload)
    assert r1 == r2
    read = adapter.run({"sheet": "s1", "range": "A1:A2", "op": "read"})
    assert read["value"] == [["1"], ["2"]]


def test_sanitization_applied_on_values() -> None:
    adapter = GSheetsAdapter()
    payload = {
        "sheet": "s1",
        "range": "A1:A1",
        "op": "append",
        "values": [["  a \n"]],
    }
    adapter.run(payload)
    read = adapter.run({"sheet": "s1", "range": "A1:A1", "op": "read"})
    assert read["value"] == [["a"]]


def test_transient_error_retries_and_succeeds() -> None:
    adapter = GSheetsAdapter()
    payload = {
        "sheet": "s1",
        "range": "A1:A1",
        "op": "append",
        "values": [["x"]],
    }
    res = adapter.run(payload)
    assert res["meta"]["attempts"] == 2


def test_route_explain_has_expected_fields() -> None:
    adapter = GSheetsAdapter()
    payload = {
        "sheet": "s1",
        "range": "A1:A1",
        "op": "append",
        "values": [["y"]],
    }
    res = adapter.run(payload)
    exp = adapter.to_route_explain(res["meta"])
    assert exp["adapter"] == "gsheets"
    assert isinstance(exp["latency_ms"], float)
    assert isinstance(exp["attempts"], int)
    assert isinstance(exp["sanitized_cells"], int)
    assert exp["idempotent"] is False


def test_success_rate_over_mvp_set_ge_95pct() -> None:
    pw = PlaywrightAdapter()
    gs = GSheetsAdapter()
    success = 0
    total = 20
    base_pw = {
        "action": "extract",
        "url": "https://example.com",
        "allowlist": ["example.com"],
        "selectors": {"h1": "h1"},
    }
    for i in range(19):
        if i % 2 == 0:
            success += pw.run(base_pw)["ok"]
        else:
            success += gs.run(
                {
                    "sheet": "s",
                    "range": "A1:A1",
                    "op": "append",
                    "values": [[i]],
                    "idempotency_key": str(i),
                }
            )["ok"]
    try:
        pw.run(
            {
                "action": "extract",
                "url": "https://bad.com",
                "allowlist": ["example.com"],
                "selectors": {},
            }
        )
    except AdapterError:
        pass
    assert success / total >= 0.95

