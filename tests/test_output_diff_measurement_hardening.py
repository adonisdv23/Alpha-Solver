"""Docs-integrity tests for OUTPUT-DIFF-MEASUREMENT-HARDENING-001.

Read-only checks that the additive measurement-hardening templates, docs, and
spec capture every rubric dimension, the lift/polish/length fields, blinded
Output A / Output B scoring, the separate blinding map, the difficulty backfill,
and strict claim boundaries. These tests parse committed docs only and touch no
runtime behaviour. Paths are resolved relative to the repo root (CWD), matching
the existing docs-boundary tests in ``tests/test_answer_quality_eval.py``.
"""
from __future__ import annotations

from pathlib import Path

EVALS = Path("docs/evals")
TEMPLATES = EVALS / "templates"

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

LIFT_KEYS = (
    "d04_assumptions",
    "d05_hidden_constraints",
    "d06_risk_failure",
    "d14_comparative_value",
)
POLISH_KEYS = ("d03_structure", "d10_next_actions", "d12_brevity")

RATINGS = ("low", "medium", "high", "stress")


def _read(path: Path) -> str:
    assert path.exists(), f"missing required file: {path}"
    return path.read_text(encoding="utf-8")


def _header(path: Path) -> str:
    return _read(path).splitlines()[0]


def test_comparison_score_table_covers_all_14_dimensions():
    header = _header(TEMPLATES / "comparison_score_table_template.csv")
    for key in DIMENSION_KEYS:
        assert f"{key}_plain" in header, f"missing {key}_plain"
        assert f"{key}_alpha" in header, f"missing {key}_alpha"


def test_comparison_score_table_has_lift_polish_length_and_flags():
    header = _header(TEMPLATES / "comparison_score_table_template.csv")
    for field in (
        "total_delta",
        "lift_delta",
        "polish_delta",
        "winning_surface",
        "lift_qualified",
        "material_constraint_verified",
        "polish_only_flag",
        "output_a_len_words",
        "output_b_len_words",
        "length_ratio",
    ):
        assert field in header, f"missing field: {field}"


def test_blinded_score_sheet_uses_output_a_b_and_has_no_brand_tokens():
    header = _header(TEMPLATES / "blinded_score_sheet_template.csv")
    for key in DIMENSION_KEYS:
        assert f"output_a_{key}" in header, f"missing output_a_{key}"
        assert f"output_b_{key}" in header, f"missing output_b_{key}"
    lowered = header.lower()
    assert "alpha" not in lowered, "blinded sheet header must not reveal Alpha"
    assert "plain" not in lowered, "blinded sheet header must not reveal Plain"


def test_blinding_map_exists_and_is_distinct_from_blinded_sheet():
    map_path = TEMPLATES / "blinding_map_template.csv"
    sheet_path = TEMPLATES / "blinded_score_sheet_template.csv"
    assert map_path.exists()
    assert sheet_path.exists()
    assert map_path.resolve() != sheet_path.resolve()
    header = _header(map_path)
    for field in (
        "output_a_identity",
        "output_b_identity",
        "assignment_method_or_seed",
        "assigned_by",
        "unblinded_by",
    ):
        assert field in header, f"missing mapping field: {field}"


def test_paired_output_capture_has_envelope_and_redaction():
    text = _read(TEMPLATES / "paired_output_capture_template.md")
    lowered = text.lower()
    for envelope_field in (
        "considerations",
        "assumptions",
        "confidence",
        "mode",
        "clarifying questions",
        "metadata",
    ):
        assert envelope_field in lowered, f"missing envelope field: {envelope_field}"
    for forbidden in (
        "api key",
        "bearer",
        "cookie",
        "csrf",
        "session",
        "raw provider payload",
        "environment dump",
        "private user data",
    ):
        assert forbidden in lowered, f"redaction list missing: {forbidden}"
    assert "## Non-claims" in text


def test_new_docs_and_spec_carry_strict_non_claims():
    targets = (
        Path(".specs/OUTPUT-DIFF-MEASUREMENT-HARDENING-001.md"),
        EVALS / "LIFT_DECISION_RULE.md",
        EVALS / "BLIND_SCORING_PROCEDURE.md",
        TEMPLATES / "paired_output_capture_template.md",
    )
    for path in targets:
        text = _read(path)
        assert (
            "## Non-claims" in text or "## Strict non-claims" in text
        ), f"{path} missing non-claims section"
        assert (
            "does not prove Alpha Solver superiority" in text
        ), f"{path} missing superiority boundary"
        # context guard: sensitive phrases must always be negated
        for line in text.splitlines():
            low = line.lower()
            if "benchmark success" in low or "provider reasoning orchestration" in low:
                assert (
                    "does not" in low or "do not" in low or "not prove" in low
                ), f"unbounded claim in {path}: {line}"


def test_lift_rule_doc_defines_clusters_as_decision_aid():
    text = _read(EVALS / "LIFT_DECISION_RULE.md")
    lowered = text.lower()
    assert "decision aid" in lowered, "lift rule must be framed as an internal decision aid"
    assert "lift_qualified" in text
    assert "polish_only_flag" in text or "polish-only" in lowered
    for key in LIFT_KEYS:
        assert key in text, f"lift cluster missing {key}"
    for key in POLISH_KEYS:
        assert key in text, f"polish cluster missing {key}"


def test_blind_scoring_procedure_is_honest_about_limits():
    text = _read(EVALS / "BLIND_SCORING_PROCEDURE.md")
    lowered = text.lower()
    assert "output a" in lowered and "output b" in lowered
    assert "procedural" in lowered, "must state blinding is procedural, not cryptographic"
    assert "blinding_map_template.csv" in text
    assert "tell" in lowered or "structural" in lowered


def test_higher_headroom_manifest_has_difficulty_rating_for_every_prompt():
    text = _read(EVALS / "prompt_sets" / "higher_headroom_prompt_set_v1.md")
    assert "Difficulty/headroom" in text
    lines = text.splitlines()
    for n in range(1, 17):
        pid = f"HHE-{n:03d}"
        rows = [ln for ln in lines if pid in ln and "|" in ln]
        assert rows, f"missing manifest row for {pid}"
        found = False
        for row in rows:
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if any(c.lower().startswith(RATINGS) for c in cells):
                found = True
                break
        assert found, f"{pid} has no difficulty/headroom rating cell"


def test_response_rubric_unchanged_14_dims_and_points_to_new_aids():
    text = _read(EVALS / "RESPONSE_QUALITY_RUBRIC.md")
    dim_headers = [
        ln for ln in text.splitlines() if ln.startswith("### ") and ln[4:5].isdigit()
    ]
    assert len(dim_headers) == 14, f"expected 14 dimension headers, found {len(dim_headers)}"
    assert "LIFT_DECISION_RULE.md" in text
    assert "BLIND_SCORING_PROCEDURE.md" in text


def test_new_spec_is_indexed():
    index = _read(Path(".specs/INDEX.md"))
    assert "OUTPUT-DIFF-MEASUREMENT-HARDENING-001.md" in index
    assert Path(".specs/OUTPUT-DIFF-MEASUREMENT-HARDENING-001.md").exists()


def test_no_secret_patterns_in_new_csv_templates():
    paths = (
        TEMPLATES / "comparison_score_table_template.csv",
        TEMPLATES / "blinded_score_sheet_template.csv",
        TEMPLATES / "blinding_map_template.csv",
    )
    for path in paths:
        combined = _read(path).lower()
        for forbidden in ("sk-", "xoxb-", "-----begin", "bearer "):
            assert forbidden not in combined, f"possible secret pattern in {path}: {forbidden}"
