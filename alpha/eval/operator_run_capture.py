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


# ---------------------------------------------------------------------------
# Substantive Lift preflight
# (OPERATOR-RUN-CAPTURE-SUBSTANTIVE-LIFT-PREFLIGHT-CLI-001)
#
# Optional, read-only structural preflight over an existing capture file. For
# each case that has both a prompt and a routed output, it runs the portable
# Substantive Lift wording checker so the operator can catch lift/case-anchor
# structure problems before qualitative review. It never mutates the capture,
# never touches the export packet schema, and never scores, ranks, blinds, or
# picks winners.
# ---------------------------------------------------------------------------

LIFT_PREFLIGHT_LANE_ID = "OPERATOR-RUN-CAPTURE-SUBSTANTIVE-LIFT-PREFLIGHT-CLI-001"
LIFT_PREFLIGHT_REPORT_SCHEMA_VERSION = "operator_lift_preflight_report/v1"

# Boundary statement repeated in every report and rendered output. A preflight
# pass is a structural wording result only.
LIFT_PREFLIGHT_BOUNDARY = (
    "Structural wording preflight only: not answer quality, not benchmark "
    "validation, not readiness, and not Alpha superiority. A pass means only "
    "that the configured local structural checks held for the supplied "
    "routed output text and prompt."
)

LIFT_PREFLIGHT_STATES = (
    "invalid_case",
    "excluded_case",
    "missing_prompt",
    "missing_routed_output",
    "safe_out_not_applicable",
    "structural_pass",
    "structural_fail",
)

# States that mean the capture needs operator attention before qualitative
# review; the CLI maps any of these to a non-zero exit code.
LIFT_PREFLIGHT_ATTENTION_STATES = frozenset(
    {"invalid_case", "missing_prompt", "missing_routed_output", "structural_fail"}
)

# Bounded SAFE-OUT responses are honest non-answers: the lift wording contract
# does not apply to them, so the preflight reports them as not applicable
# instead of failing them. Explicit prefix match only, mirroring the portable
# honesty guard's explicit-prefix style.
_LIFT_PREFLIGHT_SAFEOUT_PREFIX = "safe-out:"
_LIFT_PREFLIGHT_SOLUTION_LABEL = "solution:"


def _lift_preflight_solution_text(routed_output: str) -> str:
    """Return the SOLUTION body when an operator pasted a full envelope.

    Capture docs ask operators to paste the routed Alpha output they collected,
    which can be a full ChatGPT/Alpha Solver response that begins with a
    ``SOLUTION:`` label before the six Substantive Lift moves. The portable
    checker intentionally checks the six-move solution text itself, so the
    preflight peels only that narrow leading label when it is present.
    """
    stripped = routed_output.strip()
    if stripped.lower().startswith(_LIFT_PREFLIGHT_SOLUTION_LABEL):
        return stripped[len(_LIFT_PREFLIGHT_SOLUTION_LABEL) :].lstrip()
    return routed_output


def _lift_structural_flags(checker_result: Dict[str, Any]) -> List[str]:
    """Name the structural checks that did not hold, for operator display."""
    flags: List[str] = []
    if checker_result.get("missing_moves"):
        flags.append(f"missing_moves={checker_result['missing_moves']}")
    if checker_result.get("empty_moves"):
        flags.append(f"empty_moves={checker_result['empty_moves']}")
    if not checker_result.get("missing_moves") and not checker_result.get("order_ok"):
        flags.append("lift_block_out_of_order")
    if not checker_result.get("opens_with_intent"):
        flags.append("does_not_open_with_intent")
    if checker_result.get("generic_flags"):
        flags.append(f"generic_hedges={checker_result['generic_flags']}")
    if checker_result.get("weak_next_action"):
        flags.append("weak_next_action")
    if checker_result.get("filler_flags"):
        flags.append(f"filler={checker_result['filler_flags']}")
    if checker_result.get("unanchored_lift"):
        flags.append("unanchored_lift")
    if checker_result.get("weak_anchor_distribution"):
        flags.append("weak_anchor_distribution")
    if checker_result.get("intent_restates_prompt"):
        flags.append("intent_restates_prompt")
    return flags


