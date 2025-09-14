from service.adapters.playwright_adapter import PlaywrightAdapter
from service.adapters.base import AdapterError


def test_playwright_get_text_success() -> None:
    adapter = PlaywrightAdapter()
    res = adapter.run({"url": "https://example.com", "action": "get_text"})
    assert res["ok"] is True
    assert res["value"] == "Example Domain"
    assert res["meta"]["latency_ms"] >= 0


def test_playwright_invalid_action_schema_error() -> None:
    adapter = PlaywrightAdapter()
    try:
        adapter.run({"url": "https://example.com", "action": "bad"})
    except AdapterError as err:
        assert err.code == "SCHEMA"
        assert err.retryable is False
    else:  # pragma: no cover - protective
        assert False, "AdapterError not raised"


def test_playwright_timeout_maps_retryable() -> None:
    adapter = PlaywrightAdapter()
    try:
        adapter.run({"url": "https://example.com", "action": "get_text"}, timeout_s=0.001)
    except AdapterError as err:
        assert err.code == "TIMEOUT"
        assert err.retryable is True
    else:  # pragma: no cover - protective
        assert False, "timeout not raised"
