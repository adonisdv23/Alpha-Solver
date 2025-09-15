"""Authentication middleware supporting JWTs and API keys."""

from __future__ import annotations

import logging
import time
from typing import Dict, Iterable, Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from service.auth.api_keys import APIKeyStore
from service.auth.jwt_utils import AuthKeyStore as JWTKeyStore, JWTError, verify_jwt
from service.audit import audit_log

logger = logging.getLogger("service.middleware.auth")


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware enforcing JWT or API key authentication."""

    def __init__(
        self,
        app,
        api_key_store: APIKeyStore,
        jwt_key_store: JWTKeyStore | None = None,
        audience: str | None = None,
        issuer: str | None = None,
        exempt_paths: Optional[Iterable[str]] = None,
        scope_map: Optional[Dict[str, Iterable[str]]] = None,
        rate_limit: Optional[tuple[int, int]] = None,
        time_func=time.time,
    ) -> None:
        super().__init__(app)
        self.api_key_store = api_key_store
        self.jwt_key_store = jwt_key_store
        self.audience = audience
        self.issuer = issuer
        self.exempt_paths = set(exempt_paths or [])
        self.scope_map = {p: set(s) for p, s in (scope_map or {}).items()}
        self.rate_limit = rate_limit
        self._time = time_func
        self._counters: Dict[str, tuple[float, int]] = {}

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path in self.exempt_paths:
            return await call_next(request)

        auth = request.headers.get("authorization")
        api_key = request.headers.get("x-api-key")
        principal: Dict[str, object] | None = None

        if auth and auth.lower().startswith("bearer ") and self.jwt_key_store:
            token = auth.split(" ", 1)[1]
            try:
                payload = verify_jwt(
                    token, self.jwt_key_store, audience=self.audience, issuer=self.issuer
                )
            except JWTError as e:
                logger.warning("jwt validation failed: %s", e.code)
                audit_log.record(
                    "auth.deny", {"code": e.code, "auth_type": "jwt"}, {"principal": {}}
                )
                return JSONResponse(status_code=401, content={"code": e.code, "detail": e.detail})
            principal = {
                "sub": payload.get("sub"),
                "tenant_id": payload.get("tenant") or payload.get("tenant_id"),
                "scopes": payload.get("scopes", []),
                "auth": "jwt",
            }
        elif api_key:
            entry = self.api_key_store.find_key(api_key)
            if not entry:
                matched = self.api_key_store.match_key(api_key)
                code = "key_revoked" if matched else "invalid_api_key"
                logger.warning("api key rejected")
                audit_log.record(
                    "auth.deny", {"code": code, "auth_type": "api_key"}, {"principal": {}}
                )
                return JSONResponse(
                    status_code=401,
                    content={"code": code, "detail": "invalid API key"},
                )
            principal = {
                "key_id": entry.id,
                "tenant_id": entry.tenant_id,
                "scopes": list(entry.scopes),
                "auth": "api_key",
            }
        else:
            audit_log.record("auth.deny", {"code": "missing_api_key"}, {"principal": {}})
            return JSONResponse(
                status_code=401,
                content={"code": "missing_api_key", "detail": "missing credentials"},
            )

        # scope enforcement
        required = self.scope_map.get(path, set())
        if required and not set(principal.get("scopes", [])).issuperset(required):
            audit_log.record(
                "auth.deny",
                {"code": "insufficient_scope", "required": list(required)},
                {"principal": principal},
            )
            return JSONResponse(
                status_code=403,
                content={"code": "insufficient_scope", "detail": "insufficient scope"},
            )

        # rate limiting per tenant
        if self.rate_limit:
            window, max_requests = self.rate_limit
            tenant = str(principal.get("tenant_id") or principal.get("key_id") or "global")
            now = self._time()
            start, count = self._counters.get(tenant, (now, 0))
            if now - start >= window:
                start, count = now, 0
            if count >= max_requests:
                audit_log.record(
                    "auth.deny", {"code": "rate_limited"}, {"principal": principal}
                )
                return JSONResponse(
                    status_code=429,
                    content={"code": "rate_limited", "detail": "rate limit exceeded"},
                )
            self._counters[tenant] = (start, count + 1)

        request.state.principal = {
            k: v for k, v in principal.items() if k != "auth" and v is not None
        }
        audit_log.record(
            "auth.login",
            {"auth_type": principal.get("auth"), "key_id": principal.get("key_id")},
            {"principal": request.state.principal},
        )
        return await call_next(request)


__all__ = ["AuthMiddleware"]
