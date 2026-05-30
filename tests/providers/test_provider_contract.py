from alpha.providers import ProviderCost, ProviderError, ProviderRequest, ProviderResult, ProviderUsage


def test_provider_contract_shapes_are_inspectable():
    req = ProviderRequest(
        prompt="hello",
        system="system",
        model="gpt-test",
        max_tokens=64,
        timeout_ms=1000,
        temperature=0.1,
        seed=7,
        metadata={"request_id": "req-1", "route": "unit", "model_set": "default", "tenant": "t"},
    )
    assert req.request_id == "req-1"
    assert req.metadata["route"] == "unit"

    result = ProviderResult(
        provider="openai",
        model="gpt-test",
        text="ok",
        finish_reason="stop",
        usage=ProviderUsage(input_tokens=1, output_tokens=2, total_tokens=3),
        cost=ProviderCost(estimated_usd=None, source="unknown"),
        latency_ms=4,
        request_id=req.request_id,
        raw_metadata={"response_id": "resp-1"},
    )
    assert result.usage.total_tokens == 3
    assert result.cost.source == "unknown"

    err = ProviderError(
        provider="openai",
        category="rate_limit",
        retryable=True,
        safe_message="OpenAI rate limit exceeded.",
        status_code=429,
        request_id=req.request_id,
    )
    assert str(err) == "OpenAI rate limit exceeded."
    assert err.category == "rate_limit"
