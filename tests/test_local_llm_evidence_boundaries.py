"""Tests for the local LLM solver orchestration evidence-boundary checker.

The checker is a static docs guard only. These tests do not run local inference,
Ollama, hosted providers, benchmarks, dashboard routes, or /v1/solve.
"""
from pathlib import Path

from scripts.check_local_llm_evidence_boundaries import (
    FINAL_PACKET_DIR,
    REQUIRED_FINAL_PACKET_PHRASES,
    check_paths,
    find_promotional_claim_findings,
    find_required_final_packet_findings,
    is_relevant_doc,
    iter_relevant_docs,
)


def test_relevant_docs_include_closeout_and_skip_source_artifacts():
    assert is_relevant_doc(
        Path(
            "docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/closeout/final-boundary.md"
        )
    )
    assert not is_relevant_doc(
        Path(
            "docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/source-artifact/run_level3_validation.sh"
        )
    )
    assert not is_relevant_doc(Path("docs/RUNTIME_READINESS.md"))


def test_promotional_claim_without_boundary_language_is_flagged():
    findings = find_promotional_claim_findings(
        Path("docs/evals/runs/example-local-llm-solver-orchestration/example.md"),
        "This proves production readiness for the lane.\n",
    )

    assert len(findings) == 1
    assert findings[0].phrase == "production readiness"


def test_promotional_claim_with_boundary_language_is_allowed():
    findings = find_promotional_claim_findings(
        Path("docs/evals/runs/example-local-llm-solver-orchestration/evidence-boundary.md"),
        "## Evidence boundary\n\nThis does not prove production readiness.\n",
    )

    assert findings == []


def test_final_packet_contains_required_boundary_phrases():
    findings = find_required_final_packet_findings()

    assert findings == []
    packet_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(FINAL_PACKET_DIR.rglob("*"))
        if path.is_file() and path.suffix == ".md"
    )
    for phrase in REQUIRED_FINAL_PACKET_PHRASES:
        assert phrase in packet_text


def test_current_relevant_docs_pass_static_check():
    docs = iter_relevant_docs()

    assert docs, "expected local LLM solver orchestration docs to be discovered"
    assert check_paths(docs) == []
