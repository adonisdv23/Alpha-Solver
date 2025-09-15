from __future__ import annotations

import threading
import time
from typing import Callable, Iterable, Tuple

from .oauth_client import OAuthClient, OAuthError
from .secret_store import SecretStore


class TokenError(Exception):
    def __init__(self, code: str, detail: str | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.detail = detail or ""


class TokenProvider:
    """High level token provider with caching and refresh logic."""

    def __init__(
        self,
        oauth_client: OAuthClient,
        secret_store: SecretStore,
        config: dict,
        clock: Callable[[], float] | None = None,
    ) -> None:
        self._client = oauth_client
        self._secrets = secret_store
        self._config = config
        self._clock = clock or time.time
        self._cache: dict[Tuple[str, str, Tuple[str, ...]], dict] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    def get_token(self, provider: str, tenant_id: str, scopes: Iterable[str]) -> str:
        cfg = self._config.get("providers", {}).get(provider)
        if not cfg:
            raise TokenError("invalid_provider", f"unknown provider {provider}")
        for s in scopes:
            if s not in cfg.get("scopes", []):
                raise TokenError("invalid_scope", s)
        scopes_key = tuple(sorted(scopes))
        key = (provider, tenant_id, scopes_key)
        now = self._clock()
        with self._lock:
            entry = self._cache.get(key)
            if entry and now + cfg.get("prefetch_jitter_s", 0) < entry["expires_at"]:
                return entry["access_token"]
        # Need to fetch/refresh
        secret = self._secrets.get(provider, tenant_id)
        flow = "client_credentials"
        if entry:
            # token exists but is expiring/expired
            if secret.get("refresh_token"):
                flow = "refresh_token"
            else:
                raise TokenError("invalid_grant", "missing refresh token")
        token, exp = self._client.fetch_token(flow, provider, tenant_id, scopes_key, secret)
        with self._lock:
            self._cache[key] = {"access_token": token, "expires_at": exp}
        return token


__all__ = ["TokenProvider", "TokenError"]
