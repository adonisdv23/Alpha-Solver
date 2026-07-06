"""Local-only operator run capture harness (ALPHA-SOLVER-OPERATOR-RUN-CAPTURE-HARNESS-MVP-001).

This module turns manually generated routed-vs-plain operator runs into a
normalized, machine-validated evidence packet. It is a lab notebook, not a
runner:

- It performs no provider calls, no hosted or local model calls, no tool
  execution, and no network access.
- It does not score, rank, blind, or unblind outputs, and it rejects unknown
  fields so scoring or identity-map data cannot be smuggled into a packet.
- A produced packet records what an operator captured for specific task IDs;
  it does not claim readiness, benchmark results, or output quality.

Workflow: scaffold a capture file from a case packet, let the operator paste
plain-baseline output, routed Alpha output, and route metadata per task, then
validate and export a byte-stable JSON evidence packet suitable for later
(separately authorized) blind scoring or replay lanes.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

LANE_ID = "ALPHA-SOLVER-OPERATOR-RUN-CAPTURE-HARNESS-MVP-001"
CAPTURE_SCHEMA_VERSION = "operator_run_capture/v1"
PACKET_SCHEMA_VERSION = "operator_run_capture_packet/v1"
CAPTURE_MODE = "operator_manual"

VALIDATION_STATUSES = ("pending", "captured", "excluded")

CASE_PACKET_REQUIRED_KEYS = frozenset({"packet_id", "cases"})
CASE_PACKET_ALLOWED_KEYS = CASE_PACKET_REQUIRED_KEYS | {"description"}
CASE_REQUIRED_KEYS = frozenset({"task_id", "prompt"})
CASE_ALLOWED_KEYS = CASE_REQUIRED_KEYS | {"notes"}

CAPTURE_REQUIRED_KEYS = frozenset(
    {"schema_version", "packet_id", "capture_mode", "cases"}
)
CAPTURE_ALLOWED_KEYS = CAPTURE_REQUIRED_KEYS | {"description"}
CAPTURE_CASE_REQUIRED_KEYS = frozenset(
    {
        "task_id",
        "prompt",
        "baseline_output",
        "routed_output",
        "route_metadata",
        "validation_status",
    }
)
CAPTURE_CASE_ALLOWED_KEYS = CAPTURE_CASE_REQUIRED_KEYS | {"notes", "exclusion_reason"}

# Boundary attestation embedded in every exported packet. These statements
# cover only what this harness itself did during capture and export.
HARNESS_BOUNDARIES = {
    "provider_calls_made_by_harness": False,
    "hosted_model_calls_made_by_harness": False,
    "local_model_calls_made_by_harness": False,
    "tool_execution_performed_by_harness": False,
    "network_access_used_by_harness": False,
    "scoring_performed": False,
    "blinding_or_unblinding_performed": False,
    "readiness_or_quality_claims_made": False,
}


def _is_nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def load_json(path: Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_case_packet(packet: Any) -> List[str]:
    """Validate an operator-authored case packet. Returns a list of errors."""
    errors: List[str] = []
    if not isinstance(packet, dict):
        return ["case packet: top level must be a JSON object"]
    unknown = sorted(set(packet) - CASE_PACKET_ALLOWED_KEYS)
    if unknown:
        errors.append(f"case packet: unknown keys not allowed: {unknown}")
    missing = sorted(CASE_PACKET_REQUIRED_KEYS - set(packet))
    if missing:
        errors.append(f"case packet: missing required keys: {missing}")
    if "packet_id" in packet and not _is_nonempty_str(packet["packet_id"]):
        errors.append("case packet: packet_id must be a non-empty string")
    cases = packet.get("cases")
    if "cases" in packet:
        if not isinstance(cases, list) or not cases:
            errors.append("case packet: cases must be a non-empty list")
        else:
            seen: set = set()
            for index, case in enumerate(cases):
                label = f"case packet: cases[{index}]"
                if not isinstance(case, dict):
                    errors.append(f"{label}: must be a JSON object")
                    continue
                unknown = sorted(set(case) - CASE_ALLOWED_KEYS)
                if unknown:
                    errors.append(f"{label}: unknown keys not allowed: {unknown}")
                missing = sorted(CASE_REQUIRED_KEYS - set(case))
                if missing:
                    errors.append(f"{label}: missing required keys: {missing}")
                task_id = case.get("task_id")
                if "task_id" in case:
                    if not _is_nonempty_str(task_id):
                        errors.append(f"{label}: task_id must be a non-empty string")
                    elif task_id in seen:
                        errors.append(f"{label}: duplicate task_id {task_id!r}")
                    else:
                        seen.add(task_id)
                if "prompt" in case and not _is_nonempty_str(case.get("prompt")):
                    errors.append(f"{label}: prompt must be a non-empty string")
    return errors


def scaffold_capture(case_packet: Dict[str, Any]) -> Dict[str, Any]:
    """Build an empty capture structure from a validated case packet."""
    errors = validate_case_packet(case_packet)
    if errors:
        raise ValueError("invalid case packet: " + "; ".join(errors))
    capture: Dict[str, Any] = {
        "schema_version": CAPTURE_SCHEMA_VERSION,
        "packet_id": case_packet["packet_id"],
        "capture_mode": CAPTURE_MODE,
        "cases": [],
    }
    if _is_nonempty_str(case_packet.get("description")):
        capture["description"] = case_packet["description"]
    for case in case_packet["cases"]:
        entry: Dict[str, Any] = {
            "task_id": case["task_id"],
            "prompt": case["prompt"],
            "baseline_output": "",
            "routed_output": "",
            "route_metadata": {},
            "validation_status": "pending",
        }
        if _is_nonempty_str(case.get("notes")):
            entry["notes"] = case["notes"]
        capture["cases"].append(entry)
    return capture


def _validate_capture_case(case: Any, index: int) -> List[str]:
    label = f"cases[{index}]"
    if not isinstance(case, dict):
        return [f"{label}: must be a JSON object"]
    errors: List[str] = []
    unknown = sorted(set(case) - CAPTURE_CASE_ALLOWED_KEYS)
    if unknown:
        errors.append(f"{label}: unknown keys not allowed: {unknown}")
    missing = sorted(CAPTURE_CASE_REQUIRED_KEYS - set(case))
    if missing:
        errors.append(f"{label}: missing required keys: {missing}")
    if "task_id" in case and not _is_nonempty_str(case.get("task_id")):
        errors.append(f"{label}: task_id must be a non-empty string")
    if "prompt" in case and not _is_nonempty_str(case.get("prompt")):
        errors.append(f"{label}: prompt must be a non-empty string")
    status = case.get("validation_status")
    if "validation_status" in case and status not in VALIDATION_STATUSES:
        errors.append(
            f"{label}: validation_status must be one of {list(VALIDATION_STATUSES)}"
        )
        return errors
    if status == "captured":
        if not _is_nonempty_str(case.get("baseline_output")):
            errors.append(
                f"{label}: captured case requires non-empty baseline_output"
            )
        if not _is_nonempty_str(case.get("routed_output")):
            errors.append(f"{label}: captured case requires non-empty routed_output")
        metadata = case.get("route_metadata")
        if not isinstance(metadata, dict) or not metadata:
            errors.append(
                f"{label}: captured case requires route_metadata as a non-empty object"
            )
    elif status == "excluded":
        if not _is_nonempty_str(case.get("exclusion_reason")):
            errors.append(
                f"{label}: excluded case requires non-empty exclusion_reason"
            )
    return errors


def validate_capture(capture: Any, for_export: bool = False) -> List[str]:
    """Validate a capture file. With for_export=True, also require completion."""
    if not isinstance(capture, dict):
        return ["capture: top level must be a JSON object"]
    errors: List[str] = []
    unknown = sorted(set(capture) - CAPTURE_ALLOWED_KEYS)
    if unknown:
        errors.append(f"capture: unknown keys not allowed: {unknown}")
    missing = sorted(CAPTURE_REQUIRED_KEYS - set(capture))
    if missing:
        errors.append(f"capture: missing required keys: {missing}")
    if (
        "schema_version" in capture
        and capture["schema_version"] != CAPTURE_SCHEMA_VERSION
    ):
        errors.append(
            f"capture: schema_version must be {CAPTURE_SCHEMA_VERSION!r}, "
            f"got {capture['schema_version']!r}"
        )
    if "packet_id" in capture and not _is_nonempty_str(capture["packet_id"]):
        errors.append("capture: packet_id must be a non-empty string")
    if "capture_mode" in capture and capture["capture_mode"] != CAPTURE_MODE:
        errors.append(
            f"capture: capture_mode must be {CAPTURE_MODE!r}, "
            f"got {capture['capture_mode']!r}"
        )
    cases = capture.get("cases")
    if "cases" in capture:
        if not isinstance(cases, list) or not cases:
            errors.append("capture: cases must be a non-empty list")
            cases = []
    else:
        cases = []
    seen: set = set()
    statuses: List[Any] = []
    for index, case in enumerate(cases):
        errors.extend(_validate_capture_case(case, index))
        if isinstance(case, dict):
            task_id = case.get("task_id")
            if _is_nonempty_str(task_id):
                if task_id in seen:
                    errors.append(f"cases[{index}]: duplicate task_id {task_id!r}")
                seen.add(task_id)
            statuses.append(case.get("validation_status"))
    if for_export and not errors:
        pending = [
            case.get("task_id")
            for case in cases
            if case.get("validation_status") == "pending"
        ]
        if pending:
            errors.append(
                "export: all cases must be captured or excluded; "
                f"still pending: {pending}"
            )
        if not any(status == "captured" for status in statuses):
            errors.append("export: at least one case must have status 'captured'")
    return errors


def build_evidence_packet(capture: Dict[str, Any]) -> Dict[str, Any]:
    """Build the normalized evidence packet from a validated capture."""
    errors = validate_capture(capture, for_export=True)
    if errors:
        raise ValueError("invalid capture: " + "; ".join(errors))
    cases = sorted(capture["cases"], key=lambda case: case["task_id"])
    normalized_cases: List[Dict[str, Any]] = []
    for case in cases:
        entry: Dict[str, Any] = {
            "task_id": case["task_id"],
            "prompt": case["prompt"],
            "validation_status": case["validation_status"],
            "baseline_output": case["baseline_output"],
            "routed_output": case["routed_output"],
            "route_metadata": case["route_metadata"],
        }
        if _is_nonempty_str(case.get("notes")):
            entry["notes"] = case["notes"]
        if case["validation_status"] == "excluded":
            entry["exclusion_reason"] = case["exclusion_reason"]
        normalized_cases.append(entry)
    captured = sum(
        1 for case in normalized_cases if case["validation_status"] == "captured"
    )
    excluded = len(normalized_cases) - captured
    packet: Dict[str, Any] = {
        "schema_version": PACKET_SCHEMA_VERSION,
        "lane_id": LANE_ID,
        "packet_id": capture["packet_id"],
        "capture_mode": capture["capture_mode"],
        "harness_boundaries": dict(HARNESS_BOUNDARIES),
        "counts": {
            "captured": captured,
            "excluded": excluded,
            "total": len(normalized_cases),
        },
        "cases": normalized_cases,
    }
    if _is_nonempty_str(capture.get("description")):
        packet["description"] = capture["description"]
    packet["content_digest"] = "sha256:" + _digest(packet)
    return packet


def _digest(packet: Dict[str, Any]) -> str:
    body = {key: value for key, value in packet.items() if key != "content_digest"}
    canonical = json.dumps(
        body, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_packet_digest(packet: Dict[str, Any]) -> bool:
    """Recompute the packet digest; True when it matches the recorded value."""
    recorded = packet.get("content_digest")
    if not _is_nonempty_str(recorded):
        return False
    return recorded == "sha256:" + _digest(packet)


def render_json_bytes(payload: Dict[str, Any]) -> bytes:
    """Render a payload as byte-stable, replay-friendly JSON."""
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    return (text + "\n").encode("utf-8")
