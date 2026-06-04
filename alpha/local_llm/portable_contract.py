"""Fake-client proof seam for portable-contract local LLM request construction.

The helpers in this module are intentionally inert: they read the portable
contract from disk, build a local-LLM-shaped request, and optionally pass that
request to an injected fake client. They do not call Ollama, OpenAI, Anthropic,
other providers, or the deterministic v91 ``_tree_of_thought`` path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping, Protocol

_REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONTRACT_PATH = _REPO_ROOT / "alpha_solver_portable.py"
_LOCAL_LLM_PROOF_MODE = "local_llm"
_FAKE_BACKEND_CLASS = "fake-local-llm-proof"
_NON_EVIDENCE_LABEL = "non_evidence_fake_client_contract_consumption_proof"


class PortableContractError(RuntimeError):
    """Raised when the portable prompt source cannot be trusted."""


@dataclass(frozen=True)
class PortableContract:
    """Loaded portable contract text and safe source fingerprint metadata."""

    text: str
    source_path: str
    sha256: str
    fingerprint_algorithm: str = "sha256"

    @property
    def fingerprint(self) -> str:
        """Return the stable prompt-source fingerprint."""

        return self.sha256

    @property
    def metadata(self) -> dict[str, str]:
        """Return safe metadata that identifies the prompt source."""

        return {
            "prompt_source_path": self.source_path,
            "prompt_source_fingerprint": self.fingerprint,
            "prompt_source_sha256": self.sha256,
            "prompt_source_fingerprint_algorithm": self.fingerprint_algorithm,
        }


@dataclass(frozen=True)
class LocalLLMProofRequest:
    """Local-LLM-shaped request built without contacting a real backend."""

    system: str
    user_prompt: str
    metadata: Mapping[str, Any]
    model: str = "fake-local-llm"
    backend_class: str = _FAKE_BACKEND_CLASS


@dataclass(frozen=True)
class LocalLLMProofResult:
    """Result from the fake-client proof path.

    ``behavior_evidence`` is always false. Successful fake output only proves
    request construction and prompt-source preservation, not answer quality or
    runtime readiness.
    """

    request: LocalLLMProofRequest
    output_text: str
    status: str
    reason: str
    behavior_evidence: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)


class LocalLLMProofClient(Protocol):
    """Protocol for injected fake clients used by tests."""

    def generate(self, request: LocalLLMProofRequest) -> str:
        """Return fake text for a proof request."""


@dataclass
class FakeLocalLLMProofClient:
    """Tiny fake client that records requests and never performs I/O."""

    output_text: str = "fake proof output: portable contract consumed"
    fail: bool = False
    calls: list[LocalLLMProofRequest] = field(default_factory=list)

    def generate(self, request: LocalLLMProofRequest) -> str:
        self.calls.append(request)
        if self.fail:
            raise PortableContractError("fake local LLM proof client failed")
        return self.output_text


def _display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(_REPO_ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def load_portable_contract(
    path: str | Path | None = None, *, expected_sha256: str | None = None
) -> PortableContract:
    """Load ``alpha_solver_portable.py`` as prompt text and fingerprint it.

    The loader fails closed when the file is missing, empty, unreadable, or does
    not match a caller-supplied SHA-256 fingerprint.
    """

    contract_path = Path(path) if path is not None else DEFAULT_CONTRACT_PATH
    try:
        text = contract_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise PortableContractError(
            f"portable contract not found: {_display_path(contract_path)}"
        ) from exc
    except OSError as exc:
        raise PortableContractError(
            f"portable contract could not be read: {_display_path(contract_path)}"
        ) from exc

    if not text.strip():
        raise PortableContractError(f"portable contract is empty: {_display_path(contract_path)}")

    digest = sha256(text.encode("utf-8")).hexdigest()
    if expected_sha256 is not None and digest != expected_sha256:
        raise PortableContractError("portable contract sha256 mismatch")

    return PortableContract(text=text, source_path=_display_path(contract_path), sha256=digest)


def build_local_llm_proof_request(
    user_prompt: str,
    *,
    contract: PortableContract | None = None,
    contract_path: str | Path | None = None,
    expected_sha256: str | None = None,
    provider_mode: str = _LOCAL_LLM_PROOF_MODE,
) -> LocalLLMProofRequest:
    """Build a fake local-LLM request that consumes the portable contract.

    ``MODEL_PROVIDER=local`` remains the deterministic smoke/offline mode, so
    this proof helper accepts only the distinct ``local_llm`` mode label.
    """

    normalized_mode = provider_mode.strip().lower()
    if normalized_mode != _LOCAL_LLM_PROOF_MODE:
        raise PortableContractError(
            "local LLM proof requires provider_mode=local_llm; "
            "MODEL_PROVIDER=local remains smoke-only"
        )
    if not user_prompt.strip():
        raise PortableContractError("user prompt is required for local LLM proof request")

    loaded_contract = contract or load_portable_contract(
        contract_path, expected_sha256=expected_sha256
    )
    metadata: dict[str, Any] = {
        **loaded_contract.metadata,
        "provider_mode": _LOCAL_LLM_PROOF_MODE,
        "backend_class": _FAKE_BACKEND_CLASS,
        "no_real_provider_call": True,
        "behavior_evidence": False,
        "evidence_label": _NON_EVIDENCE_LABEL,
    }
    return LocalLLMProofRequest(
        system=loaded_contract.text,
        user_prompt=user_prompt,
        metadata=metadata,
    )


def run_fake_local_llm_contract_proof(
    user_prompt: str,
    *,
    client: LocalLLMProofClient,
    contract: PortableContract | None = None,
    contract_path: str | Path | None = None,
    expected_sha256: str | None = None,
) -> LocalLLMProofResult:
    """Run the fake-client proof path and label unsafe outputs as non-evidence.

    This function proves request construction only. It never upgrades fake output
    into behavior evidence and fails closed for fake-client errors, empty output,
    or prompt echo.
    """

    request = build_local_llm_proof_request(
        user_prompt,
        contract=contract,
        contract_path=contract_path,
        expected_sha256=expected_sha256,
    )
    result_metadata = {**request.metadata, "behavior_evidence": False}
    try:
        output_text = client.generate(request)
    except Exception as exc:  # fake-client-only failure normalization
        return LocalLLMProofResult(
            request=request,
            output_text="",
            status="failed_closed",
            reason=f"fake_client_failure:{exc.__class__.__name__}",
            metadata=result_metadata,
        )

    if not output_text.strip():
        return LocalLLMProofResult(
            request=request,
            output_text=output_text,
            status="failed_closed",
            reason="empty_output_non_evidence",
            metadata=result_metadata,
        )
    if output_text.strip() == user_prompt.strip():
        return LocalLLMProofResult(
            request=request,
            output_text=output_text,
            status="failed_closed",
            reason="prompt_echo_non_evidence",
            metadata=result_metadata,
        )

    return LocalLLMProofResult(
        request=request,
        output_text=output_text,
        status="non_evidence",
        reason="fake_client_contract_consumption_only",
        metadata=result_metadata,
    )
