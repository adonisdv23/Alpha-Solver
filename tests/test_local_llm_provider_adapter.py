from __future__ import annotations

import sys
from hashlib import sha256
from pathlib import Path

import pytest

from alpha.local_llm.portable_contract import PortableContractError, load_portable_contract
from alpha.local_llm.provider_adapter import (
    StubLocalLLMProviderBackend,
    build_local_llm_adapter_request,
    run_local_llm_provider_adapter,
)


def test_adapter_builds_local_llm_shaped_request_from_portable_contract():
    user_prompt = "Summarize the adapter wiring boundary."

    request = build_local_llm_adapter_request(user_prompt)

    assert request.provider_mode == "local_llm"
    assert request.backend_class == "stub-local-llm-provider-adapter"
    assert request.model == "local-llm-disabled-unconfigured"
    assert request.messages[0].role == "system"
    assert request.messages[0].content == request.system
    assert request.messages[1].role == "user"
    assert request.messages[1].content == user_prompt
    assert "LLM_PERSONA_PROTOCOL" in request.system
    assert request.user_prompt == user_prompt
    assert user_prompt not in request.system
    assert request.metadata["provider_mode"] == "local_llm"
    assert request.metadata["no_real_provider_call"] is True
    assert request.metadata["real_provider_call_enabled"] is False
    assert request.metadata["behavior_evidence"] is False
    assert (
        request.metadata["evidence_label"]
        == "non_evidence_local_llm_provider_adapter_wiring"
    )


def test_adapter_preserves_portable_contract_path_and_fingerprint():
    contract = load_portable_contract()
    expected_text = Path("alpha_solver_portable.py").read_text(encoding="utf-8")

    request = build_local_llm_adapter_request("Keep the prompt sources separate.")

    assert contract.source_path == "alpha_solver_portable.py"
    assert request.metadata["prompt_source_path"] == "alpha_solver_portable.py"
    assert request.metadata["prompt_source_fingerprint"] == sha256(
        expected_text.encode("utf-8")
    ).hexdigest()
    assert (
        request.metadata["prompt_source_sha256"]
        == request.metadata["prompt_source_fingerprint"]
    )
    assert request.metadata["prompt_source_fingerprint_algorithm"] == "sha256"


def test_adapter_keeps_user_prompt_separate_from_system_contract_text():
    user_prompt = "User-only adapter prompt marker 20260604."

    request = build_local_llm_adapter_request(user_prompt)

    assert request.system == request.messages[0].content
    assert request.user_prompt == request.messages[1].content
    assert request.messages[0].role == "system"
    assert request.messages[1].role == "user"
    assert user_prompt not in request.system


def test_adapter_does_not_import_or_call_v91_tree_of_thought(monkeypatch):
    imported_names: list[str] = []
    real_import = __import__

    def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
        imported_names.append(name)
        if name in {"alpha_solver_entry", "alpha-solver-v91-python"}:
            raise AssertionError(f"forbidden import: {name}")
        return real_import(name, globals, locals, fromlist, level)

    for module_name in ["alpha_solver_entry", "alpha-solver-v91-python"]:
        monkeypatch.delitem(sys.modules, module_name, raising=False)
    monkeypatch.setattr("builtins.__import__", guarded_import)

    backend = StubLocalLLMProviderBackend(output_text="adapter wiring only")
    result = run_local_llm_provider_adapter("Explain the seam.", backend=backend)

    assert result.status == "non_evidence"
    assert len(backend.calls) == 1
    assert "alpha_solver_entry" not in imported_names
    assert "alpha-solver-v91-python" not in imported_names


def test_model_provider_local_remains_smoke_only_for_adapter():
    with pytest.raises(PortableContractError, match="MODEL_PROVIDER=local remains smoke-only"):
        build_local_llm_adapter_request(
            "This must not use smoke local mode.", provider_mode="local"
        )


def test_adapter_fails_closed_on_empty_output():
    backend = StubLocalLLMProviderBackend(output_text="   ")

    result = run_local_llm_provider_adapter("Produce adapter output.", backend=backend)

    assert result.status == "failed_closed"
    assert result.reason == "empty_model_output_non_evidence"
    assert result.behavior_evidence is False
    assert result.metadata["behavior_evidence"] is False


def test_adapter_fails_closed_on_prompt_echo():
    user_prompt = "Do not echo this prompt."
    backend = StubLocalLLMProviderBackend(output_text=user_prompt)

    result = run_local_llm_provider_adapter(user_prompt, backend=backend)

    assert result.status == "failed_closed"
    assert result.reason == "prompt_echo_non_evidence"
    assert result.behavior_evidence is False


