import logging

from service.auth.secret_store import SecretStore


def make_store():
    data = {
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
    return SecretStore(data=data)


def test_rotation_and_rollback():
    store = make_store()
    s1 = store.get("default", "tenantA")
    assert s1["client_secret"] == "secretA"
    store.set(
        "default",
        "tenantA",
        {
            "version": "v2",
            "client_id": "id2",
            "client_secret": "secretB",
            "refresh_token": "refreshB",
            "kid": "kid-002",
        },
    )
    s2 = store.get("default", "tenantA")
    assert s2["client_secret"] == "secretB"
    old = store.get("default", "tenantA", version="v1")
    assert old["client_secret"] == "secretA"
    store.rollback("default", "tenantA")
    again = store.get("default", "tenantA")
    assert again["client_secret"] == "secretA"


def test_repr_redacts_secrets():
    store = make_store()
    rep = repr(store)
    assert "secretA" not in rep
    assert "refreshA" not in rep
