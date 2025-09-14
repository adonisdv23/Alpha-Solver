from service.adapters.gsheets_adapter import GSheetsAdapter
from service.adapters.playwright_adapter import PlaywrightAdapter
from service.adapters.base import AdapterError


def test_gsheets_append_idempotent() -> None:
    adapter = GSheetsAdapter()
    payload = {"sheet": "s1", "op": "append", "values": [[1], [2]]}
    r1 = adapter.run(payload, idempotency_key="k1")
    r2 = adapter.run(payload, idempotency_key="k1")
    assert r1 == r2
    read = adapter.run({"sheet": "s1", "op": "read"})
    assert read["value"] == [[1], [2]]


def test_gsheets_read_returns_rows() -> None:
    adapter = GSheetsAdapter()
    adapter.run({"sheet": "s1", "op": "append", "values": [["a"], ["b"]]})
    res = adapter.run({"sheet": "s1", "op": "read"})
    assert res["value"] == [["a"], ["b"]]


def test_gsheets_invalid_schema_error() -> None:
    adapter = GSheetsAdapter()
    try:
        adapter.run({"sheet": "s1", "op": "append"})
    except AdapterError as err:
        assert err.code == "SCHEMA"
        assert err.retryable is False
    else:  # pragma: no cover
        assert False, "AdapterError not raised"


def test_route_explain_shapes() -> None:
    pw = PlaywrightAdapter()
    gs = GSheetsAdapter()
    res_pw = pw.run({"url": "https://example.com", "action": "get_text"})
    res_gs = gs.run({"sheet": "s", "op": "read"})
    exp_pw = pw.to_route_explain(res_pw["meta"])
    exp_gs = gs.to_route_explain(res_gs["meta"])
    for exp, name in [(exp_pw, pw.name()), (exp_gs, gs.name())]:
        assert exp["adapter"] == name
        assert exp["attempts"] == 1
        assert isinstance(exp["latency_ms"], float)
        assert exp["retriable"] is False


def test_success_rate_over_20_scenarios() -> None:
    pw = PlaywrightAdapter()
    gs = GSheetsAdapter()
    success = 0
    total = 20
    for i in range(19):
        if i % 2 == 0:
            success += pw.run({"url": "https://example.com", "action": "get_text"})["ok"]
        else:
            success += gs.run({"sheet": "s", "op": "append", "values": [[i]]})["ok"]
    try:
        pw.run({"url": "https://example.com", "action": "bad"})
    except AdapterError:
        pass
    assert success / total >= 0.95
