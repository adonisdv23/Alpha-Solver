"""Docs-integrity tests for EVAL-DIFFERENTIATION-RUN-001.

These checks validate only the committed docs/spec/run scaffold. They do not run
providers, score outputs, or inspect runtime behavior.
"""
from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

SPEC = Path(".specs/EVAL-DIFFERENTIATION-RUN-001.md")
SPEC_INDEX = Path(".specs/INDEX.md")
RUN_DIR = Path(
    "docs/evals/runs/"
    "20260602-eval-differentiation-run-001-alpha-vs-plain"
)

RUN_FILES = (
    "run-plan.md",
    "prompt-manifest.md",
    "run-summary.md",
    "blinded-score-sheet.csv",
    "blinding-map.csv",
    "score-table.csv",
    "defects.md",
    "paired-output-captures/.gitkeep",
    "paired-output-captures/cmp-HHE-002-paired-output-capture.md",
    "paired-output-captures/cmp-HHE-003-paired-output-capture.md",
    "paired-output-captures/cmp-HHE-007-paired-output-capture.md",
    "paired-output-captures/cmp-HHE-009-paired-output-capture.md",
    "evidence-packets/.gitkeep",
    "evidence-packets/cmp-HHE-002-evidence-packet.md",
    "evidence-packets/cmp-HHE-003-evidence-packet.md",
    "evidence-packets/cmp-HHE-007-evidence-packet.md",
    "evidence-packets/cmp-HHE-009-evidence-packet.md",
)

PILOT_PROMPTS = ("HHE-002", "HHE-003", "HHE-007", "HHE-009")

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

HARDENING_FIELDS = (
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
    "plain_defects",
    "alpha_defects",
    "follow_up_tickets",
    "evidence_strength",
    "redactions_performed",
    "non_claims_confirmed",
)

NON_CLAIMS = (
    "MVP validation",
    "Alpha Solver superiority",
    "Answer-quality superiority",
    "Production readiness",
    "Broad runtime readiness",
    "Benchmark success",
    "Exact billing accuracy",
    "Provider reasoning orchestration",
)

SECRET_MARKERS = ("sk-", "xoxb-", "-----BEGIN")
SECRET_VALUE_PATTERNS = (re.compile(r"bearer\s+[A-Za-z0-9._~+/=-]{8,}", re.IGNORECASE),)
BIDI_CONTROL_CATEGORIES = {"RLO", "LRO", "RLE", "LRE", "PDF", "RLI", "LRI", "FSI", "PDI"}


def _read(path: Path) -> str:
    assert path.exists(), f"missing required file: {path}"
    return path.read_text(encoding="utf-8")


def _csv_rows(path: Path) -> list[list[str]]:
    assert path.exists(), f"missing required CSV: {path}"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.reader(handle))


def _csv_header(path: Path) -> list[str]:
    rows = _csv_rows(path)
    assert rows, f"{path} must include a header row"
    return rows[0]


def test_spec_exists_and_index_references_it():
    assert SPEC.exists()
    index = _read(SPEC_INDEX)
    assert "EVAL-DIFFERENTIATION-RUN-001.md" in index
    assert "Controlled Alpha-vs-Plain Run Scaffold" in index


def test_run_directory_and_required_files_exist():
    assert RUN_DIR.exists()
    assert RUN_DIR.is_dir()
    for relative in RUN_FILES:
        assert (RUN_DIR / relative).exists(), f"missing run file: {relative}"


