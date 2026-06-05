from __future__ import annotations

import sys
from hashlib import sha256
from urllib import error as urllib_error
from pathlib import Path

import pytest

from alpha.local_llm.portable_contract import PortableContractError, load_portable_contract
from alpha.local_llm.provider_adapter import (
    LocalLLMProviderAdapterError,
    OllamaLocalHTTPBackend,
    StubLocalLLMProviderBackend,
    build_ollama_chat_payload,
    build_local_llm_adapter_request,
    parse_ollama_assistant_text,
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


def test_ollama_payload_mapping_preserves_system_user_separation():
    user_prompt = "Map this adapter request to an Ollama chat payload."
    request = build_local_llm_adapter_request(user_prompt)

    payload = build_ollama_chat_payload(request, model="offline-fixture-model")

    assert payload["model"] == "offline-fixture-model"
    assert payload["stream"] is False
    assert payload["options"] == {"temperature": 0}
    assert payload["messages"] == [
        {"role": "system", "content": request.system},
        {"role": "user", "content": user_prompt},
    ]
    assert user_prompt not in payload["messages"][0]["content"]


def test_ollama_backend_uses_injected_transport_for_offline_request_mapping():
    captured: dict[str, object] = {}

    def offline_transport(endpoint, payload, timeout_seconds):
        captured["endpoint"] = endpoint
        captured["payload"] = payload
        captured["timeout_seconds"] = timeout_seconds
        return {"message": {"role": "assistant", "content": "offline fixture response"}}

    request = build_local_llm_adapter_request("Use only the injected transport.")
    backend = OllamaLocalHTTPBackend(
        endpoint="http://127.0.0.1:11434/api/chat",
        model="offline-fixture-model",
        timeout_seconds=1.25,
        enabled=True,
        transport=offline_transport,
    )

    output_text = backend.generate(request)

    assert output_text == "offline fixture response"
    assert captured["endpoint"] == "http://127.0.0.1:11434/api/chat"
    assert captured["timeout_seconds"] == 1.25
    assert captured["payload"] == {
        "model": "offline-fixture-model",
        "stream": False,
        "messages": [
            {"role": "system", "content": request.system},
            {"role": "user", "content": request.user_prompt},
        ],
        "options": {"temperature": 0},
    }


def test_ollama_backend_default_off_makes_no_network_call(monkeypatch):
    def forbidden_urlopen(*args, **kwargs):
        raise AssertionError("default-off backend must not open a socket")

    monkeypatch.setattr("alpha.local_llm.provider_adapter.urllib_request.urlopen", forbidden_urlopen)
    backend = OllamaLocalHTTPBackend()

    result = run_local_llm_provider_adapter(
        "Default-off backend should fail closed before transport.", backend=backend
    )

    assert result.status == "failed_closed"
    assert result.reason == "ollama_backend_disabled_non_evidence"
    assert result.metadata["behavior_evidence"] is False


def test_parse_ollama_successful_assistant_text_from_static_fixture():
    fixture = {
        "model": "offline-fixture-model",
        "message": {"role": "assistant", "content": "Assistant text from fixture."},
        "done": True,
    }

    assert parse_ollama_assistant_text(fixture) == "Assistant text from fixture."


@pytest.mark.parametrize(
    ("fixture", "reason_code"),
    [
        ({}, "malformed_ollama_response_non_evidence"),
        ({"message": None}, "malformed_ollama_response_non_evidence"),
        ({"message": {"role": "assistant"}}, "malformed_ollama_response_non_evidence"),
        ({"message": {"role": "assistant", "content": ["not text"]}}, "malformed_ollama_response_non_evidence"),
        ({"message": {"role": "assistant", "content": "   "}}, "empty_ollama_response_non_evidence"),
    ],
)
def test_parse_ollama_fail_closed_for_malformed_or_empty_static_fixtures(fixture, reason_code):
    with pytest.raises(LocalLLMProviderAdapterError) as exc_info:
        parse_ollama_assistant_text(fixture)

    assert exc_info.value.reason_code == reason_code


def test_parse_ollama_fail_closed_for_prompt_echo_with_request_context():
    request = build_local_llm_adapter_request("Do not echo fixture prompt.")

    with pytest.raises(LocalLLMProviderAdapterError) as exc_info:
        parse_ollama_assistant_text(
            {"message": {"role": "assistant", "content": "Do not echo fixture prompt."}},
            request=request,
        )

    assert exc_info.value.reason_code == "prompt_echo_non_evidence"


@pytest.mark.parametrize(
    ("transport_error", "expected_reason"),
    [
        (TimeoutError("offline timeout fixture"), "ollama_timeout_non_evidence"),
        (OSError("offline connection failure fixture"), "ollama_connection_failure_non_evidence"),
        (
            urllib_error.HTTPError(
                "http://127.0.0.1:11434/api/chat", 500, "fixture backend error", {}, None
            ),
            "ollama_backend_error_non_evidence",
        ),
    ],
)
def test_ollama_backend_fail_closed_for_transport_errors(transport_error, expected_reason):
    def offline_transport(endpoint, payload, timeout_seconds):
        raise transport_error

    backend = OllamaLocalHTTPBackend(enabled=True, transport=offline_transport)

    result = run_local_llm_provider_adapter("Exercise fail-closed transport.", backend=backend)

    assert result.status == "failed_closed"
    assert result.reason == expected_reason
    assert result.output_text == ""
    assert result.behavior_evidence is False


def test_ollama_backend_fail_closed_for_malformed_response_from_transport():
    backend = OllamaLocalHTTPBackend(enabled=True, transport=lambda endpoint, payload, timeout: {})

    result = run_local_llm_provider_adapter("Malformed response should fail closed.", backend=backend)

    assert result.status == "failed_closed"
    assert result.reason == "malformed_ollama_response_non_evidence"
    assert result.behavior_evidence is False


def test_ollama_backend_fail_closed_for_empty_response_from_transport():
    backend = OllamaLocalHTTPBackend(
        enabled=True,
        transport=lambda endpoint, payload, timeout: {"message": {"content": "   "}},
    )

    result = run_local_llm_provider_adapter("Empty response should fail closed.", backend=backend)

    assert result.status == "failed_closed"
    assert result.reason == "empty_ollama_response_non_evidence"
    assert result.behavior_evidence is False


def test_ollama_backend_fail_closed_for_backend_prompt_echo():
    user_prompt = "Backend must not echo this prompt."
    backend = OllamaLocalHTTPBackend(
        enabled=True,
        transport=lambda endpoint, payload, timeout: {"message": {"content": user_prompt}},
    )

    result = run_local_llm_provider_adapter(user_prompt, backend=backend)

    assert result.status == "failed_closed"
    assert result.reason == "prompt_echo_non_evidence"
    assert result.behavior_evidence is False


def test_ollama_backend_fail_closed_for_nonlocal_endpoint_before_transport():
    def forbidden_transport(endpoint, payload, timeout_seconds):
        raise AssertionError("non-local endpoint must fail before transport")

    backend = OllamaLocalHTTPBackend(
        endpoint="https://example.invalid/api/chat",
        enabled=True,
        transport=forbidden_transport,
    )

    result = run_local_llm_provider_adapter("Reject non-local endpoint.", backend=backend)

    assert result.status == "failed_closed"
    assert result.reason == "ollama_endpoint_not_local_non_evidence"
    assert result.behavior_evidence is False
