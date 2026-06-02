"""Docs-integrity tests for OUTPUT-DIFF-A3-OPERATOR-CHECKLIST-DRY-RUN-001.

This lane (A3-0) prepares the operator checklist and dry-run validation rules for
the later first scored Alpha-vs-plain differentiation run. These tests validate
only the committed docs/checklist scaffold. They do not run providers, capture
outputs, score outputs, or inspect runtime behavior.

A3-0 is explicitly not A3-1: it does not execute the run, call providers, add
outputs, add scores, populate paired-output captures, or populate evidence
packets. The tests below assert those boundaries hold.

Natural-language phrase checks use a whitespace-normalized, lowercased view of the
text so that ordinary Markdown line wrapping does not cause spurious failures.
Case-sensitive paths, planned artifact filenames, and exact decision-field tokens
are matched against the raw text instead.
"""
from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

RUN_DIR = Path(
    "docs/evals/runs/"
    "20260602-eval-differentiation-run-001-alpha-vs-plain"
)
RUN_DIR_REFERENCE = (
    "docs/evals/runs/"
    "20260602-eval-differentiation-run-001-alpha-vs-plain/"
)

CHECKLIST = RUN_DIR / "operator-checklist.md"
POPULATION_GUIDE = RUN_DIR / "artifact-population-guide.md"

PILOT_PROMPTS = ("HHE-002", "HHE-003", "HHE-007", "HHE-009")

DECISION_FIELDS = (
    "plain_total",
    "alpha_total",
    "total_delta",
    "lift_delta",
    "polish_delta",
    "lift_qualified",
    "material_constraint_verified",
    "polish_only_flag",
)

PLANNED_PAIRED_CAPTURES = tuple(
    f"paired-output-captures/cmp-{prompt}-paired-output-capture.md"
    for prompt in PILOT_PROMPTS
)
PLANNED_EVIDENCE_PACKETS = tuple(
    f"evidence-packets/cmp-{prompt}-evidence-packet.md"
    for prompt in PILOT_PROMPTS
)

DEFECT_FIELDS = (
    "defect id",
    "prompt id",
    "side",
    "rubric dimension",
    "category",
    "severity",
    "evidence pointer",
    "follow-up ticket",
    "lift_qualified",
)

DEFECT_CATEGORIES = (
    "missed requested deliverable",
    "unsupported claim",
    "treating backlog as repo proof",
    "unsafe secret/cookie/session handling",
    "raw payload preservation suggestion",
    "over-interrogation",
    "excessive caveats",
    "invented constraints",
    "plain output more direct/useful",
)

REDACTION_PROHIBITIONS = (
    "api keys",
    "bearer-token",
    "dashboard passwords",
    "cookies",
    "csrf tokens",
    "session values",
    "auth headers",
    "raw provider payloads",
    "provider account identifiers",
    "full unredacted request/response traces",
    "environment dumps",
    "private user data",
    "secret-like strings",
)

STOP_CONDITIONS = (
    "operator approval is missing",
    "branch or commit is not recorded",
    "request cap is missing or has been exceeded",
    "prompt text differs between the plain and alpha surfaces",
    "extra instructions not given to the other",
    "sensitive data that cannot be redacted",
    "runtime or provider changes would be needed",
    "blinding cannot be performed before scoring",
    "the scorer sees the alpha/plain mapping before scoring",
    "the artifact format cannot be validated",
)

NON_CLAIMS = (
    "mvp validation",
    "alpha solver superiority",
    "answer-quality superiority",
    "production readiness",
    "broad runtime readiness",
    "benchmark success",
    "exact billing accuracy",
    "provider reasoning orchestration",
)

SECRET_MARKERS = ("sk-", "xoxb-", "-----BEGIN", "bearer ")
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


def _read(path: Path) -> str:
    assert path.exists(), f"missing required file: {path}"
    return path.read_text(encoding="utf-8")


def _normalized(path: Path) -> str:
    """Lowercased text with whitespace runs collapsed to single spaces.

    This lets phrase assertions ignore Markdown line wrapping.
    """
    return re.sub(r"\s+", " ", _read(path)).lower()


def _csv_rows(path: Path) -> list[list[str]]:
    assert path.exists(), f"missing required CSV: {path}"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.reader(handle))


def test_operator_checklist_exists():
    assert CHECKLIST.exists(), "operator-checklist.md must exist"
    assert CHECKLIST.is_file()


def test_references_exact_run_directory():
    text = _read(CHECKLIST)
    assert RUN_DIR_REFERENCE in text


def test_references_exactly_the_four_prompts():
    text = _read(CHECKLIST)
    found = sorted(set(re.findall(r"HHE-\d{3}", text)))
    assert found == sorted(PILOT_PROMPTS), found


def test_includes_request_cap_guidance():
    normalized = _normalized(CHECKLIST)
    assert "8 primary generations" in normalized
    assert "4 prompts" in normalized
    assert "2 surfaces" in normalized
    assert "10 to 12" in normalized


