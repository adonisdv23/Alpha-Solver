import sys
import time
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2]))
from alpha.api.health import app


client = TestClient(app)


def test_health_endpoint_returns_statuses_fast():
    start = time.perf_counter()
    res = client.get("/health")
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert res.status_code == 200
    data = res.json()
    # expected keys
    assert {"app", "redis", "vectordb", "provider", "ts"} <= data.keys()
    assert data["app"] == "ok"
    for key in ("redis", "vectordb", "provider"):
        assert data[key] in {"ok", "down"}
    assert isinstance(data["ts"], float)
    assert elapsed_ms < 50
