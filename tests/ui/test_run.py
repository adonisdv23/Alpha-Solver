import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI
from fastapi.testclient import TestClient

from alpha.webapp.routes import run as run_route


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(run_route.router)
    return app


def test_run_page_renders_quickly_and_has_button():
    run_route.reset_state()
    app = create_app()
    with TestClient(app) as client:
        start = time.perf_counter()
        response = client.get("/run")
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        assert response.status_code == 200
        html = response.text
        assert "<button" in html
        assert "Run Demo" in html
        assert "demo-latency" in html
        assert "demo-cache" in html
        assert elapsed_ms < 2000


def test_demo_run_roundtrip_and_cache_behavior():
    run_route.reset_state()
    app = create_app()
    with TestClient(app) as client:
        first_response = client.post("/run", json={"trigger": "demo"})
        assert first_response.status_code == 200

        first_payload = first_response.json()
        assert first_payload["cache_hit"] is False
        assert isinstance(first_payload["latency_ms"], float)
        assert first_payload["latency_ms"] >= 80.0
        assert "Alpha Solver" in first_payload["result"]
        assert "Highlights" in first_payload["result"]

        second_response = client.post("/run", json={"trigger": "demo"})
        assert second_response.status_code == 200

        second_payload = second_response.json()
        assert second_payload["cache_hit"] is True
        assert second_payload["result"] == first_payload["result"]
        assert isinstance(second_payload["latency_ms"], float)
        assert second_payload["latency_ms"] > 0
        assert second_payload["latency_ms"] < first_payload["latency_ms"]
