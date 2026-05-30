import asyncio
from types import SimpleNamespace

from fastapi import FastAPI

from service import health as health_mod


def test_service_healthcheck_uses_current_local_probe_schema(monkeypatch):
    async def ok() -> bool:
        return True

    monkeypatch.setattr(health_mod, "probe_adapter_registry", ok)
    monkeypatch.setattr(health_mod, "probe_model_provider", ok)

    app = FastAPI()
    app.state.config = SimpleNamespace(version="test-version")
    app.state.start_time = health_mod.START_TIME

    payload = asyncio.run(health_mod.healthcheck(app))

    assert payload["status"] == "ok"
    assert payload["version"] == "test-version"
    assert set(payload["deps"]) == {"adapter_registry", "model_provider"}
    assert "redis" not in payload["deps"]
    assert "vectordb" not in payload["deps"]
    assert "provider" not in payload["deps"]


def test_service_healthcheck_reports_error_for_current_probe_failure(monkeypatch):
    async def ok() -> bool:
        return True

    async def failed() -> bool:
        return False

    monkeypatch.setattr(health_mod, "probe_adapter_registry", failed)
    monkeypatch.setattr(health_mod, "probe_model_provider", ok)

    app = FastAPI()
    app.state.config = SimpleNamespace(version="test-version")
    app.state.start_time = health_mod.START_TIME

    payload = asyncio.run(health_mod.healthcheck(app))

    assert payload["status"] == "error"
    assert payload["deps"] == {"adapter_registry": False, "model_provider": True}
