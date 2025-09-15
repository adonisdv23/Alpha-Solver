import hashlib
import time
from typing import Callable, Iterable, Tuple


class OAuthError(Exception):
    """Represents an OAuth related error."""

    def __init__(self, code: str, detail: str | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.detail = detail or ""


class OAuthClient:
    """Simulated OAuth client supporting two flows.

    The client does not perform any network operations. Instead it
    deterministically generates tokens based on the input parameters. This
    allows tests to run quickly and without external dependencies.
    """

    def __init__(self, clock: Callable[[], float] | None = None) -> None:
        self._clock = clock or time.time

    # ------------------------------------------------------------------
    # internal helpers
    def _scope_hash(self, scopes: Iterable[str]) -> str:
        joined = " ".join(sorted(scopes))
        return hashlib.sha1(joined.encode()).hexdigest()[:8]

    def _expiry(self, provider: str, tenant: str, scope_hash: str) -> int:
        base = hashlib.sha256(f"{provider}:{tenant}:{scope_hash}".encode()).hexdigest()
        rnd = int(base, 16) % 180  # 0-179
        return int(self._clock() + 120 + rnd)  # 120-299s

    # ------------------------------------------------------------------
    def fetch_token(
        self,
        flow: str,
        provider: str,
        tenant_id: str,
        scopes: Iterable[str],
        secret: dict,
    ) -> Tuple[str, int]:
        """Return (access_token, expires_at) or raise :class:`OAuthError`.

        ``flow`` must be either ``client_credentials`` or ``refresh_token``.
        ``secret`` is a mapping containing ``client_secret`` and optionally
        ``refresh_token``. To simulate invalid credentials any secret value
        starting with ``"invalid"`` triggers an error.
        """

        if flow not in {"client_credentials", "refresh_token"}:
            raise OAuthError("unsupported_flow")

        if flow == "client_credentials":
            if secret.get("client_secret", "").startswith("invalid"):
                raise OAuthError("invalid_client", "bad client secret")
        elif flow == "refresh_token":
            rt = secret.get("refresh_token")
            if not rt or rt.startswith("invalid"):
                raise OAuthError("invalid_grant", "bad refresh token")

        scope_hash = self._scope_hash(scopes)
        exp = self._expiry(provider, tenant_id, scope_hash)
        token = f"tok_{provider}_{tenant_id}_{scope_hash}_{exp}"
        return token, exp


__all__ = ["OAuthClient", "OAuthError"]
