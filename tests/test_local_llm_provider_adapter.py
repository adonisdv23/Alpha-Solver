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
