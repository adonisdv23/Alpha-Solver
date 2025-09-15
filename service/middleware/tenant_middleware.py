"""Middleware wiring tenant context and rate limiting."""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from service.tenancy.context import extract_tenant_id
from service.tenancy.limiter import TenantLimiter


class TenantMiddleware(BaseHTTPMiddleware):
    """Attach tenant information to the request and enforce limits."""

    def __init__(self, app, limiter: TenantLimiter) -> None:
        super().__init__(app)
        self.limiter = limiter

    async def dispatch(self, request: Request, call_next):
        tenant_id = extract_tenant_id(request)
        if not tenant_id:
            return JSONResponse(
                status_code=400,
                content={"code": "missing_tenant", "detail": "tenant id required"},
            )
        request.state.tenant_id = tenant_id
        allowed, reason = self.limiter.allow_request(tenant_id)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"code": reason, "detail": "rate limit exceeded"},
            )
        return await call_next(request)


__all__ = ["TenantMiddleware"]
