from service.adapters.playwright_adapter import PlaywrightAdapter
from service.adapters.base import AdapterError


def _payload() -> dict:
    return {
        "action": "extract",
        "url": "https://example.com",
        "allowlist": ["example.com"],
        "selectors": {
            "h1": "h1",
            "first_paragraph": "p",
            "meta_description": "meta[name='description']",
        },
    }


def test_extract_h1_para_meta_success() -> None:
    adapter = PlaywrightAdapter()
    res = adapter.run(_payload())
    assert res["ok"] is True
    val = res["value"]
    assert val["h1"] == "Example Domain"
    assert "illustrative examples" in val["first_paragraph"]
    assert val["meta_description"] == "Example description"


def test_allowlist_blocks_disallowed_domain() -> None:
    adapter = PlaywrightAdapter()
    payload = _payload()
    payload["url"] = "https://notallowed.com"
    try:
        adapter.run(payload)
    except AdapterError as err:
        assert err.code == "DOMAIN_NOT_ALLOWED"
        assert err.retryable is False
    else:  # pragma: no cover - protective
        assert False, "domain not blocked"


def test_sanitization_strips_script_and_whitespace() -> None:
    adapter = PlaywrightAdapter()
    adapter._html["https://example.com"] = (
        "<html><body><h1>  Title  </h1><p>first\nline<script>bad</script></p></body></html>"
    )
    payload = {
        "action": "extract",
        "url": "https://example.com",
        "allowlist": ["example.com"],
        "selectors": {"h1": "h1", "first_paragraph": "p"},
    }
    res = adapter.run(payload)
    assert res["value"]["h1"] == "Title"
    para = res["value"]["first_paragraph"]
    assert "bad" not in para
    assert "\n" not in para


def test_route_explain_has_expected_fields() -> None:
    adapter = PlaywrightAdapter()
    res = adapter.run(_payload())
    exp = adapter.to_route_explain(res["meta"])
    assert exp["adapter"] == "playwright"
    assert exp["attempts"] == 1
    assert isinstance(exp["latency_ms"], float)
    assert exp["allowlisted"] is True
    assert exp["sanitized_fields"] >= 1

