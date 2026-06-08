"""Static artifact-schema tests for inert Self Operator fixtures."""
from __future__ import annotations

from tests.helpers.self_operator_static_scan import FIXTURE_ROOT, finding_ids, scan_path


def test_incomplete_artifact_schema_returns_schema_incomplete() -> None:
    findings = scan_path(FIXTURE_ROOT / "incomplete_artifact_schema.json")
    assert "SELF_OPERATOR_ARTIFACT_SCHEMA_INCOMPLETE" in finding_ids(findings)
    schema_finding = next(
        finding for finding in findings if finding.id == "SELF_OPERATOR_ARTIFACT_SCHEMA_INCOMPLETE"
    )
    assert schema_finding.blocked_surface == "artifact_schema"
    assert "stop_state" in schema_finding.reason
    assert schema_finding.recommended_stop_state == "blocked"
