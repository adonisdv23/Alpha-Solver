"""Local receipt snapshots for the Alpha Solver Operator Console.

This helper is intentionally narrow and local-only. It creates one safe JSON
receipt under the existing operator-console artifact root and summarizes recent
receipt metadata. It never accepts request-supplied paths, filenames, ids, or
receipt bodies, and it never reads or writes capture/evidence/preflight files.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping

from alpha.webapp import operator_console_artifacts as artifacts

__all__ = [
    "RECEIPT_SCHEMA_VERSION",
    "RECEIPT_TYPE",
    "SOURCE",
    "CREATE_RECEIPT_ENDPOINT",
    "RECEIPT_BOUNDARY_TEXTS",
    "build_receipt_store_status",
    "create_receipt_snapshot",
    "digest_receipt_body",
    "receipt_root",
]

RECEIPT_SCHEMA_VERSION = "operator_console_receipt_v1"
RECEIPT_TYPE = "status_snapshot"
SOURCE = "operator_console"
CREATE_RECEIPT_ENDPOINT = "/dashboard/operator-console/receipts"
RECENT_LIMIT = 5
_RECEIPT_ID_RE = re.compile(r"^ocr_[0-9]{8}T[0-9]{6}Z_[0-9a-f]{16}$")
_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

RECEIPT_BOUNDARY_TEXTS = (
    "Local receipts are local audit snapshots only.",
    "Saving a receipt does not run a solve.",
    "Saving a receipt does not call /v1/solve.",
    "Saving a receipt does not call providers, models, MCP, browser automation, network, CLI, or subprocesses.",
    "Saving a receipt does not create, edit, delete, upload, save, or mutate capture/evidence/preflight artifacts.",
    "Saving a receipt writes only a safe local receipt JSON under the fixed receipt directory.",
    "Receipts store safe summaries only.",
    "Receipts do not store raw prompts, raw outputs, raw route metadata, system prompts, provider payloads, raw secrets, partial keys, or raw environment values.",
    "A receipt is not answer-quality proof, validation, production readiness, provider readiness, benchmark evidence, billing accuracy, or superiority evidence.",
    "A receipt does not authorize live execution or dry-run execution.",
)

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def receipt_root() -> Path:
    """Return the fixed receipts directory below the safe artifact root."""

    return artifacts.resolve_artifact_root() / "receipts"


def _path_label(path: Path) -> str:
    try:
        return path.resolve().relative_to(_REPO_ROOT.resolve()).as_posix()
    except (OSError, RuntimeError, ValueError):
        return "local/operator_console/receipts"


def _receipt_id(now: datetime) -> str:
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    return f"ocr_{stamp}_{secrets.token_hex(8)}"


def _json_bytes(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_receipt_body(receipt_body_without_digest: Mapping[str, Any]) -> str:
    """Return the receipt self-integrity digest over the safe body only."""

    return "sha256:" + hashlib.sha256(_json_bytes(receipt_body_without_digest)).hexdigest()


def _copy_map(src: Mapping[str, Any], keys: tuple[str, ...]) -> Dict[str, Any]:
    return {key: src.get(key) for key in keys if key in src}


def safe_snapshot(status: Mapping[str, Any]) -> Dict[str, Any]:
    """Whitelist the safe console status subset for receipt storage."""

    local = status.get("local_artifacts") or {}
    freshness = local.get("freshness") or {}
    provider_gate = status.get("provider_gate") or {}
    dry_run = status.get("dry_run_preview") or {}

    return {
        "console": _copy_map(
            status.get("console") or {},
            ("mode", "live_provider_calls", "claim_boundary", "boundary_notes"),
        ),
        "portable_contract": _copy_map(
            status.get("portable_contract") or {},
            ("present", "source_path", "contract_mode", "surfaces"),
        ),
        "run_setup": _copy_map(
            status.get("run_setup") or {},
            ("run_modes", "live_run_button_enabled", "note"),
        ),
        "route_trace": _copy_map(
            status.get("route_trace") or {},
            ("route", "confidence", "safe_out_state", "expert_team", "shortlist", "diagnostics", "note"),
        ),
        "provider_gate": _copy_map(
            provider_gate,
            (
                "configured_provider",
                "provider_mode_label",
                "live_provider_calls",
                "console_calls_providers",
                "emergency_stop",
                "live_preview_surface",
                "key_status",
                "required_provider_keys",
                "provider_key_status",
                "cap_completeness",
                "cap_status",
                "cost_cap_status",
                "token_request_cap_status",
                "live_execution_gate",
                "live_execution_blockers",
                "gate_boundary",
            ),
        ),
        "dry_run_preview": _copy_map(
            dry_run,
            (
                "preview_mode",
                "dry_run_execution",
                "would_use",
                "input_source_status",
                "evidence_packet_status",
                "preflight_status",
                "freshness_warnings",
                "provider_gate_summary",
                "preview_readiness",
                "preview_blockers",
                "boundary",
                "boundary_notes",
            ),
        ),
        "local_artifacts": {
            "artifact_root": local.get("artifact_root"),
            "detected": local.get("detected"),
            "status_generated_at_utc": local.get("status_generated_at_utc"),
            "capture": _copy_map(
                local.get("capture") or {},
                ("state", "schema_version", "packet_id", "counts", "route_metadata_present_count"),
            ),
            "evidence_packet": _copy_map(
                local.get("evidence_packet") or {},
                ("state", "schema_version", "packet_id", "content_digest", "counts"),
            ),
            "anchor_preflight": _copy_map(
                local.get("anchor_preflight") or {},
                ("state", "schema_version", "packet_id", "counts", "needs_attention_count"),
            ),
            "lift_preflight": _copy_map(
                local.get("lift_preflight") or {},
                ("state", "schema_version", "packet_id", "counts", "needs_attention_count"),
            ),
            "freshness": {
                "files": freshness.get("files", {}),
                "sequence_coherence": freshness.get("sequence_coherence", {}),
                "boundaries": freshness.get("boundaries", []),
            },
            "boundaries": local.get("boundaries", []),
            "no_artifacts_message": local.get("no_artifacts_message"),
        },
        "evidence_receipt": _copy_map(
            status.get("evidence_receipt") or {},
            ("receipt_id", "export_digest", "validation_status", "note"),
        ),
    }


def _build_receipt(status: Mapping[str, Any], now: datetime, receipt_id: str) -> Dict[str, Any]:
    body = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "receipt_id": receipt_id,
        "created_at_utc": now.isoformat().replace("+00:00", "Z"),
        "source": SOURCE,
        "receipt_type": RECEIPT_TYPE,
        "snapshot": safe_snapshot(status),
    }
    return {**body, "content_digest": digest_receipt_body(body)}


def _safe_receipt_path(root: Path, receipt_id: str) -> Path:
    if not _RECEIPT_ID_RE.fullmatch(receipt_id):
        raise ValueError("unsafe receipt id")
    path = (root / f"{receipt_id}.json").resolve()
    if not _is_within(path, root.resolve()):
        raise ValueError("receipt path escaped root")
    return path


def create_receipt_snapshot(status: Mapping[str, Any]) -> Dict[str, Any]:
    """Create exactly one receipt JSON and return safe metadata."""

    root = receipt_root().resolve()
    repo_root = _REPO_ROOT.resolve()
    if not _is_within(root, repo_root):
        raise ValueError("receipt root must stay inside repository root")
    if root.exists() and root.is_symlink():
        raise ValueError("receipt root may not be a symlink")
    root.mkdir(parents=True, exist_ok=True)

    for _attempt in range(8):
        now = datetime.now(timezone.utc)
        rid = _receipt_id(now)
        final_path = _safe_receipt_path(root, rid)
        if final_path.exists():
            continue
        tmp_path = _safe_receipt_path(root, f"{rid}").with_suffix(".tmp")
        receipt = _build_receipt(status, now, rid)
        data = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
        try:
            with tmp_path.open("x", encoding="utf-8") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.link(tmp_path, final_path)
        finally:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)
        return _metadata_from_receipt(receipt, final_path, state="created")
    raise FileExistsError("could not allocate unique receipt id")


def _metadata_from_receipt(receipt: Mapping[str, Any], path: Path, *, state: str) -> Dict[str, Any]:
    snapshot = receipt.get("snapshot") if isinstance(receipt.get("snapshot"), dict) else {}
    dry_run = snapshot.get("dry_run_preview", {}) if isinstance(snapshot, dict) else {}
    provider_gate = snapshot.get("provider_gate", {}) if isinstance(snapshot, dict) else {}
    local = snapshot.get("local_artifacts", {}) if isinstance(snapshot, dict) else {}
    capture = local.get("capture", {}) if isinstance(local, dict) else {}
    packet = local.get("evidence_packet", {}) if isinstance(local, dict) else {}
    return {
        "receipt_id": receipt.get("receipt_id"),
        "created_at_utc": receipt.get("created_at_utc"),
        "schema_version": receipt.get("schema_version"),
        "receipt_type": receipt.get("receipt_type"),
        "content_digest": receipt.get("content_digest"),
        "path_label": _path_label(path),
        "state": state,
        "snapshot_summary": {
            "preview_readiness": dry_run.get("preview_readiness"),
            "live_execution_gate": provider_gate.get("live_execution_gate"),
            "capture_state": capture.get("state"),
            "evidence_packet_state": packet.get("state"),
        },
    }


def _load_receipt_metadata(path: Path) -> Dict[str, Any]:
    try:
        if path.is_symlink() or not path.is_file():
            raise ValueError("not a regular receipt file")
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(receipt, dict):
            raise ValueError("receipt is not an object")
        body = {k: v for k, v in receipt.items() if k != "content_digest"}
        digest = receipt.get("content_digest")
        if not isinstance(digest, str) or not _DIGEST_RE.fullmatch(digest):
            raise ValueError("invalid digest shape")
        if digest_receipt_body(body) != digest:
            raise ValueError("digest mismatch")
        if receipt.get("schema_version") != RECEIPT_SCHEMA_VERSION:
            raise ValueError("unsupported schema")
        if not isinstance(receipt.get("receipt_id"), str) or not _RECEIPT_ID_RE.fullmatch(receipt["receipt_id"]):
            raise ValueError("invalid receipt id")
        return _metadata_from_receipt(receipt, path, state="present")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError):
        return {
            "receipt_id": path.stem[:80],
            "created_at_utc": None,
            "schema_version": None,
            "receipt_type": None,
            "content_digest": None,
            "path_label": _path_label(path),
            "state": "invalid",
            "snapshot_summary": {},
        }


def _sort_key(item: Mapping[str, Any]) -> tuple[str, str]:
    return (str(item.get("created_at_utc") or ""), str(item.get("receipt_id") or ""))


def list_recent_receipts(limit: int = RECENT_LIMIT) -> List[Dict[str, Any]]:
    root = receipt_root().resolve()
    if not _is_within(root, _REPO_ROOT.resolve()) or not root.exists() or root.is_symlink():
        return []
    entries = [_load_receipt_metadata(path) for path in root.glob("*.json")]
    entries.sort(key=_sort_key, reverse=True)
    return entries[: max(0, limit)]


def build_receipt_store_status() -> Dict[str, Any]:
    root = receipt_root()
    recent = list_recent_receipts()
    states: List[str] = []
    if not root.exists():
        states.append("missing_dir")
    elif not recent:
        states.append("empty")
    else:
        states.append("present")
    if any(item.get("state") == "invalid" for item in recent):
        states.append("invalid_entries")
    return {
        "receipt_root": _path_label(root),
        "enabled": True,
        "create_receipt_endpoint": CREATE_RECEIPT_ENDPOINT,
        "recent": recent,
        "count": len(recent),
        "states": states,
        "boundary": "local receipt snapshots only; safe metadata only; not proof",
        "boundary_notes": list(RECEIPT_BOUNDARY_TEXTS),
    }
