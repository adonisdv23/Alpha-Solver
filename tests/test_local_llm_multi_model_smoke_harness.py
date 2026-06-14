from __future__ import annotations

from types import SimpleNamespace
from urllib.error import URLError

from alpha.local_llm.multi_model_smoke_harness import (
    run_multi_model_smoke_harness,
)


def _content_transport(content: str):
    def transport(*, endpoint_url, payload, timeout_seconds):
        return {"message": {"role": "assistant", "content": content}}

    return transport


def test_multiple_model_names_are_iterated_safely_with_fake_transport():
    seen_models = []

    def fake_transport(*, endpoint_url, payload, timeout_seconds):
        seen_models.append(payload["model"])
        return {"message": {"role": "assistant", "content": f"fixture for {payload['model']}"}}

    results = run_multi_model_smoke_harness(
        models="llama3.2:1b, qwen2.5:0.5b",
        endpoint_url="http://127.0.0.1:11434/api/chat",
        env={},
        transport=fake_transport,
    )

    assert seen_models == ["llama3.2:1b", "qwen2.5:0.5b"]
    assert [record.model for record in results] == ["llama3.2:1b", "qwen2.5:0.5b"]
    assert all(record.status == "substantive_looking_output" for record in results)
    assert all(record.behavior_evidence is False for record in results)


def test_hosted_provider_keys_in_env_fail_closed_before_transport():
    observed = {"called": False}

    def fake_transport(*, endpoint_url, payload, timeout_seconds):
        observed["called"] = True
        return {"message": {"role": "assistant", "content": "must not run"}}

    results = run_multi_model_smoke_harness(
        models=["local-a", "local-b"],
        endpoint_url="http://127.0.0.1:11434/api/chat",
        env={"OPENAI_API_KEY": "sk-test"},
        transport=fake_transport,
    )

    assert observed["called"] is False
    assert [record.status for record in results] == ["blocked", "blocked"]
    assert all(record.reason == "provider_keys_forbidden_non_evidence" for record in results)


def test_non_loopback_endpoint_fails_closed_before_transport():
    observed = {"called": False}

    def fake_transport(*, endpoint_url, payload, timeout_seconds):
        observed["called"] = True
        return {"message": {"role": "assistant", "content": "must not run"}}

    results = run_multi_model_smoke_harness(
        models="local-a,local-b",
        endpoint_url="https://api.openai.com/v1/chat/completions",
        env={},
        transport=fake_transport,
    )

    assert observed["called"] is False
    assert all(record.status == "blocked" for record in results)
    assert all(record.reason == "endpoint_not_local_non_evidence" for record in results)


def test_empty_output_fails_closed():
    results = run_multi_model_smoke_harness(
        models="local-empty",
        endpoint_url="http://localhost:11434/api/chat",
        env={},
        transport=_content_transport("   "),
    )

    assert results[0].status == "empty_output"
    assert results[0].reason == "empty_model_output_non_evidence"
    assert results[0].behavior_evidence is False


def test_prompt_echo_is_detected():
    prompt = "Do not echo this local smoke prompt."

    results = run_multi_model_smoke_harness(
        models="local-echo",
        endpoint_url="http://localhost:11434/api/chat",
        prompt=prompt,
        env={},
        transport=_content_transport(prompt),
    )

    assert results[0].status == "prompt_echo"
    assert results[0].reason == "prompt_echo_non_evidence"
    assert results[0].behavior_evidence is False


def test_per_model_records_do_not_claim_behavior_evidence():
    results = run_multi_model_smoke_harness(
        models=["local-a"],
        endpoint_url="http://[::1]:11434/api/chat",
        env={},
        transport=_content_transport("A small safe fixture response."),
    )

    record = results[0]
    assert record.status == "substantive_looking_output"
    assert record.behavior_evidence is False
    assert record.evidence_label == "local_multi_model_smoke_only_no_behavior_evidence"
    assert record.metadata["strict_no_behavior_evidence_labeling"] is True


def test_no_hosted_fallback_exists_on_connection_failure():
    def connection_transport(*, endpoint_url, payload, timeout_seconds):
        raise ConnectionError("local ollama unavailable")

    results = run_multi_model_smoke_harness(
        models="missing-local-model",
        endpoint_url="http://127.0.0.1:11434/api/chat",
        env={},
        transport=connection_transport,
    )

    assert results[0].status == "connection_failed"
    assert results[0].reason == "connection_failure_non_evidence"
    assert results[0].metadata["no_hosted_fallback"] is True
    assert results[0].metadata["no_provider_keys_accepted"] is True


def test_default_operator_path_urllib_unavailable_maps_to_connection_failed(monkeypatch):
    observed = {"called": False}

    def unavailable_default_transport(*, endpoint_url, payload, timeout_seconds):
        observed["called"] = True
        raise URLError("connection refused by local loopback ollama fixture")

    monkeypatch.setattr(
        "alpha.local_llm.provider_adapter.urllib_ollama_json_transport",
        unavailable_default_transport,
    )

    results = run_multi_model_smoke_harness(
        models="operator-local-model",
        endpoint_url="http://127.0.0.1:11434/api/chat",
        env={},
    )

    assert observed["called"] is True
    assert results[0].status == "connection_failed"
    assert results[0].reason == "connection_failure_non_evidence"
    assert results[0].behavior_evidence is False
    assert results[0].metadata["no_hosted_fallback"] is True
    assert results[0].metadata["no_provider_keys_accepted"] is True


def test_adapter_normalized_urllib_backend_error_with_local_context_maps_to_connection_failed(
    monkeypatch,
):
    def adapter_normalized_backend_error(prompt, *, config, transport, env):
        assert transport is None
        return SimpleNamespace(
            status="failed_closed",
            reason="backend_error_non_evidence",
            output_text="",
            metadata={
                "endpoint_is_loopback": True,
                "local_backend": "ollama_chat",
                "adapter_exception_cause_class": "URLError",
                "behavior_evidence": False,
            },
        )

    monkeypatch.setattr(
        "alpha.local_llm.multi_model_smoke_harness.run_configured_local_llm_runtime",
        adapter_normalized_backend_error,
    )

    results = run_multi_model_smoke_harness(
        models="operator-local-model",
        endpoint_url="http://127.0.0.1:11434/api/chat",
        env={},
    )

    assert results[0].status == "connection_failed"
    assert results[0].reason == "backend_error_non_evidence"
    assert results[0].behavior_evidence is False
    assert results[0].metadata["default_transport_used"] is True
    assert results[0].metadata["no_hosted_fallback"] is True


def test_default_operator_path_keeps_generic_backend_errors_blocked(monkeypatch):
    def malformed_default_transport(*, endpoint_url, payload, timeout_seconds):
        raise RuntimeError("generic local backend fixture")

    monkeypatch.setattr(
        "alpha.local_llm.provider_adapter.urllib_ollama_json_transport",
        malformed_default_transport,
    )

    results = run_multi_model_smoke_harness(
        models="operator-local-model",
        endpoint_url="http://127.0.0.1:11434/api/chat",
        env={},
    )

    assert results[0].status == "blocked"
    assert results[0].reason == "backend_error_non_evidence"
    assert results[0].behavior_evidence is False
    assert results[0].metadata["no_hosted_fallback"] is True