def test_adapter_fails_closed_on_backend_error():
    backend = StubLocalLLMProviderBackend(fail=True)

    result = run_local_llm_provider_adapter("Exercise adapter error.", backend=backend)

    assert result.status == "failed_closed"
    assert result.reason == "adapter_error:PortableContractError"
    assert result.output_text == ""
    assert result.metadata["no_real_provider_call"] is True


def test_adapter_fails_closed_on_missing_contract(tmp_path):
    missing_contract = tmp_path / "missing-alpha-solver-portable.py"

    with pytest.raises(PortableContractError, match="portable contract not found"):
        build_local_llm_adapter_request(
            "Missing contract should fail closed.", contract_path=missing_contract
        )


def test_adapter_fails_closed_on_empty_contract(tmp_path):
    empty_contract = tmp_path / "alpha_solver_portable.py"
    empty_contract.write_text("   ", encoding="utf-8")

    with pytest.raises(PortableContractError, match="portable contract is empty"):
        build_local_llm_adapter_request(
            "Empty contract should fail closed.", contract_path=empty_contract
        )


def test_adapter_fails_closed_on_fingerprint_mismatch(tmp_path):
    contract = tmp_path / "alpha_solver_portable.py"
    contract.write_text("LLM_PERSONA_PROTOCOL = 'test contract'\n", encoding="utf-8")

    with pytest.raises(PortableContractError, match="sha256 mismatch"):
        build_local_llm_adapter_request(
            "Fingerprint mismatch should fail closed.",
            contract_path=contract,
            expected_sha256="0" * 64,
        )


