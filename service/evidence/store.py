from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import zipfile

# Base paths (can be monkeypatched in tests)
BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "index.jsonl"
PACKS_DIR = BASE_DIR / "packs"


def _utcnow() -> datetime:
    """Return current UTC time with tzinfo."""
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def _sanitize(obj: Any) -> Any:
    """Recursively drop PII/secret keys."""
    if isinstance(obj, dict):
        clean = {}
        for k, v in obj.items():
            if k == "pii_raw" or k.endswith("_token") or k.endswith("_secret"):
                continue
            clean[k] = _sanitize(v)
        return clean
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)


def put_pack(
    manifest: Dict[str, Any],
    simulation_lines: List[str],
    metrics: Dict[str, Any],
    *,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    now = _utcnow()
    ts = now.isoformat().replace("+00:00", "Z")
    date_str = now.strftime("%Y%m%d")
    pack_id = uuid.uuid4().hex

    pack_dir = PACKS_DIR / date_str / pack_id
    pack_dir.mkdir(parents=True, exist_ok=False)

    manifest_clean = _sanitize(manifest)
    metrics_clean = _sanitize(metrics)

    manifest_path = pack_dir / "manifest.json"
    metrics_path = pack_dir / "metrics.json"
    sim_path = pack_dir / "simulation.jsonl"
    zip_path = pack_dir / "evidence.zip"

    _atomic_write(
        manifest_path, json.dumps(manifest_clean, separators=(",", ":")).encode("utf-8")
    )
    sim_content = "\n".join(simulation_lines)
    if simulation_lines:
        sim_content += "\n"
    _atomic_write(sim_path, sim_content.encode("utf-8"))
    _atomic_write(
        metrics_path, json.dumps(metrics_clean, separators=(",", ":")).encode("utf-8")
    )

    tmp_zip = zip_path.with_name(zip_path.name + ".tmp")
    with zipfile.ZipFile(tmp_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(
            "manifest.json", json.dumps(manifest_clean, separators=(",", ":"))
        )
        z.writestr("simulation.jsonl", sim_content)
        z.writestr(
            "metrics.json", json.dumps(metrics_clean, separators=(",", ":"))
        )
    os.replace(tmp_zip, zip_path)

    h = hashlib.sha256()
    with open(zip_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    sha256_zip = h.hexdigest()
    size_zip = zip_path.stat().st_size

    entry = {
        "id": pack_id,
        "ts": ts,
        "tags": tags or [],
        "sha256_zip": sha256_zip,
        "size_zip": size_zip,
        "paths": {"zip": str(zip_path)},
    }

    lock_path = INDEX_PATH.with_suffix(".lock")
    lock_fd = None
    while True:
        try:
            lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            break
        except FileExistsError:
            time.sleep(0.01)
    try:
        INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(INDEX_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, separators=(",", ":")) + "\n")
    finally:
        if lock_fd is not None:
            os.close(lock_fd)
            os.unlink(lock_path)

    return entry


def list_packs(
    *,
    start: Optional[str] = None,
    end: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    if not INDEX_PATH.exists():
        return []
    results: List[Dict[str, Any]] = []
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if start and obj["ts"] < start:
                continue
            if end and obj["ts"] > end:
                continue
            if tag and tag not in obj.get("tags", []):
                continue
            results.append(obj)
    results.sort(key=lambda x: x["ts"], reverse=True)
    return results[:limit]


def get_pack(pack_id: str) -> Dict[str, Any]:
    if not INDEX_PATH.exists():
        raise KeyError(pack_id)
    entry: Optional[Dict[str, Any]] = None
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            if obj.get("id") == pack_id:
                entry = obj
    if entry is None:
        raise KeyError(pack_id)

    zip_path = Path(entry["paths"]["zip"])
    h = hashlib.sha256()
    with open(zip_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    size = zip_path.stat().st_size
    if h.hexdigest() != entry["sha256_zip"] or size != entry["size_zip"]:
        raise ValueError("evidence.zip integrity check failed")

    pack_dir = zip_path.parent
    manifest_path = pack_dir / "manifest.json"
    metrics_path = pack_dir / "metrics.json"
    sim_path = pack_dir / "simulation.jsonl"
    manifest = json.loads(manifest_path.read_text("utf-8"))
    metrics = json.loads(metrics_path.read_text("utf-8"))

    result = dict(entry)
    result.update(
        {
            "manifest": manifest,
            "metrics": metrics,
            "paths": {
                "zip": str(zip_path),
                "manifest": str(manifest_path),
                "metrics": str(metrics_path),
                "simulation": str(sim_path),
            },
        }
    )
    return result


def to_route_explain(entry: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "evidence_id": entry["id"],
        "sha256": entry["sha256_zip"],
        "size_zip": entry["size_zip"],
        "tags": entry.get("tags", []),
    }

