"""Evidence pack generation utilities."""
from __future__ import annotations

import hashlib
import json
import os
import zipfile
from datetime import datetime, timezone
from typing import Dict, Any, List


def sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``payload`` with PII fields removed.

    Keys named ``pii_raw`` or ending with ``"_pii"`` are dropped recursively.
    """

    def _sanitize(obj: Any) -> Any:
        if isinstance(obj, dict):
            clean = {}
            for k, v in obj.items():
                if k == "pii_raw" or k.endswith("_pii"):
                    continue
                clean[k] = _sanitize(v)
            return clean
        if isinstance(obj, list):
            return [_sanitize(v) for v in obj]
        return obj

    return _sanitize(payload)


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _p95(latencies: List[float]) -> float:
    if not latencies:
        return 0.0
    latencies = sorted(latencies)
    k = int(len(latencies) * 0.95)
    if k >= len(latencies):
        k = len(latencies) - 1
    return float(latencies[k])


def pack(sim_result: Dict[str, Any], *, meta: Dict[str, Any], out_dir: str) -> str:
    """Write an evidence pack based on ``sim_result``.

    Parameters
    ----------
    sim_result:
        Simulation result as produced by :func:`simulate`.
    meta:
        Metadata with at least an ``id`` field.
    out_dir:
        Directory where the evidence folder and zip should be written.

    Returns
    -------
    str
        Path to the generated ``evidence.zip`` file.
    """

    evidence_dir = os.path.join(out_dir, "evidence")
    os.makedirs(evidence_dir, exist_ok=True)

    items = sorted(sim_result.get("items", []), key=lambda x: x["id"])
    totals = sim_result.get("totals", {})

    # Write simulation.jsonl
    sim_path = os.path.join(evidence_dir, "simulation.jsonl")
    with open(sim_path, "w", encoding="utf-8") as f:
        for item in items:
            payload = {
                "id": item["id"],
                "tokens": item.get("tokens", 0),
                "cost_usd": item.get("cost_usd", 0.0),
                "latency_ms": item.get("latency_ms", 0.0),
                "route_explain": item.get("route_explain", {}),
            }
            json.dump(sanitize_payload(payload), f, sort_keys=True)
            f.write("\n")

    # Write metrics.json
    metrics_path = os.path.join(evidence_dir, "metrics.json")
    latencies = [item.get("latency_ms", 0.0) for item in items]
    count = len(items)
    averages = {
        "cost_usd": totals.get("cost_usd", 0.0) / count if count else 0.0,
        "tokens": totals.get("tokens", 0) / count if count else 0.0,
        "latency_ms": totals.get("latency_ms", 0.0) / count if count else 0.0,
    }
    metrics = {
        "totals": totals,
        "averages": averages,
        "p95_latency_ms": _p95(latencies),
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(sanitize_payload(metrics), f, sort_keys=True)

    # Manifest with hashes
    manifest = {
        "id": meta.get("id"),
        "created_at_utc": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
        "provider": sim_result.get("provider"),
        "model": sim_result.get("model"),
        "counts": {
            "items": count,
            "tokens": totals.get("tokens", 0),
        },
        "sha256": {
            "simulation.jsonl": _sha256(sim_path),
            "metrics.json": _sha256(metrics_path),
        },
    }
    manifest_path = os.path.join(evidence_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(sanitize_payload(manifest), f, sort_keys=True)

    # Zip the files
    zip_path = os.path.join(out_dir, "evidence.zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in ("manifest.json", "simulation.jsonl", "metrics.json"):
            zf.write(os.path.join(evidence_dir, name), arcname=name)

    return zip_path
