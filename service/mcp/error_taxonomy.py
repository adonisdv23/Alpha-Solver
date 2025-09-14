from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional
import asyncio


class ErrorClass(str, Enum):
    """Classification for MCP errors."""

    TOOL_NOT_FOUND = "TOOL_NOT_FOUND"
    SCHEMA_VALIDATION = "SCHEMA_VALIDATION"
    AUTH = "AUTH"
    RATE_LIMIT = "RATE_LIMIT"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"
    CONNECTIVITY = "CONNECTIVITY"
    RETRYABLE = "RETRYABLE"
    NON_RETRYABLE = "NON_RETRYABLE"
    SANDBOX_VIOLATION = "SANDBOX_VIOLATION"
    SECURITY = "SECURITY"
    UNKNOWN = "UNKNOWN"


@dataclass
class MCPError:
    """Normalized error for MCP interactions."""

    cls: ErrorClass
    message: str
    code: Optional[str] = None
    retryable: bool = False
    root: str = "Exception"
    meta: Optional[Dict[str, Any]] = None

    def to_json(self) -> Dict[str, Any]:
        """Return a JSON-serialisable dictionary representation."""
        return {
            "cls": self.cls.value,
            "message": self.message,
            "code": self.code,
            "retryable": self.retryable,
            "root": self.root,
            "meta": self.meta or {},
        }


def is_retryable(err: MCPError) -> bool:
    """Return True if the error is retryable."""
    return err.retryable


def to_route_explain(err: MCPError) -> Dict[str, Any]:
    """Return a minimal dict for routing/explanation purposes."""
    return {
        "cls": err.cls.value,
        "message": err.message[:100],
        "code": err.code,
        "retryable": err.retryable,
    }


def map_exception(exc: Exception) -> MCPError:
    """Map an arbitrary exception into a deterministic :class:`MCPError`."""

    root = exc.__class__.__name__
    message = str(exc) or root
    code: Optional[str] = None
    meta: Dict[str, Any] = {}

    # HTTP-style errors
    status = getattr(exc, "status_code", None)
    if status is not None:
        code = str(status)
        if status == 429:
            error_cls = ErrorClass.RATE_LIMIT
            retryable = True
        elif status in (401, 403):
            error_cls = ErrorClass.AUTH
            retryable = False
        else:
            error_cls = ErrorClass.UNKNOWN
            retryable = False
    elif isinstance(exc, TimeoutError):
        error_cls = ErrorClass.TIMEOUT
        retryable = True
    elif isinstance(exc, ConnectionError):
        error_cls = ErrorClass.CONNECTIVITY
        retryable = True
    elif isinstance(exc, asyncio.CancelledError):
        error_cls = ErrorClass.CANCELLED
        retryable = False
    elif isinstance(exc, PermissionError):
        error_cls = ErrorClass.AUTH
        retryable = False
    elif isinstance(exc, ValueError):
        error_cls = ErrorClass.SCHEMA_VALIDATION
        retryable = False
    elif "sandbox" in root.lower():
        error_cls = ErrorClass.SANDBOX_VIOLATION
        retryable = False
    else:
        error_cls = ErrorClass.UNKNOWN
        retryable = False

    if retryable:
        meta["secondary"] = ErrorClass.RETRYABLE.value

    return MCPError(
        cls=error_cls,
        message=message,
        code=code,
        retryable=retryable,
        root=root,
        meta=meta or None,
    )
