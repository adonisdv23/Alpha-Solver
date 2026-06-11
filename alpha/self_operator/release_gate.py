"""Deterministic Self Operator MVP release-gate checker.

This module is a static release-control evaluator. It inspects only local file
and directory evidence, never runs providers or models, never updates Google
Sheets, and never mutates source evidence artifacts.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Literal
import json
import re

GateStatus = Literal["pass", "blocked", "missing", "needs_review"]
FinalStatus = Literal[
    "blocked_missing_execution",
    "blocked_missing_import",
    "blocked_missing_interpretation",
    "blocked_missing_runbook_finalization",
    "blocked_missing_boundary_review",
    "blocked_release_closeout_not_reviewed",
    "eligible_for_release_closeout_review",
]

RELEASE_GATE_SCHEMA_VERSION = "self_operator.release_gate_report.v1"

EXECUTION_PACKET = Path(
    "docs/evals/runs/"
    "alpha-solver-post-level-3-level-13-self-operator-operator-supervised-local-acceptance-execution"
)
IMPORT_PACKET = Path(
    "docs/evals/runs/"
    "alpha-solver-post-level-3-level-13-self-operator-local-acceptance-result-import-tooling"
)
INTERPRETATION_PACKET = Path(
    "docs/evals/runs/"
    "alpha-solver-post-level-3-to-level-14-self-operator-acceptance-interpretation-engine"
)
RUNBOOK_PACKET = Path(
    "docs/evals/runs/"
    "alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization"
)
BOUNDARY_PACKET = Path(
    "docs/evals/runs/"
    "alpha-solver-post-level-3-level-14-self-operator-evidence-boundary-review"
)
CLOSEOUT_PACKET = Path(
    "docs/evals/runs/"
    "alpha-solver-post-level-3-level-14-self-operator-release-closeout"
)

FOUNDATION_PACKET = Path(
    "docs/evals/runs/alpha-solver-post-level-3-level-10-self-operator-static-test-scaffold-implementation"
)
APPROVAL_PACKET = Path(
    "docs/evals/runs/alpha-solver-post-level-3-level-11-self-operator-approval-stopstate-gate-foundation"
)
DRY_RUN_PACKET = Path(
    "docs/evals/runs/alpha-solver-post-level-3-level-12-self-operator-local-harness-dry-run-wrapper"
)
MANUAL_PACKET = Path(
    "docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-manual-local-acceptance-packet"
)

GATE_ORDER = (
    "implementation_foundation_complete",
    "approval_identity_fix_complete",
    "dry_run_wrapper_complete",
    "manual_acceptance_packet_complete",
    "operator_supervised_acceptance_executed",
    "result_import_complete",
    "acceptance_interpretation_complete",
    "p0_p1_defects_absent",
    "mvp_runbook_finalized_or_updated",
    "evidence_boundary_review_complete",
    "release_closeout_review_complete",
)

_PACKET_GATES: dict[str, Path] = {
    "implementation_foundation_complete": FOUNDATION_PACKET,
    "approval_identity_fix_complete": APPROVAL_PACKET,
    "dry_run_wrapper_complete": DRY_RUN_PACKET,
    "manual_acceptance_packet_complete": MANUAL_PACKET,
    "operator_supervised_acceptance_executed": EXECUTION_PACKET,
    "result_import_complete": IMPORT_PACKET,
    "acceptance_interpretation_complete": INTERPRETATION_PACKET,
    "mvp_runbook_finalized_or_updated": RUNBOOK_PACKET,
    "evidence_boundary_review_complete": BOUNDARY_PACKET,
    "release_closeout_review_complete": CLOSEOUT_PACKET,
}

_NEXT_ACTIONS: dict[str, str] = {
    "implementation_foundation_complete": "Complete and review the Self Operator implementation foundation packet.",
    "approval_identity_fix_complete": "Complete the approval identity fix/foundation evidence before release closeout.",
    "dry_run_wrapper_complete": "Complete the local dry-run wrapper evidence packet.",
    "manual_acceptance_packet_complete": "Complete the manual acceptance packet before supervised execution.",
    "operator_supervised_acceptance_executed": "Run the operator-supervised local acceptance execution lane and preserve its packet.",
    "result_import_complete": "Run the local acceptance result import tooling lane and preserve its packet.",
    "acceptance_interpretation_complete": "Run the acceptance interpretation engine lane and preserve its packet.",
    "p0_p1_defects_absent": "Resolve and review all P0/P1 defect markers before release closeout review.",
    "mvp_runbook_finalized_or_updated": "Finalize or update the Self Operator MVP runbook packet.",
    "evidence_boundary_review_complete": "Complete the evidence-boundary review packet.",
    "release_closeout_review_complete": "Complete release closeout review only after all preceding gates pass.",
}

_DEFECT_RE = re.compile(
    r"\b(P0|P1)\b[^\n]{0,80}\b(defect|violation|failure|failed|blocker|unresolved|open)\b"
    r"|\b(defect|violation|failure|failed|blocker|unresolved|open)\b[^\n]{0,80}\b(P0|P1)\b",
    re.IGNORECASE,
)
_RESOLVED_RE = re.compile(r"\b(no|none|absent|resolved|closed)\b[^\n]{0,80}\b(P0|P1)\b", re.IGNORECASE)
# Backtick-quoted tokens such as `P0` are severity-vocabulary references
# (taxonomy/contract definitions), not unresolved defect markers.
_INLINE_CODE_RE = re.compile(r"`[^`]*`")


@dataclass(frozen=True)
class SelfOperatorReleaseGate:
    """One deterministic Self Operator release gate result."""

    gate_id: str
    status: GateStatus
    evidence_path: str
    reason: str
    required_next_action: str

    def to_dict(self) -> dict[str, str]:
        return {
            "evidence_path": self.evidence_path,
            "gate_id": self.gate_id,
            "reason": self.reason,
            "required_next_action": self.required_next_action,
            "status": self.status,
        }


@dataclass(frozen=True)
class SelfOperatorReleaseGateReport:
    """Serializable Self Operator release-gate report."""

    schema_version: str
    final_status: FinalStatus
    gates: tuple[SelfOperatorReleaseGate, ...]
    earliest_missing_gate: str | None
    ready: bool
    summary: str
    non_actions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "earliest_missing_gate": self.earliest_missing_gate,
            "final_status": self.final_status,
            "gates": [gate.to_dict() for gate in self.gates],
            "non_actions": list(self.non_actions),
            "ready": self.ready,
            "schema_version": self.schema_version,
            "summary": self.summary,
        }


def evaluate_self_operator_release_gates(repo_root: Path) -> SelfOperatorReleaseGateReport:
    """Evaluate all Self Operator MVP release gates against local repo evidence."""

    root = Path(repo_root)
    gates: list[SelfOperatorReleaseGate] = []
    for gate_id in GATE_ORDER:
        if gate_id == "p0_p1_defects_absent":
            gates.append(_p0_p1_gate(root))
        else:
            gates.append(_directory_gate(root, gate_id, _PACKET_GATES[gate_id]))

    final_status = _final_status(gates)
    ready = all(gate.status == "pass" for gate in gates)
    if ready:
        final_status = "eligible_for_release_closeout_review"
    earliest_missing = next((gate.gate_id for gate in gates if gate.status != "pass"), None)
    return SelfOperatorReleaseGateReport(
        schema_version=RELEASE_GATE_SCHEMA_VERSION,
        final_status=final_status,
        gates=tuple(gates),
        earliest_missing_gate=earliest_missing,
        ready=ready,
        summary=_summary(final_status, gates),
        non_actions=(
            "does not claim MVP readiness",
            "does not update Google Sheets",
            "does not mutate source artifacts",
            "does not run providers, hosted models, local models, external APIs, browser automation, deployment, or billing",
        ),
    )


def write_release_gate_report(report: SelfOperatorReleaseGateReport, output_path: Path) -> Path:
    """Write deterministic JSON for a release-gate report."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def _directory_gate(root: Path, gate_id: str, evidence_path: Path) -> SelfOperatorReleaseGate:
    path = root / evidence_path
    if path.is_dir():
        return SelfOperatorReleaseGate(
            gate_id=gate_id,
            status="pass",
            evidence_path=evidence_path.as_posix(),
            reason="Required evidence packet directory is present.",
            required_next_action="No action for this gate; preserve evidence boundary.",
        )
    return SelfOperatorReleaseGate(
        gate_id=gate_id,
        status="missing",
        evidence_path=evidence_path.as_posix(),
        reason="Required evidence packet directory is absent.",
        required_next_action=_NEXT_ACTIONS[gate_id],
    )