def test_includes_plain_and_alpha_surface_rules():
    normalized = _normalized(CHECKLIST)
    assert "plain surface" in normalized
    assert "alpha surface" in normalized
    assert "identified" in normalized
    assert "before execution" in normalized


def test_includes_output_generation_rules():
    normalized = _normalized(CHECKLIST)
    assert "submit the same prompt to the plain surface" in normalized
    assert "submit the same prompt to the alpha surface" in normalized
    assert "sanitized answer text only" in normalized
    assert "word counts" in normalized
    assert "expert-envelope" in normalized
    assert "raw provider payloads" in normalized
    assert "response ids" in normalized
    assert "score the outputs" in normalized
    assert "unblind the outputs" in normalized


def test_includes_blinding_rules():
    normalized = _normalized(CHECKLIST)
    assert "output a" in normalized
    assert "output b" in normalized
    assert "blinding-map.csv" in normalized
    assert "random method or seed" in normalized
    assert "before consulting the map" in normalized
    assert "procedural, not cryptographic" in normalized


def test_includes_scoring_rules():
    text = _read(CHECKLIST)
    normalized = _normalized(CHECKLIST)
    assert "14 rubric dimensions" in normalized
    assert "polish-only" in normalized
    assert "docs/evals/RESPONSE_QUALITY_RUBRIC.md" in text
    assert "docs/evals/LIFT_DECISION_RULE.md" in text
    assert "blinded-score-sheet.csv" in text
    assert "score-table.csv" in text
    for field in DECISION_FIELDS:
        assert field in text, f"checklist missing decision field {field}"


def test_includes_planned_paired_output_capture_filenames():
    text = _read(CHECKLIST)
    for name in PLANNED_PAIRED_CAPTURES:
        assert name in text, f"checklist missing planned capture {name}"


def test_includes_planned_evidence_packet_filenames():
    text = _read(CHECKLIST)
    for name in PLANNED_EVIDENCE_PACKETS:
        assert name in text, f"checklist missing planned packet {name}"


def test_includes_defect_workflow_and_categories():
    normalized = _normalized(CHECKLIST)
    for field in DEFECT_FIELDS:
        assert field in normalized, f"checklist missing defect field {field}"
    for category in DEFECT_CATEGORIES:
        assert category in normalized, f"checklist missing defect category {category}"


def test_includes_redaction_rules():
    normalized = _normalized(CHECKLIST)
    assert "prohibited" in normalized
    for item in REDACTION_PROHIBITIONS:
        assert item in normalized, f"checklist missing redaction item {item}"


def test_includes_stop_conditions():
    normalized = _normalized(CHECKLIST)
    assert "stop condition" in normalized
    assert "must stop" in normalized
    for condition in STOP_CONDITIONS:
        assert condition in normalized, f"checklist missing stop condition {condition}"


def test_includes_strict_non_claims():
    normalized = _normalized(CHECKLIST)
    assert "non-claims" in normalized
    for claim in NON_CLAIMS:
        assert claim in normalized, f"checklist missing non-claim {claim}"


def test_confirms_a3_0_does_not_execute_the_run():
    normalized = _normalized(CHECKLIST)
    assert "a3-0" in normalized
    assert "execute the run" in normalized
    assert "the run is not executed" in normalized


def test_confirms_a3_0_adds_no_outputs_scores_providers_or_artifacts():
    normalized = _normalized(CHECKLIST)
    assert "no outputs are captured" in normalized
    assert "no scores are recorded" in normalized
    assert "no provider calls are made" in normalized
    assert "no paired-output captures are populated" in normalized
    assert "no evidence packets are populated" in normalized


def test_population_guide_exists_and_is_consistent():
    text = _read(POPULATION_GUIDE)
    normalized = _normalized(POPULATION_GUIDE)
    assert RUN_DIR_REFERENCE in text
    found = sorted(set(re.findall(r"HHE-\d{3}", text)))
    assert found == sorted(PILOT_PROMPTS), found
    assert "non-claims" in normalized
    assert "bearer-token" in normalized
    assert "raw provider payloads" in normalized
    for name in PLANNED_PAIRED_CAPTURES:
        assert name in text
    for name in PLANNED_EVIDENCE_PACKETS:
        assert name in text


def test_run_plan_and_summary_reference_checklist_and_stay_unexecuted():
    plan = _read(RUN_DIR / "run-plan.md")
    summary = _read(RUN_DIR / "run-summary.md")
    assert "operator-checklist.md" in plan
    assert "operator-checklist.md" in summary
    for normalized in (
        _normalized(RUN_DIR / "run-plan.md"),
        _normalized(RUN_DIR / "run-summary.md"),
    ):
        assert "not executed" in normalized
        assert "no outputs" in normalized
        assert "no scores" in normalized


