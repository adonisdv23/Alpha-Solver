"""Tests for the narrative claim-safety linter.

These tests use synthetic founder-style and demo-style fixtures only. They do
not call providers, run benchmarks, expose public endpoints, or validate
security/privacy behavior.
"""
from pathlib import Path

from scripts.check_narrative_claim_safety import (
    check_paths,
    find_claim_findings,
    find_suppression_findings,
)


def test_founder_style_memo_flags_multiple_unsupported_claim_families() -> None:
    text = """
# Founder update

Alpha Solver is production-ready and validates the MVP.
It outperforms plain providers and security validated for launch.
"""

    findings = find_claim_findings(Path("docs/narrative/founder-memo.md"), text)

    families = {finding.family for finding in findings}
    assert {"readiness", "validation", "superiority", "security_privacy"} <= families
    assert all("bounded alternative" not in finding.message for finding in findings)
    assert all(finding.allowed_alternative for finding in findings)


def test_demo_style_artifact_flags_benchmark_provider_and_public_claims() -> None:
    text = """
# Demo recap

Benchmarks show Alpha wins baselines.
OpenAI validated the provider orchestration.
The public endpoint is safe for public use.
"""

    findings = find_claim_findings(Path("docs/evals/runs/demo-artifact.md"), text)

    assert {finding.family for finding in findings} == {
        "benchmark",
        "provider",
        "public_exposure",
    }


def test_bounded_alternatives_with_claim_boundary_context_are_allowed() -> None:
    text = """
## Claim boundaries

This local fixture does not claim production-ready status, MVP validation,
provider orchestration validation, public exposure safety, or benchmark proof.
Residual risks remain for security and privacy review.
"""

    assert find_claim_findings(Path("docs/evals/runs/bounded.md"), text) == []


def test_suppression_requires_explicit_rationale() -> None:
    text = "Alpha Solver is production-ready. <!-- claim-safety-ignore -->\n"

    assert find_suppression_findings(Path("docs/narrative/bad.md"), text)
    assert find_claim_findings(Path("docs/narrative/bad.md"), text)


def test_valid_suppression_allows_single_line_with_rationale() -> None:
    text = (
        "Quoted customer text says production-ready. "
        "<!-- claim-safety-ignore: rationale=quoted external wording for negative test fixture -->\n"
    )

    assert find_suppression_findings(Path("docs/narrative/quoted.md"), text) == []
    assert find_claim_findings(Path("docs/narrative/quoted.md"), text) == []


def test_check_paths_reports_synthetic_fixture_findings(tmp_path: Path) -> None:
    rel = Path("docs/narrative/founder.md")
    path = tmp_path / rel
    path.parent.mkdir(parents=True)
    path.write_text("Alpha Solver is MVP-ready.\n", encoding="utf-8")

    claim_findings, suppression_findings = check_paths([rel], tmp_path)

    assert suppression_findings == []
    assert len(claim_findings) == 1
    assert claim_findings[0].family == "readiness"
