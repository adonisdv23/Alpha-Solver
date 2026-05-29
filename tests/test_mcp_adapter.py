import pytest

from alpha.tools.mcp_adapter import McpAdapter, McpAdapterError


def test_gsheets_write_skips_domain_allowlist_when_payload_domainless():
    adapter = McpAdapter({"allow_domains": ["example.com"]})

    result = adapter.safe_call(
        "gsheets_write",
        {"sheet_id": "s1", "rows": [[1]]},
    )

    assert result["tool"] == "gsheets_write"
    assert result["domain"] is None
    assert result["output"]["status"] == "accepted"
    assert result["output"]["row_count"] == 1


def test_playwright_web_extract_still_blocks_disallowed_domain():
    adapter = McpAdapter({"allow_domains": ["example.com"]})

    with pytest.raises(McpAdapterError, match="domain_not_allowed:bad.com"):
        adapter.safe_call(
            "playwright_web_extract",
            {"url": "https://bad.com", "selector": "main"},
        )


def test_playwright_web_extract_fails_closed_when_domain_missing_with_allowlist():
    adapter = McpAdapter({"allow_domains": ["example.com"]})

    with pytest.raises(McpAdapterError, match="domain_not_allowed:None"):
        adapter.safe_call(
            "playwright_web_extract",
            {"selector": "main"},
        )


@pytest.mark.parametrize(
    "domain_payload",
    [
        {"domain": "bad.com"},
        {"url": "https://bad.com/sheet"},
    ],
)
def test_gsheets_write_with_domain_field_still_enforces_allowlist(domain_payload):
    adapter = McpAdapter({"allow_domains": ["example.com"]})

    with pytest.raises(McpAdapterError, match="domain_not_allowed:bad.com"):
        adapter.safe_call(
            "gsheets_write",
            {"sheet_id": "s1", "rows": [[1]], **domain_payload},
        )
