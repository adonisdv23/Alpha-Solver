import logging

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from service.auth.oauth_client import OAuthClient
from service.auth.secret_store import SecretStore
from service.auth.token_provider import TokenProvider
from service.middleware.secret_middleware import SecretMiddleware


def build_app():
    provider_cfg = {
        "providers": {
            "default": {
                "prefetch_jitter_s": 30,
                "scopes": ["web.read"],
            }
        }
    }
    secrets = {
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
    store = SecretStore(data=secrets)
    client = OAuthClient()
    tp = TokenProvider(client, store, provider_cfg)

    app = FastAPI()
    app.add_middleware(
        SecretMiddleware,
        token_provider=tp,
        provider="default",
        tenant_id="tenantA",
        scopes=["web.read"],
        path_prefix="/needs-token",
    )

    @app.get("/needs-token")
    async def needs_token(request: Request):
        return {"auth": request.headers.get("authorization")}

    return app


def test_middleware_attaches_bearer_and_no_secret_logs(caplog):
    caplog.set_level(logging.INFO)
    app = build_app()
    client = TestClient(app)
    resp = client.get("/needs-token")
    assert resp.status_code == 200
    assert resp.json()["auth"].startswith("Bearer tok_")
    # ensure no secrets in logs
    for rec in caplog.records:
        msg = rec.getMessage()
        assert "secretA" not in msg
        assert "refreshA" not in msg
