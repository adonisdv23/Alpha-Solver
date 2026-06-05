from __future__ import annotations

import pytest

from alpha.local_llm.provider_adapter import (
    LocalLLMProviderAdapterError,
    LocalLLMRuntimeConfig,
    OllamaLocalHTTPBackend,
    run_configured_local_llm_runtime,
    run_local_llm_provider_adapter,
)


def _valid_env(**overrides: str) -> dict[str, str]:
    env = {
        "ALPHA_LOCAL_LLM_ENABLED": "true",
        "ALPHA_LOCAL_LLM_ENDPOINT": "http://127.0.0.1:11434/api/chat",
        "ALPHA_LOCAL_LLM_MODEL": "llama3.2:1b-local-fixture",
        "ALPHA_LOCAL_LLM_TIMEOUT_SECONDS": "2.5",
    }
    env.update(overrides)
    return env


def test_runtime_config_is_default_off_and_does_not_invoke_transport():
    observed = {"called": False}

    def fake_transport(*, endpoint_url, payload, timeout_seconds):
        observed["called"] = True
        return {"message": {"role": "assistant", "content": "must not run"}}

    with pytest.raises(LocalLLMProviderAdapterError) as exc:
        run_configured_local_llm_runtime(
            "Default-off runtime must fail before transport.",
            env={},
            transport=fake_transport,
        )

    assert exc.value.reason_code == "local_llm_disabled_non_evidence"
    assert observed["called"] is False


def test_runtime_config_requires_exact_model_name():
    with pytest.raises(LocalLLMProviderAdapterError) as exc:
        LocalLLMRuntimeConfig.from_env(_valid_env(ALPHA_LOCAL_LLM_MODEL=""))
    assert exc.value.reason_code == "missing_model_non_evidence"

    with pytest.raises(LocalLLMProviderAdapterError) as exc:
        LocalLLMRuntimeConfig.from_env(
            _valid_env(ALPHA_LOCAL_LLM_MODEL=" llama3.2:1b-local-fixture ")
        )
    assert exc.value.reason_code == "invalid_model_non_evidence"


def test_runtime_config_requires_finite_positive_timeout():
    for timeout in ("", "0", "-1", "nan", "inf", "not-a-number"):
        with pytest.raises(LocalLLMProviderAdapterError) as exc:
            LocalLLMRuntimeConfig.from_env(
                _valid_env(ALPHA_LOCAL_LLM_TIMEOUT_SECONDS=timeout)
            )
        assert exc.value.reason_code == "invalid_timeout_non_evidence"


def test_runtime_config_requires_no_provider_keys():
    with pytest.raises(LocalLLMProviderAdapterError) as exc:
        LocalLLMRuntimeConfig.from_env(_valid_env(OPENAI_API_KEY="sk-not-used"))

    assert exc.value.reason_code == "provider_keys_forbidden_non_evidence"


@pytest.mark.parametrize(
    "endpoint",
    [
        "http://127.0.0.1:11434/api/chat",
        "http://localhost:11434/api/chat",
        "http://[::1]:11434/api/chat",
    ],
)
def test_runtime_config_accepts_loopback_endpoint_and_records_provenance(endpoint):
    observed = {}

    def fake_transport(*, endpoint_url, payload, timeout_seconds):
        observed["endpoint_url"] = endpoint_url
        observed["payload"] = payload
        observed["timeout_seconds"] = timeout_seconds
        return {"message": {"role": "assistant", "content": "local runtime fixture"}}

    result = run_configured_local_llm_runtime(
        "Run through fake local runtime transport.",
        env=_valid_env(ALPHA_LOCAL_LLM_ENDPOINT=endpoint),
        transport=fake_transport,
    )

    assert result.status == "non_evidence"
    assert result.output_text == "local runtime fixture"
    assert result.behavior_evidence is False
    assert result.metadata["provider_mode"] == "local_llm"
    assert result.metadata["backend_class"] == "ollama-local-http-runtime"
    assert result.metadata["local_backend"] == "ollama_chat"
    assert result.metadata["local_model"] == "llama3.2:1b-local-fixture"
    assert result.metadata["endpoint_is_loopback"] is True
    assert result.metadata["timeout_seconds"] == 2.5
    assert result.metadata["no_provider_keys_required"] is True
    assert result.metadata["no_hosted_fallback"] is True
    assert observed["endpoint_url"] == endpoint
    assert observed["payload"]["model"] == "llama3.2:1b-local-fixture"
    assert observed["timeout_seconds"] == 2.5


