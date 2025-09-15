import sys
import time
from pathlib import Path

try:
    from fakeredis import FakeRedis
except Exception:  # pragma: no cover - fallback
    class FakeRedis:  # minimal stub
        def ping(self):
            return True

sys.path.append(str(Path(__file__).resolve().parents[2]))
from alpha.api.health import get_health


def test_health_with_redis_and_flags():
    client = FakeRedis()
    start = time.perf_counter()
    data = get_health(client, vectordb_ok=True, provider_ok=True)
    assert (time.perf_counter() - start) * 1000 < 50
    assert data["app"] == "ok"
    assert data["redis"] == "ok"
    assert data["vectordb"] == "ok"
    assert data["provider"] == "ok"
    assert "ts" in data


def test_health_defaults_down():
    data = get_health()
    assert data["redis"] == "down"
    assert data["vectordb"] == "down"
    assert data["provider"] == "down"
    assert data["app"] == "ok"
    assert "ts" in data
