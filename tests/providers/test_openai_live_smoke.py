"""Optional gated live OpenAI smoke test for FastAPI /v1/solve."""

from __future__ import annotations

import json
import os

import pytest
from fastapi.testclient import TestClient

from alpha.providers import (
    PROVIDER_COST_RECORDED,
    PROVIDER_REQUEST_COMPLETED,
    PROVIDER_REQUEST_STARTED,
)
from service.app import app

pytestmark = [pytest.mark.live, pytest.mark.openai]

_LIVE_GATE = os.getenv("ALPHA_LIVE_OPENAI") == "1"
_HAS_OPENAI_API_KEY = bool(os.getenv("OPENAI_API_KEY", "").strip())

pytestmark.append(
    pytest.mark.skipif(
        not (_LIVE_GATE and _HAS_OPENAI_API_KEY),
        reason="requires ALPHA_LIVE_OPENAI=1 and non-empty OPENAI_API_KEY",
    )
)

_FORBIDDEN_OUTPUT_TOKENS = (
    "OPENAI_API_KEY",
    "Authorization",
    "Bearer",
    "raw_metadata",
    "raw prompt",
    "raw system",
    "provider request",
    "provider response",
)


def _clear_provider_state() -> None:
    for name in (
        "provider_client_factory",
        "provider_telemetry_sink",
        "provider_accounting_sink",
    ):
        if hasattr(app.state, name):
            delattr(app.state, name)


@pytest.fixture(autouse=True)
def _live_openai_context(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    _clear_provider_state()
    yield
    _clear_provider_state()


def test_live_openai_solve_emits_success_telemetry_and_cost():
    provider_events: list[dict[str, object]] = []
    provider_accounting_records: list[dict[str, object]] = []
    app.state.provider_telemetry_sink = provider_events.append
    app.state.provider_accounting_sink = provider_accounting_records.append
    api_key = "live-openai-smoke-api-key"
    prompt = "Reply with the single word: ok"
    original_api_keys = list(app.state.config.auth.keys)
    app.state.config.auth.keys = [api_key]

    try:
        client = TestClient(app)
        response = client.post(
            "/v1/solve",
            json={
                "query": prompt,
                "context": {
                    "model_set": "cost_saver",
                    "max_tokens": 8,
                },
            },
            headers={"X-API-Key": api_key, "X-Request-ID": "live-openai-smoke"},
            timeout=70,
        )

        assert response.status_code == 200
        body = response.json()
        assert body["final_answer"].strip()
        assert body["meta"]["provider"] == "openai"
        assert body["meta"]["model"]
        assert body["meta"]["model_set"] == "cost_saver"
        assert body["meta"]["finish_reason"]
        assert body["meta"]["usage"]
        assert "safe_out" not in body
        assert "error" not in body

        event_names = [event["event"] for event in provider_events]
        assert event_names == [PROVIDER_REQUEST_STARTED, PROVIDER_REQUEST_COMPLETED]
        assert provider_events[0]["provider"] == "openai"
        assert provider_events[0]["status"] == "started"
        assert provider_events[1]["provider"] == "openai"
        assert provider_events[1]["status"] == "completed"

        assert provider_accounting_records == [
            record
            for record in provider_accounting_records
            if record.get("event") == PROVIDER_COST_RECORDED
            and record.get("provider") == "openai"
            and record.get("budget_status") == "recorded"
        ]
        assert len(provider_accounting_records) == 1

        captured = json.dumps(
            {
                "response": body,
                "events": provider_events,
                "accounting": provider_accounting_records,
            },
            sort_keys=True,
        )
        for forbidden in (*_FORBIDDEN_OUTPUT_TOKENS, prompt, api_key):
            assert forbidden not in captured
        openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
        assert openai_api_key and openai_api_key not in captured
    finally:
        app.state.config.auth.keys = original_api_keys
