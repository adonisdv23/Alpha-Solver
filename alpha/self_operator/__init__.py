"""Local-only Self Operator artifact and preflight foundations.

This package contains deterministic helpers only. The modules do not execute
proposed commands, call providers, access credentials, automate browsers,
deploy, bill, update Google Sheets, expose APIs, mutate source artifacts, or
promote evidence.
"""

from alpha.self_operator.artifact_schema import (
    CURRENT_SCHEMA_VERSION,
    ArtifactFinding,
    OperatorConfirmation,
    SelfOperatorArtifact,
    ValidationResult,
)
from alpha.self_operator.artifact_store import read_artifact_json, write_artifact_json
from alpha.self_operator.command_classification import CommandClassification, classify_command
from alpha.self_operator.preflight import ProposedTask, PreflightResult, run_local_preflight

__all__ = [
    "CURRENT_SCHEMA_VERSION",
    "ArtifactFinding",
    "CommandClassification",
    "OperatorConfirmation",
    "PreflightResult",
    "ProposedTask",
    "SelfOperatorArtifact",
    "ValidationResult",
    "classify_command",
    "read_artifact_json",
    "run_local_preflight",
    "write_artifact_json",
]
