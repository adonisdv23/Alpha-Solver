from __future__ import annotations

from registries.mcp.registry_lookup import suggest_tool


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _base_request(**overrides):
    req = {
        "intent": "browse",
        "needs_network": True,
        "latency_sla_ms": 250,
        "risk": 0.1,
    }
    req.update(overrides)
    return req


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_block_when_policy_block():
    registry = {"tool": [{"name": "web", "type": "http"}]}
    req = _base_request()
    res = suggest_tool(registry, req, {"block": True})
    assert res["decision"] == "block"
    assert res["tool"] is None


def test_choose_http_for_browse():
    registry = {
        "tool": [
            {"name": "web", "type": "http", "estimated_latency_ms": 100},
            {"name": "calc", "type": "script", "estimated_latency_ms": 80},
        ]
    }
    res = suggest_tool(registry, _base_request(), {"block": False})
    assert res["tool"] == "web"


def test_penalize_script_under_sandbox_strict():
    registry = {
        "tool": [
            {"name": "web", "type": "http", "estimated_latency_ms": 100},
            {"name": "sheety", "type": "script", "estimated_latency_ms": 80},
        ]
    }
    req = _base_request(intent="sheet", needs_network=False)
    res = suggest_tool(registry, req, {"sandbox_strict": True})
    assert res["tool"] == "web"


def test_latency_penalty_applied():
    registry = {
        "tool": [
            {"name": "fast", "type": "http", "estimated_latency_ms": 100},
            {"name": "slow", "type": "http", "estimated_latency_ms": 300},
        ]
    }
    req = _base_request(latency_sla_ms=150)
    res = suggest_tool(registry, req, {})
    assert res["tool"] == "fast"


def test_tiebreak_latency_then_name():
    registry = {
        "tool": [
            {"name": "gamma", "type": "http", "estimated_latency_ms": 300},
            {"name": "beta", "type": "http", "estimated_latency_ms": 100},
            {"name": "alpha", "type": "http", "estimated_latency_ms": 100},
        ]
    }
    res = suggest_tool(registry, _base_request(), {})
    assert res["tool"] == "alpha"


def test_confidence_bounds_0_1():
    registry = {
        "tool": [
            {"name": "web", "type": "http", "estimated_latency_ms": 100},
            {"name": "calc", "type": "script", "estimated_latency_ms": 80},
        ]
    }
    res = suggest_tool(registry, _base_request(), {})
    assert 0.0 <= res["confidence"] <= 1.0


def test_replay_10_of_10_identical():
    registry = {
        "tool": [
            {"name": "web", "type": "http", "estimated_latency_ms": 100},
            {"name": "calc", "type": "script", "estimated_latency_ms": 80},
        ]
    }
    req = _base_request()
    policy = {}
    results = [suggest_tool(registry, req, policy) for _ in range(10)]
    assert all(r == results[0] for r in results)
