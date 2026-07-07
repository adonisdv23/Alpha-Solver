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
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

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
    "FRESHNESS_JUST_UPDATED_SECONDS",
    "FRESHNESS_RECENT_SECONDS",
    "FRESHNESS_METADATA_ONLY_TEXT",
    "FRESHNESS_NO_CLAIM_TEXT",
    "FRESHNESS_OLDER_MEANING_TEXT",
    "FRESHNESS_DIGEST_TEXT",
    "FRESHNESS_BOUNDARY_TEXTS",
    "resolve_artifact_root",
    "summarize_capture",
    "summarize_evidence_packet",
    "summarize_anchor_preflight",
    "summarize_lift_preflight",
    "age_label",
    "file_freshness",
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

# Expected shape of a packet content digest: ``sha256:<64 lowercase hex>``.
# A content_digest that does not match this is never returned or rendered, so a
# corrupted packet cannot smuggle raw prompt/output text through this field.
_DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}")

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

# ---------------------------------------------------------------------------
# Freshness / sequence-coherence configuration and boundary text.
#
# Freshness is derived purely from local filesystem modified-time metadata and
# from the existing safe summaries above. It is never a quality, readiness,
# validation, benchmark, production, or superiority signal. Thresholds are fixed
# and deterministic; ``build_artifact_status`` accepts an injectable ``now`` so
# tests never depend on the wall clock.
# ---------------------------------------------------------------------------
FRESHNESS_JUST_UPDATED_SECONDS = 300  # <= 5 minutes old -> just_updated
FRESHNESS_RECENT_SECONDS = 86_400  # <= 24 hours old -> recent

FRESHNESS_METADATA_ONLY_TEXT = "Freshness is local filesystem metadata only."
FRESHNESS_NO_CLAIM_TEXT = (
    "A newer artifact is not answer-quality, benchmark, readiness, production, "
    "validation, or superiority evidence."
)
FRESHNESS_OLDER_MEANING_TEXT = (
    "An older derived artifact means only that the local file timestamp appears "
    "older than the capture timestamp."
)
FRESHNESS_DIGEST_TEXT = (
    "Digest validity is packet self-integrity only, not proof that the packet "
    "reflects the latest capture file."
)

