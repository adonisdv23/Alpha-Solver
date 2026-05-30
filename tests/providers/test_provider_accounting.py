import json

from alpha.providers import ProviderCost, ProviderResult, ProviderUsage
from alpha.providers.accounting import (
    PROVIDER_COST_RECORDED,
    build_provider_accounting_record,
    emit_provider_accounting,
)


def _result(*, cost: ProviderCost | None = None) -> ProviderResult:
    return ProviderResult(
        provider="openai",
        model="gpt-test",
        text="PROMPT-MUST-NOT-LEAK",
        finish_reason="stop",
        usage=ProviderUsage(input_tokens=10, output_tokens=5, total_tokens=15),
        cost=cost or ProviderCost(estimated_usd=0.001, source="price_hint"),
        latency_ms=25,
        request_id="req-1",
        raw_metadata={
            "provider_request_id": "openai-req-1",
            "raw_metadata": "RAW-MUST-NOT-LEAK",
            "raw": "SYSTEM-MUST-NOT-LEAK",
            "authorization": "Bearer sk-test-must-not-leak",
            "exception": "raw exception string sentinel",
        },
        retry_count=1,
    )


def test_build_provider_accounting_record_includes_safe_result_fields():
    record = build_provider_accounting_record(
        result=_result(),
        model_set="cost_saver",
        route="tot",
        request_id="req-fallback",
        tenant="tenant-a",
        provider_request_id="openai-req-1",
    )

    assert record == {
        "event": PROVIDER_COST_RECORDED,
        "provider": "openai",
        "model": "gpt-test",
        "model_set": "cost_saver",
        "route": "tot",
        "request_id": "req-1",
        "tenant": "tenant-a",
        "input_tokens": 10,
        "output_tokens": 5,
        "total_tokens": 15,
        "estimated_cost_usd": 0.001,
        "cost_source": "price_hint",
        "retry_count": 1,
        "budget_status": "recorded",
        "accounting_source": "service:/v1/solve",
        "provider_request_id": "openai-req-1",
    }


def test_build_provider_accounting_record_retains_unknown_cost_source_and_omits_none():
    result = _result(cost=ProviderCost(estimated_usd=None, source="unknown"))
    record = build_provider_accounting_record(
        result=result,
        model_set=None,
        route="tot",
        request_id="req-fallback",
        tenant=None,
    )

    assert record["cost_source"] == "unknown"
    assert "estimated_cost_usd" not in record
    assert "model_set" not in record
    assert "tenant" not in record
    assert "provider_request_id" not in record


def test_emit_provider_accounting_sink_receives_only_allowlisted_keys():
    record = build_provider_accounting_record(
        result=_result(),
        model_set="default",
        route="tot",
        request_id="req-1",
        tenant="tenant-a",
        provider_request_id="openai-req-1",
    )
    record.update(
        {
            "prompt": "PROMPT-MUST-NOT-LEAK",
            "system": "SYSTEM-MUST-NOT-LEAK",
            "raw_metadata": {"raw": "RAW-MUST-NOT-LEAK"},
            "Authorization": "Bearer sk-test-must-not-leak",
            "exception": "raw exception string sentinel",
        }
    )

    captured = []
    emit_provider_accounting(record, sink=captured.append)

    assert len(captured) == 1
    assert set(captured[0]) == {
        "event",
        "provider",
        "model",
        "model_set",
        "route",
        "request_id",
        "tenant",
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "estimated_cost_usd",
        "cost_source",
        "retry_count",
        "budget_status",
        "accounting_source",
        "provider_request_id",
    }
    serialized = json.dumps(captured)
    assert "sk-test-must-not-leak" not in serialized
    assert "Authorization" not in serialized
    assert "Bearer" not in serialized
    assert "PROMPT-MUST-NOT-LEAK" not in serialized
    assert "SYSTEM-MUST-NOT-LEAK" not in serialized
    assert "RAW-MUST-NOT-LEAK" not in serialized
    assert "raw_metadata" not in serialized
    assert "raw exception string sentinel" not in serialized
