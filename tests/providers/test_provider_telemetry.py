import json

from alpha.providers.telemetry import (
    PROVIDER_REQUEST_COMPLETED,
    build_provider_event,
    emit_provider_event,
)


def test_build_provider_event_allowlists_safe_fields_and_drops_unknowns():
    event = build_provider_event(
        PROVIDER_REQUEST_COMPLETED,
        provider="openai",
        model="gpt-test",
        model_set="default",
        route="tot",
        request_id="req-1",
        tenant="tenant-a",
        status="completed",
        retry_count=1,
        latency_ms=25,
        input_tokens=10,
        output_tokens=5,
        total_tokens=15,
        estimated_cost_usd=0.001,
        cost_source="price_hint",
        finish_reason="stop",
        provider_request_id="openai-req-1",
    )
    event["raw_metadata"] = {"raw": "RAW-MUST-NOT-LEAK"}
    event["prompt"] = "PROMPT-MUST-NOT-LEAK"

    captured = []
    emit_provider_event(event, sink=captured.append)

    assert captured == [
        {
            "event": PROVIDER_REQUEST_COMPLETED,
            "provider": "openai",
            "model": "gpt-test",
            "model_set": "default",
            "route": "tot",
            "request_id": "req-1",
            "status": "completed",
            "tenant": "tenant-a",
            "retry_count": 1,
            "latency_ms": 25,
            "input_tokens": 10,
            "output_tokens": 5,
            "total_tokens": 15,
            "estimated_cost_usd": 0.001,
            "cost_source": "price_hint",
            "finish_reason": "stop",
            "provider_request_id": "openai-req-1",
        }
    ]
    serialized = json.dumps(captured)
    assert "PROMPT-MUST-NOT-LEAK" not in serialized
    assert "RAW-MUST-NOT-LEAK" not in serialized
    assert "raw_metadata" not in serialized


def test_build_provider_event_omits_unknown_usage_and_secret_like_inputs():
    event = build_provider_event(
        "provider.request.failed",
        provider="openai",
        model="gpt-test",
        model_set="default",
        route="tot",
        request_id="req-1",
        status="failed",
        retry_count=0,
        error_category="auth",
        retryable=False,
        safe_message="OpenAI authentication failed.",
    )

    serialized = json.dumps(event)
    assert "input_tokens" not in event
    assert "estimated_cost_usd" not in event
    assert "sk-test-must-not-leak" not in serialized
    assert "Authorization" not in serialized
    assert "Bearer" not in serialized
