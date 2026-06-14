"""Tests for the local LLM solver orchestration evidence-boundary checker.

The checker is a static docs guard only. These tests do not run local inference,
Ollama, hosted providers, benchmarks, dashboard routes, or /v1/solve.
"""
from pathlib import Path

LOCAL_MODEL_CATALOG_PACKET_DIR = Path("docs/evals/runs/alpha-solver-local-model-catalog-001")

from scripts.check_local_llm_evidence_boundaries import (
    AUTHORITATIVE_FINAL_PACKET_FILES,
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
    assert is_relevant_doc(Path("docs/evals/runs/openai-fixture/README.md"))
    assert is_relevant_doc(Path("docs/evals/runs/local-openai-fixture/README.md"))
    assert is_relevant_doc(Path("docs/evals/runs/alpha-solver-openai-fixture/README.md"))
    assert is_relevant_doc(
        LOCAL_MODEL_CATALOG_PACKET_DIR / "README.md"
    )
    assert is_relevant_doc(
        Path("docs/evals/runs/alpha-solver-local-multi-model-smoke-harness-001/README.md")
    )
    assert not is_relevant_doc(Path("docs/RUNTIME_READINESS.md"))



def test_current_local_model_catalog_packet_files_are_discovered():
    docs = set(iter_relevant_docs())
    catalog_files = {
        path
        for path in LOCAL_MODEL_CATALOG_PACKET_DIR.glob("*.md")
        if path.is_file()
    }

    assert catalog_files, "expected local model catalog packet markdown files"
    assert catalog_files <= docs

def test_promotional_claim_without_boundary_language_is_flagged():
    findings = find_promotional_claim_findings(
        Path("docs/evals/runs/example-local-llm-solver-orchestration/example.md"),
        "This proves production readiness for the lane.\n",
    )

    assert len(findings) == 1
    assert findings[0].phrase == "production readiness"


def test_yaml_non_claims_boundary_language_is_allowed():
    findings = find_promotional_claim_findings(
        Path("docs/evals/runs/openai-fixture/template.md"),
        "```yaml\nnon_claims:\n  - production readiness\n```\n",
    )

    assert findings == []


def test_promotional_claim_with_boundary_language_is_allowed():
    findings = find_promotional_claim_findings(
        Path("docs/evals/runs/example-local-llm-solver-orchestration/evidence-boundary.md"),
        "## Evidence boundary\n\nThis does not prove production readiness.\n",
    )

    assert findings == []


def _write_authoritative_packet(root: Path, phrases: tuple[str, ...]) -> None:
    packet_dir = root / FINAL_PACKET_DIR
    packet_dir.mkdir(parents=True)
    for name in AUTHORITATIVE_FINAL_PACKET_FILES:
        (packet_dir / name).write_text("# Placeholder\n", encoding="utf-8")
    (packet_dir / "accepted-result.md").write_text("\n".join(phrases), encoding="utf-8")


def test_required_phrase_only_in_checks_run_does_not_satisfy_enforcement(tmp_path):
    missing_phrase = REQUIRED_FINAL_PACKET_PHRASES[0]
    authoritative_phrases = tuple(
        phrase for phrase in REQUIRED_FINAL_PACKET_PHRASES if phrase != missing_phrase
    )
    _write_authoritative_packet(tmp_path, authoritative_phrases)
    (tmp_path / FINAL_PACKET_DIR / "checks-run.md").write_text(
        f'`rg "{missing_phrase}" docs/evals/runs/.../closeout`\n',
        encoding="utf-8",
    )
    (tmp_path / FINAL_PACKET_DIR / "command-log.md").write_text(
        f"command output mentioned {missing_phrase}\n",
        encoding="utf-8",
    )

    findings = find_required_final_packet_findings(tmp_path)

    assert [finding.phrase for finding in findings] == [missing_phrase]


def test_required_phrases_in_authoritative_closeout_files_satisfy_enforcement(tmp_path):
    _write_authoritative_packet(tmp_path, REQUIRED_FINAL_PACKET_PHRASES)

    assert find_required_final_packet_findings(tmp_path) == []


def test_final_packet_contains_required_boundary_phrases():
    findings = find_required_final_packet_findings()

    assert findings == []
    packet_text = "\n".join(
        (FINAL_PACKET_DIR / name).read_text(encoding="utf-8")
        for name in AUTHORITATIVE_FINAL_PACKET_FILES
        if (FINAL_PACKET_DIR / name).is_file()
    )
    for phrase in REQUIRED_FINAL_PACKET_PHRASES:
        assert phrase in packet_text


def test_current_relevant_docs_pass_static_check():
    docs = iter_relevant_docs()

    assert docs, "expected local LLM solver orchestration docs to be discovered"
    assert (
        LOCAL_MODEL_CATALOG_PACKET_DIR / "README.md" in docs
    )
    assert check_paths(docs) == []