def test_scaffold_files_remain_header_only_and_placeholders():
    for csv_name in (
        "blinded-score-sheet.csv",
        "blinding-map.csv",
        "score-table.csv",
    ):
        rows = _csv_rows(RUN_DIR / csv_name)
        assert len(rows) == 1, f"{csv_name} must remain header-only in A3-0"

    paired_files = sorted(p.name for p in (RUN_DIR / "paired-output-captures").iterdir())
    packet_files = sorted(p.name for p in (RUN_DIR / "evidence-packets").iterdir())
    assert paired_files == [".gitkeep"], paired_files
    assert packet_files == [".gitkeep"], packet_files


def test_no_secret_like_strings_in_a3_docs():
    for path in (CHECKLIST, POPULATION_GUIDE):
        lowered = _read(path).lower()
        for marker in SECRET_MARKERS:
            assert marker.lower() not in lowered, f"{path} contains {marker}"


# Minimum physical line counts guard against line-collapsed files: a file that
# was serialized onto a few long lines fails loudly here instead of merely
# looking short. Thresholds are deliberately well above the real content size.
MIN_PHYSICAL_LINES = {
    "operator-checklist.md": 100,
    "artifact-population-guide.md": 50,
    "test_output_diff_a3_operator_checklist.py": 100,
}

REQUIRED_CHECKLIST_HEADINGS = (
    "## A. Pre-run setup",
    "## B. Output generation rules for the later A3-1 step",
    "## C. Blinding rules",
    "## D. Scoring rules for the later A3-1 step",
    "## E. Planned artifact names for A3-1",
    "## F. Defect workflow",
    "## G. Redaction rules",
    "## H. Stop conditions",
    "## I. Non-claims",
)

REQUIRED_GUIDE_HEADINGS = (
    "## Population order for A3-1",
    "## Paired-output captures",
    "## Blinding map",
    "## Blinded score sheet",
    "## Score table",
    "## Non-claims",
)


def test_markdown_and_python_files_have_reviewable_physical_formatting():
    targets = [CHECKLIST, POPULATION_GUIDE, Path(__file__)]
    for path in targets:
        text = _read(path)
        assert "\r" not in text, f"{path} contains carriage returns"
        lines = text.splitlines()
        minimum = MIN_PHYSICAL_LINES[path.name]
        assert len(lines) > minimum, f"{path} appears line-collapsed (<= {minimum} lines)"
        assert len(lines) < 500, f"{path} has an unreasonable line count"
        assert max(len(line) for line in lines) < 500, f"{path} has an overly long line"
        for character in text:
            bidi = unicodedata.bidirectional(character)
            category = unicodedata.category(character)
            assert bidi not in BIDI_CONTROL_CATEGORIES, f"{path} has bidi control"
            assert category != "Cf", f"{path} contains hidden format character"


def test_required_markdown_headings_are_standalone_lines():
    checklist_lines = _read(CHECKLIST).splitlines()
    for heading in REQUIRED_CHECKLIST_HEADINGS:
        assert heading in checklist_lines, f"checklist missing standalone heading {heading!r}"
    guide_lines = _read(POPULATION_GUIDE).splitlines()
    for heading in REQUIRED_GUIDE_HEADINGS:
        assert heading in guide_lines, f"guide missing standalone heading {heading!r}"


def _population_order_section() -> str:
    """Return the lowercased 'Population order for A3-1' section of the guide."""
    heading = "## Population order for A3-1"
    text = _read(POPULATION_GUIDE)
    start = text.index(heading)
    rest = text[start + len(heading):]
    end = rest.find("\n## ")
    section = rest if end == -1 else rest[:end]
    return section.lower()


def test_population_guide_assigns_blinded_labels_before_writing_captures():
    section = _population_order_section()
    positions = {
        "assign output a/b": section.find("assign plain and alpha to"),
        "record blinding map": section.find("record the mapping in"),
        "write paired-output capture": section.find(
            "write one sanitized paired-output capture"
        ),
        "score blinded sheet": section.find("blinded-score-sheet.csv"),
        "unblind": section.find("unblind via"),
        "fill score table": section.find("score-table.csv"),
    }
    for label, pos in positions.items():
        assert pos != -1, f"population order missing step: {label}"
    ordered = [
        positions["assign output a/b"],
        positions["record blinding map"],
        positions["write paired-output capture"],
        positions["score blinded sheet"],
        positions["unblind"],
        positions["fill score table"],
    ]
    assert ordered == sorted(ordered), f"population order is wrong: {positions}"


def test_population_guide_capture_uses_blinded_labels_and_envelope_caveat():
    normalized = _normalized(POPULATION_GUIDE)
    assert "write captures only after" in normalized
    assert "output a` / `output b` labels" in normalized
    assert "for unblinded material-lift analysis only" in normalized
    assert "must not be used to bias blinded scoring" in normalized
