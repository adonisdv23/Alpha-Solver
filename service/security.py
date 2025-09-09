"""Security helpers for the API service."""

from __future__ import annotations

import re
from fastapi import HTTPException, Request
from alpha.core.config import APISettings

# Regex to match control characters (except newlines and tabs which are generally safe)
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def validate_api_key(request: Request, config: APISettings) -> str:
    """Validate the configured API key header when authentication is enabled."""

    if not config.auth.enabled:
        return request.headers.get(config.auth.header, "")
    supplied = request.headers.get(config.auth.header)
    if supplied not in config.auth.keys:
        raise HTTPException(status_code=401, detail="invalid API key")
    return supplied


def sanitize_query(text: str, max_length: int = 1000) -> str:
    """Basic input sanitization for the query string.

    - Enforces a maximum length.
    - Rejects control characters.
    """

    if len(text) > max_length:
        raise HTTPException(status_code=400, detail="query too long")
    if _CONTROL_CHARS.search(text):
        raise HTTPException(status_code=400, detail="query contains invalid characters")
    # Very conservative disallow list for obvious code-injection patterns.
    if "__" in text or "import" in text.lower():
        raise HTTPException(status_code=400, detail="query contains disallowed patterns")
    return text


__all__ = ["validate_api_key", "sanitize_query"]
