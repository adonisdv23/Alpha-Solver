import pytest

from registries.mcp.loader import (
    ValidationError,
    get_tool,
    list_tools,
    load_registry,
)
from service.mcp.wiring import init_mcp, tool_summary


def _sample_registry():
    return {
        "version": "1.0",
        "tool": [
            {"name": "alpha-tool", "type": "script", "entry": "mod:func"},
            {"name": "beta-tool", "type": "http", "entry": "http://x"},
        ],
    }


def test_valid_registry_loads_and_lists():
    registry = load_registry(_sample_registry())
    assert list_tools(registry) == ["alpha-tool", "beta-tool"]
    tool = get_tool(registry, "alpha-tool")
    assert tool["timeout_ms"] == 15000
    assert tool["enabled"] is True


def test_disabled_tools_are_excluded():
    registry = {
        "tool": [
            {"name": "t1", "type": "script", "entry": "a:b", "enabled": False},
            {"name": "t2", "type": "http", "entry": "http://"},
        ]
    }
    loaded = load_registry(registry)
    assert list_tools(loaded) == ["t2"]
    assert get_tool(loaded, "t1") is None


def test_secret_env_is_resolved_but_not_logged(monkeypatch, capfd):
    monkeypatch.setenv("MY_SECRET", "shh")
    registry = {
        "tool": [
            {
                "name": "secret-tool",
                "type": "script",
                "entry": "m:f",
                "secrets": {"MY_SECRET": "REDACTED"},
            }
        ]
    }
    loaded = load_registry(registry)
    tool = get_tool(loaded, "secret-tool")
    captured = capfd.readouterr()
    assert "shh" not in captured.out
    assert "shh" not in captured.err
    assert tool["secrets"]["MY_SECRET"] == "shh"


def test_validation_fails_on_bad_schema():
    bad = {"tool": [{"name": "bad", "type": "http"}]}  # missing entry
    with pytest.raises(ValidationError):
        load_registry(bad)


def test_get_tool_deterministic():
    reg = load_registry(_sample_registry())
    tool1 = get_tool(reg, "alpha-tool")
    tool1["entry"] = "changed"
    tool2 = get_tool(reg, "alpha-tool")
    assert tool2["entry"] == "mod:func"


def test_tool_summary_counts():
    reg = {
        "version": "1",
        "tool": [
            {"name": "h1", "type": "http", "entry": "http://a"},
            {"name": "s1", "type": "script", "entry": "m:f", "enabled": False},
            {"name": "r1", "type": "remote", "entry": "remote:run"},
        ],
    }
    ctx = init_mcp(reg)
    summary = tool_summary(ctx)
    assert summary["enabled"] == 2
    assert summary["disabled"] == 1
    assert summary["by_type"] == {"http": 1, "script": 1, "remote": 1}
