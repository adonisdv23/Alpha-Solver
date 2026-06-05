"""Inert local LLM provider-adapter seam for portable-contract requests.

This module builds a provider-adapter-shaped request from
``alpha_solver_portable.py`` and sends it only to an injected backend. It does
not call Ollama, OpenAI, Anthropic, other hosted providers, or the deterministic
v91 ``_tree_of_thought`` fallback. Successful stub output is wiring evidence
only and is never behavior, runtime, or readiness evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from ipaddress import ip_address
from math import isfinite
import os
from typing import Any, Mapping, Protocol
from urllib.parse import urlsplit
from urllib.request import Request as URLRequest, urlopen

from .portable_contract import PortableContract, PortableContractError, load_portable_contract

_LOCAL_LLM_ADAPTER_MODE = "local_llm"
_ADAPTER_BACKEND_CLASS = "stub-local-llm-provider-adapter"
_OLLAMA_BACKEND_CLASS = "ollama-local-http-runtime"
_ADAPTER_EVIDENCE_LABEL = "non_evidence_local_llm_provider_adapter_wiring"
_DISABLED_MODEL_LABEL = "local-llm-disabled-unconfigured"
_LOCAL_LLM_ENABLED_ENV = "ALPHA_LOCAL_LLM_ENABLED"
_LOCAL_LLM_ENDPOINT_ENV = "ALPHA_LOCAL_LLM_ENDPOINT"
_LOCAL_LLM_MODEL_ENV = "ALPHA_LOCAL_LLM_MODEL"
_LOCAL_LLM_TIMEOUT_ENV = "ALPHA_LOCAL_LLM_TIMEOUT_SECONDS"
_FORBIDDEN_PROVIDER_KEY_ENVS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "DEEPSEEK_API_KEY",
)


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


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _require_exact_model_name(model: str) -> str:
    if not isinstance(model, str) or not model.strip():
        raise LocalLLMProviderAdapterError("missing_model_non_evidence")
    if model != model.strip():
        raise LocalLLMProviderAdapterError("invalid_model_non_evidence")
    return model


def _require_finite_timeout_seconds(timeout_seconds: float) -> float:
    try:
        value = float(timeout_seconds)
    except (TypeError, ValueError):
        raise LocalLLMProviderAdapterError("invalid_timeout_non_evidence") from None
    if not isfinite(value) or value <= 0:
        raise LocalLLMProviderAdapterError("invalid_timeout_non_evidence")
    return value


def _present_provider_keys(env: Mapping[str, str]) -> tuple[str, ...]:
    return tuple(key for key in _FORBIDDEN_PROVIDER_KEY_ENVS if str(env.get(key, "")).strip())


@dataclass(frozen=True)
class LocalLLMRuntimeConfig:
    """Explicit, default-off local LLM runtime configuration.

    This config is not consumed by ``/v1/solve`` or dashboard preview. It exists
    for approved local-runtime call sites and tests only, requires positive
    operator opt-in, rejects provider keys, and validates localhost/loopback plus
    finite timeout before any transport can be invoked.
    """

    endpoint_url: str
    model: str
    timeout_seconds: float
    enabled: bool = True
    provider_mode: str = _LOCAL_LLM_ADAPTER_MODE

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "LocalLLMRuntimeConfig":
        source = os.environ if env is None else env
        if not _truthy(source.get(_LOCAL_LLM_ENABLED_ENV)):
            raise LocalLLMProviderAdapterError("local_llm_disabled_non_evidence")
        present_keys = _present_provider_keys(source)
        if present_keys:
            raise LocalLLMProviderAdapterError("provider_keys_forbidden_non_evidence")
        endpoint_url = validate_ollama_local_endpoint(str(source.get(_LOCAL_LLM_ENDPOINT_ENV, "")))
        model = _require_exact_model_name(str(source.get(_LOCAL_LLM_MODEL_ENV, "")))
        timeout_seconds = _require_finite_timeout_seconds(source.get(_LOCAL_LLM_TIMEOUT_ENV, ""))
        return cls(
            endpoint_url=endpoint_url,
            model=model,
            timeout_seconds=timeout_seconds,
        )

    def build_backend(
        self, transport: OllamaJSONTransport | None = None
    ) -> "OllamaLocalHTTPBackend":
        if not self.enabled:
            raise LocalLLMProviderAdapterError("local_llm_disabled_non_evidence")
        if self.provider_mode != _LOCAL_LLM_ADAPTER_MODE:
            raise LocalLLMProviderAdapterError("provider_mode_mismatch_non_evidence")
        return OllamaLocalHTTPBackend(
            model=self.model,
            endpoint_url=self.endpoint_url,
            timeout_seconds=self.timeout_seconds,
            transport=transport,
        )


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

    def runtime_metadata(self) -> Mapping[str, Any]:
        endpoint_url = validate_ollama_local_endpoint(self.endpoint_url)
        parsed = urlsplit(endpoint_url)
        return {
            "provider_mode": _LOCAL_LLM_ADAPTER_MODE,
            "backend_class": _OLLAMA_BACKEND_CLASS,
            "local_backend": "ollama_chat",
            "local_model": self.model,
            "model": self.model,
            "endpoint_is_loopback": True,
            "endpoint_host_label": "localhost"
            if (parsed.hostname or "").lower().rstrip(".") == "localhost"
            else "loopback",
            "timeout_seconds": _require_finite_timeout_seconds(self.timeout_seconds),
            "no_provider_keys_required": True,
            "no_hosted_fallback": True,
            "behavior_evidence": False,
        }

    def generate(self, request: LocalLLMAdapterRequest) -> str:
        endpoint_url = validate_ollama_local_endpoint(self.endpoint_url)
        timeout_seconds = _require_finite_timeout_seconds(self.timeout_seconds)
        model = _require_exact_model_name(self.model)
        self.calls.append(request)
        payload = build_ollama_chat_payload(request, model=model)
        self.payloads.append(payload)
        if self.transport is None:
            raise LocalLLMProviderAdapterError(
                "provider_backend_disabled_non_evidence",
                "Ollama-style backend requires an injected transport and is default-off",
            )
        try:
            response = self.transport(
                endpoint_url=endpoint_url,
                payload=payload,
                timeout_seconds=timeout_seconds,
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


def _is_loopback_hostname(hostname: str | None) -> bool:
    if hostname is None:
        return False
    normalized = hostname.strip().lower().rstrip(".")
    if normalized == "localhost":
        return True
    try:
        return ip_address(normalized).is_loopback
    except ValueError:
        return False


def validate_ollama_local_endpoint(endpoint_url: str) -> str:
    """Return a valid local endpoint URL or fail closed before transport use."""

    if not isinstance(endpoint_url, str) or not endpoint_url.strip():
        raise LocalLLMProviderAdapterError("endpoint_not_local_non_evidence")
    parsed = urlsplit(endpoint_url.strip())
    if parsed.scheme != "http":
        raise LocalLLMProviderAdapterError("endpoint_not_local_non_evidence")
    if parsed.username is not None or parsed.password is not None:
        raise LocalLLMProviderAdapterError("endpoint_not_local_non_evidence")
    if not _is_loopback_hostname(parsed.hostname):
        raise LocalLLMProviderAdapterError("endpoint_not_local_non_evidence")
    try:
        parsed.port
    except ValueError:
        raise LocalLLMProviderAdapterError("endpoint_not_local_non_evidence") from None
    return endpoint_url.strip()


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
    model = _require_exact_model_name(model)
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


def _echo_reason(output_text: str, request: LocalLLMAdapterRequest) -> str | None:
    stripped = output_text.strip()
    if stripped == request.user_prompt.strip():
        return "prompt_echo_non_evidence"
    if stripped == request.system.strip():
        return "system_echo_non_evidence"
    return None


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
        runtime_metadata = getattr(backend, "runtime_metadata", None)
        if callable(runtime_metadata):
            result_metadata = {**result_metadata, **runtime_metadata(), "behavior_evidence": False}
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
    echo_reason = _echo_reason(output_text, request)
    if echo_reason is not None:
        return LocalLLMAdapterResult(
            request=request,
            output_text=output_text,
            status="failed_closed",
            reason=echo_reason,
            metadata={**result_metadata, "failure_label": "failed_closed_result"},
        )

    return LocalLLMAdapterResult(
        request=request,
        output_text=output_text,
        status="non_evidence",
        reason="local_llm_provider_adapter_wiring_only",
        metadata=result_metadata,
    )


def urllib_ollama_json_transport(
    *,
    endpoint_url: str,
    payload: Mapping[str, Any],
    timeout_seconds: float,
) -> Mapping[str, Any]:
    """POST JSON to a pre-validated local Ollama endpoint.

    The caller must pass a URL through ``validate_ollama_local_endpoint`` and a
    finite timeout before this transport executes. The helper uses only the
    supplied endpoint and contains no hosted-provider fallback.
    """

    endpoint_url = validate_ollama_local_endpoint(endpoint_url)
    timeout_seconds = _require_finite_timeout_seconds(timeout_seconds)
    data = json.dumps(dict(payload)).encode("utf-8")
    request = URLRequest(
        endpoint_url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=timeout_seconds) as response:  # nosec B310 - loopback URL only
        decoded = json.loads(response.read().decode("utf-8"))
    if not isinstance(decoded, Mapping):
        raise LocalLLMProviderAdapterError("malformed_response_non_evidence")
    return decoded


def run_configured_local_llm_runtime(
    user_prompt: str,
    *,
    config: LocalLLMRuntimeConfig | None = None,
    env: Mapping[str, str] | None = None,
    transport: OllamaJSONTransport | None = None,
    contract: PortableContract | None = None,
    contract_path: str | None = None,
    expected_sha256: str | None = None,
) -> LocalLLMAdapterResult:
    """Run the optional local LLM runtime path after explicit safe config.

    This is intentionally not wired to ``/v1/solve`` or dashboard preview. With
    no explicit config/env opt-in it fails before transport construction. With no
    supplied transport, it uses the loopback-only urllib transport. Tests should
    inject transports and must not make network calls.
    """

    runtime_config = config or LocalLLMRuntimeConfig.from_env(env)
    backend = runtime_config.build_backend(transport or urllib_ollama_json_transport)
    return run_local_llm_provider_adapter(
        user_prompt,
        backend=backend,
        contract=contract,
        contract_path=contract_path,
        expected_sha256=expected_sha256,
        provider_mode=_LOCAL_LLM_ADAPTER_MODE,
        model=runtime_config.model,
    )
