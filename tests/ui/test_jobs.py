from __future__ import annotations

import re
import sys
import time
from pathlib import Path
from typing import Iterable

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from alpha.webapp.routes import jobs as jobs_routes  # noqa: E402
from alpha.webapp.routes import requests as request_routes  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_jobs_state():
    request_routes.reset_state()
    yield
    request_routes.reset_state()


@pytest.fixture()
def client() -> Iterable[TestClient]:
    app = FastAPI()
    app.include_router(jobs_routes.router)
    client = TestClient(app)
    try:
        yield client
    finally:
        client.close()


def _record_job(
    job_id: str,
    *,
    provider: str = "mock",
    status: str = "done",
    latency_ms: float | None = None,
    cache_hit: bool = False,
    submitted_at: float,
) -> None:
    job = request_routes.RequestJob(
        id=job_id,
        prompt="demo",
        provider=provider,
        status=status,
        latency_ms=latency_ms,
        cache_hit=cache_hit,
        submitted_at=submitted_at,
    )
    job.started_at = submitted_at + 0.001
    if latency_ms is not None:
        job.completed_at = job.started_at + latency_ms / 1000.0
    with request_routes._JOBS_LOCK:
        request_routes._JOBS[job_id] = job


def _extract_row_ids(html: str) -> list[str]:
    return re.findall(r'data-job-id="([^"]+)"', html)


def test_jobs_page_limits_to_100_rows_and_fast(client: TestClient) -> None:
    base = 1_000.0
    for index in range(120):
        latency = 25.0 + index if index % 7 else None
        status = "done" if index % 3 == 0 else ("failed" if index % 3 == 1 else "pending")
        cache_hit = index % 2 == 0
        provider = "mock" if index % 2 == 0 else "mock-pro"
        _record_job(
            f"job-{index:03d}",
            provider=provider,
            status=status,
            latency_ms=latency,
            cache_hit=cache_hit,
            submitted_at=base + index,
        )

    start = time.perf_counter()
    response = client.get("/jobs")
    elapsed = time.perf_counter() - start
    assert response.status_code == 200
    assert elapsed < 2.0

    html = response.text
    assert "<th scope=\"col\">Job ID</th>" in html
    assert "<th scope=\"col\">Provider</th>" in html

    rows = _extract_row_ids(html)
    assert len(rows) == 100
    assert rows[0] == "job-119"
    assert rows[-1] == "job-020"


def test_jobs_page_default_sort_is_time_desc(client: TestClient) -> None:
    _record_job("alpha", submitted_at=100.0)
    _record_job("bravo", submitted_at=200.0)
    _record_job("charlie", submitted_at=150.0)

    response = client.get("/jobs")
    assert response.status_code == 200
    html = response.text
    assert "Time ↓" in html
    assert "Latency ↕" in html
    assert _extract_row_ids(html)[:3] == ["bravo", "charlie", "alpha"]


def test_jobs_page_time_sort_ascending(client: TestClient) -> None:
    _record_job("early", submitted_at=50.0)
    _record_job("mid", submitted_at=75.0)
    _record_job("late", submitted_at=100.0)

    response = client.get("/jobs?sort=time&direction=asc")
    assert response.status_code == 200
    html = response.text
    assert _extract_row_ids(html)[:3] == ["early", "mid", "late"]
    assert "Time ↑" in html
    assert "sort=time&direction=desc" in html


def test_jobs_page_latency_sort_desc_places_missing_last(client: TestClient) -> None:
    _record_job("slow", submitted_at=10.0, latency_ms=120.0)
    _record_job("fast", submitted_at=20.0, latency_ms=45.0)
    _record_job("pending", submitted_at=30.0, latency_ms=None, status="running")

    response = client.get("/jobs?sort=latency&direction=desc")
    assert response.status_code == 200
    html = response.text
    rows = _extract_row_ids(html)
    assert rows == ["slow", "fast", "pending"]
    assert "Latency ↓" in html
    assert "sort=latency&direction=asc" in html


def test_jobs_page_latency_sort_ascending(client: TestClient) -> None:
    _record_job("fast", submitted_at=10.0, latency_ms=20.0)
    _record_job("medium", submitted_at=20.0, latency_ms=65.0)
    _record_job("slow", submitted_at=30.0, latency_ms=100.0)
    _record_job("pending", submitted_at=40.0, latency_ms=None, status="queued")

    response = client.get("/jobs?sort=latency&direction=asc")
    assert response.status_code == 200
    rows = _extract_row_ids(response.text)
    assert rows == ["fast", "medium", "slow", "pending"]


def test_jobs_status_summary_counts(client: TestClient) -> None:
    _record_job("done-1", submitted_at=1.0, status="done")
    _record_job("done-2", submitted_at=2.0, status="done")
    _record_job("pending", submitted_at=3.0, status="pending")
    _record_job("failed", submitted_at=4.0, status="failed")

    html = client.get("/jobs").text
    summary_pairs = re.findall(
        r'data-status="([^"]+)"><span class="status-label">[^<]+</span><span class="status-count">(\d+)</span>',
        html,
    )
    summary = {status: int(count) for status, count in summary_pairs}
    assert summary == {"done": 2, "failed": 1, "pending": 1}


def test_jobs_row_links_to_detail_page(client: TestClient) -> None:
    _record_job("link-test", submitted_at=1.0)
    html = client.get("/jobs").text
    assert '<a href="/jobs/link-test" class="job-link">link-test</a>' in html


def test_jobs_cache_hit_display(client: TestClient) -> None:
    _record_job("cache-yes", submitted_at=1.0, cache_hit=True)
    _record_job("cache-no", submitted_at=2.0, cache_hit=False)

    html = client.get("/jobs").text
    assert re.search(r'data-job-id="cache-yes"[\s\S]*?<td class="col-cache">yes</td>', html)
    assert re.search(r'data-job-id="cache-no"[\s\S]*?<td class="col-cache">no</td>', html)


def test_jobs_handles_unknown_sort_params(client: TestClient) -> None:
    _record_job("first", submitted_at=1.0)
    _record_job("second", submitted_at=2.0)
    _record_job("third", submitted_at=3.0)

    response = client.get("/jobs?sort=unknown&direction=sideways")
    assert response.status_code == 200
    assert _extract_row_ids(response.text) == ["third", "second", "first"]


def test_jobs_page_shows_empty_state_when_no_jobs(client: TestClient) -> None:
    html = client.get("/jobs").text
    assert "No jobs recorded yet." in html
    assert "data-visible-jobs=\"0\"" in html
