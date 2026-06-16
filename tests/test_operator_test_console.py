from __future__ import annotations

import asyncio
import html as html_lib
import json

import httpx

from tools import operator_test_console as console

SECRET = "test-" + "secret-" + "value"
PROMPT = "Reply with one concise sentence that does not echo this prompt."


def _api_post(path: str, *, host: str, peer: str, payload: dict[str, str]) -> httpx.Response:
    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=console.app, client=(peer, 12345))
        async with httpx.AsyncClient(transport=transport, base_url=f"http://{host}") as client:
            return await client.post(path, headers={"host": host}, json=payload)

    return asyncio.run(run())


def test_console_documents_loopback_only_run_command():
    html = console.render_result_html()

    assert "--host 127.0.0.1" in html
    assert "/v1/solve" not in html


def test_non_loopback_host_is_rejected():
    assert console._is_loopback_request("example.com", "127.0.0.1") is False


def test_loopback_host_with_non_loopback_peer_is_rejected():
    assert console._is_loopback_request("127.0.0.1", "203.0.113.7") is False


def test_loopback_host_with_loopback_peer_is_allowed():
    assert console._is_loopback_request("127.0.0.1:8765", "127.0.0.1") is True
    assert console._is_loopback_request("localhost:8765", "localhost") is True
    assert console._is_loopback_request("[::1]:8765", "::1") is True


def test_absent_host_with_loopback_peer_is_allowed_for_framework_context():
    assert console._is_loopback_request(None, "127.0.0.1") is True


def test_api_route_rejects_non_loopback_peer():
    response = _api_post(
        "/api/run",
        host="127.0.0.1",
        peer="203.0.113.7",
        payload={"mode": "local", "model": "qwen2.5:3b", "prompt": PROMPT},
    )

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


def test_unsupported_mode_returns_failed_closed_without_provider_calls(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("provider runner should not be called")

    monkeypatch.setattr(console.smoke_runner, "run_local", fail_if_called)
    monkeypatch.setattr(console.smoke_runner, "run_openai", fail_if_called)

    result = console.run_console_smoke("bad-mode", "model", PROMPT, env={})

    assert result["status"] == "failed_closed"
    assert result["reason"] == "unsupported_mode"
    assert result["smoke_evidence_only"] is True
    assert result["behavior_evidence"] is False
    assert result["quality_evidence"] is False
    assert result["readiness_evidence"] is False


def test_api_route_unsupported_mode_returns_sanitized_json_not_500(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("provider runner should not be called")

    monkeypatch.setattr(console.smoke_runner, "run_local", fail_if_called)
    monkeypatch.setattr(console.smoke_runner, "run_openai", fail_if_called)

    response = _api_post(
        "/api/run",
        host="127.0.0.1",
        peer="127.0.0.1",
        payload={"mode": "bad-mode", "model": "model", "prompt": PROMPT},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "failed_closed"
    assert payload["reason"] == "unsupported_mode"
    assert payload["smoke_evidence_only"] is True
    assert payload["behavior_evidence"] is False
    assert payload["quality_evidence"] is False
    assert payload["readiness_evidence"] is False


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


def test_usage_token_counts_remain_visible_when_numeric():
    result = console.sanitize_result(
        {
            "usage": {
                "input_tokens": 11,
                "output_tokens": 7,
                "total_tokens": 18,
                "cached_tokens": 3,
            }
        }
    )

    assert result["usage"]["input_tokens"] == 11
    assert result["usage"]["output_tokens"] == 7
    assert result["usage"]["total_tokens"] == 18
    assert result["usage"]["cached_tokens"] == 3


def test_secret_fields_and_bearer_strings_remain_redacted():
    result = console.sanitize_result(
        {
            "api_key": SECRET,
            "Author" + "ization": "bearer " + SECRET,
            "access_token": SECRET,
            "refresh_token": SECRET,
            "nested": {"message": "bearer-prefix " + SECRET},
            "other": "s" + "k-" + SECRET,
        }
    )
    payload = json.dumps(result, sort_keys=True)

    assert SECRET not in payload
    assert result["api_key"] == "[REDACTED]"
    assert result["Author" + "ization"] == "[REDACTED]"
    assert result["access_token"] == "[REDACTED]"
    assert result["refresh_token"] == "[REDACTED]"
    assert result["nested"]["message"] == "[REDACTED]"
    assert result["other"] == "[REDACTED]"


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


def test_openai_form_state_is_preserved_after_submit():
    prompt = "Use <xml> & keep form state."
    html = console.render_result_html(
        {"mode": "openai", "provider": "openai", "model": console.DEFAULT_OPENAI_MODEL},
        form_state={"mode": "openai", "model": console.DEFAULT_OPENAI_MODEL, "prompt": prompt},
    )

    assert '<option value="openai" selected>openai</option>' in html
    assert f'value="{console.DEFAULT_OPENAI_MODEL}"' in html
    assert html_lib.escape(prompt) in html
    assert prompt not in html


def test_local_form_state_is_preserved_after_submit():
    prompt = "Local prompt should remain visible."
    html = console.render_result_html(
        {"mode": "local", "provider": "ollama", "model": "qwen2.5:3b"},
        form_state={"mode": "local", "model": "qwen2.5:3b", "prompt": prompt},
    )

    assert '<option value="local" selected>local</option>' in html
    assert 'value="qwen2.5:3b"' in html
    assert prompt in html


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

    response = _api_post(
        "/api/run",
        host="127.0.0.1",
        peer="127.0.0.1",
        payload={"mode": "local", "model": "qwen2.5:3b", "prompt": PROMPT},
    )

    assert response.status_code == 200
    assert SECRET not in response.text
    assert response.json()["api_key"] == "[REDACTED]"
