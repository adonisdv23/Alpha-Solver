"""Tenant context utilities.

Derives the tenant identifier for a request. The tenant id is primarily
sourced from the authenticated principal inserted by :class:`JWTAuthMiddleware`.
If no authenticated principal is present, the ``X-Tenant-ID`` header is used as
fallback.  The functions here are intentionally lightweight to keep request
processing fast.
"""
from __future__ import annotations

from typing import Optional

from starlette.requests import Request


def extract_tenant_id(request: Request) -> Optional[str]:
    """Return the tenant id associated with *request*.

    The lookup order is:
    1. ``request.state.principal['tenant_id']`` if available.
    2. ``X-Tenant-ID`` header.
    Returns ``None`` if no tenant identifier can be found.
    """

    principal = getattr(request.state, "principal", None)
    if principal:
        tid = principal.get("tenant_id")
        if tid:
            return str(tid)
    header_tid = request.headers.get("X-Tenant-ID")
    if header_tid:
        return header_tid
    return None


def require_tenant_id(request: Request) -> str:
    """Like :func:`extract_tenant_id` but raise ``ValueError`` if missing."""

    tenant_id = extract_tenant_id(request)
    if not tenant_id:
        raise ValueError("tenant id not found")
    return tenant_id


__all__ = ["extract_tenant_id", "require_tenant_id"]
