import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI
from fastapi.testclient import TestClient

from alpha.webapp.routes import requests as request_routes


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(request_routes.router)
    return app


def test_request_submission_flow():
    request_routes.reset_state()
    app = create_app()
    with TestClient(app) as client:
        # Verify the form renders with the expected controls.
        form_response = client.get("/requests")
        assert form_response.status_code == 200
        html = form_response.text
        assert "<textarea" in html
        assert "<select" in html

        # Submit a job and ensure the acknowledgement arrives within the SLA.
        start = time.perf_counter()
        submit_response = client.post(
            "/requests",
            json={"prompt": "demo prompt", "provider": request_routes.AVAILABLE_PROVIDERS[0]},
        )
        ack_latency_ms = (time.perf_counter() - start) * 1000
        assert submit_response.status_code == 200
        job_id = submit_response.json()["id"]
        assert isinstance(job_id, str) and job_id
        assert ack_latency_ms < 500

        # Poll until the request is marked done.
        deadline = time.perf_counter() + 5.0
        final_payload = None
        while time.perf_counter() < deadline:
            status_response = client.get(f"/requests/{job_id}")
            assert status_response.status_code == 200
            final_payload = status_response.json()
            if final_payload["status"] == "done":
                break
            time.sleep(0.05)
        assert final_payload is not None, "no status response recorded"
        assert final_payload["status"] == "done"
        assert final_payload["id"] == job_id
        assert final_payload["provider"] == request_routes.AVAILABLE_PROVIDERS[0]
        assert final_payload["cache_hit"] is False
        assert isinstance(final_payload["latency_ms"], float)
        assert final_payload["latency_ms"] >= 0
