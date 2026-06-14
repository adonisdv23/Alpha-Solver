import logging
import random
import time
from pathlib import Path

import yaml
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from service.auth.api_keys import APIKeyStore, hash_key
from service.middleware.auth_middleware import AuthMiddleware


def build_app(tmp_path: Path, scope_map=None, rate_limit=None, time_func=None):
    k1 = "key-full"
    k2 = "key-disabled"
    k3 = "key-read"
    data = {
        "keys": [
            {
                "id": "k1",
                "hash": hash_key(k1),
                "tenant_id": "t1",
                "scopes": ["read", "write"],
                "status": "active",
                "created_at": 0,
            },
            {
                "id": "k2",
                "hash": hash_key(k2),
                "tenant_id": "t1",
                "scopes": ["read"],
                "status": "disabled",
                "created_at": 0,
            },
            {
                "id": "k3",
                "hash": hash_key(k3),
                "tenant_id": "t1",
                "scopes": ["read"],
                "status": "active",
                "created_at": 0,
            },
        ]
    }
    path = tmp_path / "api_keys.yaml"
    path.write_text(yaml.safe_dump(data))
    store = APIKeyStore(path)
    app = FastAPI()
    app.add_middleware(
        AuthMiddleware,
        api_key_store=store,
        scope_map=scope_map or {},
        rate_limit=rate_limit,
        time_func=time_func or time.time,
    )

    @app.get("/protected")
    async def protected(request: Request):
        return request.state.principal

    return app, store, path, {"full": k1, "disabled": k2, "read": k3}


def test_valid_api_key(tmp_path):
    app, _store, _path, keys = build_app(tmp_path)
    client = TestClient(app)
    r = client.get("/protected", headers={"X-API-Key": keys["full"]})
    assert r.status_code == 200
    assert r.json()["tenant_id"] == "t1"
    assert r.json()["key_id"] == "k1"


def test_invalid_and_disabled_key(tmp_path):
    app, _store, _path, keys = build_app(tmp_path)
    client = TestClient(app)
    r = client.get("/protected", headers={"X-API-Key": "bad"})
    assert r.status_code == 401
    assert r.json()["code"] == "invalid_api_key"
    r = client.get("/protected", headers={"X-API-Key": keys["disabled"]})
    assert r.status_code == 401
    assert r.json()["code"] == "key_revoked"


def test_scope_enforcement(tmp_path):
    app, _store, _path, keys = build_app(tmp_path, scope_map={"/protected": ["write"]})
    client = TestClient(app)
    r = client.get("/protected", headers={"X-API-Key": keys["read"]})
    assert r.status_code == 403
    assert r.json()["code"] == "insufficient_scope"


def test_revocation(tmp_path):
    app, store, path, keys = build_app(tmp_path)
    client = TestClient(app)
    r = client.get("/protected", headers={"X-API-Key": keys["full"]})
    assert r.status_code == 200
    data = yaml.safe_load(path.read_text())
    for item in data["keys"]:
        if item["id"] == "k1":
            item["status"] = "revoked"
    path.write_text(yaml.safe_dump(data))
    r = client.get("/protected", headers={"X-API-Key": keys["full"]})
    assert r.status_code == 401
    assert r.json()["code"] == "key_revoked"


def test_rate_limit(tmp_path):
    now = [0.0]

    def _time():
        return now[0]

    app, _store, _path, keys = build_app(
        tmp_path, rate_limit=(60, 2), time_func=_time
    )
    client = TestClient(app)
    headers = {"X-API-Key": keys["full"]}
    for _ in range(2):
        assert client.get("/protected", headers=headers).status_code == 200
        now[0] += 1
    r = client.get("/protected", headers=headers)
    assert r.status_code == 429
    now[0] += 61
    assert client.get("/protected", headers=headers).status_code == 200


def test_rejection_rate(tmp_path):
    app, _store, _path, _keys = build_app(tmp_path)
    client = TestClient(app)
    bad = ["bad1", "bad2", None]
    rejected = 0
    for _ in range(100):
        val = random.choice(bad)
        headers = {"X-API-Key": val} if val else {}
        r = client.get("/protected", headers=headers)
        if r.status_code == 401:
            rejected += 1
    assert rejected >= 95


def test_no_secret_in_logs(tmp_path, caplog):
    app, _store, _path, keys = build_app(tmp_path)
    client = TestClient(app)
    bad = "bad-secret"
    with caplog.at_level(logging.WARNING, logger="service.middleware.auth"):
        client.get("/protected", headers={"X-API-Key": bad})
    assert bad not in caplog.text
    assert "api key rejected" in caplog.text
