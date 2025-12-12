"""Model Context Protocol adapter for external tools (MVP)."""
from __future__ import annotations

import time
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Tuple


class McpAdapterError(Exception):
    """Base error for adapter failures."""


class McpAdapterTimeout(McpAdapterError):
    """Raised when a tool call exceeds the timeout budget."""


class McpAdapter:
    """Minimal orchestration bridge for MCP tools.

    The adapter enforces governance hooks (allow-list, timeout, and redaction)
    while exposing deterministic wrappers for the supported MVP tools.
    """

    DEFAULT_TIMEOUT_MS = 10_000
    DEFAULT_REDACT_FIELDS = {"email", "phone_number", "full_name", "address"}

    def __init__(self, config: Optional[Mapping[str, Any]] = None) -> None:
        self.config = dict(config or {})
        self.timeout_ms = int(self.config.get("timeout_ms", self.DEFAULT_TIMEOUT_MS))
        self.allow_domains = set(self.config.get("allow_domains", []))
        self.redact_fields = set(
            self.config.get("redact_fields", self.DEFAULT_REDACT_FIELDS)
        )
        self._tools: Dict[str, Callable[[Mapping[str, Any]], Mapping[str, Any]]] = {
            "playwright_web_extract": self._call_playwright_web_extract,
            "gsheets_write": self._call_gsheets_write,
        }

    def capabilities(self) -> List[str]:
        """Return available MCP tool identifiers."""

        return sorted(self._tools)

    def safe_call(self, tool_name: str, payload: Mapping[str, Any]) -> Dict[str, Any]:
        """Execute ``tool_name`` with governance hooks and redaction.

        The method enforces allow-list checks and the default timeout budget. It
        returns a dictionary containing the redacted output and metadata about
        what protections were applied.
        """

        if tool_name not in self._tools:
            raise McpAdapterError(f"unsupported_tool:{tool_name}")

        call_fn = self._tools[tool_name]
        domain = self._extract_domain(payload)
        self._enforce_allowlist(domain)

        start = time.perf_counter()
        redactions: List[str] = []
        try:
            result = self._with_timeout(call_fn, payload)
        except McpAdapterTimeout:
            raise
        except Exception as exc:  # pragma: no cover - governance categories
            raise McpAdapterError(f"tool_error:{tool_name}:{exc}") from exc

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        redacted_result, redactions = self._redact(result)
        return {
            "tool": tool_name,
            "domain": domain,
            "elapsed_ms": elapsed_ms,
            "redactions": redactions,
            "output": redacted_result,
        }

    # Governance helpers -------------------------------------------------
    def _enforce_allowlist(self, domain: Optional[str]) -> None:
        if self.allow_domains and domain not in self.allow_domains:
            raise McpAdapterError(f"domain_not_allowed:{domain}")

    def _with_timeout(
        self, fn: Callable[[Mapping[str, Any]], Mapping[str, Any]], payload: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        start = time.perf_counter()
        result = fn(payload)
        elapsed_ms = (time.perf_counter() - start) * 1000
        if elapsed_ms > self.timeout_ms:
            raise McpAdapterTimeout(f"timeout_exceeded:{int(elapsed_ms)}ms")
        return result

    def _redact(self, output: Mapping[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        redacted = dict(output)
        redactions: List[str] = []
        for field in self.redact_fields:
            if field in redacted:
                redacted[field] = "[redacted]"
                redactions.append(field)
        return redacted, redactions

    # Tool wrappers ------------------------------------------------------
    def _call_playwright_web_extract(
        self, payload: Mapping[str, Any]
    ) -> Dict[str, Any]:
        url = payload.get("url", "")
        domain = self._extract_domain(payload)
        content = payload.get("content") or payload.get("selector") or ""
        return {
            "tool_name": "playwright_web_extract",
            "domain": domain,
            "url": url,
            "extracted": payload.get("extracted") or content,
        }

    def _call_gsheets_write(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        sheet_id = payload.get("sheet_id")
        rows = payload.get("rows", [])
        if not sheet_id:
            raise McpAdapterError("missing_sheet_id")
        if not isinstance(rows, Iterable):
            raise McpAdapterError("invalid_rows")
        return {
            "tool_name": "gsheets_write",
            "sheet_id": sheet_id,
            "row_count": len(list(rows)),
            "status": "accepted",
        }

    @staticmethod
    def _extract_domain(payload: Mapping[str, Any]) -> Optional[str]:
        url = payload.get("url") or payload.get("domain")
        if not url:
            return None
        if "//" in url:
            url = url.split("//", 1)[-1]
        return url.split("/", 1)[0]


__all__ = ["McpAdapter", "McpAdapterError", "McpAdapterTimeout"]
