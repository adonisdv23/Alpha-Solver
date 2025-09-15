import time

from fastapi.testclient import TestClient

from service.app import app
from service import health as health_mod

client = TestClient(app)


def _assert_fast_and_payload(path: str) -> None:
    start = time.perf_counter()
    res = client.get(path)
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert res.status_code == 200
    assert elapsed_ms < 100
    data = res.json()
    # Basic payload structure
    assert {"status", "version", "uptime_s", "deps"} <= data.keys()
    assert {"adapter_registry", "model_provider"} <= data["deps"].keys()


def test_health_and_ready_ok():
    _assert_fast_and_payload("/health")
    _assert_fast_and_payload("/ready")


def test_ready_dependency_failure(monkeypatch):
    async def fail_registry() -> bool:
        return False

    monkeypatch.setattr(health_mod, "probe_adapter_registry", fail_registry)
    res = client.get("/ready")
    assert res.status_code == 503
    data = res.json()
    assert data["deps"]["adapter_registry"] is False
