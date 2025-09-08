"""Security helpers for the API service."""

from __future__ import annotations

import os
import re
from fastapi import HTTPException, Request

# Regex to match control characters (except newlines and tabs which are generally safe)
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def validate_api_key(request: Request, api_key: str) -> None:
    """Validate the ``X-API-Key`` header against the configured key."""

    supplied = request.headers.get("X-API-Key")
    if not api_key or supplied != api_key:
        raise HTTPException(status_code=401, detail="invalid API key")


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
