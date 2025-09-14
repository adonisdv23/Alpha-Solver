import os
import time

import pytest

from service.mcp.policy_auth import (
    AuthError,
    StaticToken,
    BearerToken,
    OAuthClientCredentials,
    attach_auth_headers,
    deny_if_missing_env,
    validate_allowlist,
)


def test_static_bearer_headers(monkeypatch):
    monkeypatch.setenv("STATIC_TOKEN", "static-secret")
    static = StaticToken("svc", "STATIC_TOKEN")
    req = attach_auth_headers({}, static)
    assert req["Authorization"] == "Token static-secret"
    assert static.valid()
    assert static.expires_at is None

    bearer = BearerToken(lambda: "bear")
    req2 = attach_auth_headers({}, bearer)
    assert req2["Authorization"] == "Bearer bear"


def test_oauth_cc_refresh_and_headers(monkeypatch):
    monkeypatch.setenv("CLIENT_ID", "id")
    monkeypatch.setenv("CLIENT_SECRET", "sec")
    provider = OAuthClientCredentials("https://example/token", "CLIENT_ID", "CLIENT_SECRET")

    req = attach_auth_headers({}, provider)
    assert req["Authorization"] == "Bearer oauth-token-1"

    # force expiry
    provider._expires_at = time.time() - 1
    req2 = attach_auth_headers({}, provider)
    assert req2["Authorization"] == "Bearer oauth-token-2"
    assert provider.valid()


def test_missing_env_raises_autherror(monkeypatch):
    if "MISSING" in os.environ:
        del os.environ["MISSING"]
    with pytest.raises(AuthError):
        deny_if_missing_env(["MISSING"])


def test_redaction_in_route_explain(monkeypatch):
    monkeypatch.setenv("STATIC_TOKEN", "s3cr3t")
    static = StaticToken("svc", "STATIC_TOKEN")
    expl = static.to_route_explain()
    assert expl == {"auth_method": "static", "redacted": True}


def test_allowlist_policy():
    allow = ["a", "b"]
    assert validate_allowlist("a", allow)
    assert not validate_allowlist("c", allow)


def test_no_secret_values_in_logs(monkeypatch, capsys):
    monkeypatch.setenv("STATIC_TOKEN", "shh")
    static = StaticToken("svc", "STATIC_TOKEN")

    captured = []

    def fake_print(*args, **kwargs):
        captured.append(" ".join(str(a) for a in args))

    monkeypatch.setattr("builtins.print", fake_print)
    attach_auth_headers({}, static)
    # our code never prints, so captured should be empty
    assert not captured