def _p0_p1_gate(root: Path) -> SelfOperatorReleaseGate:
    scanned_paths = tuple(_iter_defect_scan_paths(root))
    defect_hits: list[str] = []
    for path in scanned_paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            scannable = _INLINE_CODE_RE.sub(" ", line)
            if _DEFECT_RE.search(scannable) and not _RESOLVED_RE.search(scannable):
                rel = _repo_relative(path, root)
                defect_hits.append(f"{rel.as_posix()}:{line_no}")
    if defect_hits:
        return SelfOperatorReleaseGate(
            gate_id="p0_p1_defects_absent",
            status="blocked",
            evidence_path=";".join(defect_hits),
            reason="Unresolved P0/P1 defect marker found in release-gate evidence.",
            required_next_action=_NEXT_ACTIONS["p0_p1_defects_absent"],
        )
    return SelfOperatorReleaseGate(
        gate_id="p0_p1_defects_absent",
        status="pass",
        evidence_path=_defect_scan_root().as_posix(),
        reason="No unresolved P0/P1 defect markers found in scanned release-gate evidence.",
        required_next_action="No action for this gate; continue to preserve defect evidence boundaries.",
    )


def _iter_defect_scan_paths(root: Path) -> Iterable[Path]:
    paths: list[Path] = []
    for packet in (EXECUTION_PACKET, IMPORT_PACKET, INTERPRETATION_PACKET, RUNBOOK_PACKET, BOUNDARY_PACKET, CLOSEOUT_PACKET):
        scan_root = root / packet
        if not scan_root.is_dir():
            continue
        for path in scan_root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".txt", ".json"}:
                if "source-artifact" not in path.parts:
                    paths.append(path)
    return sorted(paths, key=lambda item: _repo_relative(item, root).as_posix())