def test_prompt_manifest_includes_exact_first_pilot_prompts_and_metadata():
    text = _read(RUN_DIR / "prompt-manifest.md")
    headings = re.findall(r"^### (HHE-\d{3})\b", text, flags=re.MULTILINE)
    assert tuple(headings) == PILOT_PROMPTS

    required_labels = (
        "Prompt family:",
        "Difficulty/headroom:",
        "Expected deliverable:",
        "Hidden constraints or traps:",
        "Emphasized rubric dimensions:",
        "Claim-boundary concerns:",
        "Expected evidence capture:",
        "Why included in first pilot:",
    )
    for prompt_id in PILOT_PROMPTS:
        section_match = re.search(
            rf"^### {prompt_id}\b(?P<section>.*?)(?=^### HHE-\d{{3}}\b|\Z)",
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
        assert section_match, f"missing manifest section for {prompt_id}"
        section = section_match.group("section")
        for label in required_labels:
            assert label in section, f"{prompt_id} missing {label}"


def test_score_table_uses_hardened_14_dimension_and_decision_fields():
    header = set(_csv_header(RUN_DIR / "score-table.csv"))
    for key in DIMENSION_KEYS:
        assert f"{key}_plain" in header
        assert f"{key}_alpha" in header
    for field in HARDENING_FIELDS:
        assert field in header


def test_blinded_score_sheet_uses_output_a_b_without_identity_headers():
    header = _csv_header(RUN_DIR / "blinded-score-sheet.csv")
    header_text = ",".join(header).lower()
    assert "alpha" not in header_text
    assert "plain" not in header_text
    for key in DIMENSION_KEYS:
        assert f"output_a_{key}" in header
        assert f"output_b_{key}" in header


def test_blinding_map_exists_and_is_separate_from_blinded_sheet():
    map_path = RUN_DIR / "blinding-map.csv"
    sheet_path = RUN_DIR / "blinded-score-sheet.csv"
    assert map_path.exists()
    assert sheet_path.exists()
    assert map_path.resolve() != sheet_path.resolve()
    header = set(_csv_header(map_path))
    for field in (
        "comparison_id",
        "prompt_id",
        "output_a_identity",
        "output_b_identity",
        "assignment_method_or_seed",
        "assigned_by",
        "unblinded_by",
    ):
        assert field in header


def test_run_plan_preserves_capture_boundaries_and_summary_records_completed_scoring():
    plan_lowered = _read(RUN_DIR / "run-plan.md").lower()
    assert "not executed" in plan_lowered
    assert "no outputs" in plan_lowered
    assert "no scores" in plan_lowered or "no scores are recorded" in plan_lowered

    summary_lowered = _read(RUN_DIR / "run-summary.md").lower()
    assert "clean a3-1 capture had already completed" in summary_lowered
    assert "blind scoring preceded unblinding" in summary_lowered
    assert "did not rerun capture" in summary_lowered
    assert "did not call live providers" in summary_lowered
    assert "did not change runtime/provider/model behavior" in summary_lowered
    assert "did not update google sheets" in summary_lowered
    assert "did not start batch b" in summary_lowered


def test_populated_scored_artifacts_have_expected_rows_and_totals():
    paired_files = sorted(
        path.name
        for path in (RUN_DIR / "paired-output-captures").iterdir()
        if path.name != ".gitkeep"
    )
    packet_files = sorted(
        path.name
        for path in (RUN_DIR / "evidence-packets").iterdir()
        if path.name != ".gitkeep"
    )
    assert paired_files == [f"cmp-{prompt_id}-paired-output-capture.md" for prompt_id in PILOT_PROMPTS]
    assert packet_files == [f"cmp-{prompt_id}-evidence-packet.md" for prompt_id in PILOT_PROMPTS]

    expected_blinded_totals = {
        "cmp-HHE-002": (55, 52),
        "cmp-HHE-003": (68, 69),
        "cmp-HHE-007": (68, 64),
        "cmp-HHE-009": (44, 45),
    }
    blinded_rows = list(csv.DictReader((RUN_DIR / "blinded-score-sheet.csv").open()))
    assert len(blinded_rows) == 4
    for row in blinded_rows:
        comparison_id = row["comparison_id"]
        assert comparison_id in expected_blinded_totals
        output_a_total = sum(int(row[f"output_a_{key}"]) for key in DIMENSION_KEYS)
        output_b_total = sum(int(row[f"output_b_{key}"]) for key in DIMENSION_KEYS)
        assert (output_a_total, output_b_total) == expected_blinded_totals[comparison_id]
        assert int(row["output_a_total"]) == output_a_total
        assert int(row["output_b_total"]) == output_b_total

    score_rows = list(csv.DictReader((RUN_DIR / "score-table.csv").open()))
    assert len(score_rows) == 4
    expected_unblinded = {
        "cmp-HHE-002": (55, 52, -3, "Plain"),
        "cmp-HHE-003": (69, 68, -1, "Plain"),
        "cmp-HHE-007": (68, 64, -4, "Plain"),
        "cmp-HHE-009": (45, 44, -1, "Plain"),
    }
    plain_total = 0
    alpha_total = 0
    for row in score_rows:
        expected = expected_unblinded[row["comparison_id"]]
        observed = (
            int(row["plain_total"]),
            int(row["alpha_total"]),
            int(row["total_delta"]),
            row["winning_surface"],
        )
        assert observed == expected
        plain_total += observed[0]
        alpha_total += observed[1]
    assert (plain_total, alpha_total, alpha_total - plain_total) == (237, 228, -9)


def test_blinded_score_sheet_values_do_not_reveal_surface_identities():
    sheet_text = _read(RUN_DIR / "blinded-score-sheet.csv").lower()
    assert "alpha" not in sheet_text
    assert "plain" not in sheet_text
    assert "route" not in sheet_text


def test_non_claims_are_present_in_scaffold_documents():
    combined = "\n".join(_read(path) for path in (SPEC, RUN_DIR / "run-plan.md", RUN_DIR / "run-summary.md"))
    combined_lower = combined.lower()
    for claim in NON_CLAIMS:
        assert claim.lower() in combined_lower


def test_no_secret_like_strings_appear_in_committed_run_artifacts():
    for path in RUN_DIR.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for marker in SECRET_MARKERS:
                assert marker.lower() not in lowered, f"{path} contains {marker}"
            for pattern in SECRET_VALUE_PATTERNS:
                assert not pattern.search(text), f"{path} contains secret-like value"


def test_markdown_and_python_files_have_reviewable_physical_formatting():
    targets = [SPEC, Path(__file__)] + sorted(RUN_DIR.glob("*.md"))
    for path in targets:
        text = _read(path)
        assert "\r" not in text, f"{path} contains carriage returns"
        lines = text.splitlines()
        assert len(lines) > 5, f"{path} appears collapsed or too short"
        assert len(lines) < 500, f"{path} has an unreasonable line count"
        assert max(len(line) for line in lines) < 500, f"{path} has an overly long line"
        for character in text:
            bidi = unicodedata.bidirectional(character)
            category = unicodedata.category(character)
            assert bidi not in BIDI_CONTROL_CATEGORIES
            assert category != "Cf", f"{path} contains hidden format character"
