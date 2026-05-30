import inspect
import json

from alpha.providers import ProviderError, build_provider_safe_out_body, provider_safe_out_status
import alpha.providers.safeout as provider_safeout


_STATUS_CASES = {
    "missing_credentials": 503,
    "auth": 502,
    "rate_limit": 429,
    "timeout": 504,
    "network": 503,
    "provider_5xx": 502,
    "invalid_request": 400,
    "content_filter": 400,
    "unknown": 502,
}


def _error(**overrides):
    values = {
        "provider": "openai",
        "category": "unknown",
        "retryable": False,
        "safe_message": "OpenAI request failed.",
        "status_code": None,
        "request_id": None,
        "retry_count": 0,
    }
    values.update(overrides)
    return ProviderError(**values)


def test_provider_safe_out_status_preserves_all_current_mapped_categories():
    for category, status in _STATUS_CASES.items():
        assert provider_safe_out_status(_error(category=category)) == status


def test_provider_safe_out_status_defaults_unrecognized_category_to_502():
    assert provider_safe_out_status(_error(category="future_category")) == 502


def test_build_provider_safe_out_body_has_lean_exact_schema_and_safe_fields():
    body = build_provider_safe_out_body(
        _error(
            category="rate_limit",
            retryable=True,
            safe_message="OpenAI rate limit exceeded.",
            request_id="req-123",
            retry_count=2,
            status_code=429,
        )
    )

    assert set(body) == {"final_answer", "safe_out", "error"}
    assert set(body["error"]) == {
        "provider",
        "category",
        "retryable",
        "request_id",
        "retry_count",
        "status_code",
    }
    assert body == {
        "final_answer": "SAFE-OUT: OpenAI rate limit exceeded.",
        "safe_out": True,
        "error": {
            "provider": "openai",
            "category": "rate_limit",
            "retryable": True,
            "request_id": "req-123",
            "retry_count": 2,
            "status_code": 429,
        },
    }
    assert body["safe_out"] is True
    assert body["final_answer"].startswith("SAFE-OUT: ")


def test_build_provider_safe_out_body_includes_explicit_none_correlation_fields():
    body = build_provider_safe_out_body(_error())

    assert body["error"]["request_id"] is None
    assert body["error"]["status_code"] is None
    assert body["error"]["retry_count"] == 0


def test_build_provider_safe_out_body_excludes_raw_secret_prompt_and_exception_sentinels():
    body = build_provider_safe_out_body(
        _error(
            safe_message="Safe canned message.",
            request_id="req-safe",
            status_code=503,
        )
    )

    serialized = json.dumps(body)
    forbidden = [
        "sk-test-must-not-leak",
        "OPENAI_API_KEY=sk-test-must-not-leak",
        "Authorization",
        "Bearer",
        "PROMPT-MUST-NOT-LEAK",
        "SYSTEM-MUST-NOT-LEAK",
        "USER-QUERY-MUST-NOT-LEAK",
        "RAW-PROVIDER-REQUEST-MUST-NOT-LEAK",
        "RAW-PROVIDER-RESPONSE-MUST-NOT-LEAK",
        "RAW-OPENAI-ERROR-BODY-MUST-NOT-LEAK",
        "raw exception string sentinel",
        "Traceback",
        "raw_metadata",
    ]
    for sentinel in forbidden:
        assert sentinel not in serialized


def test_safeout_helper_does_not_spread_dict_or_vars():
    source = inspect.getsource(provider_safeout)

    assert ".__dict__" not in source
    assert "vars(" not in source
