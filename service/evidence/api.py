from __future__ import annotations

from fastapi import APIRouter

from . import store

router = APIRouter()


@router.post("/evidence")
def post_evidence(body: dict):
    """Store a new evidence pack.

    Args:
        body: JSON body containing ``manifest``, ``simulation_lines`` and ``metrics``.

    Returns:
        Dict describing the stored evidence pack.
    """

    manifest = body.get("manifest", {})
    simulation_lines = body.get("simulation_lines", [])
    metrics = body.get("metrics", {})
    tags = body.get("tags")
    return store.put_pack(manifest, simulation_lines, metrics, tags=tags)


@router.get("/evidence")
def get_evidence_list(start: str | None = None, end: str | None = None, tag: str | None = None, limit: int = 100):
    """Return a list of evidence packs.

    Args:
        start: Optional ISO timestamp lower bound.
        end: Optional ISO timestamp upper bound.
        tag: Tag filter.
        limit: Maximum number of results.

    Returns:
        List of evidence pack summaries.
    """

    return store.list_packs(start=start, end=end, tag=tag, limit=limit)


@router.get("/evidence/{evidence_id}")
def get_evidence(evidence_id: str):
    """Fetch details for a single evidence pack.

    Args:
        evidence_id: Identifier of the pack.

    Returns:
        Dict describing the evidence pack.
    """

    return store.get_pack(evidence_id)

