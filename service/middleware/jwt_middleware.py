import logging
from typing import Iterable, Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from service.auth.jwt_utils import AuthKeyStore, JWTError, verify_jwt

logger = logging.getLogger("service.middleware.jwt")


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Middleware that enforces JWT authentication on incoming requests."""

    def __init__(
        self,
        app,
        key_store: AuthKeyStore,
        audience: str | None = None,
        issuer: str | None = None,
        exempt_paths: Optional[Iterable[str]] = None,
    ) -> None:
        super().__init__(app)
        self.key_store = key_store
        self.audience = audience
        self.issuer = issuer
        self.exempt_paths = set(exempt_paths or [])

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exempt_paths:
            return await call_next(request)

        auth = request.headers.get("authorization")
        if not auth or not auth.lower().startswith("bearer "):
            return JSONResponse(
                status_code=401,
                content={"code": "missing_token", "detail": "Authorization header missing"},
            )
        token = auth.split(" ", 1)[1]
        try:
            payload = verify_jwt(
                token,
                self.key_store,
                audience=self.audience,
                issuer=self.issuer,
            )
        except JWTError as e:  # pragma: no cover - trivial
            logger.warning("jwt validation failed: %s", e.code)
            return JSONResponse(status_code=401, content={"code": e.code, "detail": e.detail})

        request.state.principal = {
            "sub": payload.get("sub"),
            "tenant_id": payload.get("tenant") or payload.get("tenant_id"),
            "roles": payload.get("roles", []),
        }
        return await call_next(request)


__all__ = ["JWTAuthMiddleware"]
