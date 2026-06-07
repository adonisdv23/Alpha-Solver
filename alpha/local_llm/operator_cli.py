"""Operator-only CLI wrapper for local LLM solver orchestration.

This module provides a narrow, default-off command surface for approved local
Level 2 operator use. It delegates to the existing local orchestration runner
and does not expose production solver, dashboard, hosted fallback, or provider
fallback paths.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Mapping, Sequence, TextIO

from .orchestration_runner import run_local_llm_solver_orchestration

_SUCCESS_STATUSES = frozenset({"ok", "clarify", "blocked"})

_DESCRIPTION = """
Stable operator-only wrapper for non-production, local-only Level 2 solver
orchestration. The wrapper is default-off, requires explicit local opt-in, and
is not smoke evidence, not model-quality evidence, not benchmark evidence,
not readiness evidence, and not evidence-model promotion. It does not expose
/v1/solve, dashboard routes, hosted fallback, provider fallback, or hosted
provider credential inputs.
"""

_EPILOG = """
Evidence boundary: this command may produce only normalized non-production local
orchestration results from the existing local runner. It is operator-only and
local-only. Do not use the output as production readiness, MVP readiness,
benchmark evidence, local model quality evidence, hosted provider evidence,
provider orchestration evidence, Alpha superiority evidence, billing evidence,
broad runtime readiness evidence, /v1/solve readiness, dashboard readiness, or
evidence-model promotion.
"""


def build_parser() -> argparse.ArgumentParser:
    """Build the narrow local-only operator CLI parser."""

    parser = argparse.ArgumentParser(
        prog="python -m alpha.local_llm.operator_cli",
        description=_DESCRIPTION,
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--enable-local-llm",
        action="store_true",
        required=True,
        help="Required explicit opt-in for default-off local-only operator execution.",
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument(
        "--prompt",
        metavar="TEXT",
        help="Prompt text for the local-only orchestration runner.",
    )
    prompt_group.add_argument(
        "--prompt-file",
        metavar="PATH",
        help="Read prompt text from a local UTF-8 file.",
    )
    prompt_group.add_argument(
        "--prompt-stdin",
        action="store_true",
        help="Read prompt text from stdin only when this flag is explicitly set.",
    )
    parser.add_argument(
        "--endpoint-url",
        required=True,
        help=(
            "Loopback Ollama-style local endpoint URL; existing runtime "
            "validation enforces local-only endpoints."
        ),
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Exact local model identifier for the local runtime.",
    )
    parser.add_argument(
        "--timeout-seconds",
        required=True,
        help="Finite positive local runtime timeout in seconds.",
    )
    return parser


def _read_prompt(args: argparse.Namespace, *, stdin: TextIO) -> str:
    if args.prompt is not None:
        return args.prompt
    if args.prompt_file is not None:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    if args.prompt_stdin:
        return stdin.read()
    raise RuntimeError("prompt source missing after argparse validation")


def _build_runner_env(
    args: argparse.Namespace, source_env: Mapping[str, str]
) -> dict[str, str]:
    env = dict(source_env)
    env.update(
        {
            "ALPHA_LOCAL_LLM_ENABLED": "true",
            "ALPHA_LOCAL_LLM_ENDPOINT": args.endpoint_url,
            "ALPHA_LOCAL_LLM_MODEL": args.model,
            "ALPHA_LOCAL_LLM_TIMEOUT_SECONDS": args.timeout_seconds,
        }
    )
    return env


def main(
    argv: Sequence[str] | None = None,
    *,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    environ: Mapping[str, str] | None = None,
) -> int:
    """Run the operator CLI and return a process exit code."""

    parser = build_parser()
    args = parser.parse_args(argv)
    input_stream = sys.stdin if stdin is None else stdin
    output_stream = sys.stdout if stdout is None else stdout
    error_stream = sys.stderr if stderr is None else stderr

    try:
        prompt = _read_prompt(args, stdin=input_stream)
    except (OSError, UnicodeError) as exc:
        print(f"prompt read failed: {exc.__class__.__name__}", file=error_stream)
        return 2

    if not isinstance(prompt, str) or not prompt.strip():
        print("prompt is required and must not be empty", file=error_stream)
        return 2

    runner_env = _build_runner_env(args, os.environ if environ is None else environ)
    result = run_local_llm_solver_orchestration(prompt, env=runner_env)
    print(json.dumps(result, indent=2, sort_keys=True), file=output_stream)

    status = result.get("status") if isinstance(result, Mapping) else None
    if status in _SUCCESS_STATUSES:
        return 0
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
