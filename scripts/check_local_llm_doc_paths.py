#!/usr/bin/env python3
"""Offline path/link checker for local LLM solver orchestration docs.

Purpose and limits:
- This is a deterministic, offline documentation hardening check.
- It scans only local LLM solver orchestration operator docs and evidence index
  / Level 3 packet docs, excluding preserved source-artifact payload files.
- It verifies repo-relative local LLM doc packet paths and key local LLM source
  paths referenced by those docs exist in the checkout.
- It detects simple stale selected-next-lane conflicts inside one document.
- It does not call GitHub, access the network, run models/providers, start
  Ollama, expose routes, run benchmarks, or promote evidence.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".txt", ".rst"}

OPERATOR_GUIDE_DIR = Path("docs/local_llm_solver_orchestration_operator_guide")
EVIDENCE_INDEX_DIR = Path("docs/evals/runs/local-llm-solver-orchestration-index")
LEVEL_3_PACKET_DIR = Path(
    "docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001"
)
LEVEL_3_SCAN_DIRS = (
    LEVEL_3_PACKET_DIR / "closeout",
    LEVEL_3_PACKET_DIR / "import-final-decision",
)
# The source-artifact directory is a key path that may be referenced and must
# exist, but preserved payload files inside it are intentionally not scanned.
LEVEL_3_SOURCE_ARTIFACT_DIR = LEVEL_3_PACKET_DIR / "source-artifact"

SCAN_DIRS = (
    OPERATOR_GUIDE_DIR,
    EVIDENCE_INDEX_DIR,
    *LEVEL_3_SCAN_DIRS,
)
REQUIRED_SOURCE_OF_TRUTH_PATHS = (
    OPERATOR_GUIDE_DIR,
    EVIDENCE_INDEX_DIR,
    LEVEL_3_SCAN_DIRS[0],
    LEVEL_3_SCAN_DIRS[1],
    LEVEL_3_SOURCE_ARTIFACT_DIR,
)

REPO_RELATIVE_PREFIXES = (
    "docs/",
    ".specs/",
    "scripts/",
    "tests/",
    "alpha/",
)
LOCAL_LLM_MARKERS = (
    "local_llm",
    "local-llm",
    "LOCAL-LLM",
    "local LLM",
)
IGNORED_LINK_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "#",
    "javascript:",
)
SOURCE_ARTIFACT_MARKERS = (
    "/source-artifact/",
    "-source-artifact-",
)

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
AUTOLINK_RE = re.compile(r"<([^<>\s]+)>")
BACKTICK_RE = re.compile(r"`([^`]+)`")
BARE_REPO_PATH_RE = re.compile(
    r"(?<![\w./-])((?:docs|scripts|tests|alpha)/[^\s)\],;:'\"<>]+|\.specs/[^\s)\],;:'\"<>]+)"
)
LOCAL_LANE_RE = re.compile(r"\b(?:ALPHA|NO_FURTHER|STOP-HERE)[A-Z0-9_-]*(?:LOCAL[-_]LLM|LEVEL_3|DOCS_LINK_PATH_CHECKER)[A-Z0-9_-]*\b")
SELECTED_CONTEXT_RE = re.compile(r"\bselected\s+next\s+(?:action|lane)\b", re.IGNORECASE)
HISTORICAL_CONTEXT_RE = re.compile(
    r"\b(?:prior|preserved|historical|previous|remains|closed|level\s*2|level\s*3|blocker|fallback|fix)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    reference: str
    message: str

    def format(self) -> str:
        return f"{self.path}:{self.line}: {self.reference}: {self.message}"


@dataclass(frozen=True)
class Reference:
    path: Path
    line: int
    target: str


def _repo_relative(path: Path, root: Path = ROOT) -> Path:
    try:
        return path.resolve().relative_to(root.resolve())
    except ValueError:
        return path


def _normalize_posix(value: str) -> str:
    value = unquote(value.strip())
    value = value.split("#", 1)[0].split("?", 1)[0]
    value = value.strip().strip("`.,;:")
    return value


def _is_ignored_link(value: str) -> bool:
    lowered = value.lower()
    return not value or any(lowered.startswith(prefix) for prefix in IGNORED_LINK_PREFIXES)


def _looks_repo_relative(value: str) -> bool:
    return value.startswith(REPO_RELATIVE_PREFIXES)


def _looks_local_llm_reference(value: str) -> bool:
    return _looks_repo_relative(value) and any(marker in value for marker in LOCAL_LLM_MARKERS)


def _is_source_artifact_payload(path: Path) -> bool:
    rel = path.as_posix()
    return any(marker in rel for marker in SOURCE_ARTIFACT_MARKERS)


def is_scanned_doc(path: Path, root: Path = ROOT) -> bool:
    """Return True when a file belongs to the narrow doc-checker scan set."""
    rel = _repo_relative(path, root)
    if rel.suffix.lower() not in TEXT_SUFFIXES:
        return False
    if _is_source_artifact_payload(rel):
        return False
    rel_text = rel.as_posix()
    return any(rel_text == base.as_posix() or rel_text.startswith(f"{base.as_posix()}/") for base in SCAN_DIRS)


def iter_scanned_docs(root: Path = ROOT) -> list[Path]:
    docs: list[Path] = []
    for scan_dir in SCAN_DIRS:
        base = root / scan_dir
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and is_scanned_doc(path, root):
                docs.append(_repo_relative(path, root))
    return sorted(set(docs), key=lambda item: item.as_posix())


def _iter_candidate_tokens(line: str) -> Iterator[str]:
    for pattern in (MARKDOWN_LINK_RE, AUTOLINK_RE, BACKTICK_RE, BARE_REPO_PATH_RE):
        for match in pattern.finditer(line):
            yield match.group(1)


def extract_local_references(path: Path, text: str) -> list[Reference]:
    """Extract repo-relative local LLM references from a markdown/text doc."""
    references: list[Reference] = []
    for index, line in enumerate(text.splitlines(), start=1):
        for raw in _iter_candidate_tokens(line):
            target = _normalize_posix(raw)
            if _is_ignored_link(target):
                continue
            if _looks_local_llm_reference(target):
                references.append(Reference(path=path, line=index, target=target))
    return references


def find_missing_path_findings(paths: Iterable[Path], root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[tuple[Path, int, str]] = set()
    for rel_path in paths:
        text = (root / rel_path).read_text(encoding="utf-8")
        for reference in extract_local_references(rel_path, text):
            key = (reference.path, reference.line, reference.target)
            if key in seen:
                continue
            seen.add(key)
            candidate = root / reference.target
            if not candidate.exists():
                findings.append(
                    Finding(
                        path=reference.path,
                        line=reference.line,
                        reference=reference.target,
                        message="referenced local LLM repo path does not exist",
                    )
                )
    return findings


def find_required_source_path_findings(root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    for rel_path in REQUIRED_SOURCE_OF_TRUTH_PATHS:
        if not (root / rel_path).exists():
            findings.append(
                Finding(
                    path=rel_path,
                    line=1,
                    reference=rel_path.as_posix(),
                    message="required local LLM source-of-truth path is missing",
                )
            )
    return findings


def _selected_context_has_exemption(line: str, window: str) -> bool:
    return bool(HISTORICAL_CONTEXT_RE.search(line) or HISTORICAL_CONTEXT_RE.search(window))


def find_selected_next_conflict_findings(path: Path, text: str) -> list[Finding]:
    """Find simple stale selected-next conflicts within one document.

    Multiple selected-next statements are allowed when the nearby text clearly
    marks one as prior/preserved/historical/closed or as a blocker/fallback. A
    conflict is reported when one doc presents multiple distinct selected-next
    actions without that context.
    """
    lines = text.splitlines()
    current_selected: tuple[int, str] | None = None
    findings: list[Finding] = []
    for index, line in enumerate(lines):
        if not SELECTED_CONTEXT_RE.search(line):
            continue
        window_lines = lines[index : min(len(lines), index + 5)]
        window = "\n".join(window_lines)
        lanes = sorted(set(LOCAL_LANE_RE.findall(window)))
        if not lanes:
            continue
        if _selected_context_has_exemption(line, window):
            continue
        selected_value = lanes[-1]
        if current_selected and current_selected[1] != selected_value:
            findings.append(
                Finding(
                    path=path,
                    line=index + 1,
                    reference=selected_value,
                    message=(
                        "conflicting selected-next action appears in same doc; "
                        f"earlier selected-next action at line {current_selected[0]} is {current_selected[1]}"
                    ),
                )
            )
        else:
            current_selected = (index + 1, selected_value)
    return findings


def check_paths(paths: Iterable[Path], root: Path = ROOT) -> list[Finding]:
    rel_paths = [Path(path) for path in paths]
    findings: list[Finding] = []
    findings.extend(find_missing_path_findings(rel_paths, root))
    for rel_path in rel_paths:
        text = (root / rel_path).read_text(encoding="utf-8")
        findings.extend(find_selected_next_conflict_findings(rel_path, text))
    findings.extend(find_required_source_path_findings(root))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check local LLM solver orchestration docs for stale or broken local repo paths."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Optional repo-relative docs to scan. Defaults to the local LLM orchestration docs/index packets.",
    )
    args = parser.parse_args(argv)

    paths = args.paths or iter_scanned_docs(ROOT)
    paths = [path for path in paths if is_scanned_doc(path, ROOT)]
    findings = check_paths(paths, ROOT)
    if findings:
        print("Local LLM doc path/link check failed:", file=sys.stderr)
        for finding in findings:
            print(f"  {finding.format()}", file=sys.stderr)
        return 1

    print(f"Local LLM doc path/link check passed ({len(paths)} files scanned).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
