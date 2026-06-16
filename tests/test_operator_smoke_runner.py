from __future__ import annotations

import json

import httpx

from tools import operator_smoke_runner as runner

SECRET = "test-secret-value"
PROMPT = "Reply with one concise sentence that does not echo this prompt."


def test_argument_parser_requires_explicit_mode():
    parser = runner.build_parser()
    try:
        parser.parse_args([])
    except SystemExit as exc:
        assert exc.code == 2
    else:  # pragma: no cover
        raise AssertionError("parser accepted missing mode")


def test_local_mode_rejects_non_loopback_endpoint_without_transport_call():
    env = {
        "ALPHA_LOCAL_LLM_ENABLED": "1",
        "ALPHA_LOCAL_LLM_ENDPOINT": "https://example.com/api/chat",
        "ALPHA_LOCAL_LLM_MODEL": "fixture-model",
        "ALPHA_LOCAL_LLM_TIMEOUT_SECONDS": "1",
    }

    result = runner.run_local(PROMPT, env=env)

    assert result["mode"] == "local"
    assert result["provider"] == "ollama"
    assert result["status"] == "failed_closed"
    assert result["reason"] == "endpoint_not_local_non_evidence"
    assert result["smoke_evidence_only"] is True
    assert result["behavior_evidence"] is False
    assert result["quality_evidence"] is False
    assert result["readiness_evidence"] is False


def test_local_mode_rejects_hosted_provider_keys():
    env = {
        "ALPHA_LOCAL_LLM_ENABLED": "1",
        "ALPHA_LOCAL_LLM_ENDPOINT": "http://127.0.0.1:11434/api/chat",
        "ALPHA_LOCAL_LLM_MODEL": "fixture-model",
        "ALPHA_LOCAL_LLM_TIMEOUT_SECONDS": "1",
        "OPENAI_API_KEY": SECRET,
    }

    result = runner.run_local(PROMPT, env=env)
    captured = json.dumps(result, sort_keys=True)

    assert result["status"] == "failed_closed"
    assert result["reason"] == "provider_keys_forbidden_non_evidence"
    assert SECRET not in captured


def test_openai_mode_requires_all_gates_before_provider_call(monkeypatch):
    called = {"value": False}

    def fail_if_called(self, request):
        called["value"] = True
        raise AssertionError("provider should not be called")

    monkeypatch.setattr(runner.OpenAIProviderClient, "execute", fail_if_called)

    result = runner.run_openai(PROMPT, env={"MODEL_PROVIDER": "local"})

    assert result["status"] == "failed_closed"
    assert result["reason"] == "model_provider_not_openai"
    assert called["value"] is False


def test_openai_mode_missing_key_is_sanitized(monkeypatch):
    called = {"value": False}

    def fail_if_called(self, request):
        called["value"] = True
        raise AssertionError("provider should not be called")

    monkeypatch.setattr(runner.OpenAIProviderClient, "execute", fail_if_called)

    result = runner.run_openai(
        PROMPT,
        env={"MODEL_PROVIDER": "openai", "ALPHA_LIVE_OPENAI": "1", "OPENAI_MODEL": "gpt-test"},
    )
    captured = json.dumps(result, sort_keys=True)

    assert result["reason"] == "missing_openai_api_key"
    assert called["value"] is False
    assert SECRET not in captured


def test_openai_mode_success_schema_and_no_secret_output(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/responses"
        return httpx.Response(
            200,
            json={
                "id": "resp-1",
                "model": "gpt-test",
                "status": "completed",
                "output_text": "Smoke response from mocked provider.",
                "usage": {"input_tokens": 4, "output_tokens": 5, "total_tokens": 9},
            },
        )

    class FakeClient(runner.OpenAIProviderClient):
        def __init__(self, **kwargs):
            super().__init__(transport=httpx.MockTransport(handler), **kwargs)

    monkeypatch.setattr(runner, "OpenAIProviderClient", FakeClient)
    result = runner.run_openai(
        PROMPT,
        env={
            "MODEL_PROVIDER": "openai",
            "ALPHA_LIVE_OPENAI": "1",
            "OPENAI_API_KEY": SECRET,
            "OPENAI_MODEL": "gpt-test",
            "MODEL_SET": "operator_smoke",
        },
    )
    captured = json.dumps(result, sort_keys=True)

    assert result["status"] == "passed"
    assert result["reason"] == "openai_smoke_completed"
    assert result["mode"] == "openai"
    assert result["provider"] == "openai"
    assert result["model"] == "gpt-test"
    assert result["model_set"] == "operator_smoke"
    assert result["finish_reason"] == "stop"
    assert result["usage"] == {"input_tokens": 4, "output_tokens": 5, "total_tokens": 9}
    assert result["estimated_cost_usd"] is None
    assert result["output_preview"] == "Smoke response from mocked provider."
    assert result["smoke_evidence_only"] is True
    assert result["behavior_evidence"] is False
    assert result["quality_evidence"] is False
    assert result["readiness_evidence"] is False
    assert SECRET not in captured


def test_main_prints_expected_schema_for_gated_failure(monkeypatch, capsys):
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    monkeypatch.delenv("ALPHA_LIVE_OPENAI", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    code = runner.main(["--mode", "openai", "--prompt", PROMPT])
    printed = json.loads(capsys.readouterr().out)

    assert code == 1
    expected_keys = {
        "mode",
        "provider",
        "model",
        "status",
        "reason",
        "smoke_evidence_only",
        "behavior_evidence",
        "quality_evidence",
        "readiness_evidence",
        "latency_ms",
        "finish_reason",
        "usage",
        "estimated_cost_usd",
        "output_preview",
        "redaction_status",
        "errors",
    }
    assert expected_keys <= set(printed)
    assert printed["smoke_evidence_only"] is True
    assert printed["behavior_evidence"] is False
    assert printed["quality_evidence"] is False
    assert printed["readiness_evidence"] is False
