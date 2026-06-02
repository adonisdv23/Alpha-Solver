"""Docs-integrity tests for ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001.

These checks validate the additive, blank side-by-side evidence packet contract
for future Alpha-vs-plain differentiation artifacts. They parse committed docs
only; they do not execute provider calls, score outputs, or create populated
evidence packets.
"""
from __future__ import annotations

import ast
import unicodedata
from pathlib import Path

SPEC = Path(".specs/ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001.md")
INDEX = Path(".specs/INDEX.md")
TEMPLATE = Path("docs/evals/templates/side_by_side_evidence_packet_template.md")
TEST_FILE = Path("tests/test_alpha_side_by_side_evidence_packet.py")

TARGET_FORMAT_FILES = (
    TEST_FILE,
    TEMPLATE,
    SPEC,
)

REVIEWABILITY_FILES = (
    *TARGET_FORMAT_FILES,
    INDEX,
    Path("docs/evals/ARTIFACT_PRESERVATION.md"),
    Path("docs/evals/PROMPT_QUALITY_SCORING_HARNESS.md"),
    Path("docs/evals/runs/README.md"),
)

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

TEMPLATE_TABLES = (
    ("| Field | Placeholder |", "| --- | --- |"),
    ("| Source artifact | Path |", "| --- | --- |"),
    (
        "| Dimension key | Plain score | Alpha score | Delta | Evidence note |",
        "| --- | --- | --- | --- | --- |",
    ),
    ("| Ticket/spec | Reason | Owner/status |", "| --- | --- | --- |"),
)

SPEC_REQUIRED_HEADINGS = (
    "# ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001 - Side-by-Side Evidence Packet Contract",
    "## Status",
    "## Purpose",
    "## Scope",
    "## Source artifacts",
    "## Packet contract",
    "## Required packet fields",
    "## Fourteen-dimension coverage",
    "## Redaction and storage boundaries",
    "## Non-claims",
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
BIDI_CONTROL_CATEGORIES = {
    "RLO",
    "LRO",
    "RLE",
    "LRE",
    "PDF",
    "RLI",
    "LRI",
    "FSI",
    "PDI",
}
HIDDEN_CONTROL_CATEGORIES = {"Cf"}


def _read(path: Path) -> str:
    assert path.exists(), f"missing required file: {path}"
    return path.read_text(encoding="utf-8")


def _standalone_lines(path: Path) -> set[str]:
    return {line.strip() for line in _read(path).splitlines()}


def test_spec_exists_and_is_indexed():
    assert SPEC.exists()
    index = _read(INDEX)
    assert "ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001.md" in index


def test_new_test_file_parses_as_normal_python():
    source = _read(TEST_FILE)
    lines = source.splitlines()
    ast.parse(source, filename=str(TEST_FILE))
    assert len(lines) > 100, f"{TEST_FILE} appears collapsed onto too few lines"
    assert source.startswith('"""Docs-integrity tests')
    expected_prefix = (
        '"""'
        + chr(10)
        + "from __future__ import annotations"
        + chr(10)
        + chr(10)
        + "import ast"
        + chr(10)
    )
    assert expected_prefix in source


def test_new_and_edited_files_have_reviewable_text_formatting():
    for path in REVIEWABILITY_FILES:
        text = _read(path)
        literal_newline_escape = "\\" + "n"
        assert literal_newline_escape not in text, (
            f"{path} contains literal newline escape sequences"
        )
        assert "\r" not in text, f"{path} contains carriage returns"
        lines = text.splitlines()
        assert len(lines) > 1, f"{path} appears collapsed onto one line"
        assert max(len(line) for line in lines) < 500, (
            f"{path} has an overly long line that may indicate collapsed text"
        )
        for character in text:
            bidi = unicodedata.bidirectional(character)
            category = unicodedata.category(character)
            assert bidi not in BIDI_CONTROL_CATEGORIES, (
                f"{path} contains bidirectional control character {bidi}"
            )
            assert category not in HIDDEN_CONTROL_CATEGORIES, (
                f"{path} contains hidden Unicode control category {category}"
            )


def test_target_files_have_many_physical_lines_and_bounded_line_lengths():
    for path in TARGET_FORMAT_FILES:
        lines = _read(path).splitlines()
        if path.suffix == ".py":
            assert len(lines) > 100, f"{path} is still line-collapsed"
        else:
            assert len(lines) > 50, f"{path} is still line-collapsed"
        assert max(len(line) for line in lines) < 500, (
            f"{path} still has collapsed long lines"
        )


def test_spec_contains_required_headings_as_standalone_lines():
    lines = _standalone_lines(SPEC)
    for heading in SPEC_REQUIRED_HEADINGS:
        assert heading in lines, f"spec missing standalone heading: {heading}"


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


def test_template_includes_required_sections_as_standalone_lines_and_fields():
    text = _read(TEMPLATE)
    lines = _standalone_lines(TEMPLATE)
    for section in REQUIRED_SECTIONS:
        assert section in lines, f"template missing standalone section: {section}"
    for field in IDENTITY_AND_SOURCE_FIELDS:
        assert field in text, f"template missing field: {field}"


def test_template_tables_have_standalone_header_and_separator_rows():
    lines = _read(TEMPLATE).splitlines()
    for header, separator in TEMPLATE_TABLES:
        assert header in lines, f"template missing standalone table header: {header}"
        header_index = lines.index(header)
        assert header_index + 1 < len(lines), f"template table has no separator: {header}"
        assert lines[header_index + 1] == separator, (
            f"template table separator must follow header {header!r} on its own line"
        )


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
        "do not paste any of the following here",
        "raw provider payloads",
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
    assert "## 16. Non-claims" in _standalone_lines(TEMPLATE)
    for claim in STRICT_NON_CLAIMS:
        assert claim in text, f"template missing non-claim: {claim}"


def test_template_has_no_obvious_secret_like_strings():
    text = _read(TEMPLATE)
    lowered = text.lower()
    for pattern in SECRET_LIKE_PATTERNS:
        haystack = lowered if pattern == pattern.lower() else text
        assert pattern not in haystack, f"template contains secret-like pattern: {pattern}"
