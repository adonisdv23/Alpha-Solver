#!/usr/bin/env python3
"""Static packet-consistency checker for local LLM solver orchestration, OpenAI, and DEF evidence packet docs.

Purpose and limits:
- This is a deterministic, offline documentation hardening check.
- It scans local LLM solver orchestration packet directories, OpenAI evidence
  packet directories, alpha-solver-def-* custody packet directories, and the
  local LLM solver orchestration operator guide selected-next-lane state.
- It validates lane packet continuity files, blocker fallbacks, evidence
  boundary or blocked-claims files, final decision markers, and contradictory
  selected-next state.
- It does not run local models, call Ollama, call hosted providers, exercise
  /v1/solve or dashboard routes, deploy, benchmark, bill, or promote evidence.
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
OPERATOR_GUIDE_SELECTED_NEXT_LANE = Path(
    "docs/local_llm_solver_orchestration_operator_guide/selected-next-lane.md"
)
INDEX_DECISION_LEDGER = Path(
    "docs/evals/runs/local-llm-solver-orchestration-index/decision-ledger.md"
)
INDEX_LANE_MAP = Path("docs/evals/runs/local-llm-solver-orchestration-index/lane-map.md")

PACKET_DIR_MARKERS = (
    "local-llm-solver-orchestration",
    "20260607-local-llm-controlled-usage-operator-run-001",
    "alpha-solver-post-level-3-",
    "alpha-solver-post-level-7-",
    "alpha-solver-def-",
    "alpha-solver-local-",
    "openai-",
    "local-openai-",
    "alpha-solver-openai-",
)
SOURCE_ARTIFACT_MARKERS = (
    "/source-artifact/",
    "-source-artifact-",
)

SELECTED_NEXT_FILES = ("selected-next-lane.md", "selected-next-action.md")
BLOCKER_FALLBACK_FILE = "blocker-fallback-lane.md"
BOUNDARY_FILES = (
    "evidence-boundary.md",
    "final-boundary.md",
    "blocked-claims.md",
    "blocked-work.md",
    "blocked-downstream-claims.md",
    "non-claims-and-boundaries.md",
    "non-actions.md",
)

AUTHORITATIVE_DECISION_FILES = (
    "final-decision.md",
    "accepted-result.md",
    "final-status.md",
    "selected-next-lane.md",
    "selected-next-action.md",
    "README.md",
    "closeout-summary.md",
    "current-state-summary.md",
    "decision-summary.md",
    "selected-decision.md",
)

FINAL_LEVEL_3_CLOSEOUT_DIR = Path(
    "docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/closeout"
)
CONTROLLED_USAGE_IMPORT_DIR = Path(
    "docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/import-final-decision"
)
CONTROLLED_USAGE_CLOSEOUT_DIR = Path(
    "docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/closeout"
)
LEVEL_3_IMPORT_DIR = Path(
    "docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/import-final-decision"
)

CONTROLLED_USAGE_ACCEPTED = "CONTROLLED_USAGE_OPERATOR_RUN_ACCEPTED_AS_LEVEL_2_OPERATOR_USABILITY_ARTIFACT"
LEVEL_3_ACCEPTED = (
    "LEVEL_3_VALIDATION_EXECUTION_ACCEPTED_AS_ARTIFACT_COMPLETE_NON_PROMOTIONAL_LOCAL_ORCHESTRATION_EVIDENCE"
)
NO_FURTHER_LEVEL_3 = "NO_FURTHER_LEVEL_3_VALIDATION_LANES_SELECTED"

EXPECTED_DECISION_LOCATIONS = {
    CONTROLLED_USAGE_ACCEPTED: (CONTROLLED_USAGE_IMPORT_DIR, CONTROLLED_USAGE_CLOSEOUT_DIR),
    LEVEL_3_ACCEPTED: (LEVEL_3_IMPORT_DIR, FINAL_LEVEL_3_CLOSEOUT_DIR),
    NO_FURTHER_LEVEL_3: (FINAL_LEVEL_3_CLOSEOUT_DIR,),
}

LANE_TOKEN_RE = re.compile(r"\bALPHA-[A-Z0-9][A-Z0-9-]*-00[0-9]\b")
NO_FURTHER_RE = re.compile(r"\bNO_FURTHER_[A-Z0-9_]+_LANES_SELECTED\b")
BLOCKER_PATTERN_RE = re.compile(r"blocker[- ]fallback[- ]lane", re.IGNORECASE)
BOUNDARY_PATTERN_RE = re.compile(
    r"(evidence[- ]boundary|blocked[- ]claims|non[- ]actions|non[- ]claims)",
    re.IGNORECASE,
)
CLOSED_PATTERN_RE = re.compile(
    r"\b(closed|closeout|no follow-on lane|no further lanes?)\b", re.IGNORECASE
)
IMPLEMENTATION_LANE_RE = re.compile(
    r"\bALPHA-[A-Z0-9-]*IMPLEMENTATION[A-Z0-9-]*-00[0-9]\b"
)


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str

    def format(self) -> str:
        return f"{self.path}: {self.message}"


def _repo_relative(path: Path, root: Path = ROOT) -> Path:
    try:
        return path.resolve().relative_to(root.resolve())
    except ValueError:
        return path


def _is_source_artifact(path: Path) -> bool:
    path_parts = path.parts
    path_text = path.as_posix()
    has_source_artifact_part = any(
        part == "source-artifact" or part.endswith("-source-artifact")
        for part in path_parts
    )
    return has_source_artifact_part or any(
        marker in path_text for marker in SOURCE_ARTIFACT_MARKERS
    )


def is_packet_dir(path: Path, root: Path = ROOT) -> bool:
    """Return True when a directory is an in-scope orchestration packet."""
    rel = _repo_relative(path, root).as_posix()
    if _is_source_artifact(Path(rel)):
        return False
    if not rel.startswith(RUNS_DIR.as_posix() + "/"):
        return False
    if rel == "docs/evals/runs/local-llm-solver-orchestration-index":
        return False
    if not any(marker in rel for marker in PACKET_DIR_MARKERS):
        return False
    return (path / "README.md").is_file()


def iter_packet_dirs(root: Path = ROOT) -> list[Path]:
    packets: list[Path] = []
    runs = root / RUNS_DIR
    if not runs.exists():
        return packets
    for readme in runs.rglob("README.md"):
        packet_dir = _repo_relative(readme.parent, root)
        if is_packet_dir(root / packet_dir, root):
            packets.append(packet_dir)
    return sorted(set(packets), key=lambda item: item.as_posix())


def _read_optional(root: Path, rel_path: Path) -> str:
    path = root / rel_path
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _packet_text(root: Path, packet_dir: Path) -> str:
    parts: list[str] = []
    for child in sorted((root / packet_dir).iterdir(), key=lambda item: item.name):
        if child.is_file() and child.suffix.lower() in {".md", ".txt"}:
            parts.append(child.read_text(encoding="utf-8"))
    return "\n".join(parts)


def _authoritative_packet_text(root: Path, packet_dir: Path) -> str:
    """Return text from files that are authoritative for packet decisions.

    Generated command logs such as checks-run.md, stdout/stderr captures,
    transcripts, and source-artifact payloads are intentionally excluded so
    recorded commands or rg output cannot satisfy required decision markers.
    """
    parts: list[str] = []
    for name in AUTHORITATIVE_DECISION_FILES:
        path = root / packet_dir / name
        if path.is_file():
            parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


def _selected_file_paths(root: Path, packet_dir: Path) -> list[Path]:
    return [
        packet_dir / name
        for name in SELECTED_NEXT_FILES
        if (root / packet_dir / name).is_file()
    ]


def _selected_state_text(root: Path, packet_dir: Path) -> str:
    return "\n".join(
        _read_optional(root, path) for path in _selected_file_paths(root, packet_dir)
    )


def _packet_requires_blocker_fallback(packet_dir: Path, packet_text: str) -> bool:
    rel = packet_dir.as_posix()
    return (
        "20260607-local-llm-controlled-usage-operator-run-001" in rel
        or "20260607-local-llm-solver-orchestration-level-3-validation" in rel
        or bool(BLOCKER_PATTERN_RE.search(packet_text))
    )


def _packet_requires_boundary(packet_dir: Path, packet_text: str) -> bool:
    rel = packet_dir.as_posix()
    return (
        "20260607-local-llm-controlled-usage-operator-run-001" in rel
        or "20260607-local-llm-solver-orchestration-level-3-validation" in rel
        or bool(BOUNDARY_PATTERN_RE.search(packet_text))
    )


def _has_boundary_file(root: Path, packet_dir: Path) -> bool:
    return any((root / packet_dir / name).is_file() for name in BOUNDARY_FILES)


def _has_explicit_closed_no_next(text: str) -> bool:
    return bool(NO_FURTHER_RE.search(text)) or (
        bool(CLOSED_PATTERN_RE.search(text)) and "No follow-on lane is started" in text
    )


def _lane_tokens(text: str) -> set[str]:
    return set(LANE_TOKEN_RE.findall(text))


def _future_selected_lane_tokens(text: str) -> set[str]:
    tokens = _lane_tokens(text)
    return {token for token in tokens if "FALLBACK" not in token and "FIX" not in token}


def check_packet_dir(packet_dir: Path, root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    packet_text = _packet_text(root, packet_dir)
    selected_paths = _selected_file_paths(root, packet_dir)
    selected_text = _selected_state_text(root, packet_dir)

    if not selected_paths and not _has_explicit_closed_no_next(packet_text):
        findings.append(
            Finding(packet_dir, "missing selected-next-lane.md or selected-next-action.md")
        )

    if len(selected_paths) > 1:
        findings.append(
            Finding(packet_dir, "contains both selected-next-lane.md and selected-next-action.md")
        )

    if _packet_requires_blocker_fallback(packet_dir, packet_text) and not (
        root / packet_dir / BLOCKER_FALLBACK_FILE
    ).is_file():
        findings.append(Finding(packet_dir, "missing required blocker-fallback-lane.md"))

    if _packet_requires_boundary(packet_dir, packet_text) and not _has_boundary_file(
        root, packet_dir
    ):
        findings.append(
            Finding(
                packet_dir,
                "missing required evidence-boundary, blocked-claims, "
                "non-actions, or blocked-work file",
            )
        )

    selected_no_further = bool(NO_FURTHER_RE.search(selected_text))
    future_selected = _future_selected_lane_tokens(selected_text)
    if selected_no_further and future_selected:
        findings.append(
            Finding(
                packet_dir,
                "selected-next state contains both no-further-lanes and a future selected lane/action",
            )
        )

    if selected_no_further and IMPLEMENTATION_LANE_RE.search(packet_text):
        findings.append(
            Finding(
                packet_dir,
                "closed packet says no further lanes but also references a future implementation lane",
            )
        )

    return findings


def check_operator_guide(root: Path = ROOT) -> list[Finding]:
    path = OPERATOR_GUIDE_SELECTED_NEXT_LANE
    text = _read_optional(root, path)
    if not text:
        return [Finding(path, "operator guide selected-next-lane.md is missing")]

    findings: list[Finding] = []
    if LEVEL_3_ACCEPTED not in text:
        findings.append(Finding(path, "missing final accepted Level 3 decision"))
    if NO_FURTHER_LEVEL_3 not in text:
        findings.append(
            Finding(path, "missing post-Level-3 no-further-lanes closeout state")
        )

    future_selected = _future_selected_lane_tokens(text)
    # The current guide may record only closed/no-further state and its docs
    # consolidation no-further action. A concrete ALPHA lane here would stale the
    # guide against the Level 3 closeout.
    if future_selected:
        findings.append(
            Finding(path, "operator guide selected-next-lane state selects a future ALPHA lane")
        )
    return findings


def check_expected_decisions(root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    for phrase, dirs in EXPECTED_DECISION_LOCATIONS.items():
        for packet_dir in dirs:
            if not (root / packet_dir).is_dir():
                findings.append(
                    Finding(
                        packet_dir,
                        f"expected decision packet directory is missing for {phrase}",
                    )
                )
                continue
            if phrase not in _authoritative_packet_text(root, packet_dir):
                findings.append(
                    Finding(packet_dir, f"missing expected decision marker {phrase}")
                )

    ledger_text = _read_optional(root, INDEX_DECISION_LEDGER)
    lane_map_text = _read_optional(root, INDEX_LANE_MAP)
    for phrase in (CONTROLLED_USAGE_ACCEPTED, LEVEL_3_ACCEPTED, NO_FURTHER_LEVEL_3):
        if phrase not in ledger_text:
            findings.append(
                Finding(
                    INDEX_DECISION_LEDGER,
                    f"missing indexed final decision marker {phrase}",
                )
            )
    if NO_FURTHER_LEVEL_3 not in lane_map_text:
        findings.append(
            Finding(
                INDEX_LANE_MAP,
                f"missing lane-map closeout marker {NO_FURTHER_LEVEL_3}",
            )
        )
    return findings


def check_packet_consistency(
    packet_dirs: Iterable[Path] | None = None, root: Path = ROOT
) -> list[Finding]:
    dirs = list(packet_dirs) if packet_dirs is not None else iter_packet_dirs(root)
    findings: list[Finding] = []
    for packet_dir in dirs:
        findings.extend(check_packet_dir(packet_dir, root))
    findings.extend(check_operator_guide(root))
    findings.extend(check_expected_decisions(root))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check local LLM solver orchestration packet consistency."
    )
    parser.add_argument(
        "packet_dirs",
        nargs="*",
        type=Path,
        help=(
            "Optional repo-relative packet directories. Defaults to discovered "
            "local LLM packet directories."
        ),
    )
    args = parser.parse_args(argv)

    packet_dirs = args.packet_dirs or iter_packet_dirs(ROOT)
    findings = check_packet_consistency(packet_dirs, ROOT)
    if findings:
        print("Local LLM packet consistency check failed:", file=sys.stderr)
        for finding in findings:
            print(f"  {finding.format()}", file=sys.stderr)
        return 1

    print(
        f"Local LLM packet consistency check passed "
        f"({len(packet_dirs)} packet directories scanned)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