@pytest.mark.parametrize(
    "endpoint",
    [
        "https://127.0.0.1:11434/api/chat",
        "http://user:pass@127.0.0.1:11434/api/chat",
        "http://example.com/api/chat",
        "http://192.168.1.25:11434/api/chat",
        "http:///api/chat",
    ],
)
def test_runtime_config_rejects_non_local_or_ambiguous_endpoints(endpoint):
    with pytest.raises(LocalLLMProviderAdapterError) as exc:
        LocalLLMRuntimeConfig.from_env(_valid_env(ALPHA_LOCAL_LLM_ENDPOINT=endpoint))

    assert exc.value.reason_code == "endpoint_not_local_non_evidence"


def test_runtime_path_does_not_silently_fall_back_to_hosted_provider_on_failure():
    observed = {"calls": 0}

    def connection_failure(*, endpoint_url, payload, timeout_seconds):
        observed["calls"] += 1
        raise ConnectionError("offline local connection fixture")

    result = run_configured_local_llm_runtime(
        "Connection failure must remain a local failure.",
        env=_valid_env(),
        transport=connection_failure,
    )

    assert observed["calls"] == 1
    assert result.status == "failed_closed"
    assert result.reason == "connection_failure_non_evidence"
    assert result.output_text == ""
    assert result.metadata["no_hosted_fallback"] is True
    assert result.metadata["behavior_evidence"] is False


def test_runtime_backend_fails_closed_on_system_echo_with_specific_reason():
    def echo_system_transport(*, endpoint_url, payload, timeout_seconds):
        return {"message": {"role": "assistant", "content": payload["messages"][0]["content"]}}

    result = run_configured_local_llm_runtime(
        "System echo must not be successful behavior.",
        env=_valid_env(),
        transport=echo_system_transport,
    )

    assert result.status == "failed_closed"
    assert result.reason == "system_echo_non_evidence"
    assert result.metadata["behavior_evidence"] is False


def test_backend_invalid_timeout_fails_closed_before_transport_invocation():
    observed = {"called": False}

    def fake_transport(*, endpoint_url, payload, timeout_seconds):
        observed["called"] = True
        return {"message": {"role": "assistant", "content": "must not run"}}

    backend = OllamaLocalHTTPBackend(
        model="llama3.2:1b-local-fixture",
        timeout_seconds=float("inf"),
        transport=fake_transport,
    )

    result = run_local_llm_provider_adapter(
        "Invalid runtime timeout fails closed.",
        backend=backend,
        model="llama3.2:1b-local-fixture",
    )

    assert result.status == "failed_closed"
    assert result.reason == "invalid_timeout_non_evidence"
    assert observed["called"] is False


def test_backend_missing_model_fails_closed_before_transport_invocation():
    observed = {"called": False}

    def fake_transport(*, endpoint_url, payload, timeout_seconds):
        observed["called"] = True
        return {"message": {"role": "assistant", "content": "must not run"}}

    backend = OllamaLocalHTTPBackend(model="", transport=fake_transport)

    result = run_local_llm_provider_adapter(
        "Missing model fails closed.",
        backend=backend,
        model="llama3.2:1b-local-fixture",
    )

    assert result.status == "failed_closed"
    assert result.reason == "missing_model_non_evidence"
    assert observed["called"] is False
