"""Job history dashboard routes for the Alpha Solver UI."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import List, Sequence

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from . import requests as request_routes

__all__ = ["router"]


router = APIRouter()

_TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "jobs.html"
_TEMPLATE_CACHE: str | None = None
_MAX_ROWS = 100
_DEFAULT_SORT_FIELD = "time"
_DEFAULT_SORT_DIRECTION = "desc"
_VALID_SORT_FIELDS = {"time", "latency"}
_VALID_DIRECTIONS = {"asc", "desc"}


def _load_template() -> str:
    global _TEMPLATE_CACHE
    if _TEMPLATE_CACHE is None:
        _TEMPLATE_CACHE = _TEMPLATE_PATH.read_text(encoding="utf-8")
    return _TEMPLATE_CACHE


def _snapshot_jobs() -> List[request_routes.RequestJob]:
    """Return jobs ordered by submission time (newest first)."""

    with request_routes._JOBS_LOCK:
        jobs = list(request_routes._JOBS.values())
    return sorted(jobs, key=lambda job: job.submitted_at, reverse=True)


def _normalize_sort_field(value: str | None) -> str:
    if not value:
        return _DEFAULT_SORT_FIELD
    value_lower = value.lower()
    if value_lower in _VALID_SORT_FIELDS:
        return value_lower
    return _DEFAULT_SORT_FIELD


def _normalize_direction(value: str | None) -> str:
    if not value:
        return _DEFAULT_SORT_DIRECTION
    value_lower = value.lower()
    if value_lower in _VALID_DIRECTIONS:
        return value_lower
    return _DEFAULT_SORT_DIRECTION


def _sort_jobs(
    jobs: Sequence[request_routes.RequestJob],
    field: str,
    direction: str,
) -> List[request_routes.RequestJob]:
    if field == "latency":
        if direction == "asc":
            return sorted(
                jobs,
                key=lambda job: (
                    job.latency_ms is None,
                    job.latency_ms if job.latency_ms is not None else float("inf"),
                    -job.submitted_at,
                    job.id,
                ),
            )
        return sorted(
            jobs,
            key=lambda job: (
                job.latency_ms is None,
                -(job.latency_ms or 0.0),
                -job.submitted_at,
                job.id,
            ),
        )
    if direction == "asc":
        return sorted(jobs, key=lambda job: (job.submitted_at, job.id))
    return sorted(jobs, key=lambda job: (-job.submitted_at, job.id))


def _format_latency(job: request_routes.RequestJob) -> tuple[str, str]:
    if job.latency_ms is None:
        return "—", "pending"
    return f"{job.latency_ms:.1f} ms", f"{job.latency_ms:.6f}"


def _render_rows(jobs: Sequence[request_routes.RequestJob]) -> str:
    if not jobs:
        return """
            <tr class=\"empty\">
              <td colspan=\"5\">No jobs recorded yet.</td>
            </tr>
        """.strip()

    rows: list[str] = []
    for job in jobs:
        latency_display, latency_attr = _format_latency(job)
        cache_display = "yes" if job.cache_hit else "no"
        rows.append(
            """
            <tr data-job-id=\"{job_id}\" data-status=\"{status}\" data-submitted=\"{submitted:.6f}\" data-latency=\"{latency_attr}\">
              <td class=\"col-id\"><a href=\"/jobs/{job_id}\" class=\"job-link\">{job_id}</a></td>
              <td class=\"col-provider\">{provider}</td>
              <td class=\"col-status\">{status}</td>
              <td class=\"col-latency\">{latency}</td>
              <td class=\"col-cache\">{cache}</td>
            </tr>
            """.format(
                job_id=job.id,
                provider=job.provider,
                status=job.status,
                latency=latency_display,
                cache=cache_display,
                latency_attr=latency_attr,
                submitted=job.submitted_at,
            ).strip()
        )
    return "\n".join(rows)


def _render_status_summary(jobs: Sequence[request_routes.RequestJob]) -> str:
    if not jobs:
        return "          <li class=\"empty\">No jobs recorded yet.</li>"
    counts = Counter(job.status for job in jobs)
    items: list[str] = []
    for status, count in sorted(counts.items()):
        items.append(
            f"          <li data-status=\"{status}\"><span class=\"status-label\">{status}</span><span class=\"status-count\">{count}</span></li>"
        )
    return "\n".join(items)


def _sort_link(field: str, label: str, current_field: str, current_direction: str) -> tuple[str, str, str]:
    is_active = field == current_field
    if is_active:
        next_direction = "asc" if current_direction == "desc" else "desc"
        arrow = "↓" if current_direction == "desc" else "↑"
        href = f"/jobs?sort={field}&direction={next_direction}"
        full_label = f"{label} {arrow}"
        active_suffix = " active"
    else:
        href = f"/jobs?sort={field}&direction=desc"
        full_label = f"{label} ↕"
        active_suffix = ""
    return href, full_label, active_suffix


def _summarize_count(display_count: int, total_count: int) -> str:
    if display_count == 0:
        return "No jobs recorded yet."
    if total_count > display_count:
        return f"Showing last {display_count} of {total_count} jobs."
    if display_count == 1:
        return "Showing 1 job."
    return f"Showing {display_count} jobs."


def _render_jobs_page(
    jobs: Sequence[request_routes.RequestJob],
    sort_field: str,
    sort_direction: str,
    display_count: int,
    total_count: int,
) -> str:
    base = _load_template()
    rows_html = _render_rows(jobs)
    status_summary = _render_status_summary(jobs)
    time_href, time_label, time_class = _sort_link("time", "Time", sort_field, sort_direction)
    latency_href, latency_label, latency_class = _sort_link("latency", "Latency", sort_field, sort_direction)
    summary_line = _summarize_count(display_count, total_count)

    replacements = {
        "job_count": str(display_count),
        "total_jobs": str(total_count),
        "rows": rows_html,
        "status_items": status_summary,
        "time_sort_href": time_href,
        "time_sort_label": time_label,
        "time_sort_active_class": time_class,
        "latency_sort_href": latency_href,
        "latency_sort_label": latency_label,
        "latency_sort_active_class": latency_class,
        "summary_line": summary_line,
    }
    rendered = base
    for key, value in replacements.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


@router.get("/jobs", response_class=HTMLResponse)
async def jobs_dashboard(request: Request) -> HTMLResponse:
    """Render the dashboard job history view."""

    sort_field = _normalize_sort_field(request.query_params.get("sort"))
    sort_direction = _normalize_direction(request.query_params.get("direction"))

    snapshot = _snapshot_jobs()
    total_count = len(snapshot)
    recent_jobs = snapshot[:_MAX_ROWS]
    sorted_jobs = _sort_jobs(recent_jobs, sort_field, sort_direction)
    html = _render_jobs_page(sorted_jobs, sort_field, sort_direction, len(recent_jobs), total_count)
    return HTMLResponse(content=html)
