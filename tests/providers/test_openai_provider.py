import json

import httpx
import pytest

from alpha.providers import OpenAIProviderClient, ProviderError, ProviderRequest

SECRET = "sk-test-secret-value"


def _request(**overrides):
    values = {
        "prompt": "Hello",
        "system": "Be concise",
        "model": "gpt-test",
        "max_tokens": 32,
        "timeout_ms": 250,
        "temperature": 0.0,
        "seed": 123,
        "metadata": {
            "request_id": "req-123",
            "route": "unit",
            "model_set": "default",
            "tenant": "tenant-a",
        },
    }
    values.update(overrides)
    return ProviderRequest(**values)


def _client_for(handler, *, api_key=SECRET, **kwargs):
    transport = httpx.MockTransport(handler)
    return OpenAIProviderClient(api_key=api_key, transport=transport, **kwargs)


def _json_response(status_code, payload, headers=None):
    return httpx.Response(status_code, json=payload, headers=headers or {})


def test_missing_openai_api_key_is_safe(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = OpenAIProviderClient()

    with pytest.raises(ProviderError) as excinfo:
        client.execute(_request())

    err = excinfo.value
    assert err.category == "missing_credentials"
    assert err.retryable is False
    assert "OPENAI_API_KEY" in err.safe_message
    assert SECRET not in repr(err)
    assert SECRET not in str(err)


def test_openai_api_key_can_come_from_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", SECRET)
    seen = {}

    def handler(request):
        seen["authorization"] = request.headers.get("authorization")
        return _json_response(200, {"id": "resp-1", "model": "gpt-test", "output_text": "ok"})

    result = OpenAIProviderClient(transport=httpx.MockTransport(handler)).execute(_request())

    assert result.text == "ok"
    assert result.retry_count == 0
    assert seen["authorization"] == f"Bearer {SECRET}"
    assert SECRET not in repr(result)
    assert SECRET not in json.dumps(result.raw_metadata)


def test_successful_responses_api_payload_normalizes_usage_and_unknown_cost():
    def handler(request):
        body = json.loads(request.content)
        assert body["model"] == "gpt-test"
        assert body["max_output_tokens"] == 32
        assert body["temperature"] == 0.0
        assert "seed" not in body
        assert body["input"][0]["role"] == "system"
        assert body["input"][1]["role"] == "user"
        return _json_response(
            200,
            {
                "id": "resp-1",
                "model": "gpt-test",
                "status": "completed",
                "output_text": "normalized text",
                "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
            },
            headers={"x-request-id": "openai-req-1"},
        )

    result = _client_for(handler).execute(_request())

    assert result.provider == "openai"
    assert result.model == "gpt-test"
    assert result.text == "normalized text"
    assert result.finish_reason == "stop"
    assert result.usage.input_tokens == 10
    assert result.usage.output_tokens == 5
    assert result.usage.total_tokens == 15
    assert result.cost.estimated_usd is None
    assert result.cost.source == "unknown"
    assert result.request_id == "req-123"
    assert result.raw_metadata == {
        "response_id": "resp-1",
        "status": "completed",
        "http_status": 200,
        "provider_request_id": "openai-req-1",
    }


def test_chat_completions_style_payload_normalizes_text_and_usage():
    def handler(request):
        return _json_response(
            200,
            {
                "id": "chatcmpl-1",
                "model": "gpt-chat",
                "choices": [{"message": {"content": "chat text"}, "finish_reason": "length"}],
                "usage": {"prompt_tokens": 11, "completion_tokens": 7, "total_tokens": 18},
            },
        )

    result = _client_for(handler).execute(_request(model="gpt-chat"))

    assert result.text == "chat text"
    assert result.finish_reason == "length"
    assert result.usage.input_tokens == 11
    assert result.usage.output_tokens == 7
    assert result.usage.total_tokens == 18


def test_price_hint_estimates_cost_only_when_usage_available():
    def handler(request):
        return _json_response(
            200,
            {
                "model": "gpt-test",
                "output_text": "ok",
                "usage": {"input_tokens": 1000, "output_tokens": 500, "total_tokens": 1500},
            },
        )

    result = _client_for(
        handler, price_hint={"input_per_1k": 0.005, "output_per_1k": 0.015}
    ).execute(_request())

    assert result.cost.source == "price_hint"
    assert result.cost.estimated_usd == pytest.approx(0.0125)


def test_provider_reported_cost_takes_precedence():
    def handler(request):
        return _json_response(
            200,
            {"model": "gpt-test", "output_text": "ok", "cost": {"estimated_usd": 0.123}},
        )

    result = _client_for(handler, price_hint={"input_per_1k": 1, "output_per_1k": 1}).execute(
        _request()
    )

    assert result.cost.source == "provider"
    assert result.cost.estimated_usd == pytest.approx(0.123)


def test_retry_behavior_is_bounded_for_retryable_failures():
    calls = []
    backoffs = []

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            return _json_response(429, {"error": {"type": "rate_limit_error"}})
        return _json_response(200, {"model": "gpt-test", "output_text": "ok"})

    result = _client_for(handler, backoff=backoffs.append).execute(_request())

    assert result.text == "ok"
    assert result.retry_count == 1
    assert len(calls) == 2
    assert backoffs == [1]


def test_retry_stops_after_one_retry():
    calls = []

    def handler(request):
        calls.append(request)
        return _json_response(500, {"error": {"type": "server_error"}})

    with pytest.raises(ProviderError) as excinfo:
        _client_for(handler).execute(_request())

    assert excinfo.value.category == "provider_5xx"
    assert excinfo.value.retryable is True
    assert excinfo.value.retry_count == 1
    assert len(calls) == 2


def test_non_retryable_failure_is_not_retried():
    calls = []

    def handler(request):
        calls.append(request)
        return _json_response(401, {"error": {"type": "auth"}})

    with pytest.raises(ProviderError) as excinfo:
        _client_for(handler).execute(_request())

    assert excinfo.value.category == "auth"
    assert excinfo.value.retryable is False
    assert len(calls) == 1


def test_timeout_maps_to_safe_typed_error_without_hanging():
    calls = []

    def handler(request):
        calls.append(request)
        raise httpx.TimeoutException(f"timeout with {SECRET}", request=request)

    with pytest.raises(ProviderError) as excinfo:
        _client_for(handler, max_retries=0).execute(_request())

    err = excinfo.value
    assert err.category == "timeout"
    assert err.retryable is True
    assert SECRET not in str(err)
    assert SECRET not in repr(err)
    assert len(calls) == 1


@pytest.mark.parametrize(
    ("status", "payload", "category", "retryable"),
    [
        (403, {"error": {"type": "auth"}}, "auth", False),
        (429, {"error": {"type": "rate_limit_error"}}, "rate_limit", True),
        (500, {"error": {"type": "server_error"}}, "provider_5xx", True),
        (400, {"error": {"type": "invalid_request_error"}}, "invalid_request", False),
        (400, {"error": {"type": "content_filter"}}, "content_filter", False),
        (418, {"error": {"type": "teapot"}}, "invalid_request", False),
    ],
)
def test_http_failures_map_to_categories(status, payload, category, retryable):
    calls = []

    def handler(request):
        calls.append(request)
        return _json_response(status, payload)

    with pytest.raises(ProviderError) as excinfo:
        _client_for(handler).execute(_request())

    assert excinfo.value.category == category
    assert excinfo.value.retryable is retryable
    assert excinfo.value.status_code == status
    assert len(calls) == (2 if retryable else 1)


def test_network_and_unknown_errors_are_safe():
    def network_handler(request):
        raise httpx.ConnectError(f"connect failed with {SECRET}", request=request)

    with pytest.raises(ProviderError) as network_exc:
        _client_for(network_handler, max_retries=0).execute(_request())
    assert network_exc.value.category == "network"
    assert SECRET not in str(network_exc.value)
    assert SECRET not in repr(network_exc.value)

    def invalid_json_handler(request):
        return httpx.Response(200, content=b"not-json")

    with pytest.raises(ProviderError) as unknown_exc:
        _client_for(invalid_json_handler).execute(_request())
    assert unknown_exc.value.category == "unknown"
    assert SECRET not in str(unknown_exc.value)
    assert SECRET not in repr(unknown_exc.value)


def test_api_key_value_never_appears_in_returned_safe_shapes():
    def handler(request):
        return _json_response(
            400,
            {"error": {"message": f"bad request includes {SECRET}", "type": "invalid_request_error"}},
            headers={"authorization": f"Bearer {SECRET}"},
        )

    with pytest.raises(ProviderError) as excinfo:
        _client_for(handler).execute(_request())

    err = excinfo.value
    assert SECRET not in err.safe_message
    assert SECRET not in str(err)
    assert SECRET not in repr(err)
