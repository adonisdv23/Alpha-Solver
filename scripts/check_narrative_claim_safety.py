#!/usr/bin/env python3
"""Offline narrative claim-safety linter for docs packets and narrative artifacts.

The checker flags high-risk unsupported claim wording in narrative Markdown/text
artifacts. It is intentionally conservative and incomplete: a pass means only
that the configured static phrases were not found outside allowed boundary or
suppression contexts. It does not validate product behavior, benchmarks,
security, privacy, providers, public exposure, or readiness.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".txt", ".rst"}
LANE_ID = "ALPHA-SOLVER-NARRATIVE-CLAIM-SAFETY-LINTER-001"
SUPPRESSION_TOKEN = "claim-safety-ignore"
MIN_RATIONALE_CHARS = 16


@dataclass(frozen=True)
class ClaimRule:
    family: str
    pattern: re.Pattern[str]
    allowed_alternative: str


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    family: str
    snippet: str
    message: str
    allowed_alternative: str

    def format(self) -> str:
        return (
            f"{self.path}:{self.line}: {self.family}: {self.message}: "
            f"{self.snippet!r}; bounded alternative: {self.allowed_alternative}"
        )


@dataclass(frozen=True)
class SuppressionFinding:
    path: Path
    line: int
    message: str

    def format(self) -> str:
        return f"{self.path}:{self.line}: suppression: {self.message}"


CLAIM_RULES: tuple[ClaimRule, ...] = tuple(
    ClaimRule(family, re.compile(pattern, re.IGNORECASE), alternative)
    for family, pattern, alternative in (
        (
            "readiness",
            r"\b(?:mvp|production|pilot|release|customer|runtime|public)\s*-?\s*ready\b|\bready\s+for\s+(?:production|customers|public|launch|scale|pilot)\b|\bproduction readiness (?:is )?(?:proven|validated|confirmed|achieved)\b",
            "State the artifact is operator-review-ready or records a limited local/supervised check, with remaining blockers.",
        ),
        (
            "validation",
            r"\b(?:validates?|validated|proves?|proven|confirms?|certifies?)\s+(?:the\s+)?(?:mvp|product|system|solver|alpha solver|readiness|architecture)\b|\b(?:mvp|product|system|solver|alpha solver)\s+(?:is\s+)?(?:validated|proven|certified)\b",
            "Say the check produced bounded evidence for the named fixture/run and list non-claims.",
        ),
        (
            "benchmark",
            r"\bbenchmark(?:ed|s)?\s+(?:show|shows|prove|proves|confirm|confirms|validate|validates)\b|\b(?:statistically significant|sota|state-of-the-art|best-in-class)\b|\b(?:wins?|outperforms?|beats?)\s+(?:benchmarks?|baselines?|plain providers?|competitors?)\b",
            "Describe the exact sample, prompt set, and metric as exploratory or fixture-bound rather than benchmark proof.",
        ),
        (
            "superiority",
            r"\b(?:alpha solver|alpha)\s+(?:is\s+)?(?:better|superior|smarter|more accurate|more reliable)\s+than\b|\b(?:outperforms?|beats?|surpasses)\s+(?:plain\s+)?(?:providers?|models?|chatgpt|openai)\b",
            "Use comparison-specific wording such as 'in this limited fixture, reviewer X preferred output Y for criterion Z'.",
        ),
        (
            "provider",
            r"\b(?:openai|anthropic|gemini|hosted provider|provider)\s+(?:validated|approved|certified|confirmed)\b|\bprovider\s+(?:reasoning\s+)?orchestration\s+(?:is\s+)?(?:validated|proven|ready|confirmed)\b|\b(?:uses|calls)\s+live\s+(?:openai|providers?)\b",
            "State provider behavior only when directly evidenced, otherwise say provider-backed execution was not run or remains out of scope.",
        ),
        (
            "public_exposure",
            r"\b(?:publicly accessible|public endpoint|internet-facing|open to the public|available to everyone|externally exposed)\b|\b(?:safe|approved)\s+for\s+public\s+(?:use|sharing|launch|exposure)\b",
            "Say whether an artifact is local, private, authenticated, or not assessed for public exposure.",
        ),
        (
            "security_privacy",
            r"\b(?:secure|security (?:validated|proven|certified)|privacy (?:validated|proven|certified)|pii-safe|secret-safe|no secrets? can leak|cannot leak|fully redacted|zero risk)\b",
            "Use bounded wording such as 'static checks found no known test secret fixture leaks; security/privacy review remains incomplete'.",
        ),
    )
)

BOUNDARY_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bnon[-_ ]claims?\b",
        r"\bclaim[-_ ]boundar(?:y|ies)\b",
        r"\bdoes not claim\b",
        r"\bdoes not .*\b(?:validate|prove|confirm|certify)\b",
        r"\bmust not claim\b",
        r"\bno .* claim\b",
        r"\bunsupported .* claim\b",
        r"\bblocked claims?\b",
        r"\bout of scope\b",
        r"\bresidual risks?\b",
        r"\bnot (?:validated|proven|ready|secure|public)\b",
    )
)


def _repo_relative(path: Path, root: Path = ROOT) -> Path:
    try:
        return path.resolve().relative_to(root.resolve())
    except ValueError:
        return path


def _window(lines: Sequence[str], index: int, radius: int = 2) -> str:
    return "\n".join(lines[max(0, index - radius) : min(len(lines), index + radius + 1)])


def _has_boundary_context(text: str) -> bool:
    return any(pattern.search(text) for pattern in BOUNDARY_PATTERNS)


def _suppression_rationale(line: str) -> str | None:
    if SUPPRESSION_TOKEN not in line:
        return None
    match = re.search(r"claim-safety-ignore\s*:\s*rationale\s*=\s*(.+)$", line, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _line_has_valid_suppression(line: str) -> bool:
    rationale = _suppression_rationale(line)
    return rationale is not None and len(rationale) >= MIN_RATIONALE_CHARS


def find_suppression_findings(path: Path, text: str) -> list[SuppressionFinding]:
    findings: list[SuppressionFinding] = []
    for index, line in enumerate(text.splitlines()):
        rationale = _suppression_rationale(line)
        if rationale is not None and len(rationale) < MIN_RATIONALE_CHARS:
            findings.append(
                SuppressionFinding(
                    path=path,
                    line=index + 1,
                    message="claim-safety-ignore requires 'rationale=' with an explicit rationale of at least 16 characters",
                )
            )
    return findings


def find_claim_findings(path: Path, text: str) -> list[Finding]:
    lines = text.splitlines()
    findings: list[Finding] = []
    for index, line in enumerate(lines):
        if _line_has_valid_suppression(line):
            continue
        for rule in CLAIM_RULES:
            match = rule.pattern.search(line)
            if not match:
                continue
            if _has_boundary_context(_window(lines, index, radius=2)):
                continue
            findings.append(
                Finding(
                    path=path,
                    line=index + 1,
                    family=rule.family,
                    snippet=match.group(0),
                    message="unsupported narrative claim requires evidence boundary or explicit suppression rationale",
                    allowed_alternative=rule.allowed_alternative,
                )
            )
    return findings


def iter_default_paths(root: Path = ROOT) -> list[Path]:
    bases = [root / "docs" / "evals" / "runs", root / "docs" / "narrative"]
    paths: list[Path] = []
    for base in bases:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                paths.append(_repo_relative(path, root))
    return sorted(paths, key=lambda item: item.as_posix())


def check_paths(paths: Iterable[Path], root: Path = ROOT) -> tuple[list[Finding], list[SuppressionFinding]]:
    claim_findings: list[Finding] = []
    suppression_findings: list[SuppressionFinding] = []
    for rel_path in paths:
        path = root / rel_path
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        suppression_findings.extend(find_suppression_findings(rel_path, text))
        claim_findings.extend(find_claim_findings(rel_path, text))
    return claim_findings, suppression_findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check narrative docs for unsupported claim wording.")
    parser.add_argument("paths", nargs="*", type=Path, help="Repo-relative files to scan. Defaults to docs/evals/runs and docs/narrative.")
    args = parser.parse_args(argv)

    paths = args.paths or iter_default_paths(ROOT)
    claim_findings, suppression_findings = check_paths(paths, ROOT)
    if claim_findings or suppression_findings:
        print(f"{LANE_ID} failed:", file=sys.stderr)
        for finding in suppression_findings:
            print(f"  {finding.format()}", file=sys.stderr)
        for finding in claim_findings:
            print(f"  {finding.format()}", file=sys.stderr)
        return 1
    print(f"{LANE_ID} passed ({len(paths)} files scanned). This is not a completeness claim.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
