from __future__ import annotations

from fastapi import APIRouter

from . import store

router = APIRouter()


@router.post("/evidence")
def post_evidence(body: dict):
    manifest = body.get("manifest", {})
    simulation_lines = body.get("simulation_lines", [])
    metrics = body.get("metrics", {})
    tags = body.get("tags")
    return store.put_pack(manifest, simulation_lines, metrics, tags=tags)


@router.get("/evidence")
def get_evidence_list(start: str | None = None, end: str | None = None, tag: str | None = None, limit: int = 100):
    return store.list_packs(start=start, end=end, tag=tag, limit=limit)


@router.get("/evidence/{evidence_id}")
def get_evidence(evidence_id: str):
    return store.get_pack(evidence_id)

