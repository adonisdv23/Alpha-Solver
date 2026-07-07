"""Read-only local artifact status for the Alpha Solver Operator Console.

This module summarizes a narrow, fixed local artifact directory so the operator
console can show whether local capture / export / preflight artifacts exist and
whether they are structurally valid. It is strictly read-only and local-only:

* It never creates, modifies, deletes, or writes any artifact.
* It never runs providers, models, ``/v1/solve``, MCP, browser automation, CLI
  commands, network calls, or external tools.
* It never returns raw prompts, baseline outputs, routed outputs, or raw route
  metadata. Only counts, states, schema versions, ids, and digests are exposed.

Artifact root: the fixed directory ``local/operator_console/`` under the repo
root. An optional narrow override env (`ALPHA_OPERATOR_CONSOLE_ARTIFACT_ROOT`)
is honored only when it resolves to a path *inside* the repository root; any
path-traversal or outside-root value is rejected and the fixed default is used.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from alpha.eval import operator_run_capture as capture_lib

__all__ = [
    "ARTIFACT_ROOT_ENV",
    "DEFAULT_ARTIFACT_ROOT",
    "CAPTURE_FILENAME",
    "EVIDENCE_PACKET_FILENAME",
    "ANCHOR_PREFLIGHT_FILENAME",
    "LIFT_PREFLIGHT_FILENAME",
    "ARTIFACT_SUPPORT_TEXT",
    "NO_EXECUTION_TEXT",
    "NO_RAW_TEXT",
    "NO_CLAIM_TEXT",
    "NO_ARTIFACTS_TEXT",
    "BOUNDARY_TEXTS",
    "resolve_artifact_root",
    "summarize_capture",
    "summarize_evidence_packet",
    "summarize_anchor_preflight",
    "summarize_lift_preflight",
    "build_artifact_status",
]

# Repository root: alpha/webapp/operator_console_artifacts.py -> parents[2].
_REPO_ROOT = Path(__file__).resolve().parents[2]

ARTIFACT_ROOT_ENV = "ALPHA_OPERATOR_CONSOLE_ARTIFACT_ROOT"
DEFAULT_ARTIFACT_ROOT = _REPO_ROOT / "local" / "operator_console"

CAPTURE_FILENAME = "capture.json"
EVIDENCE_PACKET_FILENAME = "evidence_packet.json"
ANCHOR_PREFLIGHT_FILENAME = "anchor_preflight_report.json"
LIFT_PREFLIGHT_FILENAME = "lift_preflight_report.json"

# ---------------------------------------------------------------------------
# Boundary text. Surfaced in both the rendered console and the status JSON so
# the operator always sees the read-only, no-execution, no-claim boundaries.
# ---------------------------------------------------------------------------
ARTIFACT_SUPPORT_TEXT = "Local artifacts are structural support artifacts only."
NO_EXECUTION_TEXT = (
    "This console does not execute providers, models, /v1/solve, MCP, tools, "
    "browser automation, or CLI commands."
)
NO_RAW_TEXT = "No raw prompts or raw outputs are displayed by default."
NO_CLAIM_TEXT = (
    "No answer-quality, benchmark, readiness, production, validation, or "
    "superiority claim is made."
)
NO_ARTIFACTS_TEXT = "No local operator artifacts detected."

BOUNDARY_TEXTS = (
    ARTIFACT_SUPPORT_TEXT,
    NO_EXECUTION_TEXT,
    NO_RAW_TEXT,
    NO_CLAIM_TEXT,
)


def _is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def resolve_artifact_root() -> Path:
    """Return the artifact root, honoring only a safe inside-repo override.

    The fixed default is ``<repo>/local/operator_console``. If the override env
    is set, it is resolved (relative values are anchored at the repo root) and
    accepted only when it stays inside the repository root; otherwise the fixed
    default is returned. Path traversal and outside-root values are rejected.
    """

    raw = os.getenv(ARTIFACT_ROOT_ENV)
    if not raw or not raw.strip():
        return DEFAULT_ARTIFACT_ROOT

    candidate = Path(raw.strip())
    if not candidate.is_absolute():
        candidate = _REPO_ROOT / candidate
    try:
        resolved = candidate.resolve()
    except (OSError, RuntimeError, ValueError):
        return DEFAULT_ARTIFACT_ROOT

    if not _is_within(resolved, _REPO_ROOT.resolve()):
        # Reject path traversal / outside-root override; fall back to default.
        return DEFAULT_ARTIFACT_ROOT
    return resolved


def _read_json(path: Path) -> Tuple[str, Any]:
    """Return ``(state, data)`` where state is missing / invalid_json / ok.

    Never raises: unreadable or malformed files map to a safe state.
    """

    try:
        if not path.is_file():
            return "missing", None
        text = path.read_text(encoding="utf-8")
    except OSError:
        return "missing", None
    try:
        return "ok", json.loads(text)
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        return "invalid_json", None


def _safe_str(value: Any) -> Optional[str]:
    return value if isinstance(value, str) and value.strip() else None


def _int_counts(raw: Any, keys: Tuple[str, ...]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    if isinstance(raw, dict):
        for key in keys:
            value = raw.get(key)
            if isinstance(value, bool):
                continue
            if isinstance(value, int):
                counts[key] = value
    return counts


def summarize_capture(root: Path) -> Dict[str, Any]:
    """Summarize ``capture.json`` as counts/states only (no raw case content)."""

    state, data = _read_json(root / CAPTURE_FILENAME)
    if state != "ok":
        return {"state": state}

    try:
        errors = capture_lib.validate_capture(data)
    except Exception:  # pragma: no cover - defensive: never 500 on bad input
        return {"state": "invalid_structure"}
    if errors:
        return {"state": "invalid_structure", "error_count": len(errors)}

    try:
        export_ready = not capture_lib.validate_capture(data, for_export=True)
    except Exception:  # pragma: no cover - defensive
        export_ready = False

    cases = data.get("cases") if isinstance(data, dict) else []
    if not isinstance(cases, list):
        cases = []

    def _count(status: str) -> int:
        return sum(
            1
            for case in cases
            if isinstance(case, dict) and case.get("validation_status") == status
        )

    route_metadata_present = sum(
        1
        for case in cases
        if isinstance(case, dict) and isinstance(case.get("route_metadata"), dict)
        and case.get("route_metadata")
    )

    return {
        "state": "export_ready" if export_ready else "structurally_valid",
        "schema_version": _safe_str(data.get("schema_version")),
        "packet_id": _safe_str(data.get("packet_id")),
        "counts": {
            "total": len(cases),
            "captured": _count("captured"),
            "excluded": _count("excluded"),
            "pending": _count("pending"),
        },
        "route_metadata_present_count": route_metadata_present,
    }


def summarize_evidence_packet(root: Path) -> Dict[str, Any]:
    """Summarize ``evidence_packet.json`` including digest verification."""

    state, data = _read_json(root / EVIDENCE_PACKET_FILENAME)
    if state != "ok":
        return {"state": state}

    if not isinstance(data, dict):
        return {"state": "invalid_structure"}
    if data.get("schema_version") != capture_lib.PACKET_SCHEMA_VERSION:
        return {"state": "invalid_structure"}
    if not _safe_str(data.get("packet_id")):
        return {"state": "invalid_structure"}
    if not isinstance(data.get("counts"), dict) or not isinstance(
        data.get("cases"), list
    ):
        return {"state": "invalid_structure"}

    content_digest = _safe_str(data.get("content_digest"))
    if content_digest is None:
        digest_state = "digest_unverifiable"
    else:
        try:
            digest_state = (
                "digest_valid"
                if capture_lib.verify_packet_digest(data)
                else "digest_invalid"
            )
        except Exception:  # pragma: no cover - defensive
            digest_state = "digest_unverifiable"

    return {
        "state": digest_state,
        "schema_version": _safe_str(data.get("schema_version")),
        "packet_id": _safe_str(data.get("packet_id")),
        "content_digest": content_digest,
        "counts": _int_counts(
            data.get("counts"), ("total", "captured", "excluded")
        ),
    }


def _summarize_preflight(
    root: Path, filename: str, schema_version: str, states: Tuple[str, ...]
) -> Dict[str, Any]:
    state, data = _read_json(root / filename)
    if state != "ok":
        return {"state": state}
    if not isinstance(data, dict):
        return {"state": "invalid_structure"}
    if data.get("schema_version") != schema_version:
        return {"state": "invalid_structure"}
    summary = data.get("summary")
    if not isinstance(summary, dict):
        return {"state": "invalid_structure"}

    needs_attention = summary.get("needs_attention")
    needs_attention_count = (
        len(needs_attention) if isinstance(needs_attention, list) else 0
    )
    return {
        "state": "present",
        "schema_version": _safe_str(data.get("schema_version")),
        "packet_id": _safe_str(data.get("packet_id")),
        "state_counts": _int_counts(summary.get("counts"), states + ("total",)),
        "needs_attention_count": needs_attention_count,
    }


def summarize_anchor_preflight(root: Path) -> Dict[str, Any]:
    """Summarize ``anchor_preflight_report.json`` (counts + attention only)."""

    return _summarize_preflight(
        root,
        ANCHOR_PREFLIGHT_FILENAME,
        capture_lib.ANCHOR_PREFLIGHT_REPORT_SCHEMA_VERSION,
        capture_lib.ANCHOR_PREFLIGHT_STATES,
    )


def summarize_lift_preflight(root: Path) -> Dict[str, Any]:
    """Summarize ``lift_preflight_report.json`` (counts + attention only)."""

    return _summarize_preflight(
        root,
        LIFT_PREFLIGHT_FILENAME,
        capture_lib.LIFT_PREFLIGHT_REPORT_SCHEMA_VERSION,
        capture_lib.LIFT_PREFLIGHT_STATES,
    )


def _display_root(root: Path) -> str:
    try:
        rel = root.resolve().relative_to(_REPO_ROOT.resolve())
        return str(rel)
    except ValueError:  # pragma: no cover - resolve keeps root inside repo
        return root.name


def build_artifact_status(root: Optional[Path] = None) -> Dict[str, Any]:
    """Assemble the read-only local artifact status payload.

    Pure function over the local filesystem. Reads at most the four fixed
    artifact files, returns counts/states/digests only, and performs no
    provider, network, model, tool, or CLI call.
    """

    resolved = root if root is not None else resolve_artifact_root()
    capture = summarize_capture(resolved)
    packet = summarize_evidence_packet(resolved)
    anchor = summarize_anchor_preflight(resolved)
    lift = summarize_lift_preflight(resolved)

    detected = any(
        section.get("state") != "missing"
        for section in (capture, packet, anchor, lift)
    )

    return {
        "artifact_root": _display_root(resolved),
        "detected": detected,
        "no_artifacts_message": NO_ARTIFACTS_TEXT,
        "capture": capture,
        "evidence_packet": packet,
        "anchor_preflight": anchor,
        "lift_preflight": lift,
        "boundaries": list(BOUNDARY_TEXTS),
    }
