"""Docs-integrity tests for ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001.

These checks validate the additive, blank side-by-side evidence packet contract
for future Alpha-vs-plain differentiation artifacts. They parse committed docs
only; they do not execute provider calls, score outputs, or create populated
evidence packets.
"""
from __future__ import annotations

from pathlib import Path

SPEC = Path(".specs/ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001.md")
INDEX = Path(".specs/INDEX.md")
TEMPLATE = Path("docs/evals/templates/side_by_side_evidence_packet_template.md")

REQUIRED_ARTIFACTS = (
    "docs/evals/templates/paired_output_capture_template.md",
    "docs/evals/templates/blinded_score_sheet_template.csv",
    "docs/evals/templates/blinding_map_template.csv",
    "docs/evals/templates/comparison_score_table_template.csv",
    "docs/evals/templates/run_report_template.md",
    "docs/evals/RESPONSE_QUALITY_RUBRIC.md",
    "docs/evals/LIFT_DECISION_RULE.md",
    "docs/evals/BLIND_SCORING_PROCEDURE.md",
    "docs/evals/ARTIFACT_PRESERVATION.md",
)

REQUIRED_SECTIONS = (
    "## 1. Packet identity",
    "## 2. Source artifact references",
    "## 3. Prompt under review",
    "## 4. Output capture summary",
    "## 5. Blinded scoring record",
    "## 6. Unblinding record",
    "## 7. Fourteen-dimension scores",
    "## 8. Lift / polish / total decision aid",
    "## 9. Expert-envelope evidence",
    "## 10. Material constraints, assumptions, and risks",
    "## 11. Defects, regressions, and over-interrogation",
    "## 12. Evidence-limited explanation",
    "## 13. Conservative interpretation",
    "## 14. Redactions performed",
    "## 15. Follow-up tickets",
    "## 16. Non-claims",
)

DIMENSION_KEYS = (
    "d01_intent",
    "d02_direct",
    "d03_structure",
    "d04_assumptions",
    "d05_hidden_constraints",
    "d06_risk_failure",
    "d07_claim_boundary",
    "d08_evidence_uncertainty",
    "d09_decision",
    "d10_next_actions",
    "d11_specificity",
    "d12_brevity",
    "d13_safety",
    "d14_comparative_value",
)

IDENTITY_AND_SOURCE_FIELDS = (
    "packet_id",
    "comparison_id",
    "parent_run_id",
    "run_directory",
    "prompt_id",
    "prompt_family",
    "difficulty_headroom",
    "evidence_strength",
    "non_claims_confirmed",
    "blinded_score_sheet path",
    "blinding_map path",
    "paired_output_capture path",
    "comparison_score_table path",
    "run_report path",
)

LIFT_POLISH_LENGTH_FIELDS = (
    "plain_total",
    "alpha_total",
    "total_delta",
    "lift_delta",
    "polish_delta",
    "winning_surface",
    "lift_qualified",
    "material_constraint_verified",
    "polish_only_flag",
    "length_ratio",
)

EXPERT_ENVELOPE_FIELDS = (
    "considerations",
    "assumptions",
    "material/correct tags",
    "confidence",
    "mode",
    "clarifying questions",
    "sanitized metadata",
)

STRICT_NON_CLAIMS = (
    "MVP validation",
    "Alpha Solver superiority",
    "answer-quality superiority",
    "production readiness",
    "broad runtime readiness",
    "benchmark success",
    "exact billing accuracy",
    "provider reasoning orchestration",
)

SECRET_LIKE_PATTERNS = ("sk-", "xoxb-", "-----BEGIN", "bearer ")


def _read(path: Path) -> str:
    assert path.exists(), f"missing required file: {path}"
    return path.read_text(encoding="utf-8")


def test_spec_exists_and_is_indexed():
    assert SPEC.exists()
    index = _read(INDEX)
    assert "ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001.md" in index


def test_template_exists_and_references_hardened_artifacts():
    text = _read(TEMPLATE)
    for artifact in REQUIRED_ARTIFACTS:
        assert artifact in text, f"template missing artifact reference: {artifact}"
    lowered = text.lower()
    assert "review/index/interpretation artifact" in lowered
    assert "does not replace" in lowered
    for source_name in (
        "score table",
        "paired-output capture",
        "blinded score sheet",
        "blinding map",
        "run report",
    ):
        assert source_name in lowered


def test_template_includes_required_sections_and_identity_fields():
    text = _read(TEMPLATE)
    for section in REQUIRED_SECTIONS:
        assert section in text, f"template missing section: {section}"
    for field in IDENTITY_AND_SOURCE_FIELDS:
        assert field in text, f"template missing field: {field}"


def test_template_includes_all_14_rubric_dimension_keys():
    text = _read(TEMPLATE)
    for key in DIMENSION_KEYS:
        assert key in text, f"template missing rubric dimension key: {key}"


def test_template_includes_lift_polish_length_fields():
    text = _read(TEMPLATE)
    for field in LIFT_POLISH_LENGTH_FIELDS:
        assert field in text, f"template missing lift/polish/length field: {field}"
    assert "LIFT_DECISION_RULE.md" in text


def test_template_includes_expert_envelope_fields():
    text = _read(TEMPLATE)
    for field in EXPERT_ENVELOPE_FIELDS:
        assert field in text, f"template missing expert-envelope field: {field}"


def test_template_includes_defects_and_over_interrogation():
    text = _read(TEMPLATE)
    lowered = text.lower()
    assert "defects, regressions, and over-interrogation" in lowered
    assert "over-interrogation defect category" in text
    assert "unnecessary clarification" in lowered
    assert "excessive caveats" in lowered


def test_template_enforces_redaction_and_storage_boundaries():
    text = _read(TEMPLATE)
    lowered = text.lower()
    for phrase in (
        "redactions performed",
        "storage boundary",
        "sanitized",
        "do not paste raw provider payloads",
        "provider account identifiers",
        "private user data",
        "full unredacted request/response traces",
        "environment dumps",
        "dashboard credentials",
        "cookies",
        "csrf tokens",
        "session values",
        "authorization-token material",
    ):
        assert phrase in lowered, f"template missing redaction/storage phrase: {phrase}"


def test_template_carries_strict_non_claims():
    text = _read(TEMPLATE)
    assert "## 16. Non-claims" in text
    for claim in STRICT_NON_CLAIMS:
        assert claim in text, f"template missing non-claim: {claim}"


def test_template_has_no_obvious_secret_like_strings():
    text = _read(TEMPLATE)
    lowered = text.lower()
    for pattern in SECRET_LIKE_PATTERNS:
        haystack = lowered if pattern == pattern.lower() else text
        assert pattern not in haystack, f"template contains secret-like pattern: {pattern}"
