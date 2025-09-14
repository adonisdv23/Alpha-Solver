import time
import socket

import pytest

from service.mcp.sandbox_limits import (
    SandboxPolicy,
    SandboxDecision,
    evaluate_descriptor,
    run_with_limits,
    to_route_explain,
)


def test_descriptor_denied_when_scripts_disallowed():
    policy = SandboxPolicy()
    descriptor = {"type": "script"}
    decision = evaluate_descriptor(descriptor, policy)
    assert decision is SandboxDecision.DENY


def test_descriptor_allows_when_scripts_enabled():
    policy = SandboxPolicy(allow_scripts=True)
    descriptor = {"type": "script"}
    decision = evaluate_descriptor(descriptor, policy)
    assert decision is SandboxDecision.ALLOW


def test_denies_network_when_not_allowlisted():
    policy = SandboxPolicy()

    def network_call() -> str:
        socket.create_connection(("bad.example", 80))
        return "ok"

    result, decision, _ = run_with_limits(network_call, policy=policy)
    assert result is None
    assert decision is SandboxDecision.POLICY_VIOLATION


def test_allows_network_when_allowlisted():
    policy = SandboxPolicy(allow_network=True, network_allowlist=["good.example"])

    def network_call() -> str:
        socket.create_connection(("good.example", 80))
        return "ok"

    result, decision, _ = run_with_limits(network_call, policy=policy)
    assert result == "ok"
    assert decision is SandboxDecision.ALLOW


def test_times_out_long_running_callable():
    policy = SandboxPolicy(max_time_ms=50)

    def long() -> str:
        time.sleep(0.2)
        return "done"

    result, decision, _ = run_with_limits(long, policy=policy)
    assert result is None
    assert decision is SandboxDecision.TIMEOUT


def test_size_limit_trips_on_large_output():
    policy = SandboxPolicy(max_output_bytes=10)

    def big() -> str:
        return "x" * 20

    result, decision, meta = run_with_limits(big, policy=policy)
    assert result is None
    assert decision is SandboxDecision.SIZE_LIMIT
    assert meta["output_bytes"] > policy.max_output_bytes


def test_to_route_explain_shape():
    policy = SandboxPolicy()

    def small() -> str:
        return "hi"

    result, decision, meta = run_with_limits(small, policy=policy)
    route = to_route_explain(decision, meta)
    assert route["sandbox_decision"] == decision.name
    assert set(route["budgets"]) == {
        "elapsed_ms",
        "max_time_ms",
        "output_bytes",
        "max_output_bytes",
        "allow_network",
    }
