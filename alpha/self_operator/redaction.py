"""Deterministic local redaction helpers for Self Operator artifacts."""
from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

REDACTION_TEXT = "[REDACTED_SELF_OPERATOR_SECRET]"
SECRET_KEYWORDS = ("api_key", "apikey", "token", "secret", "password", "credential", "credentials")
_SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(api[_-]?key|token|secret|password|credential)s?\b\s*[:=]\s*([^\s,;\]}\)]+)"
)
_BEARER_RE = re.compile(r"(?i)\bbearer\s+([A-Za-z0-9._~+/=-]{8,})")
_PLACEHOLDER_SECRET_RE = re.compile(r"(?i)\b(fake|placeholder|example)[_-]?(api[_-]?key|token|secret|password|credential)\b")


def contains_secret_marker(value: Any) -> bool:
    """Return True when a value contains obvious secret-like marker text."""

    if isinstance(value, str):
        lowered = value.lower()
        return bool(
            any(keyword in lowered for keyword in SECRET_KEYWORDS)
            or _SECRET_ASSIGNMENT_RE.search(value)
            or _BEARER_RE.search(value)
            or _PLACEHOLDER_SECRET_RE.search(value)
        )
    if isinstance(value, Mapping):
        return any(contains_secret_marker(key) or contains_secret_marker(item) for key, item in value.items())
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        return any(contains_secret_marker(item) for item in value)
    return False


def redact_string(value: str) -> str:
    """Redact obvious key/value and bearer-token markers in a string."""

    redacted = _SECRET_ASSIGNMENT_RE.sub(lambda match: f"{match.group(1)}={REDACTION_TEXT}", value)
    redacted = _BEARER_RE.sub(f"Bearer {REDACTION_TEXT}", redacted)
    if _PLACEHOLDER_SECRET_RE.search(redacted):
        return REDACTION_TEXT
    return redacted


def redact_value(value: Any) -> Any:
    """Return a recursively redacted copy while preserving mappings/lists."""

    if isinstance(value, str):
        return redact_string(value)
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if any(keyword in key_text.lower() for keyword in SECRET_KEYWORDS):
                result[key_text] = REDACTION_TEXT
            else:
                result[key_text] = redact_value(item)
        return result
    if isinstance(value, tuple):
        return tuple(redact_value(item) for item in value)
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    return value
