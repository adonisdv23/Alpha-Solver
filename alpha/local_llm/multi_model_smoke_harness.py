"""Local-only multi-model smoke harness for Ollama adapter checks.

This module iterates operator-supplied local Ollama model names through the
existing Alpha Solver local LLM provider adapter. It is smoke evidence only:
results are not behavior evidence, not quality evidence, and not routing or
production readiness evidence. Tests should inject fake transports.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping, Sequence, TextIO

from .provider_adapter import (
    LocalLLMProviderAdapterError,
    LocalLLMRuntimeConfig,
    OllamaJSONTransport,
    run_configured_local_llm_runtime,
    validate_ollama_local_endpoint,
)

_ALLOWED_STATUSES = frozenset({
    "not_installed",
    "connection_failed",
    "timeout",
    "empty_output",
    "prompt_echo",
    "substantive_looking_output",
    "blocked",
})
_FORBIDDEN_PROVIDER_KEY_ENVS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "DEEPSEEK_API_KEY",
)
_REASON_STATUS_MAP = {
    "connection_failure_non_evidence": "connection_failed",
    "timeout_non_evidence": "timeout",
    "empty_model_output_non_evidence": "empty_output",
    "prompt_echo_non_evidence": "prompt_echo",
    "system_echo_non_evidence": "prompt_echo",
    "model_not_installed_non_evidence": "not_installed",
}
_URLLIB_CONNECTION_EXCEPTION_CLASSES = frozenset({"URLError"})

SMOKE_EVIDENCE_LABEL = "local_multi_model_smoke_only_no_behavior_evidence"
DEFAULT_SMOKE_PROMPT = (
    "Local smoke check only. Reply with one short sentence about a safe test object. "
    "Do not echo this prompt."
)


@dataclass(frozen=True)
class ModelSmokeResult:
    """Single model smoke record with no behavior-evidence claims."""

    model: str
    status: str
    reason: str
    behavior_evidence: bool = False
    evidence_label: str = SMOKE_EVIDENCE_LABEL
    output_preview: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in _ALLOWED_STATUSES:
            raise ValueError(f"unsupported smoke status: {self.status}")
        if self.behavior_evidence is not False:
            raise ValueError("multi-model smoke results cannot claim behavior evidence")


def parse_model_names(value: str | Sequence[str]) -> tuple[str, ...]:
    """Parse comma/newline/sequence model input into exact non-empty names."""

    raw_items: list[str] = []
    if isinstance(value, str):
        raw_items.extend(part for chunk in value.splitlines() for part in chunk.split(","))
    else:
        raw_items.extend(str(item) for item in value)
    models = tuple(item.strip() for item in raw_items if item.strip())
    if not models:
        raise LocalLLMProviderAdapterError("missing_model_non_evidence")
    if any(model != model.strip() for model in models):
        raise LocalLLMProviderAdapterError("invalid_model_non_evidence")
    return models


def _present_provider_keys(env: Mapping[str, str]) -> tuple[str, ...]:
    return tuple(key for key in _FORBIDDEN_PROVIDER_KEY_ENVS if str(env.get(key, "")).strip())


def _safe_preview(text: str, limit: int = 160) -> str:
    text = " ".join(text.strip().split())
    return text[:limit]


def _is_default_loopback_urllib_connection_failure(
    *,
    reason: str,
    metadata: Mapping[str, Any],
    default_transport_used: bool,
) -> bool:
    """Detect only default local urllib connection failures.

    This intentionally does not map every ``backend_error_non_evidence`` to
    ``connection_failed``. The mapping applies only when the operator/default
    transport path was used, the adapter metadata still identifies a loopback
    Ollama backend, and the preserved exception/cause class is urllib's
    connection-oriented ``URLError``.
    """

    if reason != "backend_error_non_evidence" or not default_transport_used:
        return False
    if metadata.get("endpoint_is_loopback") is not True:
        return False
    if metadata.get("local_backend") != "ollama_chat":
        return False
    exception_class = str(metadata.get("adapter_exception_class", ""))
    cause_class = str(metadata.get("adapter_exception_cause_class", ""))
    return (
        exception_class in _URLLIB_CONNECTION_EXCEPTION_CLASSES
        or cause_class in _URLLIB_CONNECTION_EXCEPTION_CLASSES
    )


def _status_from_adapter_result(
    *,
    reason: str,
    metadata: Mapping[str, Any],
    default_transport_used: bool,
) -> str:
    if _is_default_loopback_urllib_connection_failure(
        reason=reason,
        metadata=metadata,
        default_transport_used=default_transport_used,
    ):
        return "connection_failed"
    return _REASON_STATUS_MAP.get(reason, "blocked")


def run_multi_model_smoke_harness(
    *,
    models: Sequence[str] | str,
    endpoint_url: str,
    prompt: str = DEFAULT_SMOKE_PROMPT,
    timeout_seconds: float = 10.0,
    env: Mapping[str, str] | None = None,
    transport: OllamaJSONTransport | None = None,
) -> tuple[ModelSmokeResult, ...]:
    """Run local-only adapter smoke checks for each model name.

    The function validates loopback endpoint and hosted-provider-key absence
    before any transport can be invoked. It never falls back to hosted
    providers; callers must pass fake transports in tests.
    """

    source_env = os.environ if env is None else env
    present_keys = _present_provider_keys(source_env)
    parsed_models = parse_model_names(models)
    if not isinstance(prompt, str) or not prompt.strip():
        raise LocalLLMProviderAdapterError("missing_prompt_non_evidence")
    if present_keys:
        return tuple(
            ModelSmokeResult(
                model=model,
                status="blocked",
                reason="provider_keys_forbidden_non_evidence",
                metadata={"blocked_provider_key_names": present_keys, "no_hosted_fallback": True},
            )
            for model in parsed_models
        )
    try:
        endpoint_url = validate_ollama_local_endpoint(endpoint_url)
    except LocalLLMProviderAdapterError as exc:
        return tuple(
            ModelSmokeResult(
                model=model,
                status="blocked",
                reason=exc.reason_code,
                metadata={"endpoint_is_loopback": False, "no_hosted_fallback": True},
            )
            for model in parsed_models
        )

    records: list[ModelSmokeResult] = []
    for model in parsed_models:
        config = LocalLLMRuntimeConfig(
            endpoint_url=endpoint_url,
            model=model,
            timeout_seconds=timeout_seconds,
            enabled=True,
        )
        result = run_configured_local_llm_runtime(
            prompt, config=config, transport=transport, env={}
        )
        result_metadata = dict(result.metadata)
        default_transport_used = transport is None
        if result.status == "non_evidence":
            status = "substantive_looking_output"
        else:
            status = _status_from_adapter_result(
                reason=result.reason,
                metadata=result_metadata,
                default_transport_used=default_transport_used,
            )
        records.append(
            ModelSmokeResult(
                model=model,
                status=status,
                reason=result.reason,
                output_preview=_safe_preview(result.output_text),
                metadata={
                    **result_metadata,
                    "adapter_status": result.status,
                    "default_transport_used": default_transport_used,
                    "no_hosted_fallback": True,
                    "no_provider_keys_accepted": True,
                    "strict_no_behavior_evidence_labeling": True,
                },
            )
        )
    return tuple(records)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m alpha.local_llm.multi_model_smoke_harness",
        description="Local-only multi-model Ollama adapter smoke harness; no behavior evidence.",
    )
    parser.add_argument("--local-only", action="store_true", required=True)
    parser.add_argument("--models", required=True, help="Comma-separated local Ollama model names.")
    parser.add_argument("--endpoint-url", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=10.0)
    parser.add_argument("--prompt", default=DEFAULT_SMOKE_PROMPT)
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    environ: Mapping[str, str] | None = None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    out = sys.stdout if stdout is None else stdout
    err = sys.stderr if stderr is None else stderr
    try:
        results = run_multi_model_smoke_harness(
            models=args.models,
            endpoint_url=args.endpoint_url,
            prompt=args.prompt,
            timeout_seconds=args.timeout_seconds,
            env=os.environ if environ is None else environ,
        )
    except LocalLLMProviderAdapterError as exc:
        print(f"blocked: {exc.reason_code}", file=err)
        return 2
    print(json.dumps([asdict(record) for record in results], indent=2, sort_keys=True), file=out)
    return 0 if all(record.status in {"substantive_looking_output"} for record in results) else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
