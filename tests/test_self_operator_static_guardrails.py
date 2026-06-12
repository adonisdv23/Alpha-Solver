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


def _write_final_packet_fixture(root: Path) -> None:
    packet_dir = root / "docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/closeout"
    packet_dir.mkdir(parents=True)
    (packet_dir / "README.md").write_text(
        "\n".join(
            [
                "behavior_evidence=False",
                "no_hosted_fallback=True",
                "no_provider_keys_required=True",
                "NO_FURTHER_LEVEL_3_VALIDATION_LANES_SELECTED",
                "LEVEL_3_VALIDATION_EXECUTION_ACCEPTED_AS_ARTIFACT_COMPLETE_NON_PROMOTIONAL_LOCAL_ORCHESTRATION_EVIDENCE",
            ]
        ),
        encoding="utf-8",
    )


def test_checker_scope_includes_post_packets_council_bundle_and_legacy_paths() -> None:
    from scripts import check_local_llm_doc_paths as doc_paths
    from scripts import check_local_llm_evidence_boundaries as evidence_boundaries

    post_packet = Path(
        "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-scope-extension/sample.md"
    )
    council_bundle = Path(
        "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle/README.md"
    )
    legacy_run_packet = Path(
        "docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/closeout/README.md"
    )
    legacy_operator_doc = Path("docs/local_llm_solver_orchestration_operator_guide/README.md")

    assert evidence_boundaries.is_relevant_doc(post_packet)
    assert evidence_boundaries.is_relevant_doc(council_bundle)
    assert evidence_boundaries.is_relevant_doc(legacy_run_packet)
    assert evidence_boundaries.is_relevant_doc(legacy_operator_doc)

    assert doc_paths.is_scanned_doc(post_packet)
    assert doc_paths.is_scanned_doc(council_bundle)
    assert doc_paths.is_scanned_doc(legacy_run_packet)
    assert doc_paths.is_scanned_doc(legacy_operator_doc)
    assert doc_paths.COUNCIL_AUDIT_EVIDENCE_BUNDLE_DIR in doc_paths.REQUIRED_SOURCE_OF_TRUTH_PATHS


def test_evidence_boundary_checker_catches_forbidden_readiness_term_in_post_packet_fixture(tmp_path: Path) -> None:
    from scripts import check_local_llm_evidence_boundaries as evidence_boundaries

    _write_final_packet_fixture(tmp_path)
    rel_path = Path(
        "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-scope-extension/sample.md"
    )
    sample = tmp_path / rel_path
    sample.parent.mkdir(parents=True)
    sample.write_text("# Sample\n\nThis packet asserts production readiness for Alpha Solver.\n", encoding="utf-8")

    findings = evidence_boundaries.check_paths([rel_path], root=tmp_path)

    assert any(
        finding.path == rel_path
        and finding.phrase == "production readiness"
        and "lacks nearby boundary language" in finding.message
        for finding in findings
    )


def test_doc_path_checker_checks_references_in_post_packet_fixture(tmp_path: Path) -> None:
    from scripts import check_local_llm_doc_paths as doc_paths

    rel_path = Path(
        "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-scope-extension/sample.md"
    )
    missing_reference = (
        "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-scope-extension/missing.md"
    )
    sample = tmp_path / rel_path
    sample.parent.mkdir(parents=True)
    sample.write_text(f"# Sample\n\nSee `{missing_reference}`.\n", encoding="utf-8")

    # Required source-of-truth directories are present so this fixture isolates missing reference behavior.
    for required_path in doc_paths.REQUIRED_SOURCE_OF_TRUTH_PATHS:
        (tmp_path / required_path).mkdir(parents=True, exist_ok=True)

    findings = doc_paths.check_paths([rel_path], root=tmp_path)

    assert any(
        finding.path == rel_path
        and finding.reference == missing_reference
        and "does not exist" in finding.message
        for finding in findings
    )


def test_evidence_boundary_checker_does_not_treat_before_as_boundary_language(tmp_path: Path) -> None:
    from scripts import check_local_llm_evidence_boundaries as evidence_boundaries

    _write_final_packet_fixture(tmp_path)
    rel_path = Path(
        "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-scope-extension/before-sample.md"
    )
    sample = tmp_path / rel_path
    sample.parent.mkdir(parents=True)
    sample.write_text(
        "# Sample\n\n"
        "The team will review sequencing before any later work.\n"
        "This packet asserts production readiness for Alpha Solver.\n",
        encoding="utf-8",
    )

    findings = evidence_boundaries.check_paths([rel_path], root=tmp_path)

    assert any(finding.path == rel_path and finding.phrase == "production readiness" for finding in findings)


def test_evidence_boundary_checker_ignores_generic_no_or_not_far_from_forbidden_phrase(tmp_path: Path) -> None:
    from scripts import check_local_llm_evidence_boundaries as evidence_boundaries

    _write_final_packet_fixture(tmp_path)
    rel_path = Path(
        "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-scope-extension/generic-no-not.md"
    )
    sample = tmp_path / rel_path
    sample.parent.mkdir(parents=True)
    sample.write_text(
        "# Sample\n\n"
        "No implementation work was performed in this fixture.\n"
        "This sentence is neutral filler.\n"
        "This sentence is also neutral filler.\n"
        "This note is not about claims.\n"
        "This packet asserts production readiness for Alpha Solver.\n",
        encoding="utf-8",
    )

    findings = evidence_boundaries.check_paths([rel_path], root=tmp_path)

    assert any(finding.path == rel_path and finding.phrase == "production readiness" for finding in findings)


def test_evidence_boundary_checker_allows_explicit_nearby_readiness_boundary(tmp_path: Path) -> None:
    from scripts import check_local_llm_evidence_boundaries as evidence_boundaries

    _write_final_packet_fixture(tmp_path)
    rel_path = Path(
        "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-scope-extension/explicit-boundary.md"
    )
    sample = tmp_path / rel_path
    sample.parent.mkdir(parents=True)
    sample.write_text(
        "# Sample\n\n"
        "This does not claim production readiness.\n"
        "No readiness claim is made.\n",
        encoding="utf-8",
    )

    findings = evidence_boundaries.check_paths([rel_path], root=tmp_path)

    assert not [finding for finding in findings if finding.path == rel_path]
