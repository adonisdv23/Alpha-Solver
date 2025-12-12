"""Observability card helpers for MCP calls."""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

PII_FIELDS = {"email", "phone_number", "full_name", "address"}


def redact_pii(payload: Mapping[str, Any], pii_fields: Iterable[str] = PII_FIELDS) -> Tuple[Dict[str, Any], List[str]]:
    """Return a copy of ``payload`` with PII fields scrubbed."""

    sanitized = dict(payload)
    redactions: List[str] = []
    for field in pii_fields:
        if field in sanitized:
            sanitized[field] = "[redacted]"
            redactions.append(field)
    return sanitized, redactions


def allowlist_verdict(domain: Optional[str], allow_domains: Iterable[str]) -> Tuple[bool, Optional[str]]:
    allowed_set = set(allow_domains)
    if not allowed_set:
        return True, None
    if domain in allowed_set:
        return True, None
    return False, f"domain_not_allowed:{domain}"


class ObsCard:
    """Capture auditable MCP interactions with enforced redaction."""

    def __init__(self) -> None:
        self.entries: List[Dict[str, Any]] = []

    def record_mcp_call(
        self,
        *,
        tool_name: str,
        domain: Optional[str],
        output: Mapping[str, Any],
        timing_ms: int,
        retries: int,
        budget_verdict: str,
        allow_domains: Iterable[str] = (),
    ) -> Dict[str, Any]:
        allowed, denied_reason = allowlist_verdict(domain, allow_domains)
        sanitized, redactions = redact_pii(output)
        entry = {
            "tool_name": tool_name,
            "domain": domain,
            "timing_ms": timing_ms,
            "retries": retries,
            "budget_verdict": budget_verdict,
            "redactions": redactions,
            "denied_reason": denied_reason,
            "output": sanitized if allowed else {},
        }
        self.entries.append(entry)
        return entry

    def as_list(self) -> List[Dict[str, Any]]:
        return list(self.entries)


__all__ = ["ObsCard", "PII_FIELDS", "redact_pii", "allowlist_verdict"]
