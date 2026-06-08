"""Static Self Operator scanner helpers used only by tests.

The helpers in this module scan inert text/JSON fixtures deterministically. They
never import fixture modules, execute fixture code, open network connections, or
call runtime Self Operator surfaces.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "self_operator_static"


@dataclass(frozen=True, order=True)
class StaticFinding:
    """Stable static finding returned by the test-only scanner."""

    id: str
    path: str
    reason: str
    blocked_surface: str
    recommended_stop_state: str = "blocked"

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class SurfaceRule:
    id: str
    blocked_surface: str
    reason: str
    patterns: tuple[str, ...]


SURFACE_RULES: tuple[SurfaceRule, ...] = (
    SurfaceRule(
        "SELF_OPERATOR_PROVIDER_CALL_BLOCKED",
        "provider_calls",
        "detected provider-call surface",
        (r"STATIC_FIXTURE_SURFACE:\s*provider_calls", r"\bprovider_client\.", r"\bhosted_model_call\b"),
    ),
    SurfaceRule(
        "SELF_OPERATOR_EXTERNAL_API_BLOCKED",
        "external_api_calls",
        "detected external API surface",
        (r"STATIC_FIXTURE_SURFACE:\s*external_api_calls", r"\brequests\.(get|post|put|delete)\(", r"\bhttpx\.(get|post|put|delete)\("),
    ),
    SurfaceRule(
        "SELF_OPERATOR_CREDENTIAL_ACCESS_BLOCKED",
        "credential_access",
        "detected credential or secret access surface",
        (r"STATIC_FIXTURE_SURFACE:\s*credential_access", r"\bos\.environ\[", r"\b[A-Z0-9_]*(API_KEY|SECRET|TOKEN)\b"),
    ),
    SurfaceRule(
        "SELF_OPERATOR_BROWSER_AUTOMATION_BLOCKED",
        "browser_automation",
        "detected browser automation surface",
        (r"STATIC_FIXTURE_SURFACE:\s*browser_automation", r"\bplaywright\b", r"\bselenium\b", r"\bbrowser\.new_page\("),
    ),
    SurfaceRule(
        "SELF_OPERATOR_DEPLOYMENT_BLOCKED",
        "deployment",
        "detected deployment surface",
        (r"STATIC_FIXTURE_SURFACE:\s*deployment", r"\bdeploy_(job|target)\b", r"\bkubectl\b", r"\bterraform\b"),
    ),
    SurfaceRule(
        "SELF_OPERATOR_BILLING_BLOCKED",
        "billing",
        "detected billing surface",
        (r"STATIC_FIXTURE_SURFACE:\s*billing", r"\bbilling_(account|portal|meter)\b", r"\bcharge_customer\b"),
    ),
    SurfaceRule(
        "SELF_OPERATOR_ROUTE_EXPOSURE_BLOCKED",
        "route_exposure",
        "detected route, API, CLI, or dashboard exposure surface",
        (r"STATIC_FIXTURE_SURFACE:\s*route_exposure", r"/v1/solve", r"\bdashboard_route\b", r"\bcli_command\b"),
    ),
    SurfaceRule(
        "SELF_OPERATOR_FALLBACK_BLOCKED",
        "fallback",
        "detected fallback promotion surface",
        (r"STATIC_FIXTURE_SURFACE:\s*fallback", r"\bfallback_to_provider\b", r"\bpromote_fallback\b"),
    ),
    SurfaceRule(
        "SELF_OPERATOR_HOSTED_FALLBACK_BLOCKED",
        "hosted_fallback",
        "detected hosted fallback surface",
        (r"STATIC_FIXTURE_SURFACE:\s*hosted_fallback", r"\bhosted_fallback\b", r"\bprovider_fallback\b"),
    ),
    SurfaceRule(
        "SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED",
        "evidence_promotion",
        "detected evidence promotion surface",
        (r"STATIC_FIXTURE_SURFACE:\s*evidence_promotion", r"\bpromote_evidence\b", r"\bmark_runtime_ready\b", r"\bproduction_ready\b"),
    ),
)

FINDING_IDS: tuple[str, ...] = tuple(rule.id for rule in SURFACE_RULES) + (
    "SELF_OPERATOR_APPROVAL_GATE_REQUIRED",
    "SELF_OPERATOR_ARTIFACT_SCHEMA_INCOMPLETE",
    "SELF_OPERATOR_STOP_STATE_REQUIRED",
)

REQUIRED_ARTIFACT_FIELDS: tuple[str, ...] = (
    "schema_version",
    "run_id",
    "lane_id",
    "operator_confirmation",
    "stop_state",
    "findings",
    "evidence_boundary",
)


_REGEX_FLAGS = re.IGNORECASE | re.MULTILINE


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_text_fixture(path: Path | str) -> tuple[str, str]:
    fixture_path = Path(path)
    text = fixture_path.read_text(encoding="utf-8")
    return text, repo_relative(fixture_path)


def scan_path(path: Path | str) -> list[StaticFinding]:
    text, display_path = read_text_fixture(path)
    return scan_text(text, path=display_path)


def scan_paths(paths: Iterable[Path | str]) -> list[StaticFinding]:
    findings: list[StaticFinding] = []
    for path in paths:
        findings.extend(scan_path(path))
    return sorted(findings)


def scan_text(text: str, *, path: str = "<text>") -> list[StaticFinding]:
    """Return deterministic findings for inert fixture text."""

    findings: list[StaticFinding] = []
    for rule in SURFACE_RULES:
        if any(re.search(pattern, text, flags=_REGEX_FLAGS) for pattern in rule.patterns):
            findings.append(
                StaticFinding(
                    id=rule.id,
                    path=path,
                    reason=rule.reason,
                    blocked_surface=rule.blocked_surface,
                )
            )

    json_payload = _load_json_if_possible(text)
    if isinstance(json_payload, Mapping):
        findings.extend(_scan_json_payload(json_payload, path=path))

    return sorted(findings)


def finding_ids(findings: Sequence[StaticFinding]) -> set[str]:
    return {finding.id for finding in findings}


def findings_as_dicts(findings: Sequence[StaticFinding]) -> list[dict[str, str]]:
    return [finding.to_dict() for finding in findings]


def _load_json_if_possible(text: str) -> object | None:
    stripped = text.strip()
    if not stripped or stripped[0] not in "[{":
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return None


def _scan_json_payload(payload: Mapping[str, object], *, path: str) -> list[StaticFinding]:
    findings: list[StaticFinding] = []
    approval = payload.get("operator_confirmation")
    if not isinstance(approval, Mapping) or approval.get("explicit") is not True:
        findings.append(
            StaticFinding(
                id="SELF_OPERATOR_APPROVAL_GATE_REQUIRED",
                path=path,
                reason="missing explicit operator confirmation",
                blocked_surface="approval_gate",
            )
        )

    missing_fields = [field for field in REQUIRED_ARTIFACT_FIELDS if field not in payload]
    if missing_fields:
        findings.append(
            StaticFinding(
                id="SELF_OPERATOR_ARTIFACT_SCHEMA_INCOMPLETE",
                path=path,
                reason="missing required artifact fields: " + ", ".join(missing_fields),
                blocked_surface="artifact_schema",
            )
        )

    stop_state = payload.get("stop_state")
    if not isinstance(stop_state, str) or not stop_state.strip():
        findings.append(
            StaticFinding(
                id="SELF_OPERATOR_STOP_STATE_REQUIRED",
                path=path,
                reason="missing required stop state",
                blocked_surface="stop_state",
            )
        )
    return findings
