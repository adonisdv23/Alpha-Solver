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
                "reasoning_tokens": 2,
                "prompt_token_count": 4,
            }
        }
    )

    assert result["usage"]["input_tokens"] == 11
    assert result["usage"]["output_tokens"] == 7
    assert result["usage"]["total_tokens"] == 18
    assert result["usage"]["cached_tokens"] == 3
    assert result["usage"]["reasoning_tokens"] == 2
    assert result["usage"]["prompt_token_count"] == 4


def test_usage_access_and_refresh_tokens_redact_even_when_numeric():
    result = console.sanitize_result(
        {
            "usage": {
                "input_tokens": 11,
                "access_token": 123456,
                "refresh_token": 789,
            }
        }
    )

    assert result["usage"]["input_tokens"] == 11
    assert result["usage"]["access_token"] == "[REDACTED]"
    assert result["usage"]["refresh_token"] == "[REDACTED]"


def test_secret_fields_and_bearer_strings_remain_redacted():
    result = console.sanitize_result(
        {
            "api_key": SECRET,
            "Author" + "ization": "bear" + "er " + SECRET,
            "access_token": SECRET,
            "refresh_token": SECRET,
            "nested": {"message": "bearer-prefix " + SECRET},
            "upper": "Bear" + "er " + SECRET,
            "lower": "bear" + "er " + SECRET,
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
    assert result["upper"] == "[REDACTED]"
    assert result["lower"] == "[REDACTED]"
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

    # Friendly result display uses readable labels and a clear passed state.
    assert "Status" in html
    assert "state-passed" in html
    assert ">passed<" in html
    assert ">ollama<" in html
    assert ">qwen2.5:3b<" in html
    assert ">123<" in html


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

    assert ">openai<" in html
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


# UI polish coverage: dropdowns, prompt limit, friendly result display, copy JSON.


def test_mode_dropdown_exists_with_local_and_openai():
    html = console.render_result_html()

    assert '<select name="mode" id="mode-select">' in html
    assert "<option value=\"local\"" in html
    assert "<option value=\"openai\"" in html


def test_model_dropdown_exists_and_is_mode_aware():
    html = console.render_result_html()

    assert '<select name="model" id="model-select">' in html
    # The browser-side options map carries both mode lists for mode-aware switching.
    assert '"local":' in html
    assert '"openai":' in html


def test_local_model_dropdown_options_present():
    html = console.render_result_html({"mode": "local", "provider": "ollama", "model": "qwen2.5:3b"})

    for option in ("qwen2.5:3b", "gemma3:4b", "llama3.2:1b", "llama3.2:latest"):
        assert f'"{option}"' in html


def test_openai_model_dropdown_options_present():
    html = console.render_result_html(
        {"mode": "openai", "provider": "openai", "model": console.DEFAULT_OPENAI_MODEL},
        form_state={"mode": "openai", "model": console.DEFAULT_OPENAI_MODEL, "prompt": PROMPT},
    )

    for option in ("gpt-4.1-mini", "gpt-4.1", "gpt-4o-mini"):
        assert f'"{option}"' in html


def test_custom_model_input_is_supported():
    html = console.render_result_html()

    assert 'name="custom_model"' in html
    assert '"custom"' in html
    assert "custom (enter below)" in html


def test_custom_model_value_is_preserved_after_submit():
    html = console.render_result_html(
        {"mode": "openai", "provider": "openai", "model": "my-private-model"},
        form_state={"mode": "openai", "model_option": "custom", "custom_model": "my-private-model", "prompt": PROMPT},
    )

    assert '<option value="custom" selected>' in html
    assert 'name="custom_model" id="custom-model" value="my-private-model"' in html


def test_prompt_length_limit_500_is_visible():
    html = console.render_result_html()

    assert "/ 500 characters" in html
    assert "max length: 500" in html


def test_prompt_over_limit_warning_copy_is_present():
    html = console.render_result_html()

    assert "Prompt is over the 500-character smoke-runner limit. Shorten the prompt and retry." in html


def test_friendly_result_display_includes_reason():
    result = console.sanitize_result(
        {
            "mode": "openai",
            "provider": "openai",
            "model": "gpt-4.1-mini",
            "status": "failed_closed",
            "reason": "missing_openai_api_key",
            "errors": [{"message": "OPENAI_API_KEY required"}],
        }
    )
    html = console.render_result_html(result)

    assert "Reason" in html
    assert "missing_openai_api_key" in html
    # The safe reason gets a friendly operator-facing explanation.
    assert "OPENAI_API_KEY set in the local terminal environment" in html
    assert "state-failed" in html


def test_friendly_result_display_includes_errors():
    result = console.sanitize_result(
        {
            "mode": "local",
            "provider": "ollama",
            "model": "qwen2.5:3b",
            "status": "failed_closed",
            "reason": "endpoint_not_local_non_evidence",
            "errors": [{"message": "endpoint_not_local_non_evidence"}],
        }
    )
    html = console.render_result_html(result)

    assert "Errors" in html
    assert "endpoint_not_local_non_evidence" in html


def test_prompt_too_long_result_renders_operator_message():
    result = console.run_console_smoke("local", "qwen2.5:3b", "x" * 501)
    html = console.render_result_html(result, form_state={"mode": "local", "model": "qwen2.5:3b", "prompt": "x" * 501})

    assert result["reason"] == "prompt_too_long"
    assert "Prompt is over the 500-character smoke-runner limit. Shorten the prompt and retry." in html
    assert "state-failed" in html


def test_passed_status_renders_clear_passed_state():
    result = console.sanitize_result(
        {"mode": "local", "provider": "ollama", "model": "qwen2.5:3b", "status": "passed", "latency_ms": 12}
    )
    html = console.render_result_html(result)

    assert "state-passed" in html
    assert "Passed (smoke only)" in html


def test_copy_json_button_targets_only_sanitized_json():
    html = console.render_result_html(
        console.sanitize_result({"status": "passed", "provider": "ollama"})
    )

    assert 'id="copy-json"' in html
    assert "copySanitizedJson" in html

    body = html.split("function copySanitizedJson()", 1)[1].split("function ", 1)[0]
    # The copy routine reads only the sanitized JSON panel text content.
    assert 'getElementById("sanitized-json")' in body
    assert ".textContent" in body
    # It must not read form state (mode, model, custom model, or prompt) when copying.
    assert "mode-select" not in body
    assert "model-select" not in body
    assert "prompt-input" not in body
    assert "custom-model" not in body


def test_secret_and_password_keys_remain_redacted():
    result = console.sanitize_result(
        {
            "secret": SECRET,
            "password": SECRET,
            "nested": {"password": SECRET, "secret": SECRET},
        }
    )
    payload = json.dumps(result, sort_keys=True)

    assert SECRET not in payload
    assert result["secret"] == "[REDACTED]"
    assert result["password"] == "[REDACTED]"
    assert result["nested"]["password"] == "[REDACTED]"
    assert result["nested"]["secret"] == "[REDACTED]"


def test_no_external_assets_or_telemetry_in_rendered_html():
    html = console.render_result_html()

    assert "http://" not in html.replace("http://127.0.0.1:11434/api/chat", "")
    assert "https://" not in html
    assert "src=" not in html
    assert "cdn" not in html.lower()
    assert "/v1/solve" not in html

def test_route_preview_panel_renders_and_is_separate_from_smoke_execution():
    html = console.render_result_html()

    assert 'id="route-preview-panel"' in html
    assert 'action="/preview"' in html
    assert 'action="/run"' in html
    assert html.index('action="/preview"') < html.index('action="/run"')
    assert 'Preview route only' in html
    assert 'Run bounded smoke check' in html


def test_route_preview_hidden_inputs_stay_synced_with_visible_smoke_controls():
    html = console.render_result_html()

    assert 'name="mode" id="preview-mode"' in html
    assert 'name="model" id="preview-model"' in html
    assert 'name="custom_model" id="preview-custom-model"' in html
    assert 'function syncPreviewInputs()' in html
    assert 'previewMode.value = modeSelect.value' in html
    assert 'previewModel.value = modelSelect.value' in html
    assert 'previewCustomModel.value = customModel.value' in html
    assert 'customModel.addEventListener("input", syncPreviewInputs)' in html


def test_preview_form_uses_current_changed_model_selection_without_smoke_execution(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("smoke execution must not run during preview")

    seen = {}

    def fake_preview(task, mode, model):
        seen.update({"task": task, "mode": mode, "model": model})
        return {
            "status": "preview_only",
            "task": task,
            "task_family": "general",
            "model_route": {
                "recommended_model": model,
                "provider_or_local_execution_authorized": False,
                "reasons": ["test_current_selection"],
                "warnings": [],
            },
            "tool_route": {"recommended_tool_family": "none", "execution_authorized": False},
            "fallback_path": [],
            "evidence_boundary": console.ROUTE_PREVIEW_BOUNDARY,
            "provider_or_local_execution_authorized": False,
            "tool_execution_authorized": False,
        }

    monkeypatch.setattr(console.smoke_runner, "run_local", fail_if_called)
    monkeypatch.setattr(console.smoke_runner, "run_openai", fail_if_called)
    monkeypatch.setattr(console, "build_route_preview", fake_preview)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=console.app, client=("127.0.0.1", 12345))
        async with httpx.AsyncClient(transport=transport, base_url="http://127.0.0.1") as client:
            return await client.post(
                "/preview",
                headers={"host": "127.0.0.1"},
                data={
                    "mode": "openai",
                    "model": "custom",
                    "custom_model": "gpt-current-preview",
                    "task": "preview this current route",
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    assert seen == {
        "mode": "openai",
        "model": "gpt-current-preview",
        "task": "preview this current route",
    }
    assert "gpt-current-preview" in response.text
    assert "Provider/local execution authorized" in response.text
    assert "Tool execution authorized" in response.text
    assert ">false<" in response.text


def test_route_preview_uses_existing_router_metadata_and_displays_fields():
    preview = console.build_route_preview("browse repo files and run pytest", "local", "qwen2.5:3b")
    html = console.render_result_html(route_preview=preview)

    assert preview["model_route"]["recommended_model"] == "qwen2.5:3b"
    assert preview["tool_route"]["recommended_tool_family"]
    assert "Recommended mode" in html
    assert "Recommended model" in html
    assert "Selected backend type" in html
    assert "Selected cost tier" in html
    assert "Selected latency tier" in html
    assert "Selected context tier" in html
    assert "Selected privacy tier" in html
    assert "Smoke eligibility" in html
    assert "No-call evidence flag" in html
    assert "Confidence label" in html
    assert "Operator caveat" in html
    assert "Catalog inclusion is not model quality evidence" in html
    assert "qwen2.5:3b" in html
    assert "Recommended tool route" in html
    assert "Tool category" in html
    assert preview["tool_route"]["recommended_tool_id"] in html
    assert "Route reasons (grouped)" in html
    assert "routing_preview_only" in html
    assert "tool_recommendation_preview_only" in html
    assert "untrusted_input_cannot_authorize_execution" in html
    assert "Fallback candidates" in html
    assert "mode: local" in html
    assert "backend_type: local" in html
    assert "Tool fallback or alternative routes" in html
    assert "Evidence boundary" in html
    assert "metadata-only" in html
    assert "Provider/local execution authorized" in html
    assert ">false<" in html
    assert "Tool execution authorized" in html


def test_route_preview_failed_closed_renders_operator_safe_failure():
    preview = console.build_route_preview("x" * 501, "local", "qwen2.5:3b")
    html = console.render_result_html(route_preview=preview)

    assert preview["model_route"]["status"] == "failed_closed"
    assert "failed_closed" in html
    assert "prompt_too_long_for_smoke_runner" in html
    assert "Recommended model" in html
    assert ">none<" in html


def test_route_preview_openai_metadata_can_render_without_execution(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("smoke execution must not run during hosted metadata preview")

    monkeypatch.setattr(console.smoke_runner, "run_openai", fail_if_called)
    preview = console.build_route_preview("summarize a local note", "openai", "gpt-4.1-mini")
    html = console.render_result_html(route_preview=preview)

    assert preview["model_route"]["recommended_mode"] == "openai"
    assert preview["model_route"]["selected_backend_type"] == "hosted"
    assert "gpt-4.1-mini" in html
    assert "hosted" in html
    assert preview["provider_or_local_execution_authorized"] is False

def test_route_preview_never_authorizes_provider_local_or_tool_execution():
    preview = console.build_route_preview("call github and browse", "local", "qwen2.5:3b")

    assert preview["provider_or_local_execution_authorized"] is False
    assert preview["tool_execution_authorized"] is False
    assert preview["model_route"]["provider_or_local_execution_authorized"] is False
    assert preview["tool_route"]["execution_authorized"] is False


def test_route_preview_api_does_not_invoke_smoke_provider_or_tools(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("smoke execution must not run during preview")

    monkeypatch.setattr(console.smoke_runner, "run_local", fail_if_called)
    monkeypatch.setattr(console.smoke_runner, "run_openai", fail_if_called)

    response = _api_post(
        "/api/preview",
        host="127.0.0.1",
        peer="127.0.0.1",
        payload={"mode": "local", "model": "qwen2.5:3b", "task": "run a local smoke check"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "preview_only"
    assert response.json()["provider_or_local_execution_authorized"] is False
    assert response.json()["tool_execution_authorized"] is False


def test_manual_model_override_still_flows_to_bounded_smoke(monkeypatch):
    seen = {}

    def fake_run_local(prompt, env=None):
        seen["model"] = env["ALPHA_LOCAL_LLM_MODEL"]
        return {"mode": "local", "provider": "ollama", "model": seen["model"], "status": "passed"}

    monkeypatch.setattr(console.smoke_runner, "run_local", fake_run_local)
    result = console.run_console_smoke("local", "custom-local-model", PROMPT, env={})

    assert seen["model"] == "custom-local-model"
    assert result["model"] == "custom-local-model"
    assert result["smoke_evidence_only"] is True


def test_route_preview_escapes_untrusted_task_output():
    task = '<script>alert("x")</script> browse'
    preview = console.build_route_preview(task, "local", "qwen2.5:3b")
    html = console.render_result_html(route_preview=preview)

    assert task not in html
    assert html_lib.escape(task) in html
    assert "<script>alert" not in html


def test_target_parity_five_step_route_flow_and_cards_render():
    preview = console.build_route_preview("summarize repo markdown and compute average", "local", "qwen2.5:3b")
    html = console.render_result_html(route_preview=preview)

    for text in ("Read task", "Pick route", "Explain route", "Run or recommend safe path", "Capture evidence"):
        assert text in html
    for card_id in (
        "task-interpretation-card",
        "model-route-card",
        "tool-route-card",
        "manual-override-card",
        "route-evidence-card",
    ):
        assert card_id in html
    assert "Document indicator" in html
    assert "Computation indicator" in html


def test_evidence_card_has_required_boundary_and_copyable_route_json():
    preview = console.build_route_preview("browse current repo files", "local", "qwen2.5:3b")
    html = console.render_result_html(route_preview=preview)

    assert "No-call evidence flag" in html
    assert "Preview-vs-execution boundary" in html
    assert "Catalog-not-quality evidence caveat" in html
    assert "Copyable route evidence JSON" in html
    assert 'id="route-evidence-json"' in html
    assert "Provider or local model execution is not authorized by preview" in html


def test_manual_override_copy_or_controls_are_visible():
    html = console.render_result_html()

    assert "Manual override controls" in html
    assert "Mode dropdown" in html
    assert "custom model input" in html
    assert "Tool override" in html


def test_preview_rendering_does_not_call_smoke_or_tools(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("execution path must not run during preview rendering")

    monkeypatch.setattr(console.smoke_runner, "run_local", fail_if_called)
    monkeypatch.setattr(console.smoke_runner, "run_openai", fail_if_called)
    preview = console.build_route_preview("call github and browse", "local", "qwen2.5:3b")
    html = console.render_result_html(route_preview=preview)

    assert "possible_prompt_injection_or_authority_escalation_text" in html
    assert "Tool execution authorized" in html
    assert ">false<" in html


def test_best_path_summary_card_renders_before_detailed_route_cards():
    preview = console.build_route_preview("summarize repo markdown", "local", "qwen2.5:3b")
    html = console.render_result_html(route_preview=preview)

    assert 'id="best-path-summary-card"' in html
    assert html.index('id="best-path-summary-card"') < html.index('id="model-route-card"')
    assert html.index('id="best-path-summary-card"') < html.index('id="tool-route-card"')


def test_best_path_summary_shows_required_fields_and_boundary():
    preview = console.build_route_preview("summarize repo markdown", "local", "qwen2.5:3b")
    html = console.render_result_html(route_preview=preview)

    for text in (
        "Recommended route type",
        "Primary option",
        "Safe next action",
        "Risk flags",
        "Catalog inclusion is not quality evidence; recommendation is not execution authorization.",
        "Copyable best-path JSON",
    ):
        assert text in html
    assert 'id="best-path-json"' in html
    assert preview["best_path_summary"]["metadata_only"] is True
    assert preview["best_path_summary"]["provider_or_local_execution_authorized"] is False
    assert preview["best_path_summary"]["tool_execution_authorized"] is False


def test_tool_looking_prompt_produces_tool_oriented_summary_without_execution(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("preview must not execute tools or smoke runners")

    monkeypatch.setattr(console.smoke_runner, "run_local", fail_if_called)
    monkeypatch.setattr(console.smoke_runner, "run_openai", fail_if_called)
    preview = console.build_route_preview("call github tool for repo issue metadata", "local", "qwen2.5:3b")

    assert preview["best_path_summary"]["recommended_route_type"] in {"tool route", "hybrid route"}
    assert preview["best_path_summary"]["safe_next_action"] == "preview_only"
    assert preview["tool_execution_authorized"] is False


def test_computation_prompt_produces_task_signal_summary_without_quality_claim():
    preview = console.build_route_preview("compute the average of 2 4 and 6", "local", "qwen2.5:3b")
    html = console.render_result_html(route_preview=preview)

    assert preview["task_interpretation"]["computation_indicator"] is True
    assert preview["best_path_summary"]["recommended_route_type"] == "model route"
    assert "Computation indicator" in html
    assert "Catalog inclusion is not quality evidence" in html


def test_privacy_sensitive_prompt_shows_privacy_risk_and_caveat():
    preview = console.build_route_preview("summarize this private confidential note", "local", "qwen2.5:3b")
    html = console.render_result_html(route_preview=preview)

    assert "privacy-sensitive" in preview["best_path_summary"]["risk_flags"]
    assert "local/privacy caveat" in " ".join(preview["best_path_summary"]["why_this_route"])
    assert "privacy-sensitive" in html
    assert "local/privacy caveat" in html


def test_no_eligible_route_best_path_fails_closed_with_no_execution_copy():
    preview = console.build_route_preview("x" * 501, "local", "qwen2.5:3b")
    html = console.render_result_html(route_preview=preview)

    assert preview["best_path_summary"]["status"] == "failed_closed"
    assert preview["best_path_summary"]["recommended_route_type"] == "no eligible route"
    assert preview["best_path_summary"]["safe_next_action"] == "do_not_execute"
    assert "No eligible route" in html or "no eligible route" in html
    assert "do_not_execute" in html


def test_optional_tool_no_match_does_not_fail_best_path_when_model_route_is_valid():
    preview = console.build_route_preview("hello world", "local", "qwen2.5:3b")
    summary = preview["best_path_summary"]

    assert preview["tool_route"]["status"] == "failed_closed"
    assert "no_matching_tool_family" in preview["tool_route"]["reasons"]
    assert preview["model_route"]["status"] == "preview_only"
    assert summary["status"] == "recommend_only"
    assert summary["recommended_route_type"] == "model route"
    assert summary["primary_option"] == preview["model_route"]["recommended_model"]
    assert summary["safe_next_action"] == "smoke_run_allowed_through_existing_smoke_path"
    assert "unsupported/no eligible route" not in summary["risk_flags"]
    assert summary["provider_or_local_execution_authorized"] is False
    assert summary["tool_execution_authorized"] is False


def test_current_facts_prompt_uses_tool_preview_and_keeps_execution_unauthorized():
    preview = console.build_route_preview("latest news today", "local", "qwen2.5:3b")
    summary = preview["best_path_summary"]

    assert preview["task_interpretation"]["current_facts_indicator"] is True
    assert preview["tool_route"]["recommended_tool_id"] == "web_current_research"
    assert summary["recommended_route_type"] in {"tool route", "hybrid route"}
    assert summary["primary_option"] == "web_current_research"
    assert summary["safe_next_action"] == "preview_only"
    assert "current facts" in summary["risk_flags"]
    assert summary["provider_or_local_execution_authorized"] is False
    assert summary["tool_execution_authorized"] is False


def test_copyable_best_path_json_contains_only_metadata_fields():
    preview = console.build_route_preview("browse repo docs", "local", "qwen2.5:3b")
    summary = preview["best_path_summary"]

    allowed = {
        "status",
        "recommended_route_type",
        "primary_option",
        "why_this_route",
        "safe_next_action",
        "fallback_summary",
        "risk_flags",
        "evidence_boundary",
        "manual_override_summary",
        "metadata_only",
        "provider_or_local_execution_authorized",
        "tool_execution_authorized",
    }
    assert set(summary) == allowed
    assert "task" not in summary
    assert "output_preview" not in summary
    assert "usage" not in summary


def test_preview_rendering_does_not_call_external_execution_paths(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("external execution path must not run during preview")

    monkeypatch.setattr(console.smoke_runner, "run_local", fail_if_called)
    monkeypatch.setattr(console.smoke_runner, "run_openai", fail_if_called)
    html = console.render_result_html(route_preview=console.build_route_preview("run a tool-looking task", "local", "qwen2.5:3b"))

    assert "Best Path Summary" in html
    assert "Tool execution authorized" in html
    assert ">false<" in html


def test_target_parity_gap_closure_cards_render_without_broad_claims():
    preview = console.build_route_preview("latest private repo spreadsheet summary", "local", "qwen2.5:3b")
    html = console.render_result_html(route_preview=preview)

    for card_id in (
        "catalog-snapshot-card",
        "target-status-card",
        "target-difference-card",
        "improvement-loop-card",
    ):
        assert card_id in html
    for text in (
        "Built now / next / future",
        "Target parity difference panel",
        "Improvement loop (review-only)",
        "Model and tool catalog snapshot",
        "review-only loop step",
        "no scoring or benchmark claim",
    ):
        assert text in html
    assert "benchmark-backed routing" in html
    assert "Future" in html
    assert "Tool recommendation is metadata-only and not tool execution" in html
    assert "no provider/local model execution from preview" in html


def test_default_route_preview_shows_target_context_before_execution():
    html = console.render_result_html()

    assert "Built now / next / future" in html
    assert 'id="catalog-snapshot-card"' in html
    assert "Model and tool catalog snapshot" in html
    assert "Target parity difference panel" in html
    assert "Improvement loop (review-only)" in html
    assert "No route preview yet" in html
    assert "Preview route only" in html
    assert html.index("Preview route only") < html.index("Run bounded smoke check")
