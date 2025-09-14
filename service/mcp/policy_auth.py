from __future__ import annotations

"""Minimal auth helpers for MCP policies.

This module provides a small token provider abstraction with several strategies
used in tests.  All providers expose a :class:`TokenProvider` interface with a
``get_token`` method, ``expires_at`` timestamp and ``valid`` method.  The
implementation deliberately avoids any real network calls; the OAuth client
credentials strategy simulates token fetching with deterministic values.
"""

import os
import time
from typing import Any, Callable, Dict, List, Optional


class AuthError(Exception):
    """Raised when authentication prerequisites are not met."""


# ---------------------------------------------------------------------------
# Policy guards
# ---------------------------------------------------------------------------

def deny_if_missing_env(vars: List[str]) -> None:
    """Ensure all environment variables exist or raise :class:`AuthError`."""

    missing = [v for v in vars if v not in os.environ]
    if missing:
        raise AuthError(f"missing env vars: {', '.join(missing)}")


def validate_allowlist(name: str, allow: List[str]) -> bool:
    """Return ``True`` if *name* is present in the allowlist."""

    return name in allow


def _redact_key(key: str) -> bool:
    k = key.lower()
    return "token" in k or "secret" in k or "authorization" in k


def redact_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``data`` with token-like fields redacted."""

    redacted: Dict[str, Any] = {}
    for k, v in data.items():
        if isinstance(v, dict):
            redacted[k] = redact_dict(v)
        else:
            redacted[k] = "***" if _redact_key(k) else v
    return redacted


# ---------------------------------------------------------------------------
# Token providers
# ---------------------------------------------------------------------------


class TokenProvider:
    """Base token provider interface."""

    auth_method: str = ""

    _token: Optional[str] = None
    _expires_at: Optional[float] = None

    def get_token(self) -> str:  # pragma: no cover - interface method
        raise NotImplementedError

    # expiry ---------------------------------------------------------------
    @property
    def expires_at(self) -> Optional[float]:
        return self._expires_at

    def valid(self) -> bool:
        if self._expires_at is None:
            return True
        return time.time() < self._expires_at

    # ------------------------------------------------------------------
    def to_route_explain(self) -> Dict[str, Any]:
        """Return minimal, redacted metadata for routing/explanation."""

        return {"auth_method": self.auth_method, "redacted": True}


class StaticToken(TokenProvider):
    """Token provider that reads a static token from an environment variable."""

    def __init__(self, name: str, env: str):
        self.name = name
        self.env = env
        self.auth_method = "static"
        deny_if_missing_env([env])
        self._token = os.environ[env]
        self._expires_at = None

    def get_token(self) -> str:
        return self._token


class BearerToken(TokenProvider):
    """Token provider using an arbitrary callable to supply a bearer token."""

    def __init__(self, getter: Callable[[], str]):
        self.getter = getter
        self.auth_method = "bearer"
        self._expires_at = None

    def get_token(self) -> str:
        if self._token is None:
            self._token = self.getter()
        return self._token


class OAuthClientCredentials(TokenProvider):
    """Simulated OAuth2 client-credentials flow.

    No network requests are made.  Instead, a deterministic token is generated
    whenever a refresh is required.  Each refresh increments an internal
    counter to produce a new token value and sets the expiry one minute ahead.
    """

    def __init__(
        self,
        token_url: str,
        client_id_env: str,
        client_secret_env: str,
        scope: Optional[str] = None,
    ):
        self.token_url = token_url
        self.client_id_env = client_id_env
        self.client_secret_env = client_secret_env
        self.scope = scope
        self.auth_method = "oauth_cc"

        deny_if_missing_env([client_id_env, client_secret_env])
        self.client_id = os.environ[client_id_env]
        self.client_secret = os.environ[client_secret_env]

        self._counter = 0
        self._token = None
        self._expires_at = None

    def _refresh(self) -> None:
        self._counter += 1
        # deterministic token and expiry
        self._token = f"oauth-token-{self._counter}"
        self._expires_at = time.time() + 60  # 1 minute from now

    def get_token(self) -> str:
        if not self.valid() or self._token is None:
            self._refresh()
        return self._token


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def attach_auth_headers(req: Dict[str, Any], provider: TokenProvider) -> Dict[str, Any]:
    """Return a new request dictionary with the auth header attached."""

    token = provider.get_token()
    header = f"Bearer {token}"
    if provider.auth_method == "static":
        header = f"Token {token}"
    new_req = dict(req)
    new_req["Authorization"] = header
    return new_req


__all__ = [
    "AuthError",
    "deny_if_missing_env",
    "validate_allowlist",
    "TokenProvider",
    "StaticToken",
    "BearerToken",
    "OAuthClientCredentials",
    "attach_auth_headers",
    "redact_dict",
]