def _lift_preflight_capture_case_shape_errors(case: Any, index: int) -> List[str]:
    """Validate capture-case shape before Substantive Lift preflight.

    The preflight has separate states for empty prompt and empty routed output,
    so this helper reuses the capture-case validator while allowing those two
    text fields to be blank when their keys are present. Missing keys, unknown
    keys, invalid statuses, invalid metadata, and malformed excluded cases stay
    schema errors and must never be reported as structural lift results.
    """
    if not isinstance(case, dict):
        return _validate_capture_case(case, index)
    validation_case = dict(case)
    if "prompt" in validation_case and not _is_nonempty_str(
        validation_case.get("prompt")
    ):
        validation_case["prompt"] = "preflight prompt placeholder"
    if "routed_output" in validation_case and not _is_nonempty_str(
        validation_case.get("routed_output")
    ):
        validation_case["routed_output"] = "preflight routed output placeholder"
    return _validate_capture_case(validation_case, index)


def _lift_preflight_case(case: Any, index: int, checker: Any) -> Dict[str, Any]:
    finding: Dict[str, Any] = {
        "task_id": f"cases[{index}]",
        "state": "invalid_case",
        "anchor_checks_vacuous": False,
        "case_anchor_count": 0,
        "structural_flags": [],
        "detail": "",
    }
    shape_errors = _lift_preflight_capture_case_shape_errors(case, index)
    if shape_errors:
        finding["detail"] = "; ".join(shape_errors)
        return finding
    if _is_nonempty_str(case.get("task_id")):
        finding["task_id"] = case["task_id"]

    if case.get("validation_status") == "excluded":
        finding["state"] = "excluded_case"
        finding["detail"] = "case was excluded during capture; preflight skipped"
        return finding

    prompt = case.get("prompt")
    if not _is_nonempty_str(prompt):
        finding["state"] = "missing_prompt"
        finding["detail"] = (
            "prompt is missing or empty; the preflight needs the prompt text"
        )
        return finding

    routed_output = case.get("routed_output")
    if not _is_nonempty_str(routed_output):
        finding["state"] = "missing_routed_output"
        finding["detail"] = (
            "routed_output is missing or empty; there is no text to preflight"
        )
        return finding

    solution_text = _lift_preflight_solution_text(routed_output)

    if solution_text.strip().lower().startswith(_LIFT_PREFLIGHT_SAFEOUT_PREFIX):
        finding["state"] = "safe_out_not_applicable"
        finding["detail"] = (
            "routed output is a bounded SAFE-OUT response; the Substantive "
            "Lift wording contract does not apply to honest non-answers"
        )
        return finding

    checker_result = checker(solution_text, prompt=prompt)
    finding["case_anchor_count"] = len(checker_result.get("case_anchors", []))
    finding["anchor_checks_vacuous"] = finding["case_anchor_count"] == 0
    finding["checker"] = checker_result
    if checker_result.get("ok"):
        finding["state"] = "structural_pass"
        finding["detail"] = "configured structural wording checks held"
    else:
        finding["state"] = "structural_fail"
        finding["structural_flags"] = _lift_structural_flags(checker_result)
        finding["detail"] = "; ".join(finding["structural_flags"])
    return finding


def lift_preflight_capture(capture: Any) -> Dict[str, Any]:
    """Run the read-only Substantive Lift structural preflight over a capture.

    Uses ``check_substantive_lift(routed_output, prompt=prompt)`` from the
    portable spec monolith for every case that carries both texts. The result
    is a local report structure, not an evidence packet: it carries no scores,
    ranks, winners, blind labels, source maps, or identity maps, and the
    input capture is never modified. A ``structural_pass`` state means only
    that the configured local structural checks held for the supplied text
    and prompt; it is not an answer-quality judgment.
    """
    # Local import so the harness stays importable on its own; the checker
    # lives in the repo-root portable spec monolith.
    from alpha_solver_portable import check_substantive_lift

    if not isinstance(capture, dict):
        raise ValueError("lift preflight: capture top level must be a JSON object")
    cases = capture.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("lift preflight: capture cases must be a non-empty list")

    findings = [
        _lift_preflight_case(case, index, check_substantive_lift)
        for index, case in enumerate(cases)
    ]
    counts = {state: 0 for state in LIFT_PREFLIGHT_STATES}
    for finding in findings:
        counts[finding["state"]] += 1
    needs_attention = [
        finding["task_id"]
        for finding in findings
        if finding["state"] in LIFT_PREFLIGHT_ATTENTION_STATES
    ]
    packet_id = (
        capture["packet_id"] if _is_nonempty_str(capture.get("packet_id")) else None
    )
    return {
        "schema_version": LIFT_PREFLIGHT_REPORT_SCHEMA_VERSION,
        "lane_id": LIFT_PREFLIGHT_LANE_ID,
        "packet_id": packet_id,
        "boundary": LIFT_PREFLIGHT_BOUNDARY,
        "cases": findings,
        "summary": {
            "counts": {**counts, "total": len(findings)},
            "needs_attention": needs_attention,
        },
    }


