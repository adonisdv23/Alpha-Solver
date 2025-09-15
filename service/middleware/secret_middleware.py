from __future__ import annotations

from typing import Iterable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from service.auth.token_provider import TokenProvider


class SecretMiddleware(BaseHTTPMiddleware):
    """Attach OAuth bearer tokens for protected routes.

    The middleware is intentionally small; it only injects an Authorization
    header for paths matching ``path_prefix``. No secrets are logged.
    """

    def __init__(
        self,
        app,
        token_provider: TokenProvider,
        provider: str,
        tenant_id: str,
        scopes: Iterable[str],
        path_prefix: str = "/",
    ) -> None:
        super().__init__(app)
        self._tp = token_provider
        self._provider = provider
        self._tenant = tenant_id
        self._scopes = tuple(scopes)
        self._prefix = path_prefix

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(self._prefix):
            token = self._tp.get_token(self._provider, self._tenant, self._scopes)
            headers = list(request.scope.get("headers", []))
            headers.append((b"authorization", f"Bearer {token}".encode()))
            request.scope["headers"] = headers
        response = await call_next(request)
        return response


__all__ = ["SecretMiddleware"]
