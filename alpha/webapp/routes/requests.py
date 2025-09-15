"""Request submission UI routes for the Alpha Solver dashboard."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import HTMLResponse

AVAILABLE_PROVIDERS = ("mock", "mock-pro")

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
_REQUEST_TEMPLATE_PATH = _TEMPLATES_DIR / "request.html"

router = APIRouter()


@dataclass
class RequestJob:
    """In-memory record tracking the lifecycle of a dashboard request."""

    id: str
    prompt: str
    provider: str
    status: str = "pending"
    latency_ms: Optional[float] = None
    cache_hit: bool = False
    submitted_at: float = field(default_factory=time.perf_counter)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None


_JOBS: Dict[str, RequestJob] = {}
_JOBS_LOCK = threading.Lock()
_BASE_TEMPLATE_CACHE: Optional[str] = None


def _load_template() -> str:
    global _BASE_TEMPLATE_CACHE
    if _BASE_TEMPLATE_CACHE is None:
        _BASE_TEMPLATE_CACHE = _REQUEST_TEMPLATE_PATH.read_text(encoding="utf-8")
    return _BASE_TEMPLATE_CACHE


def _render_request_form_html() -> str:
    base_template = _load_template()
    options = "\n".join(
        f"            <option value=\"{provider}\">{provider}</option>"
        for provider in AVAILABLE_PROVIDERS
    )
    return base_template.replace("{{provider_options}}", options)


def reset_state() -> None:
    """Clear in-memory job state.

    This helper keeps tests hermetic and is no-op for production usage.
    """

    with _JOBS_LOCK:
        _JOBS.clear()


def _serialize(job: RequestJob) -> Dict[str, object]:
    """Serialize a job record for the API response."""

    return {
        "id": job.id,
        "status": job.status,
        "latency_ms": job.latency_ms,
        "provider": job.provider,
        "cache_hit": job.cache_hit,
    }


def _mock_provider_latency(prompt: str, provider: str) -> float:
    """Simulate a provider call and return the elapsed latency in milliseconds."""

    # Keep things deterministic but non-zero by deriving a short delay from the
    # prompt size and provider name.
    base_delay = 0.05 if provider == AVAILABLE_PROVIDERS[0] else 0.065
    jitter = min(len(prompt) / 1000.0, 0.035)
    start = time.perf_counter()
    time.sleep(base_delay + jitter)
    return (time.perf_counter() - start) * 1000.0


def _run_job(job_id: str) -> None:
    """Background execution that marks a request as complete."""

    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
        if not job:
            return
        job.status = "running"
        job.started_at = time.perf_counter()
        prompt = job.prompt
        provider = job.provider

    latency_ms = _mock_provider_latency(prompt, provider)

    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
        if not job:
            return
        job.latency_ms = latency_ms
        job.completed_at = time.perf_counter()
        job.status = "done"


@router.get("/requests", response_class=HTMLResponse)
async def request_form(request: Request) -> HTMLResponse:
    """Render the dashboard request submission form."""

    _ = request  # FastAPI requires the request parameter even for static templates.
    return HTMLResponse(content=_render_request_form_html())


@router.post("/requests")
async def submit_request(payload: Dict[str, str], background_tasks: BackgroundTasks) -> Dict[str, str]:
    """Submit a new request and schedule background processing."""

    prompt_raw = payload.get("prompt", "") if payload else ""
    provider = payload.get("provider", AVAILABLE_PROVIDERS[0]) if payload else AVAILABLE_PROVIDERS[0]

    prompt = prompt_raw.strip()
    if not prompt:
        raise HTTPException(status_code=422, detail="prompt is required")
    if provider not in AVAILABLE_PROVIDERS:
        raise HTTPException(status_code=422, detail="unknown provider")

    job_id = str(uuid.uuid4())
    job = RequestJob(id=job_id, prompt=prompt, provider=provider)

    with _JOBS_LOCK:
        _JOBS[job_id] = job

    background_tasks.add_task(_run_job, job_id)

    return {"id": job_id}


@router.get("/requests/{request_id}")
async def request_status(request_id: str) -> Dict[str, object]:
    """Return the status of a submitted request."""

    with _JOBS_LOCK:
        job = _JOBS.get(request_id)
        if not job:
            raise HTTPException(status_code=404, detail="request not found")
        return _serialize(job)
