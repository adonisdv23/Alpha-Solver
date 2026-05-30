"""No-secret provider SAFE-OUT response helpers.

The provider SAFE-OUT body is intentionally allowlist-built for the explicit
FastAPI ``/v1/solve`` OpenAI provider failure path. This module never inspects
raw provider payloads, raw metadata, environment/config dumps, or exception
objects beyond the normalized ``ProviderError`` safe fields.
"""

from __future__ import annotations

from typing import Any

from .base import ProviderError

_PROVIDER_SAFE_OUT_STATUS_BY_CATEGORY: dict[str, int] = {
    "missing_credentials": 503,
    "auth": 502,
    "rate_limit": 429,
    "timeout": 504,
    "network": 503,
    "provider_5xx": 502,
    "invalid_request": 400,
    "content_filter": 400,
    "unknown": 502,
}
_DEFAULT_PROVIDER_SAFE_OUT_STATUS = 502


def provider_safe_out_status(error: ProviderError) -> int:
    """Return the preserved HTTP status mapping for a provider failure."""

    return _PROVIDER_SAFE_OUT_STATUS_BY_CATEGORY.get(
        error.category, _DEFAULT_PROVIDER_SAFE_OUT_STATUS
    )


def build_provider_safe_out_body(error: ProviderError) -> dict[str, Any]:
    """Build the lean provider SAFE-OUT response body from safe fields only."""

    return {
        "final_answer": f"SAFE-OUT: {error.safe_message}",
        "safe_out": True,
        "error": {
            "provider": error.provider,
            "category": error.category,
            "retryable": error.retryable,
            "request_id": error.request_id,
            "retry_count": error.retry_count,
            "status_code": error.status_code,
        },
    }


__all__ = ["build_provider_safe_out_body", "provider_safe_out_status"]
