import time
import pytest

from service.auth.oauth_client import OAuthClient, OAuthError
from service.auth.secret_store import SecretStore
from service.auth.token_provider import TokenProvider, TokenError


def build_provider(clock):
    provider_cfg = {
        "providers": {
            "default": {
                "flows": ["client_credentials", "refresh_token"],
                "cache_ttl_s": 300,
                "prefetch_jitter_s": 30,
                "scopes": ["web.read"],
            }
        }
    }
    secrets_data = {
        "secrets": [
            {
                "provider": "default",
                "tenant_id": "tenantA",
                "version": "v1",
                "client_id": "id1",
                "client_secret": "secretA",
                "refresh_token": "refreshA",
                "kid": "kid-001",
            }
        ]
    }
    store = SecretStore(data=secrets_data)
    client = OAuthClient(clock=clock)
    return TokenProvider(client, store, provider_cfg, clock=clock)


def test_cache_and_prefetch():
    now = [1000.0]
    clock = lambda: now[0]
    tp = build_provider(clock)
    start = time.perf_counter()
    tok1 = tp.get_token("default", "tenantA", ["web.read"])
    miss = time.perf_counter() - start
    assert miss < 0.6
    start = time.perf_counter()
    tok2 = tp.get_token("default", "tenantA", ["web.read"])
    hit = time.perf_counter() - start
    assert hit < 0.1
    assert tok1 == tok2
    exp = int(tok1.split("_")[-1])
    now[0] = exp - 29  # jitter =30 -> trigger refresh
    tok3 = tp.get_token("default", "tenantA", ["web.read"])
    assert tok3 != tok1


def test_invalid_scope_and_creds():
    now = [1000.0]
    clock = lambda: now[0]
    tp = build_provider(clock)
    with pytest.raises(TokenError) as exc:
        tp.get_token("default", "tenantA", ["bad.scope"])
    assert exc.value.code == "invalid_scope"

    secrets_bad = {
        "secrets": [
            {
                "provider": "default",
                "tenant_id": "bad",
                "version": "v1",
                "client_id": "id",
                "client_secret": "invalid-secret",
                "refresh_token": "refreshA",
                "kid": "kid-001",
            }
        ]
    }
    store_bad = SecretStore(data=secrets_bad)
    client = OAuthClient(clock=clock)
    tp_bad = TokenProvider(client, store_bad, {"providers": {"default": {"scopes": ["web.read"], "prefetch_jitter_s": 30}}}, clock=clock)
    failures = 0
    for _ in range(50):
        try:
            tp_bad.get_token("default", "bad", ["web.read"])
        except OAuthError:
            failures += 1
    assert failures >= 49


def test_refresh_flow():
    now = [1000.0]
    clock = lambda: now[0]
    tp = build_provider(clock)
    tok1 = tp.get_token("default", "tenantA", ["web.read"])
    exp = int(tok1.split("_")[-1])
    now[0] = exp + 1
    tok2 = tp.get_token("default", "tenantA", ["web.read"])
    assert tok2 != tok1

    # missing refresh token
    secrets_no = {
        "secrets": [
            {
                "provider": "default",
                "tenant_id": "t2",
                "version": "v1",
                "client_id": "id",
                "client_secret": "secretA",
                "kid": "kid-003",
            }
        ]
    }
    store_no = SecretStore(data=secrets_no)
    client = OAuthClient(clock=clock)
    tp_no = TokenProvider(client, store_no, {"providers": {"default": {"scopes": ["web.read"], "prefetch_jitter_s": 30}}}, clock=clock)
    tok = tp_no.get_token("default", "t2", ["web.read"])
    exp2 = int(tok.split("_")[-1])
    now[0] = exp2 + 1
    with pytest.raises(TokenError) as exc:
        tp_no.get_token("default", "t2", ["web.read"])
    assert exc.value.code == "invalid_grant"
