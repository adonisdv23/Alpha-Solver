import pytest

from service.models.modelset_registry import ModelSetRegistry
from service.models.modelset_resolver import ModelSetResolver


def estimate_cost_latency(ms, tokens_in=100, tokens_out=0):
    ph = ms.price_hint or {}
    cost = tokens_in / 1000 * ph.get("input_per_1k", 0) + tokens_out / 1000 * ph.get(
        "output_per_1k", 0
    )
    return cost, ms.timeout_ms


def test_switch_changes_estimates():
    reg = ModelSetRegistry()
    resolver = ModelSetResolver(registry=reg)
    default_ms, _ = resolver.resolve()
    saver_ms, _ = resolver.resolve(requested="cost_saver")
    default_cost, default_latency = estimate_cost_latency(default_ms, tokens_in=1000)
    saver_cost, saver_latency = estimate_cost_latency(saver_ms, tokens_in=1000)
    assert saver_cost < default_cost
    assert saver_latency < default_latency


def test_resolver_priority_and_fallback():
    reg = ModelSetRegistry()
    resolver = ModelSetResolver(registry=reg)

    # header overrides tenant default
    explain = {}
    ms, reason = resolver.resolve(
        headers={"X-Model-Set": "cost_saver"}, tenant_default="default", route_explain=explain
    )
    assert ms.name == "cost_saver"
    assert reason == "requested"
    assert explain["model_set"] == "cost_saver"
    assert explain["model_set_reason"] == "requested"

    # tenant default used when no header
    explain = {}
    ms, reason = resolver.resolve(tenant_default="cost_saver", route_explain=explain)
    assert ms.name == "cost_saver"
    assert reason == "tenant-default"
    assert explain["model_set"] == "cost_saver"

    # global default fallback
    explain = {}
    ms, reason = resolver.resolve(route_explain=explain)
    assert ms.name == "default"
    assert reason == "global-default"
    assert explain["model_set_reason"] == "global-default"

    # unknown requested falls back
    explain = {}
    ms, reason = resolver.resolve(requested="unknown", route_explain=explain)
    assert ms.name == "default"
    assert reason.startswith("unknown-requested")
    assert explain["model_set_reason"].startswith("unknown-requested")

    # unknown tenant default falls back deterministically
    explain = {}
    ms, reason = resolver.resolve(tenant_default="mystery", route_explain=explain)
    assert ms.name == "default"
    assert reason.startswith("unknown-tenant-default")
    assert explain["model_set_reason"].startswith("unknown-tenant-default")