def test_ollama_payload_mapping_preserves_contract_and_user_messages():
    from alpha.local_llm.provider_adapter import build_ollama_chat_payload

    user_prompt = "Map this request without contacting a provider."
    request = build_local_llm_adapter_request(user_prompt)

    payload = build_ollama_chat_payload(request, model="offline-fixture-model")

    assert payload == {
        "model": "offline-fixture-model",
        "messages": [
            {"role": "system", "content": request.system},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
    }
    assert request.metadata["provider_mode"] == "local_llm"
    assert request.metadata["behavior_evidence"] is False
    assert request.metadata["real_provider_call_enabled"] is False


def test_ollama_parser_extracts_assistant_text_from_static_fixture():
    from alpha.local_llm.provider_adapter import parse_ollama_chat_response

    fixture = {
        "model": "offline-fixture-model",
        "created_at": "2026-06-05T00:00:00Z",
        "message": {
            "role": "assistant",
            "content": "Offline fixture response from parser only.",
        },
        "done": True,
    }

    assert parse_ollama_chat_response(fixture) == "Offline fixture response from parser only."


def test_ollama_backend_default_off_without_injected_transport():
    from alpha.local_llm.provider_adapter import OllamaLocalHTTPBackend

    backend = OllamaLocalHTTPBackend(model="offline-fixture-model")

    result = run_local_llm_provider_adapter(
        "Default construction must remain inert.", backend=backend
    )

    assert result.status == "failed_closed"
    assert result.reason == "provider_backend_disabled_non_evidence"
    assert result.behavior_evidence is False
    assert len(backend.calls) == 1
    assert len(backend.payloads) == 1


def test_ollama_backend_uses_injected_transport_only_and_records_payload():
    from alpha.local_llm.provider_adapter import OllamaLocalHTTPBackend

    observed = {}

    def fake_transport(*, endpoint_url, payload, timeout_seconds):
        observed["endpoint_url"] = endpoint_url
        observed["payload"] = payload
        observed["timeout_seconds"] = timeout_seconds
        return {"message": {"role": "assistant", "content": "offline transport fixture"}}

    backend = OllamaLocalHTTPBackend(
        model="offline-fixture-model",
        endpoint_url="http://127.0.0.1:11434/api/chat",
        timeout_seconds=2.5,
        transport=fake_transport,
    )

    result = run_local_llm_provider_adapter(
        "Use the fake transport only.", backend=backend
    )

    assert result.status == "non_evidence"
    assert result.reason == "local_llm_provider_adapter_wiring_only"
    assert result.output_text == "offline transport fixture"
    assert observed["endpoint_url"] == "http://127.0.0.1:11434/api/chat"
    assert observed["timeout_seconds"] == 2.5
    assert observed["payload"]["model"] == "offline-fixture-model"
    assert observed["payload"]["messages"][0]["role"] == "system"
    assert observed["payload"]["messages"][1] == {
        "role": "user",
        "content": "Use the fake transport only.",
    }
    assert observed["payload"]["stream"] is False
    assert result.behavior_evidence is False


@pytest.mark.parametrize(
    ("fixture", "reason"),
    [
        ({}, "malformed_response_non_evidence"),
        ({"message": "not a mapping"}, "malformed_response_non_evidence"),
        ({"message": {"role": "tool", "content": "text"}}, "malformed_response_non_evidence"),
        ({"message": {"role": "assistant"}}, "malformed_response_non_evidence"),
        ({"message": {"role": "assistant", "content": ["text"]}}, "malformed_response_non_evidence"),
        ({"message": {"role": "assistant", "content": "   "}}, "empty_model_output_non_evidence"),
    ],
)
def test_ollama_parser_fails_closed_on_malformed_or_empty_static_fixtures(
    fixture, reason
):
    from alpha.local_llm.provider_adapter import (
        LocalLLMProviderAdapterError,
        parse_ollama_chat_response,
    )

    with pytest.raises(LocalLLMProviderAdapterError) as exc_info:
        parse_ollama_chat_response(fixture)

    assert exc_info.value.reason_code == reason


def test_ollama_backend_fails_closed_on_timeout_from_injected_transport():
    from alpha.local_llm.provider_adapter import OllamaLocalHTTPBackend

    def timeout_transport(*, endpoint_url, payload, timeout_seconds):
        raise TimeoutError("offline timeout fixture")

    backend = OllamaLocalHTTPBackend(
        model="offline-fixture-model", transport=timeout_transport
    )

    result = run_local_llm_provider_adapter("Timeout should fail closed.", backend=backend)

    assert result.status == "failed_closed"
    assert result.reason == "timeout_non_evidence"
    assert result.metadata["failure_label"] == "failed_closed_result"
    assert result.behavior_evidence is False


def test_ollama_backend_fails_closed_on_connection_failure_from_injected_transport():
    from alpha.local_llm.provider_adapter import OllamaLocalHTTPBackend

    def connection_transport(*, endpoint_url, payload, timeout_seconds):
        raise ConnectionError("offline connection fixture")

    backend = OllamaLocalHTTPBackend(
        model="offline-fixture-model", transport=connection_transport
    )

    result = run_local_llm_provider_adapter(
        "Connection failure should fail closed.", backend=backend
    )

    assert result.status == "failed_closed"
    assert result.reason == "connection_failure_non_evidence"
    assert result.metadata["failure_label"] == "failed_closed_result"
    assert result.behavior_evidence is False


def test_ollama_backend_fails_closed_on_generic_backend_error():
    from alpha.local_llm.provider_adapter import OllamaLocalHTTPBackend

    def error_transport(*, endpoint_url, payload, timeout_seconds):
        raise RuntimeError("offline backend fixture")

    backend = OllamaLocalHTTPBackend(model="offline-fixture-model", transport=error_transport)

    result = run_local_llm_provider_adapter(
        "Backend errors should fail closed.", backend=backend
    )

    assert result.status == "failed_closed"
    assert result.reason == "backend_error_non_evidence"
    assert result.metadata["failure_label"] == "failed_closed_result"
    assert result.behavior_evidence is False


def test_ollama_backend_fails_closed_on_prompt_echo_from_static_fixture():
    from alpha.local_llm.provider_adapter import OllamaLocalHTTPBackend

    user_prompt = "Echo detection fixture."

    def echo_transport(*, endpoint_url, payload, timeout_seconds):
        return {"message": {"role": "assistant", "content": user_prompt}}

    backend = OllamaLocalHTTPBackend(model="offline-fixture-model", transport=echo_transport)

    result = run_local_llm_provider_adapter(user_prompt, backend=backend)

    assert result.status == "failed_closed"
    assert result.reason == "prompt_echo_non_evidence"
    assert result.metadata["failure_label"] == "failed_closed_result"
    assert result.behavior_evidence is False


def test_ollama_backend_fails_closed_on_system_contract_echo_from_static_fixture():
    from alpha.local_llm.provider_adapter import OllamaLocalHTTPBackend

    def echo_system_transport(*, endpoint_url, payload, timeout_seconds):
        return {"message": {"role": "assistant", "content": payload["messages"][0]["content"]}}

    backend = OllamaLocalHTTPBackend(
        model="offline-fixture-model", transport=echo_system_transport
    )

    result = run_local_llm_provider_adapter(
        "System echo should fail closed.", backend=backend
    )

    assert result.status == "failed_closed"
    assert result.reason == "prompt_echo_non_evidence"
    assert result.metadata["failure_label"] == "failed_closed_result"
    assert result.behavior_evidence is False
