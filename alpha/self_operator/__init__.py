"""Local-only Self Operator artifact and preflight foundations.

This package contains deterministic helpers only. The modules do not execute
proposed commands, call providers, access credentials, automate browsers,
deploy, bill, update Google Sheets, expose APIs, mutate source artifacts, or
promote evidence.
"""

from alpha.self_operator.approval import (
    APPROVAL_SCHEMA_VERSION,
    OPERATOR_CONFIRMATION_HARD_STOP,
    ApprovalRecord,
    approval_from_mapping,
)
from alpha.self_operator.artifact_schema import (
    CURRENT_SCHEMA_VERSION,
    ArtifactFinding,
    OperatorConfirmation,
    SelfOperatorArtifact,
    ValidationResult,
)
from alpha.self_operator.artifact_store import read_artifact_json, write_artifact_json
from alpha.self_operator.command_classification import CommandClassification, classify_command
from alpha.self_operator.dry_run import (
    BLOCKER_FALLBACK_LANE,
    DRY_RUN_LANE_ID,
    DRY_RUN_RESULT_SCHEMA_VERSION,
    SELECTED_NEXT_LANE,
    DryRunResult,
    run_local_dry_run_wrapper,
    write_dry_run_result_json,
)
from alpha.self_operator.execution_gate import (
    ALLOWED_GATE_STATUS,
    GATE_RESULT_SCHEMA_VERSION,
    ExecutionGateResult,
    evaluate_execution_gate,
    write_execution_gate_result_json,
)
from alpha.self_operator.preflight import ProposedTask, PreflightResult, run_local_preflight
from alpha.self_operator.stop_state import (
    STOP_STATE_SCHEMA_VERSION,
    StopStateRecord,
    write_stop_state_json,
)

__all__ = [
    "ALLOWED_GATE_STATUS",
    "APPROVAL_SCHEMA_VERSION",
    "CURRENT_SCHEMA_VERSION",
    "ArtifactFinding",
    "ApprovalRecord",
    "BLOCKER_FALLBACK_LANE",
    "CommandClassification",
    "DRY_RUN_LANE_ID",
    "DRY_RUN_RESULT_SCHEMA_VERSION",
    "DryRunResult",
    "ExecutionGateResult",
    "GATE_RESULT_SCHEMA_VERSION",
    "OPERATOR_CONFIRMATION_HARD_STOP",
    "OperatorConfirmation",
    "PreflightResult",
    "ProposedTask",
    "SELECTED_NEXT_LANE",
    "STOP_STATE_SCHEMA_VERSION",
    "SelfOperatorArtifact",
    "StopStateRecord",
    "ValidationResult",
    "approval_from_mapping",
    "classify_command",
    "evaluate_execution_gate",
    "read_artifact_json",
    "run_local_dry_run_wrapper",
    "run_local_preflight",
    "write_artifact_json",
    "write_dry_run_result_json",
    "write_execution_gate_result_json",
    "write_stop_state_json",
]