def render_lift_preflight_text(report: Dict[str, Any]) -> str:
    """Render a preflight report as operator-readable console text."""
    lines = [
        (
            f"Substantive Lift preflight for packet {report['packet_id']!r} "
            f"({report['summary']['counts']['total']} cases)"
        ),
        f"boundary: {report['boundary']}",
    ]
    for finding in report["cases"]:
        line = f"  {finding['task_id']}: {finding['state']}"
        if finding["state"] in ("structural_pass", "structural_fail"):
            if finding["anchor_checks_vacuous"]:
                line += (
                    " (anchor checks vacuous: prompt has no extractable anchors)"
                )
            else:
                line += f" (anchors={finding['case_anchor_count']})"
        if finding["state"] not in ("structural_pass",) and finding["detail"]:
            line += f" — {finding['detail']}"
        lines.append(line)
    counts = report["summary"]["counts"]
    summary_bits = [
        f"{state}={counts[state]}"
        for state in LIFT_PREFLIGHT_STATES
        if counts[state]
    ]
    lines.append("summary: " + (" ".join(summary_bits) if summary_bits else "empty"))
    needs_attention = report["summary"]["needs_attention"]
    if needs_attention:
        lines.append("needs attention: " + ", ".join(needs_attention))
    else:
        lines.append("needs attention: none")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Case-packet anchor preflight
# (OPERATOR-RUN-CAPTURE-CASE-PACKET-ANCHOR-PREFLIGHT-CLI-001)
#
# Authoring-time companion to the Substantive Lift preflight above. Given a
# case packet (before any manual capture), it reports which prompts carry
# extractable case anchors and which do not, so the operator learns up front
# which prompts will actually exercise the lift contract's anchoring checks
# instead of discovering vacuous anchor coverage after an expensive manual
# run. It only reports anchor presence; it never scores, ranks, compares, or
# judges prompt quality, and anchor-free is informational, not a defect.
# ---------------------------------------------------------------------------

ANCHOR_PREFLIGHT_LANE_ID = "OPERATOR-RUN-CAPTURE-CASE-PACKET-ANCHOR-PREFLIGHT-CLI-001"
ANCHOR_PREFLIGHT_REPORT_SCHEMA_VERSION = "operator_anchor_preflight_report/v1"

ANCHOR_PREFLIGHT_BOUNDARY = (
    "Structural anchor-presence preflight only: it reports whether a prompt "
    "carries extractable case anchors so the operator knows the lift "
    "anchoring checks will be meaningful, not vacuous. Anchor-free is "
    "informational, not a defect; some prompts are legitimately low-headroom. "
    "This is not answer quality, not benchmark validation, not readiness, and "
    "not Alpha superiority."
)

# anchor_bearing: prompt yields >=1 anchor; lift anchoring checks will apply.
# anchor_free: prompt yields no anchors; lift anchoring checks would be vacuous.
# invalid_case: the case is not a well-formed object with a non-empty prompt.
ANCHOR_PREFLIGHT_STATES = ("invalid_case", "anchor_free", "anchor_bearing")


def _anchor_preflight_case(case: Any, index: int, extract: Any) -> Dict[str, Any]:
    finding: Dict[str, Any] = {
        "task_id": f"cases[{index}]",
        "state": "invalid_case",
        "anchor_count": 0,
        "anchors": [],
        "detail": "",
    }
    if not isinstance(case, dict):
        finding["detail"] = "case is not a JSON object"
        return finding
    if _is_nonempty_str(case.get("task_id")):
        finding["task_id"] = case["task_id"]
    prompt = case.get("prompt")
    if not _is_nonempty_str(prompt):
        finding["detail"] = "prompt is missing or empty; cannot extract anchors"
        return finding

    anchors = list(extract(prompt))
    finding["anchor_count"] = len(anchors)
    finding["anchors"] = anchors
    if anchors:
        finding["state"] = "anchor_bearing"
        finding["detail"] = "lift anchoring checks will apply to this prompt"
    else:
        finding["state"] = "anchor_free"
        finding["detail"] = (
            "no extractable anchors; lift anchoring checks would be vacuous "
            "(fine for a low-headroom prompt; add concrete objects if the "
            "prompt is meant to be high-headroom)"
        )
    return finding


