from fastapi.testclient import TestClient

from service.app import app

client = TestClient(app)

def test_health():
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_ready_toggle():
    app.state.ready = True
    res = client.get("/readyz")
    assert res.status_code == 200
    app.state.ready = False
    res = client.get("/readyz")
    assert res.status_code == 503
    app.state.ready = True