FRESHNESS_BOUNDARY_TEXTS = (
    FRESHNESS_METADATA_ONLY_TEXT,
    FRESHNESS_NO_CLAIM_TEXT,
    FRESHNESS_OLDER_MEANING_TEXT,
    FRESHNESS_DIGEST_TEXT,
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
    except UnicodeDecodeError:
        # Undecodable bytes are a malformed artifact, not a missing one, and
        # read_text raises this before the JSON handler below would run.
        return "invalid_json", None
    except OSError:
        return "missing", None
    try:
        return "ok", json.loads(text)
    except (json.JSONDecodeError, ValueError):
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

    raw_digest = data.get("content_digest")
    has_digest = isinstance(raw_digest, str) and bool(raw_digest.strip())
    if not has_digest:
        # No recorded digest: nothing to verify and nothing to expose.
        digest_state = "digest_unverifiable"
        safe_digest: Optional[str] = None
    elif not _DIGEST_RE.fullmatch(raw_digest):
        # A malformed content_digest could carry raw prompt/output text; never
        # return or render its value, and fail to a safe non-leaking state.
        return {"state": "invalid_structure"}
    else:
        safe_digest = raw_digest
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
        "content_digest": safe_digest,
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


# ---------------------------------------------------------------------------
# Freshness and sequence-coherence helpers. These read only filesystem
# modified-time metadata for the four fixed files and compare against the
# existing safe summaries. They never read raw artifact content.
# ---------------------------------------------------------------------------
def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _iso_utc(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def age_label(age_seconds: Optional[int], metadata_state: str) -> str:
    """Map an age (seconds) to a deterministic, bounded freshness label.

    Returns one of ``missing`` / ``just_updated`` / ``recent`` / ``older`` /
    ``unknown``. Purely a function of the (already computed) age and metadata
    state; it makes no quality or readiness judgment.
    """

    if metadata_state == "missing":
        return "missing"
    if metadata_state != "present" or age_seconds is None:
        return "unknown"
    if age_seconds <= FRESHNESS_JUST_UPDATED_SECONDS:
        return "just_updated"
    if age_seconds <= FRESHNESS_RECENT_SECONDS:
        return "recent"
    return "older"


def _file_mtime(path: Path) -> Optional[float]:
    """Return the file's modified-time epoch, or ``None`` if unavailable."""

    try:
        if not path.is_file():
            return None
        return path.stat().st_mtime
    except OSError:
        return None


def file_freshness(path: Path, now_ts: float) -> Dict[str, Any]:
    """Return safe filesystem freshness metadata for one fixed file.

    Only a safe relative label (the fixed filename), existence, a UTC ISO-8601
    modified time, a nonnegative integer age, and a bounded metadata/age state
    are returned. No absolute path, no raw file content, and no non-metadata
    field is exposed.
    """

    label = path.name
    try:
        exists = path.is_file()
    except OSError:  # pragma: no cover - defensive: treat as missing
        exists = False
    if not exists:
        return {
            "path_label": label,
            "exists": False,
            "modified_at_utc": None,
            "age_seconds": None,
            "metadata_state": "missing",
            "age_label": "missing",
        }
    try:
        mtime = path.stat().st_mtime
    except OSError:  # pragma: no cover - defensive: unreadable stat
        return {
            "path_label": label,
            "exists": True,
            "modified_at_utc": None,
            "age_seconds": None,
            "metadata_state": "unavailable",
            "age_label": "unknown",
        }
    age_seconds = max(0, int(now_ts - mtime))
    return {
        "path_label": label,
        "exists": True,
        "modified_at_utc": _iso_utc(mtime),
        "age_seconds": age_seconds,
        "metadata_state": "present",
        "age_label": age_label(age_seconds, "present"),
    }


def _ordering_state(
    derived_mtime: Optional[float], capture_mtime: Optional[float]
) -> str:
    """Compare two file modified times into a bounded ordering state."""

    if derived_mtime is None or capture_mtime is None:
        return "not_comparable"
    if derived_mtime < capture_mtime:
        return "older_than_capture"
    return "same_or_newer_than_capture"


def _sequence_coherence(
    derived_summary: Mapping[str, Any],
    derived_mtime: Optional[float],
    capture_summary: Mapping[str, Any],
    capture_mtime: Optional[float],
    *,
    compare_counts: bool = False,
    include_digest: bool = False,
) -> Dict[str, Any]:
    """Derive a bounded coherence entry for one derived artifact vs capture.

    ``state`` is the filesystem ordering (``not_comparable`` /
    ``same_or_newer_than_capture`` / ``older_than_capture``). ``flags`` carries
    additional safe mismatch signals drawn only from the existing safe summaries
    (packet ids, counts, digest state). ``metadata_only_no_claim`` is always
    present to reinforce that this is metadata, not a quality claim.
    """

    state = _ordering_state(derived_mtime, capture_mtime)
    flags: List[str] = []

    derived_id = derived_summary.get("packet_id")
    capture_id = capture_summary.get("packet_id")
    if derived_id and capture_id and derived_id != capture_id:
        flags.append("packet_id_mismatch")

    if compare_counts:
        d_counts = derived_summary.get("counts")
        c_counts = capture_summary.get("counts")
        if isinstance(d_counts, dict) and isinstance(c_counts, dict):
            for key in ("total", "captured", "excluded"):
                d_val = d_counts.get(key)
                c_val = c_counts.get(key)
                if (
                    isinstance(d_val, int)
                    and isinstance(c_val, int)
                    and d_val != c_val
                ):
                    flags.append("counts_mismatch")
                    break

    if include_digest:
        derived_state = derived_summary.get("state")
        if derived_state == "digest_invalid":
            flags.append("digest_invalid")
        elif derived_state == "digest_unverifiable":
            flags.append("digest_unverifiable")

    flags.append("metadata_only_no_claim")
    return {"state": state, "flags": flags}


def _display_root(root: Path) -> str:
    try:
        rel = root.resolve().relative_to(_REPO_ROOT.resolve())
        return str(rel)
    except ValueError:  # pragma: no cover - resolve keeps root inside repo
        return root.name


def build_artifact_status(
    root: Optional[Path] = None, now: Optional[datetime] = None
) -> Dict[str, Any]:
    """Assemble the read-only local artifact status payload.

    Pure function over the local filesystem. Reads at most the four fixed
    artifact files (content plus modified-time metadata), returns
    counts/states/digests and safe freshness/coherence metadata only, and
    performs no provider, network, model, tool, or CLI call.

    ``now`` may be injected (a timezone-aware UTC ``datetime``) so freshness age
    labels are deterministic in tests; when omitted the current UTC time is
    used. Sequence-coherence ordering compares file modified times only and is
    independent of ``now``.
    """

    resolved = root if root is not None else resolve_artifact_root()
    now_dt = now if now is not None else _utcnow()
    now_ts = now_dt.timestamp()

    capture = summarize_capture(resolved)
    packet = summarize_evidence_packet(resolved)
    anchor = summarize_anchor_preflight(resolved)
    lift = summarize_lift_preflight(resolved)

    detected = any(
        section.get("state") != "missing"
        for section in (capture, packet, anchor, lift)
    )

    capture_path = resolved / CAPTURE_FILENAME
    packet_path = resolved / EVIDENCE_PACKET_FILENAME
    anchor_path = resolved / ANCHOR_PREFLIGHT_FILENAME
    lift_path = resolved / LIFT_PREFLIGHT_FILENAME

    capture_mtime = _file_mtime(capture_path)
    packet_mtime = _file_mtime(packet_path)
    anchor_mtime = _file_mtime(anchor_path)
    lift_mtime = _file_mtime(lift_path)

    freshness = {
        "files": {
            "capture": file_freshness(capture_path, now_ts),
            "evidence_packet": file_freshness(packet_path, now_ts),
            "anchor_preflight": file_freshness(anchor_path, now_ts),
            "lift_preflight": file_freshness(lift_path, now_ts),
        },
        "sequence_coherence": {
            "evidence_packet_vs_capture": _sequence_coherence(
                packet,
                packet_mtime,
                capture,
                capture_mtime,
                compare_counts=True,
                include_digest=True,
            ),
            "anchor_preflight_vs_capture": _sequence_coherence(
                anchor, anchor_mtime, capture, capture_mtime
            ),
            "lift_preflight_vs_capture": _sequence_coherence(
                lift, lift_mtime, capture, capture_mtime
            ),
        },
        "boundaries": list(FRESHNESS_BOUNDARY_TEXTS),
    }

    return {
        "artifact_root": _display_root(resolved),
        "status_generated_at_utc": now_dt.isoformat(),
        "detected": detected,
        "no_artifacts_message": NO_ARTIFACTS_TEXT,
        "capture": capture,
        "evidence_packet": packet,
        "anchor_preflight": anchor,
        "lift_preflight": lift,
        "freshness": freshness,
        "boundaries": list(BOUNDARY_TEXTS),
    }
