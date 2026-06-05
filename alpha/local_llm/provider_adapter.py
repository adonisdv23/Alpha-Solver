"""Inert local LLM provider-adapter seam for portable-contract requests.

This module builds a provider-adapter-shaped request from
``alpha_solver_portable.py`` and sends it only to an injected backend. It does
not call Ollama, OpenAI, Anthropic, other hosted providers, or the deterministic
v91 ``_tree_of_thought`` fallback. Successful stub or offline fixture output is
wiring evidence only and is never behavior, runtime, or readiness evidence.
"""

from __future__ import annotations

import json
import socket
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Protocol
from urllib import error as urllib_error
from urllib import request as urllib_request
from urllib.parse import urlparse

from .portable_contract import PortableContract, PortableContractError, load_portable_contract

_LOCAL_LLM_ADAPTER_MODE = "local_llm"
_ADAPTER_BACKEND_CLASS = "stub-local-llm-provider-adapter"
_OLLAMA_BACKEND_CLASS = "ollama-local-http-offline-adapter"
_ADAPTER_EVIDENCE_LABEL = "non_evidence_local_llm_provider_adapter_wiring"
_DISABLED_MODEL_LABEL = "local-llm-disabled-unconfigured"
_ALLOWED_LOCAL_HOSTS = {"127.0.0.1", "::1", "localhost"}


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
    request construction, prompt-source preservation, parser behavior, and
    injected-backend handoff occurred.
    """

    request: LocalLLMAdapterRequest
    output_text: str
    status: str
    reason: str
    behavior_evidence: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)


class LocalLLMProviderAdapterError(PortableContractError):
    """Fail-closed provider-adapter error with a stable non-evidence reason."""

    def __init__(self, reason_code: str, detail: str = "") -> None:
        super().__init__(detail or reason_code)
        self.reason_code = reason_code
        self.detail = detail


class LocalLLMProviderBackend(Protocol):
    """Injected local-backend seam used by offline tests and future adapters."""

    def generate(self, request: LocalLLMAdapterRequest) -> str:
        """Return text for an adapter request."""


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


OllamaTransport = Callable[[str, Mapping[str, Any], float], Mapping[str, Any]]


@dataclass(frozen=True)
class OllamaLocalHTTPBackend:
    """Default-off Ollama-style local HTTP backend behind the injected seam.

    The backend is inert unless ``enabled=True`` is passed explicitly by a later
    authorized lane. Tests can inject ``transport`` callables to exercise request
    mapping and response parsing without opening sockets.
    """

    endpoint: str = "http://127.0.0.1:11434/api/chat"
    model: str = _DISABLED_MODEL_LABEL
    timeout_seconds: float = 5.0
    enabled: bool = False
    transport: OllamaTransport | None = None

    @property
    def backend_class(self) -> str:
        """Return the backend label used for non-evidence metadata/tests."""

        return _OLLAMA_BACKEND_CLASS

    def build_payload(self, request: LocalLLMAdapterRequest) -> dict[str, Any]:
        """Map an adapter request to the Ollama ``/api/chat`` JSON shape."""

        return build_ollama_chat_payload(request, model=self.model)

    def generate(self, request: LocalLLMAdapterRequest) -> str:
        """Generate via an explicitly enabled local endpoint or injected transport."""

        if not self.enabled:
            raise LocalLLMProviderAdapterError(
                "ollama_backend_disabled_non_evidence",
                "Ollama local HTTP backend is default-off and unconfigured.",
            )
        _validate_local_ollama_endpoint(self.endpoint)
        if self.timeout_seconds <= 0:
            raise LocalLLMProviderAdapterError(
                "ollama_timeout_invalid_non_evidence", "timeout must be positive"
            )

        payload = self.build_payload(request)
        transport = self.transport or _urllib_ollama_transport
        try:
            response = transport(self.endpoint, payload, self.timeout_seconds)
        except TimeoutError as exc:
            raise LocalLLMProviderAdapterError(
                "ollama_timeout_non_evidence", "Ollama-style local request timed out."
            ) from exc
        except socket.timeout as exc:
            raise LocalLLMProviderAdapterError(
                "ollama_timeout_non_evidence", "Ollama-style local request timed out."
            ) from exc
        except urllib_error.HTTPError as exc:
            raise LocalLLMProviderAdapterError(
                "ollama_backend_error_non_evidence", f"HTTP status {exc.code}"
            ) from exc
        except OSError as exc:
            raise LocalLLMProviderAdapterError(
                "ollama_connection_failure_non_evidence",
                "Ollama-style local endpoint connection failed.",
            ) from exc

        return parse_ollama_assistant_text(response, request=request)


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
    request: LocalLLMAdapterRequest, *, model: str = _DISABLED_MODEL_LABEL
) -> dict[str, Any]:
    """Return an Ollama-style ``/api/chat`` payload without sending it."""

    return {
        "model": model,
        "stream": False,
        "messages": [
            {"role": message.role, "content": message.content}
            for message in request.messages
        ],
        "options": {"temperature": 0},
    }


def parse_ollama_assistant_text(
    response: Mapping[str, Any], *, request: LocalLLMAdapterRequest | None = None
) -> str:
    """Extract assistant text from a static Ollama-style response fixture."""

    if not isinstance(response, Mapping):
        raise LocalLLMProviderAdapterError(
            "malformed_ollama_response_non_evidence", "response is not a mapping"
        )
    message = response.get("message")
    if not isinstance(message, Mapping):
        raise LocalLLMProviderAdapterError(
            "malformed_ollama_response_non_evidence", "missing message object"
        )
    content = message.get("content")
    if not isinstance(content, str):
        raise LocalLLMProviderAdapterError(
            "malformed_ollama_response_non_evidence", "message content is not text"
        )
    if not content.strip():
        raise LocalLLMProviderAdapterError(
            "empty_ollama_response_non_evidence", "assistant content is empty"
        )
    if request is not None and _is_prompt_echo(content, request):
        raise LocalLLMProviderAdapterError(
            "prompt_echo_non_evidence", "assistant content echoes prompt or contract"
        )
    return content


def _validate_local_ollama_endpoint(endpoint: str) -> None:
    parsed = urlparse(endpoint)
    if parsed.scheme != "http" or parsed.hostname not in _ALLOWED_LOCAL_HOSTS:
        raise LocalLLMProviderAdapterError(
            "ollama_endpoint_not_local_non_evidence",
            "Ollama-style backend is restricted to explicit local HTTP endpoints.",
        )


def _urllib_ollama_transport(
    endpoint: str, payload: Mapping[str, Any], timeout_seconds: float
) -> Mapping[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    http_request = urllib_request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib_request.urlopen(http_request, timeout=timeout_seconds) as response:
        raw = response.read().decode("utf-8")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LocalLLMProviderAdapterError(
            "malformed_ollama_response_non_evidence", "response body is not JSON"
        ) from exc
    if not isinstance(parsed, Mapping):
        raise LocalLLMProviderAdapterError(
            "malformed_ollama_response_non_evidence", "response body is not a JSON object"
        )
    return parsed


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
    except LocalLLMProviderAdapterError as exc:
        return LocalLLMAdapterResult(
            request=request,
            output_text="",
            status="failed_closed",
            reason=exc.reason_code,
            metadata=result_metadata,
        )
    except Exception as exc:  # injected-backend-only failure normalization
        return LocalLLMAdapterResult(
            request=request,
            output_text="",
            status="failed_closed",
            reason=f"adapter_error:{exc.__class__.__name__}",
            metadata=result_metadata,
        )

    if not output_text.strip():
        return LocalLLMAdapterResult(
            request=request,
            output_text=output_text,
            status="failed_closed",
            reason="empty_model_output_non_evidence",
            metadata=result_metadata,
        )
    if _is_prompt_echo(output_text, request):
        return LocalLLMAdapterResult(
            request=request,
            output_text=output_text,
            status="failed_closed",
            reason="prompt_echo_non_evidence",
            metadata=result_metadata,
        )

    return LocalLLMAdapterResult(
        request=request,
        output_text=output_text,
        status="non_evidence",
        reason="local_llm_provider_adapter_wiring_only",
        metadata=result_metadata,
    )
