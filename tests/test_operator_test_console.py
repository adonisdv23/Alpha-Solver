from __future__ import annotations

import json

from fastapi.testclient import TestClient

from tools import operator_test_console as console

SECRET = "test-" + "secret-" + "value"
PROMPT = "Reply with one concise sentence that does not echo this prompt."


def test_console_documents_loopback_only_run_command():
    html = console.render_result_html()

    assert "--host 127.0.0.1" in html
    assert "/v1/solve" not in html


def test_console_rejects_non_loopback_host():
    client = TestClient(console.app)

    response = client.get("/", headers={"host": "example.com"})

    assert response.status_code == 403
    assert response.json()["detail"] == "operator_test_console_loopback_only"


def test_openai_mode_preserves_fail_closed_environment_gates(monkeypatch):
    called = {"value": False}

    def fail_if_called(self, request):
        called["value"] = True
        raise AssertionError("provider should not be called")

    monkeypatch.setattr(console.smoke_runner.OpenAIProviderClient, "execute", fail_if_called)
    result = console.run_console_smoke("openai", "gpt-test", PROMPT, env={"MODEL_PROVIDER": "local"})

    assert result["status"] == "failed_closed"
    assert result["reason"] == "model_provider_not_openai"
    assert called["value"] is False


def test_local_mode_rejects_non_loopback_endpoint():
    result = console.run_console_smoke(
        "local",
        "qwen2.5:3b",
        PROMPT,
        env={
            "ALPHA_LOCAL_LLM_ENABLED": "1",
            "ALPHA_LOCAL_LLM_ENDPOINT": "https://example.com/api/chat",
            "ALPHA_LOCAL_LLM_TIMEOUT_SECONDS": "1",
        },
    )

    assert result["status"] == "failed_closed"
    assert result["reason"] == "endpoint_not_local_non_evidence"


def test_sanitized_json_rendered_without_secrets():
    result = console.sanitize_result(
        {
            "status": "failed_closed",
            "provider": "openai",
            "model": "gpt-test",
            "api_key": SECRET,
            "errors": [{"message": "bearer-prefix " + SECRET}],
        }
    )
    html = console.render_result_html(result)
    payload = json.dumps(result, sort_keys=True)

    assert SECRET not in payload
    assert SECRET not in html
    assert "[REDACTED]" in payload
    assert "sanitized-json" in html


def test_evidence_flags_remain_smoke_only():
    result = console.sanitize_result(
        {
            "smoke_evidence_only": False,
            "behavior_evidence": True,
            "quality_evidence": True,
            "readiness_evidence": True,
        }
    )

    assert result["smoke_evidence_only"] is True
    assert result["behavior_evidence"] is False
    assert result["quality_evidence"] is False
    assert result["readiness_evidence"] is False


def test_no_api_key_field_or_secret_in_rendered_output():
    html = console.render_result_html({"status": "passed", "api_key": SECRET})

    assert "type=\"password\"" not in html
    assert "name=\"api_key\"" not in html
    assert SECRET not in html


def test_ui_result_rendering_handles_local_ollama_shape():
    result = console.sanitize_result(
        {
            "mode": "local",
            "provider": "ollama",
            "model": "qwen2.5:3b",
            "status": "passed",
            "latency_ms": 123,
            "usage": None,
            "output_preview": "ok",
        }
    )
    html = console.render_result_html(result)

    assert "Status: passed" in html
    assert "Provider: ollama" in html
    assert "Model: qwen2.5:3b" in html
    assert "Latency ms: 123" in html


def test_ui_result_rendering_handles_openai_shape_with_usage_tokens():
    result = console.sanitize_result(
        {
            "mode": "openai",
            "provider": "openai",
            "model": "gpt-4.1-mini-2025-04-14",
            "status": "passed",
            "latency_ms": 456,
            "usage": {"input_tokens": 4, "output_tokens": 5, "total_tokens": 9},
            "estimated_cost_usd": None,
            "output_preview": "ok",
        }
    )
    html = console.render_result_html(result)

    assert "Provider: openai" in html
    assert "gpt-4.1-mini-2025-04-14" in html
    assert "input_tokens" in html
    assert "Estimated cost" not in html


def test_loopback_api_returns_sanitized_json(monkeypatch):
    def fake_run_local(prompt, env=None):
        return {
            "mode": "local",
            "provider": "ollama",
            "model": env["ALPHA_LOCAL_LLM_MODEL"],
            "status": "passed",
            "output_preview": "ok",
            "api_key": SECRET,
        }

    monkeypatch.setattr(console.smoke_runner, "run_local", fake_run_local)
    client = TestClient(console.app)

    response = client.post(
        "/api/run",
        headers={"host": "127.0.0.1"},
        json={"mode": "local", "model": "qwen2.5:3b", "prompt": PROMPT},
    )

    assert response.status_code == 200
    assert SECRET not in response.text
    assert response.json()["api_key"] == "[REDACTED]"