def anchor_preflight_case_packet(
    case_packet: Any, require_anchors: bool = False
) -> Dict[str, Any]:
    """Report per-prompt case-anchor presence for an operator case packet.

    Runs :func:`_extract_case_anchors` from the portable spec monolith over
    each case prompt so the operator can see, before any manual capture, which
    prompts are anchor-bearing and which are anchor-free. The result is a local
    report structure, not a capture or evidence packet: it carries no scores,
    ranks, winners, blind labels, source maps, or identity maps, and it never
    modifies the input. Anchor-free is informational; when ``require_anchors``
    is True the operator is opting into a stricter authoring gate that lists
    anchor-free cases as needing attention.
    """
    from alpha_solver_portable import _extract_case_anchors

    if not isinstance(case_packet, dict):
        raise ValueError("anchor preflight: case packet top level must be an object")
    cases = case_packet.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("anchor preflight: case packet cases must be a non-empty list")

    validation_errors = validate_case_packet(case_packet)
    if validation_errors:
        detail = "case packet failed validation: " + "; ".join(validation_errors)
        findings = []
        for index, case in enumerate(cases):
            task_id = f"cases[{index}]"
            if isinstance(case, dict) and _is_nonempty_str(case.get("task_id")):
                task_id = case["task_id"]
            findings.append(
                {
                    "task_id": task_id,
                    "state": "invalid_case",
                    "anchor_count": 0,
                    "anchors": [],
                    "detail": detail,
                }
            )
    else:
        findings = [
            _anchor_preflight_case(case, index, _extract_case_anchors)
            for index, case in enumerate(cases)
        ]
    counts = {state: 0 for state in ANCHOR_PREFLIGHT_STATES}
    for finding in findings:
        counts[finding["state"]] += 1
    attention_states = {"invalid_case"}
    if require_anchors:
        attention_states = attention_states | {"anchor_free"}
    needs_attention = [
        finding["task_id"]
        for finding in findings
        if finding["state"] in attention_states
    ]
    packet_id = (
        case_packet["packet_id"]
        if _is_nonempty_str(case_packet.get("packet_id"))
        else None
    )
    return {
        "schema_version": ANCHOR_PREFLIGHT_REPORT_SCHEMA_VERSION,
        "lane_id": ANCHOR_PREFLIGHT_LANE_ID,
        "packet_id": packet_id,
        "require_anchors": bool(require_anchors),
        "boundary": ANCHOR_PREFLIGHT_BOUNDARY,
        "cases": findings,
        "summary": {
            "counts": {**counts, "total": len(findings)},
            "needs_attention": needs_attention,
        },
    }


def render_anchor_preflight_text(report: Dict[str, Any]) -> str:
    """Render a case-packet anchor preflight report as operator console text."""
    lines = [
        (
            f"Case-packet anchor preflight for packet {report['packet_id']!r} "
            f"({report['summary']['counts']['total']} cases"
            f"{', require-anchors' if report['require_anchors'] else ''})"
        ),
        f"boundary: {report['boundary']}",
    ]
    for finding in report["cases"]:
        line = f"  {finding['task_id']}: {finding['state']}"
        if finding["state"] == "anchor_bearing":
            line += f" (anchors={finding['anchor_count']})"
        elif finding["detail"]:
            line += f" — {finding['detail']}"
        lines.append(line)
    counts = report["summary"]["counts"]
    summary_bits = [
        f"{state}={counts[state]}"
        for state in ANCHOR_PREFLIGHT_STATES
        if counts[state]
    ]
    lines.append("summary: " + (" ".join(summary_bits) if summary_bits else "empty"))
    needs_attention = report["summary"]["needs_attention"]
    if needs_attention:
        lines.append("needs attention: " + ", ".join(needs_attention))
    else:
        lines.append("needs attention: none")
    return "\n".join(lines)