def _defect_scan_root() -> Path:
    return Path("docs/evals/runs/self-operator-release-gate-packets")


def _repo_relative(path: Path, root: Path) -> Path:
    try:
        return path.resolve().relative_to(root.resolve())
    except ValueError:
        return path


def _final_status(gates: list[SelfOperatorReleaseGate]) -> FinalStatus:
    by_id = {gate.gate_id: gate for gate in gates}
    if by_id["operator_supervised_acceptance_executed"].status != "pass":
        return "blocked_missing_execution"
    if by_id["result_import_complete"].status != "pass":
        return "blocked_missing_import"
    if by_id["acceptance_interpretation_complete"].status != "pass":
        return "blocked_missing_interpretation"
    if by_id["p0_p1_defects_absent"].status != "pass":
        return "blocked_release_closeout_not_reviewed"
    if by_id["mvp_runbook_finalized_or_updated"].status != "pass":
        return "blocked_missing_runbook_finalization"
    if by_id["evidence_boundary_review_complete"].status != "pass":
        return "blocked_missing_boundary_review"
    if by_id["release_closeout_review_complete"].status != "pass":
        return "blocked_release_closeout_not_reviewed"
    if all(gate.status == "pass" for gate in gates):
        return "eligible_for_release_closeout_review"
    return "blocked_missing_execution"


def _summary(final_status: FinalStatus, gates: list[SelfOperatorReleaseGate]) -> str:
    passed = sum(1 for gate in gates if gate.status == "pass")
    total = len(gates)
    if final_status == "eligible_for_release_closeout_review":
        return f"{passed}/{total} gates pass; eligible for release closeout review, with no readiness claim."
    return f"{passed}/{total} gates pass; final status is {final_status}. This is not a readiness claim."
