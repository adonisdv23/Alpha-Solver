import os
import uuid

import pytest

os.environ.setdefault("API_KEY", "test")
os.environ.setdefault("RATE_LIMIT_PER_MINUTE", "2")

from fastapi.testclient import TestClient

from alpha.providers import (
    PROVIDER_COST_RECORDED,
    PROVIDER_REQUEST_COMPLETED,
    PROVIDER_REQUEST_FAILED,
    PROVIDER_REQUEST_STARTED,
    PROVIDER_REQUEST_TIMEOUT,
    FakeProviderClient,
    ProviderCost,
    ProviderError,
    ProviderResult,
    ProviderUsage,
)
from service.app import app


def _clear_provider_factory():
    if hasattr(app.state, "provider_client_factory"):
        delattr(app.state, "provider_client_factory")


def _clear_provider_telemetry_sink():
    if hasattr(app.state, "provider_telemetry_sink"):
        delattr(app.state, "provider_telemetry_sink")


def _clear_provider_accounting_sink():
    if hasattr(app.state, "provider_accounting_sink"):
        delattr(app.state, "provider_accounting_sink")


@pytest.fixture(autouse=True)
def _default_local_provider(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    _clear_provider_factory()
    _clear_provider_telemetry_sink()
    _clear_provider_accounting_sink()
    yield
    _clear_provider_factory()
    _clear_provider_telemetry_sink()
    _clear_provider_accounting_sink()


def _client():
    key = str(uuid.uuid4())
    app.state.config.api_key = key
    return TestClient(app), key


def _assert_provider_safe_out_schema(
    body, *, category, retryable, request_id, retry_count=0, status_code=None
):
    assert set(body) == {"final_answer", "safe_out", "error"}
    assert body["safe_out"] is True
    assert body["final_answer"].startswith("SAFE-OUT: ")
    assert set(body["error"]) == {
        "provider",
        "category",
        "retryable",
        "request_id",
        "retry_count",
        "status_code",
    }
    assert body["error"]["provider"] == "openai"
    assert body["error"]["category"] == category
    assert body["error"]["retryable"] is retryable
    assert body["error"]["request_id"] == request_id
    assert body["error"]["retry_count"] == retry_count
    assert body["error"]["status_code"] == status_code


def _assert_no_fallback_telemetry(provider_events):
    event_names = [event["event"] for event in provider_events]
    assert "provider.fallback.local" not in event_names
    assert all("fallback" not in event_name for event_name in event_names)


def test_health_ready_and_openapi():
    client, key = _client()
    assert client.get("/healthz").status_code == 200
    assert client.get("/readyz").status_code == 200
    app.state.ready = False
    assert client.get("/readyz").status_code == 503
    app.state.ready = True
    schema = client.get("/openapi.json").json()
    enum_vals = schema["components"]["schemas"]["SolveRequest"]["properties"]["strategy"]["enum"]
    assert set(enum_vals) == {"cot", "react", "tot"}
    assert client.get("/metrics").status_code == 200


def test_solve_endpoint(monkeypatch):
    client, key = _client()

    def fake_solver(query: str, **kwargs):
        return {"final_answer": "ok"}

    monkeypatch.setattr("service.app._tree_of_thought", fake_solver)
    resp = client.post("/v1/solve", json={"query": "hi"}, headers={"X-API-Key": key})
    assert resp.status_code == 200
    assert resp.json()["final_answer"] == "ok"


def test_solve_endpoint_react(monkeypatch):
    client, key = _client()

    def fake_react(prompt: str, seed: int, max_steps: int = 2, rules=None):
        return {"final_answer": "ok", "trace": [], "confidence": 0.9, "meta": {"strategy": "react", "seed": seed}}

    monkeypatch.setattr("alpha.reasoning.react_lite.run_react_lite", fake_react)
    resp = client.post(
        "/v1/solve",
        json={"query": "hi", "strategy": "react"},
        headers={"X-API-Key": key},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["final_answer"] == "ok"
    assert body["meta"]["strategy"] == "react"


def test_solve_local_mode_ignores_provider_factory(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    app.state.provider_client_factory = lambda _model_set: (_ for _ in ()).throw(
        AssertionError("provider should not be used in local mode")
    )
    provider_events = []
    provider_accounting_records = []
    app.state.provider_telemetry_sink = provider_events.append
    app.state.provider_accounting_sink = provider_accounting_records.append

    def fake_solver(query: str, **kwargs):
        return {"final_answer": f"local:{query}"}

    monkeypatch.setattr("service.app._tree_of_thought", fake_solver)
    client, key = _client()
    resp = client.post("/v1/solve", json={"query": "hi"}, headers={"X-API-Key": key})

    assert resp.status_code == 200
    assert resp.json() == {"final_answer": "local:hi"}
    assert "safe_out" not in resp.json()
    assert provider_events == []
    assert provider_accounting_records == []
    _clear_provider_factory()
    _clear_provider_telemetry_sink()
    _clear_provider_accounting_sink()


def test_solve_openai_mode_uses_fake_provider_and_returns_normalized_text(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    fake = FakeProviderClient(
        [
            ProviderResult(
                provider="openai",
                model="gpt-test",
                text="provider answer",
                finish_reason="stop",
                usage=ProviderUsage(input_tokens=3, output_tokens=5, total_tokens=8),
                cost=ProviderCost(estimated_usd=0.001, source="price_hint"),
                latency_ms=12,
                request_id="req-test",
                raw_metadata={"raw": "must-not-leak", "provider_request_id": "openai-req-1"},
            )
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    provider_events = []
    provider_accounting_records = []
    app.state.provider_telemetry_sink = provider_events.append
    app.state.provider_accounting_sink = provider_accounting_records.append
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={
            "query": "hello provider",
            "context": {
                "system": "system prompt",
                "temperature": 0.2,
                "seed": 123,
                "tenant": "tenant-a",
                "model_set": "cost_saver",
            },
        },
        headers={"X-API-Key": key, "X-Request-ID": "req-test"},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["final_answer"] == "provider answer"
    assert body["meta"]["provider"] == "openai"
    assert body["meta"]["model"] == "gpt-test"
    assert body["meta"]["model_set"] == "cost_saver"
    assert body["meta"]["usage"] == {
        "input_tokens": 3,
        "output_tokens": 5,
        "total_tokens": 8,
    }
    assert "raw" not in str(body)

    assert [event["event"] for event in provider_events] == [
        PROVIDER_REQUEST_STARTED,
        PROVIDER_REQUEST_COMPLETED,
    ]
    started, completed = provider_events
    assert started == {
        "event": PROVIDER_REQUEST_STARTED,
        "provider": "openai",
        "model": "gpt-5-mini",
        "model_set": "cost_saver",
        "route": "tot",
        "request_id": "req-test",
        "status": "started",
        "tenant": "tenant-a",
    }
    assert completed["provider"] == "openai"
    assert completed["model"] == "gpt-test"
    assert completed["model_set"] == "cost_saver"
    assert completed["route"] == "tot"
    assert completed["request_id"] == "req-test"
    assert completed["status"] == "completed"
    assert completed["tenant"] == "tenant-a"
    assert completed["retry_count"] == 0
    assert completed["latency_ms"] == 12
    assert completed["input_tokens"] == 3
    assert completed["output_tokens"] == 5
    assert completed["total_tokens"] == 8
    assert completed["estimated_cost_usd"] == 0.001
    assert completed["cost_source"] == "price_hint"
    assert completed["finish_reason"] == "stop"
    assert completed["provider_request_id"] == "openai-req-1"

    assert provider_accounting_records == [
        {
            "event": PROVIDER_COST_RECORDED,
            "provider": "openai",
            "model": "gpt-test",
            "model_set": "cost_saver",
            "route": "tot",
            "request_id": "req-test",
            "tenant": "tenant-a",
            "input_tokens": 3,
            "output_tokens": 5,
            "total_tokens": 8,
            "estimated_cost_usd": 0.001,
            "cost_source": "price_hint",
            "retry_count": 0,
            "budget_status": "recorded",
            "accounting_source": "service:/v1/solve",
            "provider_request_id": "openai-req-1",
        }
    ]
    serialized_accounting = str(provider_accounting_records)
    assert "hello provider" not in serialized_accounting
    assert "system prompt" not in serialized_accounting
    assert "must-not-leak" not in serialized_accounting
    assert "Authorization" not in serialized_accounting
    assert "Bearer" not in serialized_accounting

    serialized_events = str(provider_events)
    assert "hello provider" not in serialized_events
    assert "system prompt" not in serialized_events
    assert "must-not-leak" not in serialized_events
    assert "Authorization" not in serialized_events
    assert "Bearer" not in serialized_events

    assert len(fake.requests) == 1
    provider_request = fake.requests[0]
    assert provider_request.prompt == "hello provider"
    assert provider_request.system == "system prompt"
    assert provider_request.model == "gpt-5-mini"
    assert provider_request.max_tokens == 1024
    assert provider_request.timeout_ms == 45000
    assert provider_request.temperature == 0.2
    assert provider_request.seed == 123
    assert provider_request.metadata["request_id"] == "req-test"
    assert provider_request.metadata["route"] == "tot"
    assert provider_request.metadata["model_set"] == "cost_saver"
    assert provider_request.metadata["tenant"] == "tenant-a"
    _clear_provider_factory()
    _clear_provider_telemetry_sink()
    _clear_provider_accounting_sink()


def test_solve_openai_missing_credentials_returns_safe_response(monkeypatch):
    secret = "sk-test-should-not-appear"
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    _clear_provider_factory()
    provider_accounting_records = []
    app.state.provider_accounting_sink = provider_accounting_records.append
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": "hi"},
        headers={"X-API-Key": key, "X-Request-ID": "req-missing"},
    )

    body = resp.json()
    body_text = resp.text
    assert resp.status_code == 503
    _assert_provider_safe_out_schema(
        body,
        category="missing_credentials",
        retryable=False,
        request_id="req-missing",
        status_code=None,
    )
    assert "OPENAI_API_KEY" in body_text
    assert secret not in body_text
    assert provider_accounting_records == []


@pytest.mark.parametrize(
    ("category", "status"),
    [
        ("timeout", 504),
        ("rate_limit", 429),
        ("network", 503),
    ],
)
def test_solve_openai_provider_errors_return_safe_responses(monkeypatch, category, status):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    secret = "sk-test-secret-value"
    fake = FakeProviderClient(
        [
            ProviderError(
                provider="openai",
                category=category,
                retryable=True,
                safe_message=f"safe {category} message",
                request_id="req-error",
            )
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    provider_events = []
    provider_accounting_records = []
    app.state.provider_telemetry_sink = provider_events.append
    app.state.provider_accounting_sink = provider_accounting_records.append
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": f"do not leak {secret}"},
        headers={"X-API-Key": key, "X-Request-ID": "req-error"},
    )

    body = resp.json()
    body_text = resp.text
    assert resp.status_code == status
    _assert_provider_safe_out_schema(
        body,
        category=category,
        retryable=True,
        request_id="req-error",
        status_code=None,
    )
    assert category in body_text
    assert secret not in body_text
    assert len(fake.requests) == 1
    assert [event["event"] for event in provider_events] == [
        PROVIDER_REQUEST_STARTED,
        PROVIDER_REQUEST_TIMEOUT if category == "timeout" else PROVIDER_REQUEST_FAILED,
    ]
    _assert_no_fallback_telemetry(provider_events)
    assert provider_accounting_records == []
    failure_event = provider_events[1]
    assert failure_event["provider"] == "openai"
    assert failure_event["model"] == "gpt-5"
    assert failure_event["model_set"] == "default"
    assert failure_event["route"] == "tot"
    assert failure_event["request_id"] == "req-error"
    assert failure_event["status"] == ("timeout" if category == "timeout" else "failed")
    assert failure_event["error_category"] == category
    assert failure_event["retryable"] is True
    assert failure_event["retry_count"] == 0
    assert failure_event["safe_message"] == f"safe {category} message"
    serialized_events = str(provider_events)
    assert secret not in serialized_events
    assert "Authorization" not in serialized_events
    assert "Bearer" not in serialized_events
    _clear_provider_factory()
    _clear_provider_telemetry_sink()
    _clear_provider_accounting_sink()


def test_solve_openai_unknown_provider_exception_emits_no_accounting(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    secret = "raw exception string sentinel sk-test-must-not-leak"

    class ExplodingProvider:
        def execute(self, provider_request):
            raise RuntimeError(secret)

    app.state.provider_client_factory = lambda _model_set: ExplodingProvider()
    provider_events = []
    provider_accounting_records = []
    app.state.provider_telemetry_sink = provider_events.append
    app.state.provider_accounting_sink = provider_accounting_records.append
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": "PROMPT-MUST-NOT-LEAK"},
        headers={"X-API-Key": key, "X-Request-ID": "req-unknown"},
    )

    assert resp.status_code == 502
    body = resp.json()
    body_text = resp.text
    _assert_provider_safe_out_schema(
        body,
        category="unknown",
        retryable=False,
        request_id="req-unknown",
        status_code=None,
    )
    assert body["final_answer"] == "SAFE-OUT: OpenAI request failed."
    assert secret not in body_text
    assert provider_accounting_records == []
    assert [event["event"] for event in provider_events] == [
        PROVIDER_REQUEST_STARTED,
        PROVIDER_REQUEST_FAILED,
    ]
    _assert_no_fallback_telemetry(provider_events)
    serialized_events = str(provider_events)
    assert secret not in serialized_events
    assert "PROMPT-MUST-NOT-LEAK" not in serialized_events
    _clear_provider_factory()
    _clear_provider_telemetry_sink()
    _clear_provider_accounting_sink()
