"""Static tests for Level 10 Self Operator guardrails.

These tests scan inert fixture text only. They do not import fixture code, run
models, call providers, open browser automation, deploy, bill, mutate Google
Sheets, expose routes, or promote evidence.
"""
from __future__ import annotations

import json
from pathlib import Path

from tests.helpers.self_operator_static_scan import (
    FINDING_IDS,
    FIXTURE_ROOT,
    StaticFinding,
    finding_ids,
    findings_as_dicts,
    scan_path,
    scan_paths,
)

PROMPT_PACK = Path(
    "docs/evals/runs/"
    "alpha-solver-post-level-3-level-9-self-operator-level-10-code-prompt-pack"
)
REQUIRED_OPERATOR_CONFIRMATION_STOP = "stop if explicit operator confirmation is missing"

def fixture(name: str) -> Path:
    return FIXTURE_ROOT / name


def ids_for(name: str) -> set[str]:
    return finding_ids(scan_path(fixture(name)))


def test_clean_inert_fixture_returns_no_findings() -> None:
    assert scan_path(fixture("clean_noop.py.txt")) == []


def test_provider_fixture_returns_provider_call_block() -> None:
    findings = scan_path(fixture("forbidden_provider_call.py.txt"))
    assert ids_for("forbidden_provider_call.py.txt") == {"SELF_OPERATOR_PROVIDER_CALL_BLOCKED"}
    assert findings == [
        StaticFinding(
            id="SELF_OPERATOR_PROVIDER_CALL_BLOCKED",
            path="tests/fixtures/self_operator_static/forbidden_provider_call.py.txt",
            reason="detected provider-call surface",
            blocked_surface="provider_calls",
        )
    ]


def test_external_api_fixture_returns_external_api_block() -> None:
    assert ids_for("forbidden_external_api.py.txt") == {"SELF_OPERATOR_EXTERNAL_API_BLOCKED"}


def test_credential_fixture_returns_credential_access_block() -> None:
    assert ids_for("forbidden_credentials.py.txt") == {"SELF_OPERATOR_CREDENTIAL_ACCESS_BLOCKED"}


def test_browser_deployment_billing_fixture_returns_expected_blocks() -> None:
    assert ids_for("forbidden_browser_deploy_billing.py.txt") == {
        "SELF_OPERATOR_BROWSER_AUTOMATION_BLOCKED",
        "SELF_OPERATOR_DEPLOYMENT_BLOCKED",
        "SELF_OPERATOR_BILLING_BLOCKED",
    }


def test_route_cli_dashboard_fixture_returns_route_exposure_block() -> None:
    assert ids_for("forbidden_routes_cli_dashboard.py.txt") == {"SELF_OPERATOR_ROUTE_EXPOSURE_BLOCKED"}


def test_fallback_hosted_fallback_and_evidence_promotion_fixture_returns_expected_blocks() -> None:
    assert ids_for("forbidden_fallback_promotion.py.txt") == {
        "SELF_OPERATOR_FALLBACK_BLOCKED",
        "SELF_OPERATOR_HOSTED_FALLBACK_BLOCKED",
        "SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED",
    }


def test_expected_static_findings_ledger_matches_scanner_output() -> None:
    expected = json.loads(fixture("expected_static_findings.json").read_text(encoding="utf-8"))
    for fixture_name, expected_ids in expected.items():
        assert ids_for(fixture_name) == set(expected_ids), fixture_name


def test_scanner_returns_stable_json_serializable_finding_objects() -> None:
    findings = scan_paths(
        [
            fixture("forbidden_provider_call.py.txt"),
            fixture("forbidden_external_api.py.txt"),
        ]
    )
    finding_dicts = findings_as_dicts(findings)
    assert finding_dicts == sorted(finding_dicts, key=lambda item: (item["id"], item["path"]))
    assert all(
        set(item) == {"id", "path", "reason", "blocked_surface", "recommended_stop_state"}
        for item in finding_dicts
    )
    assert {item["recommended_stop_state"] for item in finding_dicts} == {"blocked"}
    json.dumps(finding_dicts, sort_keys=True)


def test_finding_id_registry_covers_required_static_level_10_ids() -> None:
    assert set(FINDING_IDS) == {
        "SELF_OPERATOR_PROVIDER_CALL_BLOCKED",
        "SELF_OPERATOR_EXTERNAL_API_BLOCKED",
        "SELF_OPERATOR_CREDENTIAL_ACCESS_BLOCKED",
        "SELF_OPERATOR_BROWSER_AUTOMATION_BLOCKED",
        "SELF_OPERATOR_DEPLOYMENT_BLOCKED",
        "SELF_OPERATOR_BILLING_BLOCKED",
        "SELF_OPERATOR_ROUTE_EXPOSURE_BLOCKED",
        "SELF_OPERATOR_FALLBACK_BLOCKED",
        "SELF_OPERATOR_HOSTED_FALLBACK_BLOCKED",
        "SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED",
        "SELF_OPERATOR_APPROVAL_GATE_REQUIRED",
        "SELF_OPERATOR_ARTIFACT_SCHEMA_INCOMPLETE",
        "SELF_OPERATOR_STOP_STATE_REQUIRED",
    }


def test_level_10_prompt_pack_contains_operator_confirmation_hard_stop() -> None:
    prompt_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(PROMPT_PACK.glob("*.md")))
    assert REQUIRED_OPERATOR_CONFIRMATION_STOP in prompt_text
