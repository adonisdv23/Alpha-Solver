#!/usr/bin/env python3
"""Static evidence-boundary checker for local LLM solver orchestration docs.

Purpose and limits:
- This is a deterministic, offline documentation hardening check.
- It scans local LLM solver orchestration evidence-boundary docs for risky
  promotional claim phrases and requires nearby boundary language.
- It also checks that the final Level 3 closeout packet preserves the accepted
  non-promotional boundary phrases.
- It does not validate behavior, run benchmarks, call models/providers, read
  secrets, start Ollama, or exercise runtime routes.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = Path("docs/evals/runs")
DOCS_DIR_PREFIXES = (
    "docs/local_llm_solver_orchestration",
)
LOCAL_ORCHESTRATION_DIR_MARKER = "local-llm-solver-orchestration"
SOURCE_ARTIFACT_MARKERS = (
    "/source-artifact/",
    "-source-artifact-",
)
TEXT_SUFFIXES = {".md", ".txt", ".rst"}

LANE_NAME = "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-EVIDENCE-BOUNDARY-STATIC-CHECK-SCAFFOLD-001"
SELECTED_NEXT_ACTION = "NO_FURTHER_EVIDENCE_BOUNDARY_STATIC_CHECK_SCAFFOLD_LANES_SELECTED"
BLOCKER_FALLBACK_LANE = "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-EVIDENCE-BOUNDARY-STATIC-CHECK-SCAFFOLD-FIX-001"

FINAL_PACKET_DIR = Path(
    "docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/closeout"
)
AUTHORITATIVE_FINAL_PACKET_FILES = (
    "README.md",
    "accepted-result.md",
    "final-boundary.md",
    "final-status.md",
    "selected-next-action.md",
    "blocked-claims.md",
)
REQUIRED_FINAL_PACKET_PHRASES = (
    "behavior_evidence=False",
    "no_hosted_fallback=True",
    "no_provider_keys_required=True",
    "NO_FURTHER_LEVEL_3_VALIDATION_LANES_SELECTED",
    "LEVEL_3_VALIDATION_EXECUTION_ACCEPTED_AS_ARTIFACT_COMPLETE_NON_PROMOTIONAL_LOCAL_ORCHESTRATION_EVIDENCE",
)

UNSUPPORTED_CLAIM_PHRASES = (
    "production readiness",
    "MVP readiness",
    "benchmark evidence",
    "local model quality evidence",
    "provider-orchestration evidence",
    "provider orchestration evidence",
    "Alpha superiority",
    "billing evidence",
    "dashboard readiness",
    "/v1/solve readiness",
    "broad runtime readiness",
    "evidence-model promotion",
    "provider fallback readiness",
    "hosted fallback readiness",
)

BOUNDARY_LANGUAGE_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bblocked(?:-|\s)?claims?\b",
        r"\bevidence(?:-|\s)?boundary\b",
        r"\bboundary\b",
        r"\bdecision boundary\b",
        r"\baccepted boundary\b",
        r"\bexcluded(?: evidence)? categories\b",
        r"\bnon(?:-|\s)?claims?\b",
        r"\bnon(?:-|\s)?actions?\b",
        r"\bnon(?:-|\s)?decision\b",
        r"\bnon(?:-|\s)?execution\b",
        r"\bnon(?:-|\s)?promotional\b",
        r"\bunsupported\b",
        r"\bdenied\b",
        r"\bunsafe\b",
        r"\bforbidden\b",
        r"\bnot\b",
        r"\bdoes not\b",
        r"\bdo not\b",
        r"\bno\b",
        r"\bwithout\b",
        r"\bseparate from\b",
        r"\bis not\b",
        r"\bnot prove\b",
        r"\bnot changed\b",
        r"\bremains bounded\b",
        r"\bmust not\b",
    )
)


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    phrase: str
    message: str

    def format(self) -> str:
        return f"{self.path}:{self.line}: {self.phrase}: {self.message}"


def _repo_relative(path: Path, root: Path = ROOT) -> Path:
    try:
        return path.resolve().relative_to(root.resolve())
    except ValueError:
        return path


def _is_source_artifact(path: Path) -> bool:
    as_posix = path.as_posix()
    return any(marker in as_posix for marker in SOURCE_ARTIFACT_MARKERS)


def is_relevant_doc(path: Path) -> bool:
    """Return True for local LLM solver orchestration docs that should be scanned."""
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    rel = _repo_relative(path).as_posix()
    if _is_source_artifact(Path(rel)):
        return False
    if rel.startswith(DOCS_DIR_PREFIXES):
        return True
    return rel.startswith(RUNS_DIR.as_posix()) and LOCAL_ORCHESTRATION_DIR_MARKER in rel


def iter_relevant_docs(root: Path = ROOT) -> list[Path]:
    docs: list[Path] = []
    for base in (root / "docs",):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and is_relevant_doc(path):
                docs.append(_repo_relative(path, root))
    return sorted(docs, key=lambda item: item.as_posix())


def _window(lines: list[str], index: int, radius: int = 2) -> str:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)
    return "\n".join(lines[start:end])


def _has_boundary_language(text: str) -> bool:
    return any(pattern.search(text) for pattern in BOUNDARY_LANGUAGE_PATTERNS)


def _path_is_boundary_context(path: Path) -> bool:
    path_text = path.as_posix().lower()
    return any(
        marker in path_text
        for marker in (
            "blocked",
            "boundary",
            "non-claim",
            "non_claim",
            "safe-use",
            "allowed-cli-boundary",
            "failure-modes",
            "stop-conditions",
            "checks-run",
        )
    )


def _section_context(lines: list[str], index: int) -> str:
    section_start = 0
    for candidate in range(index, -1, -1):
        if lines[candidate].lstrip().startswith("#"):
            section_start = candidate
            break
    return "\n".join(lines[section_start : index + 1])


def find_promotional_claim_findings(path: Path, text: str) -> list[Finding]:
    if _path_is_boundary_context(path):
        return []

    lines = text.splitlines()
    findings: list[Finding] = []
    for index, line in enumerate(lines):
        for phrase in UNSUPPORTED_CLAIM_PHRASES:
            if re.search(re.escape(phrase), line, re.IGNORECASE):
                context = "\n".join((_window(lines, index, radius=3), _section_context(lines, index)))
                if not _has_boundary_language(context):
                    findings.append(
                        Finding(
                            path=path,
                            line=index + 1,
                            phrase=phrase,
                            message="unsupported promotional claim phrase lacks nearby boundary language",
                        )
                    )
    return findings


def find_required_final_packet_findings(root: Path = ROOT) -> list[Finding]:
    packet_dir = root / FINAL_PACKET_DIR
    if not packet_dir.exists():
        return [
            Finding(
                path=FINAL_PACKET_DIR,
                line=1,
                phrase="final packet directory",
                message="required final packet directory is missing",
            )
        ]
    combined_parts: list[str] = []
    for name in AUTHORITATIVE_FINAL_PACKET_FILES:
        path = packet_dir / name
        if path.is_file():
            combined_parts.append(path.read_text(encoding="utf-8"))
    combined = "\n".join(combined_parts)
    findings: list[Finding] = []
    for phrase in REQUIRED_FINAL_PACKET_PHRASES:
        if phrase not in combined:
            findings.append(
                Finding(
                    path=FINAL_PACKET_DIR,
                    line=1,
                    phrase=phrase,
                    message="required final packet boundary phrase is missing",
                )
            )
    return findings


def check_paths(paths: Iterable[Path], root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    for rel_path in paths:
        path = root / rel_path
        text = path.read_text(encoding="utf-8")
        findings.extend(find_promotional_claim_findings(rel_path, text))
    findings.extend(find_required_final_packet_findings(root))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check local LLM solver orchestration docs for evidence-boundary phrasing."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Optional repo-relative files to scan. Defaults to relevant docs.",
    )
    args = parser.parse_args(argv)

    paths = args.paths or iter_relevant_docs(ROOT)
    paths = [path for path in paths if is_relevant_doc(path)]
    findings = check_paths(paths, ROOT)
    if findings:
        print("Local LLM evidence-boundary static check failed:", file=sys.stderr)
        for finding in findings:
            print(f"  {finding.format()}", file=sys.stderr)
        return 1

    print(f"Local LLM evidence-boundary static check passed ({len(paths)} files scanned).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
