from __future__ import annotations

import importlib
import sys
from hashlib import sha256
from pathlib import Path

import pytest

from alpha.local_llm.portable_contract import (
    FakeLocalLLMProofClient,
    PortableContractError,
    build_local_llm_proof_request,
    load_portable_contract,
    run_fake_local_llm_contract_proof,
)


def test_loads_alpha_solver_portable_as_prompt_source_with_fingerprint():
    contract = load_portable_contract()
    expected_text = Path("alpha_solver_portable.py").read_text(encoding="utf-8")

    assert contract.source_path == "alpha_solver_portable.py"
    assert contract.text == expected_text
    assert "LLM_PERSONA_PROTOCOL" in contract.text
    assert contract.sha256 == sha256(expected_text.encode("utf-8")).hexdigest()
    assert contract.metadata == {
        "prompt_source_path": "alpha_solver_portable.py",
        "prompt_source_fingerprint": contract.sha256,
        "prompt_source_sha256": contract.sha256,
        "prompt_source_fingerprint_algorithm": "sha256",
    }


def test_builds_local_llm_style_request_with_contract_and_separate_user_prompt():
    user_prompt = "Draft a compact Alpha Solver proof summary."

    request = build_local_llm_proof_request(user_prompt)

    assert "LLM_PERSONA_PROTOCOL" in request.system
    assert request.user_prompt == user_prompt
    assert user_prompt not in request.system
    assert request.metadata["prompt_source_path"] == "alpha_solver_portable.py"
    assert request.metadata["prompt_source_fingerprint"]
    assert (
        request.metadata["prompt_source_sha256"]
        == request.metadata["prompt_source_fingerprint"]
    )
    assert request.metadata["backend_class"] == "fake-local-llm-proof"
    assert request.metadata["provider_mode"] == "local_llm"
    assert request.metadata["no_real_provider_call"] is True
    assert request.metadata["behavior_evidence"] is False
    assert (
        request.metadata["evidence_label"]
        == "non_evidence_fake_client_contract_consumption_proof"
    )


def test_fake_client_proof_records_request_without_real_provider_call():
    client = FakeLocalLLMProofClient(output_text="fake structured response")

    result = run_fake_local_llm_contract_proof("Explain this proof.", client=client)

    assert result.status == "non_evidence"
    assert result.behavior_evidence is False
    assert result.metadata["no_real_provider_call"] is True
    assert result.metadata["backend_class"] == "fake-local-llm-proof"
    assert len(client.calls) == 1
    assert client.calls[0] is result.request
    assert "Alpha Solver" in result.request.system
    assert result.request.user_prompt == "Explain this proof."


def test_fake_client_proof_does_not_import_or_call_v91_or_tree_of_thought(monkeypatch):
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

    client = FakeLocalLLMProofClient(output_text="fake structured response")
    result = run_fake_local_llm_contract_proof("Prove no v91 fallback.", client=client)

    assert result.status == "non_evidence"
    assert "alpha_solver_entry" not in imported_names
    assert "alpha-solver-v91-python" not in imported_names
    assert "alpha_solver_entry" not in sys.modules
    assert "alpha-solver-v91-python" not in sys.modules


def test_model_provider_local_label_is_rejected_for_proof_mode():
    with pytest.raises(PortableContractError, match="MODEL_PROVIDER=local remains smoke-only"):
        build_local_llm_proof_request("Do not overload local smoke.", provider_mode="local")


def test_existing_model_provider_local_openai_gate_remains_separate(monkeypatch):
    service_app = importlib.import_module("service.app")

    monkeypatch.setenv("MODEL_PROVIDER", "local")

    assert service_app._is_openai_provider_enabled() is False


def test_missing_contract_fails_closed(tmp_path):
    missing = tmp_path / "alpha_solver_portable.py"

    with pytest.raises(PortableContractError, match="portable contract not found"):
        load_portable_contract(missing)


def test_prompt_source_hash_mismatch_fails_closed(tmp_path):
    contract_path = tmp_path / "alpha_solver_portable.py"
    contract_path.write_text("portable contract text", encoding="utf-8")

    with pytest.raises(PortableContractError, match="sha256 mismatch"):
        load_portable_contract(contract_path, expected_sha256="0" * 64)


def test_empty_output_prompt_echo_and_fake_client_failure_fail_closed():
    empty = run_fake_local_llm_contract_proof(
        "Explain proof.", client=FakeLocalLLMProofClient(output_text="  ")
    )
    echo = run_fake_local_llm_contract_proof(
        "Explain proof.", client=FakeLocalLLMProofClient(output_text="Explain proof.")
    )
    failed = run_fake_local_llm_contract_proof(
        "Explain proof.", client=FakeLocalLLMProofClient(fail=True)
    )

    assert empty.status == "failed_closed"
    assert empty.reason == "empty_output_non_evidence"
    assert empty.behavior_evidence is False
    assert echo.status == "failed_closed"
    assert echo.reason == "prompt_echo_non_evidence"
    assert echo.behavior_evidence is False
    assert failed.status == "failed_closed"
    assert failed.reason.startswith("fake_client_failure:")
    assert failed.behavior_evidence is False
