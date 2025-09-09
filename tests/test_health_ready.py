from fastapi.testclient import TestClient
from service.app import app


def test_health_and_ready():
    client = TestClient(app)
    r = client.get("/healthz")
    assert r.status_code == 200
    app.state.ready = False
    r = client.get("/readyz")
    assert r.status_code == 503
    app.state.ready = True
    r = client.get("/readyz")
    assert r.status_code == 200
