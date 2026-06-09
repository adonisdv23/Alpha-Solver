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

FIND_MUTATING_FLAGS = frozenset({"-delete", "-exec", "-execdir", "-ok", "-okdir"})
GIT_BRANCH_MUTATING_LONG_FLAGS = frozenset({"--delete", "--move", "--copy"})
GIT_BRANCH_MUTATING_SHORT_FLAGS = frozenset("dDmMcC")
COMMON_WRITE_OPTIONS = frozenset({"--output", "--output-file", "--outfile", "--out-file"})
RG_EXECUTION_OPTIONS = frozenset({"--pre"})

_SHELL_META_RE = re.compile(r"[;&|`]")
_FLAGS = re.IGNORECASE


def classify_command(command: str | Sequence[str]) -> CommandClassification:
    """Classify a proposed command without executing it."""

    argv = _parse_command(command)
    normalized = " ".join(argv)
    if not argv:
        return _unclear(argv, "empty_command", "empty command requires operator review")
    for rule in FORBIDDEN_RULES:
        if any(re.search(pattern, normalized, flags=_FLAGS) for pattern in rule.patterns):
            return _forbidden(rule, argv)
    allowed_result = _classify_allowed_local(argv)
    if allowed_result is not None:
        return allowed_result
    if isinstance(command, str) and _SHELL_META_RE.search(command):
        return _unclear(argv, "shell_meta_requires_review", "shell metacharacters require operator review")
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


def _classify_allowed_local(argv: tuple[str, ...]) -> CommandClassification | None:
    for prefix in ALLOWED_EXACT_PREFIXES:
        if argv[: len(prefix)] != prefix:
            continue
        if _has_common_write_option(argv):
            return _source_mutation_block(argv, "allowed command includes output/write option")
        if prefix == ("find",) and _find_has_mutating_action(argv):
            return _source_mutation_block(argv, "find command includes mutating action")
        if prefix == ("git", "branch") and _git_branch_has_mutating_option(argv):
            return _source_mutation_block(argv, "git branch command includes mutating option")
        if prefix == ("git", "diff") and _git_diff_has_output_option(argv):
            return _source_mutation_block(argv, "git diff command writes output to a file")
        if prefix == ("rg",) and _rg_has_execution_option(argv):
            return _source_mutation_block(argv, "rg command includes execution option")
        return CommandClassification(
            command=argv,
            category="allowed local read/check command",
            allowed=True,
            reason_code="allowed_local_read_check",
        )
    return None


def _has_common_write_option(argv: tuple[str, ...]) -> bool:
    return any(arg in COMMON_WRITE_OPTIONS or _option_starts_with_equals(arg, COMMON_WRITE_OPTIONS) for arg in argv)


def _find_has_mutating_action(argv: tuple[str, ...]) -> bool:
    return any(arg in FIND_MUTATING_FLAGS for arg in argv[1:])


def _git_branch_has_mutating_option(argv: tuple[str, ...]) -> bool:
    for arg in argv[2:]:
        if arg in GIT_BRANCH_MUTATING_LONG_FLAGS or _option_starts_with_equals(arg, GIT_BRANCH_MUTATING_LONG_FLAGS):
            return True
        if arg.startswith("-") and not arg.startswith("--") and any(flag in arg[1:] for flag in GIT_BRANCH_MUTATING_SHORT_FLAGS):
            return True
    return False


def _git_diff_has_output_option(argv: tuple[str, ...]) -> bool:
    return any(arg == "--output" or arg.startswith("--output=") for arg in argv[2:])


def _rg_has_execution_option(argv: tuple[str, ...]) -> bool:
    return any(arg in RG_EXECUTION_OPTIONS or _option_starts_with_equals(arg, RG_EXECUTION_OPTIONS) for arg in argv[1:])


def _option_starts_with_equals(arg: str, options: frozenset[str]) -> bool:
    return any(arg.startswith(f"{option}=") for option in options)


def _forbidden(rule: CommandRule, argv: tuple[str, ...]) -> CommandClassification:
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


def _source_mutation_block(argv: tuple[str, ...], message: str) -> CommandClassification:
    finding = ArtifactFinding(
        id="SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED",
        reason_code="source_artifact_mutation",
        message=message,
        surface="command_classification",
    )
    return CommandClassification(
        command=argv,
        category="forbidden source-artifact mutation",
        allowed=False,
        reason_code="source_artifact_mutation",
        findings=(finding,),
    )


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
