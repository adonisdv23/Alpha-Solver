"""Deterministic local command classification guardrails.

The classifier never executes commands. It only inspects command strings or argv
lists and returns stable findings/reason codes for local preflight callers.
"""
from __future__ import annotations

import re
import shlex
from dataclasses import asdict, dataclass
from typing import Any, Sequence

from alpha.self_operator.artifact_schema import ArtifactFinding


@dataclass(frozen=True)
class CommandClassification:
    command: tuple[str, ...]
    category: str
    allowed: bool
    reason_code: str
    findings: tuple[ArtifactFinding, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["command"] = list(self.command)
        payload["findings"] = [finding.to_dict() for finding in self.findings]
        return payload


@dataclass(frozen=True)
class CommandRule:
    category: str
    reason_code: str
    finding_id: str
    patterns: tuple[str, ...]


FORBIDDEN_RULES: tuple[CommandRule, ...] = (
    CommandRule("forbidden provider call", "provider_call", "SELF_OPERATOR_PROVIDER_CALL_BLOCKED", (r"\b(openai|anthropic|gemini|deepseek)\b", r"\bprovider(_|-)?call\b", r"\bhosted(_|-)?model\b")),
    CommandRule("forbidden network/external API command", "network_external_api", "SELF_OPERATOR_EXTERNAL_API_BLOCKED", (r"\b(curl|wget|httpie|ssh|scp|rsync|nc|telnet)\b", r"\b(pip|uv|npm|pnpm|yarn)\s+(install|add|update|publish)\b", r"\bgit\s+(pull|push|fetch|clone|submodule)\b")),
    CommandRule("forbidden browser automation", "browser_automation", "SELF_OPERATOR_BROWSER_AUTOMATION_BLOCKED", (r"\b(playwright|selenium|chromium|chrome|browser)\b",)),
    CommandRule("forbidden deployment", "deployment", "SELF_OPERATOR_DEPLOYMENT_BLOCKED", (r"\b(kubectl|terraform|helm|vercel|netlify|flyctl|aws|gcloud|az)\b", r"\bdeploy\b")),
    CommandRule("forbidden billing", "billing", "SELF_OPERATOR_BILLING_BLOCKED", (r"\b(billing|invoice|charge_customer|stripe)\b",)),
    CommandRule("forbidden credential or secret access", "credential_secret_access", "SELF_OPERATOR_CREDENTIAL_ACCESS_BLOCKED", (r"\b(printenv|env|dotenv)\b", r"\bos\.environ\b", r"\b(api[_-]?key|token|secret|password|credential)s?\b", r"\b(cat|sed|awk|jq)\b.*\.(env|netrc|pypirc)\b")),
    CommandRule("forbidden Google Sheets action", "google_sheets", "SELF_OPERATOR_GOOGLE_SHEETS_BLOCKED", (r"(gspread|google[-_ ]?sheets|google_sheets|sheets\.google|gsheets)",)),
    CommandRule("forbidden source-artifact mutation", "source_artifact_mutation", "SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED", (r"\b(rm|mv|cp|touch|chmod|chown|truncate)\b", r"\b(sed|perl)\b.*\s-i\b", r">>|\s>\s", r"\bpython\b.*\b(write_text|open\(.+['\"]w)")),
    CommandRule("forbidden evidence promotion", "evidence_promotion", "SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED", (r"\b(promote[_-]?evidence|evidence[_-]?promotion|mark[_-]?accepted|acceptance[_-]?passed|mvp[_-]?ready|production[_-]?ready)\b",)),
)

ALLOWED_EXACT_PREFIXES: tuple[tuple[str, ...], ...] = (
    ("git", "status"),
    ("git", "diff"),
    ("git", "branch"),
    ("git", "log"),
    ("rg",),
    ("find",),
    ("sed", "-n"),
    ("python", "-m", "pytest"),
    ("python3", "-m", "pytest"),
    ("python", "scripts/check_local_llm_packet_consistency.py"),
    ("make", "check-local-llm-orchestration-guardrails"),
)

_SHELL_META_RE = re.compile(r"[;&|`]")
_FLAGS = re.IGNORECASE


def classify_command(command: str | Sequence[str]) -> CommandClassification:
    """Classify a proposed command without executing it."""

    argv = _parse_command(command)
    normalized = " ".join(argv)
    if not argv:
        return _unclear(argv, "empty_command", "empty command requires operator review")
    if isinstance(command, str) and _SHELL_META_RE.search(command):
        return _unclear(argv, "shell_meta_requires_review", "shell metacharacters require operator review")
    for rule in FORBIDDEN_RULES:
        if any(re.search(pattern, normalized, flags=_FLAGS) for pattern in rule.patterns):
            finding = ArtifactFinding(
                id=rule.finding_id,
                reason_code=rule.reason_code,
                message=rule.category,
                surface="command_classification",
            )
            return CommandClassification(
                command=argv,
                category=rule.category,
                allowed=False,
                reason_code=rule.reason_code,
                findings=(finding,),
            )
    if _is_allowed_local(argv):
        return CommandClassification(
            command=argv,
            category="allowed local read/check command",
            allowed=True,
            reason_code="allowed_local_read_check",
        )
    return _unclear(argv, "unclear_requires_operator_review", "unclear command requiring operator review")


def classify_commands(commands: Sequence[str | Sequence[str]]) -> tuple[CommandClassification, ...]:
    return tuple(classify_command(command) for command in commands)


def _parse_command(command: str | Sequence[str]) -> tuple[str, ...]:
    if isinstance(command, str):
        try:
            return tuple(shlex.split(command))
        except ValueError:
            return (command,)
    return tuple(str(part) for part in command)


def _is_allowed_local(argv: tuple[str, ...]) -> bool:
    for prefix in ALLOWED_EXACT_PREFIXES:
        if argv[: len(prefix)] == prefix:
            return True
    return False


def _unclear(argv: tuple[str, ...], reason_code: str, message: str) -> CommandClassification:
    finding = ArtifactFinding(
        id="SELF_OPERATOR_COMMAND_REQUIRES_OPERATOR_REVIEW",
        reason_code=reason_code,
        message=message,
        severity="warning",
        surface="command_classification",
        stop_state="review_required",
    )
    return CommandClassification(
        command=argv,
        category="unclear command requiring operator review",
        allowed=False,
        reason_code=reason_code,
        findings=(finding,),
    )
