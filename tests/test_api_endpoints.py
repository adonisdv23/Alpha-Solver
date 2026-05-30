import os
import uuid

import pytest

os.environ.setdefault("API_KEY", "test")
os.environ.setdefault("RATE_LIMIT_PER_MINUTE", "2")

from fastapi.testclient import TestClient

from alpha.providers import (
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


@pytest.fixture(autouse=True)
def _default_local_provider(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    _clear_provider_factory()
    yield
    _clear_provider_factory()


def _client():
    key = str(uuid.uuid4())
    app.state.config.api_key = key
    return TestClient(app), key


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

    def fake_solver(query: str, **kwargs):
        return {"final_answer": f"local:{query}"}

    monkeypatch.setattr("service.app._tree_of_thought", fake_solver)
    client, key = _client()
    resp = client.post("/v1/solve", json={"query": "hi"}, headers={"X-API-Key": key})

    assert resp.status_code == 200
    assert resp.json() == {"final_answer": "local:hi"}
    _clear_provider_factory()


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
                raw_metadata={"raw": "must-not-leak"},
            )
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
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


def test_solve_openai_missing_credentials_returns_safe_response(monkeypatch):
    secret = "sk-test-should-not-appear"
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    _clear_provider_factory()
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": "hi"},
        headers={"X-API-Key": key, "X-Request-ID": "req-missing"},
    )

    body_text = resp.text
    assert resp.status_code == 503
    assert "SAFE-OUT" in body_text
    assert "missing_credentials" in body_text
    assert "OPENAI_API_KEY" in body_text
    assert secret not in body_text


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
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": f"do not leak {secret}"},
        headers={"X-API-Key": key, "X-Request-ID": "req-error"},
    )

    body_text = resp.text
    assert resp.status_code == status
    assert "SAFE-OUT" in body_text
    assert category in body_text
    assert secret not in body_text
    assert len(fake.requests) == 1
    _clear_provider_factory()
