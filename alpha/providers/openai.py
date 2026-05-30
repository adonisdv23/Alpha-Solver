"""Minimal OpenAI provider client.

This module is the first real provider execution lane. It deliberately lives
outside ``alpha.adapters.openai`` so prompt-rendering adapters remain local and
side-effect free.

The live-capable path uses the OpenAI Responses API (``POST /v1/responses``)
via ``httpx``. Tests inject a fake ``httpx`` transport/client and never require
network access or real credentials.
"""

from __future__ import annotations

import os
import time
from collections.abc import Callable, Mapping
from typing import Any

import httpx

from .base import (
    RETRYABLE_CATEGORIES,
    ProviderCost,
    ProviderError,
    ProviderRequest,
    ProviderResult,
    ProviderUsage,
)

_OPENAI_PROVIDER = "openai"
_DEFAULT_BASE_URL = "https://api.openai.com/v1"
_MISSING_KEY_MESSAGE = "Missing required environment variable OPENAI_API_KEY."


class OpenAIProviderClient:
    """Small synchronous OpenAI client with deterministic retry semantics."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = _DEFAULT_BASE_URL,
        client: httpx.Client | None = None,
        transport: httpx.BaseTransport | None = None,
        max_retries: int = 1,
        backoff: Callable[[int], None] | None = None,
        price_hint: Mapping[str, float] | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._client = client
        self._transport = transport
        self._max_retries = max(0, max_retries)
        self._backoff = backoff or (lambda _attempt: None)
        self._price_hint = dict(price_hint or {})

    def execute(self, request: ProviderRequest) -> ProviderResult:
        """Execute an OpenAI request or raise a safe typed ``ProviderError``."""
        api_key = self._api_key if self._api_key is not None else os.getenv("OPENAI_API_KEY")
        if not api_key or not api_key.strip():
            raise ProviderError(
                provider=_OPENAI_PROVIDER,
                category="missing_credentials",
                retryable=False,
                safe_message=_MISSING_KEY_MESSAGE,
                request_id=request.request_id,
            )

        attempts = self._max_retries + 1
        last_error: ProviderError | None = None
        for attempt in range(attempts):
            started = time.monotonic()
            try:
                response = self._post(request, api_key)
                latency_ms = int((time.monotonic() - started) * 1000)
                if response.status_code >= 400:
                    raise self._error_from_response(response, request.request_id)
                return self._result_from_response(response, request, latency_ms)
            except ProviderError as exc:
                last_error = exc
            except httpx.TimeoutException:
                last_error = ProviderError(
                    provider=_OPENAI_PROVIDER,
                    category="timeout",
                    retryable=True,
                    safe_message="OpenAI request timed out.",
                    request_id=request.request_id,
                )
            except httpx.RequestError:
                last_error = ProviderError(
                    provider=_OPENAI_PROVIDER,
                    category="network",
                    retryable=True,
                    safe_message="OpenAI request failed due to a network error.",
                    request_id=request.request_id,
                )
            except ValueError:
                last_error = ProviderError(
                    provider=_OPENAI_PROVIDER,
                    category="unknown",
                    retryable=False,
                    safe_message="OpenAI response could not be decoded safely.",
                    request_id=request.request_id,
                )

            if (
                attempt < attempts - 1
                and last_error is not None
                and last_error.category in RETRYABLE_CATEGORIES
                and last_error.retryable
            ):
                self._backoff(attempt + 1)
                continue
            break

        if last_error is None:  # pragma: no cover - defensive guard
            last_error = ProviderError(
                provider=_OPENAI_PROVIDER,
                category="unknown",
                retryable=False,
                safe_message="OpenAI request failed.",
                request_id=request.request_id,
            )
        raise last_error

    def _post(self, request: ProviderRequest, api_key: str) -> httpx.Response:
        payload: dict[str, Any] = {
            "model": request.model,
            "input": self._responses_input(request),
            "max_output_tokens": request.max_tokens,
        }
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        # ``seed`` is carried in ProviderRequest for deterministic-capable
        # providers. The current Responses API request body is kept minimal and
        # does not send seed until a later spec validates endpoint support.

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        timeout = httpx.Timeout(max(request.timeout_ms, 1) / 1000.0)

        if self._client is not None:
            return self._client.post(
                f"{self._base_url}/responses", json=payload, headers=headers, timeout=timeout
            )
        with httpx.Client(transport=self._transport) as client:
            return client.post(
                f"{self._base_url}/responses", json=payload, headers=headers, timeout=timeout
            )

    @staticmethod
    def _responses_input(request: ProviderRequest) -> list[dict[str, Any]]:
        messages: list[dict[str, Any]] = []
        if request.system:
            messages.append(
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": request.system}],
                }
            )
        messages.append(
            {"role": "user", "content": [{"type": "input_text", "text": request.prompt}]}
        )
        return messages

    def _result_from_response(
        self, response: httpx.Response, request: ProviderRequest, latency_ms: int
    ) -> ProviderResult:
        data = response.json()
        usage = _usage_from_payload(data)
        return ProviderResult(
            provider=_OPENAI_PROVIDER,
            model=str(data.get("model") or request.model),
            text=_text_from_payload(data),
            finish_reason=_finish_reason_from_payload(data),
            usage=usage,
            cost=_cost_from_payload(data, usage, self._price_hint),
            latency_ms=latency_ms,
            request_id=request.request_id,
            raw_metadata=_safe_raw_metadata(data, response),
        )

    @staticmethod
    def _error_from_response(response: httpx.Response, request_id: str | None) -> ProviderError:
        category = _category_from_response(response)
        return ProviderError(
            provider=_OPENAI_PROVIDER,
            category=category,
            retryable=category in RETRYABLE_CATEGORIES,
            safe_message=_safe_error_message(category),
            status_code=response.status_code,
            request_id=request_id,
        )


def _text_from_payload(data: Mapping[str, Any]) -> str:
    output_text = data.get("output_text")
    if isinstance(output_text, str):
        return output_text

    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0] if isinstance(choices[0], Mapping) else {}
        message = first.get("message") if isinstance(first, Mapping) else None
        if isinstance(message, Mapping) and isinstance(message.get("content"), str):
            return message["content"]
        if isinstance(first.get("text"), str):
            return first["text"]

    output = data.get("output")
    if isinstance(output, list):
        parts: list[str] = []
        for item in output:
            if not isinstance(item, Mapping):
                continue
            content = item.get("content")
            if not isinstance(content, list):
                continue
            for content_item in content:
                if not isinstance(content_item, Mapping):
                    continue
                text = content_item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        if parts:
            return "".join(parts)
    return ""


def _finish_reason_from_payload(data: Mapping[str, Any]) -> str:
    choices = data.get("choices")
    if isinstance(choices, list) and choices and isinstance(choices[0], Mapping):
        reason = choices[0].get("finish_reason")
        if isinstance(reason, str):
            return reason
    output = data.get("output")
    if isinstance(output, list) and output and isinstance(output[0], Mapping):
        reason = output[0].get("finish_reason")
        if isinstance(reason, str):
            return reason
    status = data.get("status")
    if status == "completed":
        return "stop"
    if isinstance(status, str) and status:
        return status
    return "unknown"


def _usage_from_payload(data: Mapping[str, Any]) -> ProviderUsage:
    raw = data.get("usage")
    if not isinstance(raw, Mapping):
        return ProviderUsage()
    input_tokens = _int_or_none(raw.get("input_tokens", raw.get("prompt_tokens")))
    output_tokens = _int_or_none(raw.get("output_tokens", raw.get("completion_tokens")))
    total_tokens = _int_or_none(raw.get("total_tokens"))
    return ProviderUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
    )


def _cost_from_payload(
    data: Mapping[str, Any], usage: ProviderUsage, price_hint: Mapping[str, float]
) -> ProviderCost:
    provider_cost = data.get("cost")
    if isinstance(provider_cost, Mapping):
        estimated = provider_cost.get("estimated_usd") or provider_cost.get("usd")
        if isinstance(estimated, (int, float)):
            return ProviderCost(estimated_usd=float(estimated), source="provider")
    if usage.input_tokens is None or usage.output_tokens is None:
        return ProviderCost(estimated_usd=None, source="unknown")
    input_price = price_hint.get("input_per_1k")
    output_price = price_hint.get("output_per_1k")
    if not isinstance(input_price, (int, float)) or not isinstance(output_price, (int, float)):
        return ProviderCost(estimated_usd=None, source="unknown")
    estimated = (usage.input_tokens / 1000.0 * float(input_price)) + (
        usage.output_tokens / 1000.0 * float(output_price)
    )
    return ProviderCost(estimated_usd=estimated, source="price_hint")


def _safe_raw_metadata(data: Mapping[str, Any], response: httpx.Response) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "response_id": data.get("id"),
        "created": data.get("created"),
        "status": data.get("status"),
        "http_status": response.status_code,
    }
    provider_request_id = response.headers.get("x-request-id") or response.headers.get(
        "openai-request-id"
    )
    if provider_request_id:
        metadata["provider_request_id"] = provider_request_id
    return {k: v for k, v in metadata.items() if v is not None}


def _category_from_response(response: httpx.Response) -> str:
    status = response.status_code
    error_code = ""
    error_type = ""
    try:
        data = response.json()
    except ValueError:
        data = {}
    if isinstance(data, Mapping):
        error = data.get("error")
        if isinstance(error, Mapping):
            error_code = str(error.get("code") or "").lower()
            error_type = str(error.get("type") or "").lower()
    if "content_filter" in {error_code, error_type}:
        return "content_filter"
    if status in {401, 403}:
        return "auth"
    if status == 429:
        return "rate_limit"
    if 500 <= status <= 599:
        return "provider_5xx"
    if 400 <= status <= 499:
        return "invalid_request"
    return "unknown"


def _safe_error_message(category: str) -> str:
    messages = {
        "auth": "OpenAI authentication failed.",
        "rate_limit": "OpenAI rate limit exceeded.",
        "timeout": "OpenAI request timed out.",
        "network": "OpenAI request failed due to a network error.",
        "provider_5xx": "OpenAI provider returned a server error.",
        "invalid_request": "OpenAI rejected the request.",
        "content_filter": "OpenAI blocked the response due to content filtering.",
        "unknown": "OpenAI request failed.",
    }
    return messages.get(category, messages["unknown"])


def _int_or_none(value: Any) -> int | None:
    return value if isinstance(value, int) else None
