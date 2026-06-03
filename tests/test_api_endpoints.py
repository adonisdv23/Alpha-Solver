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


def _provider_result(text, *, request_id="req-expert", model="gpt-test", finish_reason="stop"):
    return ProviderResult(
        provider="openai",
        model=model,
        text=text,
        finish_reason=finish_reason,
        usage=ProviderUsage(input_tokens=1, output_tokens=1, total_tokens=2),
        cost=ProviderCost(estimated_usd=0.0, source="price_hint"),
        latency_ms=1,
        request_id=request_id,
        raw_metadata={"provider_request_id": f"provider-{request_id}"},
    )


def test_solve_openai_expert_complex_route_makes_two_calls_and_returns_envelope(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    fake = FakeProviderClient(
        [
            _provider_result(
                '{"considerations":["Check migration risk"],'
                '"assumptions":["Traffic can be shifted gradually"],'
                '"confidence":0.72}'
            ),
            _provider_result("Use a staged migration with rollback checkpoints."),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={
            "query": (
                "Review this database migration plan, compare risks and tradeoffs, "
                "and decide whether the team should proceed this quarter."
            ),
            "context": {"route": "expert"},
        },
        headers={"X-API-Key": key, "X-Request-ID": "req-expert"},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["answer"] == "Use a staged migration with rollback checkpoints."
    assert body["final_answer"] == body["answer"]
    assert body["considerations"] == ["Check migration risk"]
    assert body["assumptions"] == ["Traffic can be shifted gradually"]
    assert body["confidence"] == 0.72
    assert body["mode"] == "answer_with_assumptions"
    assert body["meta"] == {
        "route": "expert",
        "complexity": "complex",
        "provider": "openai",
        "model": "gpt-test",
        "call_count": 2,
    }
    assert len(fake.requests) == 2
    assert fake.requests[0].metadata["route"] == "expert"
    assert fake.requests[1].metadata["route"] == "expert"
    blocked = "orches" + "tration"
    assert blocked not in resp.text.lower()
    _clear_provider_factory()


def test_solve_openai_expert_direct_mode_empty_step_two_returns_safe_out(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    fake = FakeProviderClient(
        [
            _provider_result(
                '{"considerations":["Check the requested decision"],'
                '"assumptions":[],"confidence":0.95}'
            ),
            _provider_result("   ", request_id="req-empty-step-two"),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={
            "query": (
                "Review this database migration plan, compare reliability risks "
                "and tradeoffs, and decide whether the team should proceed this "
                "quarter with rollback checkpoints."
            ),
            "context": {"route": "expert"},
        },
        headers={"X-API-Key": key, "X-Request-ID": "req-empty-step-two"},
    )

    assert resp.status_code == 502
    body = resp.json()
    _assert_provider_safe_out_schema(
        body,
        category="unknown",
        retryable=False,
        request_id="req-empty-step-two",
    )
    assert body["final_answer"] == "SAFE-OUT: Provider returned an empty expert answer."
    assert "answer" not in body
    assert body["final_answer"].strip()
    assert len(fake.requests) == 2
    _clear_provider_factory()


def test_solve_openai_expert_empty_step_two_safe_out_does_not_leak_raw_data(
    monkeypatch,
):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    secret = "sk-test-empty-expert-secret"
    raw_payload = "raw-provider-payload-secret"
    prompt_sentinel = "MUST_NOT_LEAK_RAW_PROMPT_SENTINEL"
    fake = FakeProviderClient(
        [
            _provider_result(
                '{"considerations":["Use safe response assembly"],'
                '"assumptions":[],"confidence":0.95}',
                request_id="req-empty-redact-preview",
            ),
            ProviderResult(
                provider="openai",
                model="gpt-test",
                text=" \n\t ",
                finish_reason="stop",
                usage=ProviderUsage(input_tokens=1, output_tokens=0, total_tokens=1),
                cost=ProviderCost(estimated_usd=0.0, source="price_hint"),
                latency_ms=1,
                request_id="req-empty-redact",
                raw_metadata={
                    "raw": raw_payload,
                    "api_key": secret,
                    "Authorization": f"Bearer {secret}",
                    "prompt": prompt_sentinel,
                    "provider_request_id": "provider-req-empty-redact",
                },
            ),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={
            "query": (
                f"Review {prompt_sentinel} migration reliability risks, compare "
                "tradeoffs, and decide whether this complex plan should proceed."
            ),
            "context": {"route": "expert"},
        },
        headers={"X-API-Key": key, "X-Request-ID": "req-empty-redact"},
    )

    assert resp.status_code == 502
    body = resp.json()
    _assert_provider_safe_out_schema(
        body, category="unknown", retryable=False, request_id="req-empty-redact"
    )
    serialized = resp.text
    assert secret not in serialized
    assert key not in serialized
    assert raw_payload not in serialized
    assert prompt_sentinel not in serialized
    assert "raw_metadata" not in serialized
    assert "provider_request_id" not in serialized
    assert "Authorization" not in serialized
    assert "Bearer" not in serialized
    assert "metadata" not in serialized
    assert "prompt" not in serialized.lower()
    _clear_provider_factory()


def test_solve_openai_expert_complex_route_preserves_requested_plan_shape(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    prompt = (
        "Create a two-hour operator test plan for /dashboard/expert-preview "
        "that separates setup, prompt runs, evidence capture, and rollback."
    )
    structured_answer = (
        "# Two-hour operator test plan for /dashboard/expert-preview\n\n"
        "| Time box | Section | Tasks | Evidence |\n"
        "| --- | --- | --- | --- |\n"
        "| 0:00-0:20 | Setup | Confirm local-provider config and login. | Smoke notes. |\n"
        "| 0:20-1:15 | Prompt runs | Run the controlled prompts. | Prompt/result summaries. |\n"
        "| 1:15-1:45 | Evidence capture | Save sanitized observations. | Evidence packet. |\n"
        "| 1:45-2:00 | Rollback | Return MODEL_PROVIDER=local and record status. | Rollback note. |\n\n"
        "Assumptions: supervised operator demo only; no production-readiness claim."
    )
    fake = FakeProviderClient(
        [
            _provider_result(
                '{"considerations":["Keep the requested two-hour test-plan deliverable first",'
                '"Preserve section separation for setup, prompt runs, evidence capture, and rollback"],'
                '"assumptions":["The run is a supervised operator preview, not MVP validation"],'
                '"confidence":0.82}'
            ),
            _provider_result(structured_answer),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": prompt, "context": {"route": "expert"}},
        headers={"X-API-Key": key, "X-Request-ID": "req-format"},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["final_answer"] == structured_answer
    assert body["answer"] == structured_answer
    assert "Two-hour operator test plan" in body["final_answer"]
    for section in ("Setup", "Prompt runs", "Evidence capture", "Rollback"):
        assert section in body["final_answer"]
    for time_box in ("0:00-0:20", "0:20-1:15", "1:15-1:45", "1:45-2:00"):
        assert time_box in body["final_answer"]
    assert body["considerations"] == [
        "Keep the requested two-hour test-plan deliverable first",
        "Preserve section separation for setup, prompt runs, evidence capture, and rollback",
    ]
    assert body["assumptions"] == [
        "The run is a supervised operator preview, not MVP validation"
    ]
    assert body["mode"] == "direct"
    assert len(fake.requests) == 2
    answer_prompt = fake.requests[1].prompt
    assert "Preserve the user's requested output format first" in answer_prompt
    assert "plan, checklist, table, release note, email, rubric, runbook" in answer_prompt
    assert "headings, section names, order, time boxes, bullets, tables" in answer_prompt
    assert "do not let them replace the requested deliverable" in answer_prompt
    assert prompt in answer_prompt
    _clear_provider_factory()


def test_solve_openai_expert_answerable_operator_plan_uses_assumptions_not_clarify(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    prompt = (
        "Create a two-hour operator test plan for /dashboard/expert-preview "
        "that separates setup, prompt runs, evidence capture, and rollback."
    )
    structured_answer = (
        "# Two-hour operator test plan for /dashboard/expert-preview\n\n"
        "Assumptions: supervised operator test; local rollback is available.\n\n"
        "## Setup\n"
        "- 0:00-0:20: Confirm dashboard auth, local-provider defaults, and evidence template.\n\n"
        "## Prompt runs\n"
        "- 0:20-1:10: Run the controlled prompts and record plain vs Alpha summaries.\n\n"
        "## Evidence capture\n"
        "- 1:10-1:45: Capture sanitized screenshots, request IDs, and observed modes.\n\n"
        "## Rollback\n"
        "- 1:45-2:00: Restore MODEL_PROVIDER=local and document unresolved issues."
    )
    fake = FakeProviderClient(
        [
            _provider_result(
                '{"considerations":["The request includes a concrete route and named sections"],'
                '"assumptions":["Run is a supervised operator preview"],"confidence":0.50}'
            ),
            _provider_result(structured_answer),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": prompt, "context": {"route": "expert"}},
        headers={"X-API-Key": key, "X-Request-ID": "req-clarify-threshold"},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] == "answer_with_assumptions"
    assert body["final_answer"] == structured_answer
    assert body["answer"] == structured_answer
    assert body["answer"] != "I need a few details before I can answer this well."
    assert "clarifying_questions" not in body
    for section in ("Setup", "Prompt runs", "Evidence capture", "Rollback"):
        assert section in body["final_answer"]
    assert "Assumptions" in body["final_answer"]
    assert body["assumptions"] == ["Run is a supervised operator preview"]
    assert len(fake.requests) == 2
    _clear_provider_factory()


@pytest.mark.parametrize(
    "step_one_text",
    [
        "",
        "not json and no confidence metadata",
        "{malformed json",
        '{"considerations":[],"assumptions":[]}',
    ],
)
def test_solve_openai_expert_actionable_plan_missing_step_one_metadata_answers_with_defaults(
    monkeypatch, step_one_text
):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    prompt = (
        "Create a two-hour operator test plan for /dashboard/expert-preview "
        "that separates setup, prompt runs, evidence capture, and rollback."
    )
    fake = FakeProviderClient(
        [
            _provider_result(step_one_text),
            _provider_result("   "),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": prompt, "context": {"route": "expert"}},
        headers={"X-API-Key": key, "X-Request-ID": "req-live-step1-fallback"},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] == "answer_with_assumptions"
    assert body["answer"].strip()
    assert body["final_answer"] == body["answer"]
    assert body["answer"] != "I need a few details before I can answer this well."
    assert "Two-hour operator test plan" in body["answer"]
    for section in ("Setup", "Prompt runs", "Evidence capture", "Rollback"):
        assert section in body["answer"]
    assert body["assumptions"] == [
        "Supervised operator preview only.",
        "Local rollback is available after the controlled run.",
        (
            "No MVP validation, production-readiness, Alpha Solver superiority, "
            "broad benchmark success, or exact billing accuracy claim is made from this run."
        ),
        "Evidence must be sanitized before capture or sharing.",
    ]
    assert "clarifying_questions" not in body
    assert body["meta"]["confidence_available"] is False
    assert body["meta"]["preview_parse_status"] in {"unstructured", "json"}
    assert len(fake.requests) == 2
    _clear_provider_factory()


def test_solve_openai_expert_answer_with_assumptions_empty_step_two_uses_plan_fallback(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    prompt = (
        "Create a two-hour operator test plan for /dashboard/expert-preview "
        "that separates setup, prompt runs, evidence capture, and rollback."
    )
    fake = FakeProviderClient(
        [
            _provider_result(
                '{"considerations":["Keep the requested deliverable primary"],'
                '"assumptions":["Run is a supervised operator preview"],"confidence":0.50}'
            ),
            _provider_result("   "),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": prompt, "context": {"route": "expert"}},
        headers={"X-API-Key": key, "X-Request-ID": "req-empty-primary"},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] == "answer_with_assumptions"
    assert body["answer"].strip()
    assert body["final_answer"] == body["answer"]
    assert "Two-hour operator test plan" in body["answer"]
    for section in ("Setup", "Prompt runs", "Evidence capture", "Rollback"):
        assert section in body["answer"]
    assert "I need a few details before I can answer this well." not in body["answer"]
    assert "clarifying_questions" not in body
    assert body["considerations"] == ["Keep the requested deliverable primary"]
    assert body["assumptions"] == ["Run is a supervised operator preview"]
    assert len(fake.requests) == 2
    _clear_provider_factory()

def test_solve_openai_expert_prompt_preserves_claim_boundaries(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    fake = FakeProviderClient(
        [
            _provider_result(
                '{"considerations":["Avoid broad conclusions from one demo"],'
                '"assumptions":["Evidence is limited"],"confidence":0.9}'
            ),
            _provider_result(
                "Release note: this supports follow-up testing but does not validate the MVP."
            ),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={
            "query": (
                "Write a release note for one operator demo, include scope boundaries and "
                "next-step caveats, and avoid claiming MVP validation, Alpha Solver "
                "superiority, production readiness, broad runtime readiness, answer-quality "
                "benchmark success, or provider reasoning orchestration."
            ),
            "context": {"route": "expert"},
        },
        headers={"X-API-Key": key, "X-Request-ID": "req-claims"},
    )

    assert resp.status_code == 200
    assert len(fake.requests) == 2
    answer_prompt = fake.requests[1].prompt
    assert "Do not overclaim certainty" in answer_prompt
    assert "validation" in answer_prompt
    assert "production readiness" in answer_prompt
    assert "superiority" in answer_prompt
    assert "provider reasoning orchestration" in answer_prompt
    body = resp.json()
    assert "does not validate the MVP" in body["final_answer"]
    assert body["considerations"] == ["Avoid broad conclusions from one demo"]
    assert body["assumptions"] == ["Evidence is limited"]
    _clear_provider_factory()


def test_solve_openai_expert_complex_route_preserves_system_prompt(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    fake = FakeProviderClient(
        [
            _provider_result(
                '{"considerations":["Follow caller constraints"],'
                '"assumptions":["System instruction remains authoritative"],'
                '"confidence":0.8}'
            ),
            _provider_result("Answer constrained by system prompt."),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()
    system_prompt = "You must answer in exactly two bullet points."

    resp = client.post(
        "/v1/solve",
        json={
            "query": (
                "Review this security migration plan, compare risks and tradeoffs, "
                "and decide whether the team should proceed this quarter."
            ),
            "context": {"route": "expert", "system": system_prompt},
        },
        headers={"X-API-Key": key, "X-Request-ID": "req-expert-system"},
    )

    assert resp.status_code == 200
    assert len(fake.requests) == 2
    assert fake.requests[0].system == system_prompt
    assert fake.requests[1].system == system_prompt
    _clear_provider_factory()


def test_solve_openai_expert_trivial_route_makes_one_direct_call(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    fake = FakeProviderClient([_provider_result("Short direct answer.")])
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": "Define alpha.", "context": {"route": "expert"}},
        headers={"X-API-Key": key},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["answer"] == "Short direct answer."
    assert body["final_answer"] == "Short direct answer."
    assert body["considerations"] == []
    assert body["assumptions"] == []
    assert body["confidence"] == 0.0
    assert body["mode"] == "direct"
    assert body["meta"]["complexity"] == "trivial"
    assert body["meta"]["call_count"] == 1
    assert len(fake.requests) == 1
    _clear_provider_factory()


def test_solve_openai_expert_clarify_mode_surfaces_questions_without_extra_call(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    raw_answer = "Proceed only after confirming the missing requirements."
    fake = FakeProviderClient(
        [
            _provider_result(
                '{"considerations":["Several requirements are missing"],'
                '"assumptions":["Budget is flexible",'
                '"The user has not specified the desired output format."],'
                '"confidence":0.50}'
            ),
            _provider_result(raw_answer),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={
            "query": (
                "Plan a security review and architecture migration where the goals, "
                "timeline, owners, and risk tolerance are uncertain."
            ),
            "context": {"route": "expert"},
        },
        headers={"X-API-Key": key},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] == "clarify"
    assert body["answer"] == "I need a few details before I can answer this well."
    assert body["final_answer"] == body["answer"]
    assert body["answer"] != raw_answer
    assert body["assumptions"] == [
        "Budget is flexible",
        "The user has not specified the desired output format.",
    ]
    assert body["considerations"] == ["Several requirements are missing"]
    assert 2 <= len(body["clarifying_questions"]) <= 4
    assert body["clarifying_questions"] == [
        "What is the main outcome you want from this request?",
        "What output format or deliverable should I produce?",
        "What timeline or deadline constraints should I preserve?",
        "What budget or resource constraints should I account for?",
    ]
    assert "Can you clarify?" not in body["clarifying_questions"]
    assert body["meta"]["call_count"] == 2
    assert len(fake.requests) == 2
    serialized = resp.text
    assert "raw_metadata" not in serialized
    assert "provider_request_id" not in serialized
    assert "Authorization" not in serialized
    assert "Bearer" not in serialized
    blocked = "orches" + "tration"
    assert blocked not in serialized.lower()
    _clear_provider_factory()


def test_solve_openai_expert_unstructured_preview_confidence_falls_back_to_clarify(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    raw_answer = (
        "This long provider answer should not be visible when preview confidence is unavailable."
    )
    fake = FakeProviderClient(
        [
            _provider_result(
                "Here is a prose review with some risks and assumptions, but no compact "
                "JSON object, no section headings, and no numeric confidence value."
            ),
            _provider_result(raw_answer),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={
            "query": (
                "Plan a security review and architecture migration where goals, timeline, "
                "owners, risk tolerance, and compliance constraints are uncertain."
            ),
            "context": {"route": "expert"},
        },
        headers={"X-API-Key": key},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] == "clarify"
    assert body["confidence"] == 0.0
    assert body["answer"] == "I need a few details before I can answer this well."
    assert body["final_answer"] == body["answer"]
    assert body["considerations"] == []
    assert body["assumptions"] == []
    assert 2 <= len(body["clarifying_questions"]) <= 4
    assert body["clarifying_questions"][0] == "What is the main outcome you want from this request?"
    assert body["meta"]["preview_parse_status"] == "unstructured"
    assert body["meta"]["confidence_available"] is False
    assert body["meta"]["call_count"] == 2
    assert raw_answer not in resp.text
    assert len(fake.requests) == 2
    _clear_provider_factory()


def test_solve_openai_expert_trivial_route_does_not_add_clarifying_questions(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    fake = FakeProviderClient([_provider_result("Short direct answer.")])
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": "Define alpha.", "context": {"route": "expert"}},
        headers={"X-API-Key": key},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] == "direct"
    assert "clarifying_questions" not in body
    assert body["meta"]["call_count"] == 1
    assert len(fake.requests) == 1
    _clear_provider_factory()


def test_solve_openai_expert_block_mode_remains_distinct_from_clarify(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    raw_answer = "This long provider answer should not be visible for true block mode."
    fake = FakeProviderClient(
        [
            _provider_result(
                '{"considerations":["The request may be unsafe"],'
                '"assumptions":[],"confidence":0.05}'
            ),
            _provider_result(raw_answer),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={
            "query": (
                "Review this uncertain security migration risk decision and decide "
                "whether the proposed ambiguous access-control plan should proceed."
            ),
            "context": {"route": "expert"},
        },
        headers={"X-API-Key": key},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] == "block"
    assert body["confidence"] == 0.05
    assert body["answer"] == (
        "I cannot safely provide a final answer for this request in the supervised preview."
    )
    assert body["final_answer"] == body["answer"]
    assert body["considerations"] == ["The request may be unsafe"]
    assert "clarifying_questions" not in body
    assert body["meta"]["call_count"] == 2
    assert "confidence_available" not in body["meta"]
    assert raw_answer not in resp.text
    assert len(fake.requests) == 2
    _clear_provider_factory()


def test_solve_openai_non_expert_route_preserves_pass_through_shape(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    fake = FakeProviderClient([_provider_result("provider answer")])
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": "hello provider", "context": {"route": "tot"}},
        headers={"X-API-Key": key, "X-Request-ID": "req-pass"},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert set(body) == {"final_answer", "meta"}
    assert body["final_answer"] == "provider answer"
    assert "answer" not in body
    assert len(fake.requests) == 1
    assert fake.requests[0].metadata["route"] == "tot"
    _clear_provider_factory()


@pytest.mark.parametrize(
    ("provider_text", "finish_reason"),
    [
        ("", "incomplete"),
        (" \n\t ", "stop"),
    ],
)
def test_solve_openai_plain_empty_final_answer_returns_safe_out(
    monkeypatch, provider_text, finish_reason
):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    fake = FakeProviderClient(
        [
            _provider_result(
                provider_text,
                request_id="req-empty-provider-final",
                finish_reason=finish_reason,
            )
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": "hello provider", "context": {"route": "tot"}},
        headers={"X-API-Key": key, "X-Request-ID": "req-empty-provider-final"},
    )

    assert resp.status_code == 502
    body = resp.json()
    _assert_provider_safe_out_schema(
        body,
        category="unknown",
        retryable=False,
        request_id="req-empty-provider-final",
    )
    assert body["final_answer"] == "SAFE-OUT: Provider returned an empty answer."
    assert body["final_answer"].strip()
    assert "answer" not in body
    assert len(fake.requests) == 1
    assert fake.requests[0].metadata["route"] == "tot"
    _clear_provider_factory()


def test_solve_openai_plain_empty_final_answer_safe_out_does_not_leak_raw_data(
    monkeypatch,
):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    secret = "sk-test-plain-empty-secret"
    raw_payload = "plain-empty-raw-provider-payload"
    prompt_sentinel = "PLAIN_EMPTY_PROMPT_MUST_NOT_LEAK"
    fake = FakeProviderClient(
        [
            ProviderResult(
                provider="openai",
                model="gpt-test",
                text="",
                finish_reason="incomplete",
                usage=ProviderUsage(input_tokens=1, output_tokens=0, total_tokens=1),
                cost=ProviderCost(estimated_usd=0.0, source="price_hint"),
                latency_ms=1,
                request_id="req-empty-plain-redact",
                raw_metadata={
                    "raw": raw_payload,
                    "api_key": secret,
                    "Authorization": f"Bearer {secret}",
                    "prompt": prompt_sentinel,
                    "provider_request_id": "provider-req-empty-plain-redact",
                },
            )
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": f"Review {prompt_sentinel} and return a short answer."},
        headers={"X-API-Key": key, "X-Request-ID": "req-empty-plain-redact"},
    )

    assert resp.status_code == 502
    body = resp.json()
    _assert_provider_safe_out_schema(
        body,
        category="unknown",
        retryable=False,
        request_id="req-empty-plain-redact",
    )
    serialized = resp.text
    assert secret not in serialized
    assert key not in serialized
    assert raw_payload not in serialized
    assert prompt_sentinel not in serialized
    assert "raw_metadata" not in serialized
    assert "provider_request_id" not in serialized
    assert "Authorization" not in serialized
    assert "Bearer" not in serialized
    assert "metadata" not in serialized
    assert "traceback" not in serialized.lower()
    assert "prompt" not in serialized.lower()
    assert "answer" not in body
    _clear_provider_factory()


def test_solve_openai_expert_trivial_empty_final_answer_returns_safe_out(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    fake = FakeProviderClient(
        [_provider_result("", request_id="req-empty-trivial", finish_reason="incomplete")]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={"query": "Define alpha.", "context": {"route": "expert"}},
        headers={"X-API-Key": key, "X-Request-ID": "req-empty-trivial"},
    )

    assert resp.status_code == 502
    body = resp.json()
    _assert_provider_safe_out_schema(
        body,
        category="unknown",
        retryable=False,
        request_id="req-empty-trivial",
    )
    assert body["final_answer"].strip()
    assert "answer" not in body
    assert len(fake.requests) == 1
    _clear_provider_factory()


def test_solve_expert_route_local_mode_preserves_local_response(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    app.state.provider_client_factory = lambda _model_set: (_ for _ in ()).throw(
        AssertionError("provider should not be used in local mode")
    )

    def fake_solver(query: str):
        return {"final_answer": f"local:{query}"}

    monkeypatch.setattr("service.app._tree_of_thought", fake_solver)
    client, key = _client()
    resp = client.post(
        "/v1/solve",
        json={"query": "hi", "context": {"route": "expert"}},
        headers={"X-API-Key": key},
    )

    assert resp.status_code == 200
    assert resp.json() == {"final_answer": "local:hi"}
    _clear_provider_factory()


def test_solve_openai_expert_envelope_does_not_leak_secrets_or_raw_metadata(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    secret = "sk-test-expert-secret"
    fake = FakeProviderClient(
        [
            ProviderResult(
                provider="openai",
                model="gpt-test",
                text='{"considerations":["Use safe metadata"],"assumptions":[],"confidence":0.9}',
                finish_reason="stop",
                usage=ProviderUsage(input_tokens=1, output_tokens=1, total_tokens=2),
                cost=ProviderCost(estimated_usd=0.0, source="price_hint"),
                latency_ms=1,
                request_id="req-leak",
                raw_metadata={"raw": secret, "provider_request_id": "provider-req-leak"},
            ),
            _provider_result("Safe final answer.", request_id="req-leak"),
        ]
    )
    app.state.provider_client_factory = lambda _model_set: fake
    client, key = _client()

    resp = client.post(
        "/v1/solve",
        json={
            "query": "Review a security architecture migration with uncertain risks.",
            "context": {"route": "expert"},
        },
        headers={"X-API-Key": key, "X-Request-ID": "req-leak"},
    )

    assert resp.status_code == 200
    serialized = resp.text
    assert secret not in serialized
    assert "raw_metadata" not in serialized
    assert "provider_request_id" not in serialized
    assert "Authorization" not in serialized
    assert "Bearer" not in serialized
    blocked = "orches" + "tration"
    assert blocked not in serialized.lower()
    _clear_provider_factory()
