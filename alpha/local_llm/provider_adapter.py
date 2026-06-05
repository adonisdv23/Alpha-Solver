"""Inert local LLM provider-adapter seam for portable-contract requests.

This module builds a provider-adapter-shaped request from
``alpha_solver_portable.py`` and sends it only to an injected backend. It does
not call Ollama, OpenAI, Anthropic, other hosted providers, or the deterministic
v91 ``_tree_of_thought`` fallback. Successful stub output is wiring evidence
only and is never behavior, runtime, or readiness evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol

from .portable_contract import PortableContract, PortableContractError, load_portable_contract

_LOCAL_LLM_ADAPTER_MODE = "local_llm"
_ADAPTER_BACKEND_CLASS = "stub-local-llm-provider-adapter"
_ADAPTER_EVIDENCE_LABEL = "non_evidence_local_llm_provider_adapter_wiring"
_DISABLED_MODEL_LABEL = "local-llm-disabled-unconfigured"


@dataclass(frozen=True)
class LocalLLMAdapterMessage:
    """Single role/content message for an inert local LLM adapter request."""

    role: str
    content: str


@dataclass(frozen=True)
class LocalLLMAdapterRequest:
    """Local-LLM-shaped request that preserves contract and user boundaries."""

    system: str
    user_prompt: str
    messages: tuple[LocalLLMAdapterMessage, LocalLLMAdapterMessage]
    metadata: Mapping[str, Any]
    model: str = _DISABLED_MODEL_LABEL
    provider_mode: str = _LOCAL_LLM_ADAPTER_MODE
    backend_class: str = _ADAPTER_BACKEND_CLASS


@dataclass(frozen=True)
class LocalLLMAdapterResult:
    """Normalized adapter result.

    ``behavior_evidence`` is always false. A non-failed result proves only that
    request construction, prompt-source preservation, and injected-backend
    handoff occurred.
    """

    request: LocalLLMAdapterRequest
    output_text: str
    status: str
    reason: str
    behavior_evidence: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)


class LocalLLMProviderBackend(Protocol):
    """Injected local-backend seam used by offline tests and future adapters."""

    def generate(self, request: LocalLLMAdapterRequest) -> str:
        """Return text for an adapter request."""


class OllamaJSONTransport(Protocol):
    """Injected JSON transport for an Ollama-style local HTTP endpoint.

    Default adapter construction does not provide a transport, so this protocol
    keeps network execution opt-in and testable with offline fakes.
    """

    def __call__(
        self,
        *,
        endpoint_url: str,
        payload: Mapping[str, Any],
        timeout_seconds: float,
    ) -> Mapping[str, Any]:
        """Return a decoded JSON response for a mapped Ollama-style payload."""


class LocalLLMProviderAdapterError(PortableContractError):
    """Fail-closed backend error carrying a stable adapter reason code."""

    def __init__(self, reason_code: str, detail: str | None = None):
        super().__init__(detail or reason_code)
        self.reason_code = reason_code


@dataclass
class StubLocalLLMProviderBackend:
    """Offline stub backend that records requests and performs no I/O."""

    output_text: str = "stub local LLM adapter output: request accepted"
    fail: bool = False
    calls: list[LocalLLMAdapterRequest] = field(default_factory=list)

    def generate(self, request: LocalLLMAdapterRequest) -> str:
        self.calls.append(request)
        if self.fail:
            raise PortableContractError("stub local LLM provider adapter failed")
        return self.output_text


@dataclass
class OllamaLocalHTTPBackend:
    """Default-off Ollama-style local HTTP backend behind the injected seam.

    The class maps Alpha Solver adapter requests to the Ollama ``/api/chat``
    JSON shape and parses Ollama-style JSON responses. It performs no network
    I/O unless an explicit transport callable is injected by a later approved
    smoke lane. Offline tests inject fake transports only.
    """

    model: str
    endpoint_url: str = "http://127.0.0.1:11434/api/chat"
    timeout_seconds: float = 10.0
    transport: OllamaJSONTransport | None = None
    calls: list[LocalLLMAdapterRequest] = field(default_factory=list)
    payloads: list[Mapping[str, Any]] = field(default_factory=list)

    def generate(self, request: LocalLLMAdapterRequest) -> str:
        self.calls.append(request)
        payload = build_ollama_chat_payload(request, model=self.model)
        self.payloads.append(payload)
        if self.transport is None:
            raise LocalLLMProviderAdapterError(
                "provider_backend_disabled_non_evidence",
                "Ollama-style backend requires an injected transport and is default-off",
            )
        try:
            response = self.transport(
                endpoint_url=self.endpoint_url,
                payload=payload,
                timeout_seconds=self.timeout_seconds,
            )
        except TimeoutError as exc:
            raise LocalLLMProviderAdapterError("timeout_non_evidence", str(exc)) from exc
        except ConnectionError as exc:
            raise LocalLLMProviderAdapterError(
                "connection_failure_non_evidence", str(exc)
            ) from exc
        except LocalLLMProviderAdapterError:
            raise
        except Exception as exc:
            raise LocalLLMProviderAdapterError(
                "backend_error_non_evidence", str(exc)
            ) from exc
        return parse_ollama_chat_response(response)


def _normalize_mode(provider_mode: str) -> str:
    normalized = provider_mode.strip().lower()
    if normalized != _LOCAL_LLM_ADAPTER_MODE:
        raise PortableContractError(
            "local LLM provider adapter requires provider_mode=local_llm; "
            "MODEL_PROVIDER=local remains smoke-only"
        )
    return normalized


def build_local_llm_adapter_request(
    user_prompt: str,
    *,
    contract: PortableContract | None = None,
    contract_path: str | None = None,
    expected_sha256: str | None = None,
    provider_mode: str = _LOCAL_LLM_ADAPTER_MODE,
    model: str = _DISABLED_MODEL_LABEL,
) -> LocalLLMAdapterRequest:
    """Build an inert provider-adapter request from the portable contract.

    The portable contract is loaded as the system/contract message and the user
    prompt is preserved as a separate user message. The function accepts only the
    distinct ``local_llm`` mode label so ``MODEL_PROVIDER=local`` remains the
    existing smoke-only mode unless a separate approved lane changes it.
    """

    normalized_mode = _normalize_mode(provider_mode)
    if not user_prompt.strip():
        raise PortableContractError("user prompt is required for local LLM adapter request")

    loaded_contract = contract or load_portable_contract(
        contract_path, expected_sha256=expected_sha256
    )
    messages = (
        LocalLLMAdapterMessage(role="system", content=loaded_contract.text),
        LocalLLMAdapterMessage(role="user", content=user_prompt),
    )
    metadata: dict[str, Any] = {
        **loaded_contract.metadata,
        "provider_mode": normalized_mode,
        "backend_class": _ADAPTER_BACKEND_CLASS,
        "model": model,
        "no_real_provider_call": True,
        "real_provider_call_enabled": False,
        "behavior_evidence": False,
        "evidence_label": _ADAPTER_EVIDENCE_LABEL,
    }
    return LocalLLMAdapterRequest(
        system=loaded_contract.text,
        user_prompt=user_prompt,
        messages=messages,
        metadata=metadata,
        model=model,
        provider_mode=normalized_mode,
    )


def build_ollama_chat_payload(
    request: LocalLLMAdapterRequest,
    *,
    model: str,
    stream: bool = False,
    options: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    """Map an adapter request to an Ollama-style ``/api/chat`` payload."""

    if request.provider_mode != _LOCAL_LLM_ADAPTER_MODE:
        raise LocalLLMProviderAdapterError("provider_mode_mismatch_non_evidence")
    if not model.strip():
        raise LocalLLMProviderAdapterError("missing_model_non_evidence")
    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": message.role, "content": message.content}
            for message in request.messages
        ],
        "stream": stream,
    }
    if options is not None:
        payload["options"] = dict(options)
    return payload


def parse_ollama_chat_response(response: Any) -> str:
    """Extract assistant text from a static Ollama-style JSON response."""

    if not isinstance(response, Mapping):
        raise LocalLLMProviderAdapterError("malformed_response_non_evidence")
    message = response.get("message")
    if not isinstance(message, Mapping):
        raise LocalLLMProviderAdapterError("malformed_response_non_evidence")
    if message.get("role") not in {None, "assistant"}:
        raise LocalLLMProviderAdapterError("malformed_response_non_evidence")
    content = message.get("content")
    if not isinstance(content, str):
        raise LocalLLMProviderAdapterError("malformed_response_non_evidence")
    if not content.strip():
        raise LocalLLMProviderAdapterError("empty_model_output_non_evidence")
    return content


def _is_prompt_echo(output_text: str, request: LocalLLMAdapterRequest) -> bool:
    stripped = output_text.strip()
    return stripped in {request.user_prompt.strip(), request.system.strip()}


def run_local_llm_provider_adapter(
    user_prompt: str,
    *,
    backend: LocalLLMProviderBackend,
    contract: PortableContract | None = None,
    contract_path: str | None = None,
    expected_sha256: str | None = None,
    provider_mode: str = _LOCAL_LLM_ADAPTER_MODE,
    model: str = _DISABLED_MODEL_LABEL,
) -> LocalLLMAdapterResult:
    """Run the inert adapter against an injected backend and fail closed.

    This seam performs no default provider calls. Adapter/backend errors, empty
    output, and prompt echo are normalized as ``failed_closed`` non-evidence.
    """

    request = build_local_llm_adapter_request(
        user_prompt,
        contract=contract,
        contract_path=contract_path,
        expected_sha256=expected_sha256,
        provider_mode=provider_mode,
        model=model,
    )
    result_metadata = {**request.metadata, "behavior_evidence": False}
    try:
        output_text = backend.generate(request)
    except Exception as exc:  # injected-backend-only failure normalization
        reason = getattr(exc, "reason_code", f"adapter_error:{exc.__class__.__name__}")
        return LocalLLMAdapterResult(
            request=request,
            output_text="",
            status="failed_closed",
            reason=reason,
            metadata={**result_metadata, "failure_label": "failed_closed_result"},
        )

    if not output_text.strip():
        return LocalLLMAdapterResult(
            request=request,
            output_text=output_text,
            status="failed_closed",
            reason="empty_model_output_non_evidence",
            metadata={**result_metadata, "failure_label": "failed_closed_result"},
        )
    if _is_prompt_echo(output_text, request):
        return LocalLLMAdapterResult(
            request=request,
            output_text=output_text,
            status="failed_closed",
            reason="prompt_echo_non_evidence",
            metadata={**result_metadata, "failure_label": "failed_closed_result"},
        )

    return LocalLLMAdapterResult(
        request=request,
        output_text=output_text,
        status="non_evidence",
        reason="local_llm_provider_adapter_wiring_only",
        metadata=result_metadata,
    )
