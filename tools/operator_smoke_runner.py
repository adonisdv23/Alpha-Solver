#!/usr/bin/env python3
"""Operator-facing local/Ollama and OpenAI smoke runner.

This runner is intentionally explicit and evidence-bounded. It never runs both
modes by default, prints sanitized JSON only, and treats every result as smoke
only rather than quality, benchmark, readiness, or superiority evidence.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import os
import sys
import time
from typing import Any, Mapping

from alpha.local_llm.provider_adapter import (
    LocalLLMProviderAdapterError,
    LocalLLMRuntimeConfig,
    run_configured_local_llm_runtime,
)
from alpha.providers import OpenAIProviderClient, ProviderError, ProviderRequest

DEFAULT_PROMPT = "Reply with one concise sentence that does not echo this prompt."
DEFAULT_TIMEOUT_SECONDS = 10.0
DEFAULT_OPENAI_MODEL = "gpt-4.1-mini"
MAX_PROMPT_CHARS = 500
MAX_OUTPUT_PREVIEW_CHARS = 240
OPENAI_MAX_TOKENS = 64

SECRET_MARKERS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "DEEPSEEK_API_KEY",
    "api_key",
    "token",
)


def _clip(value: str | None, limit: int = MAX_OUTPUT_PREVIEW_CHARS) -> str:
    text = "" if value is None else str(value)
    sanitized = " ".join(text.replace("\r", " ").replace("\n", " ").split())
    if len(sanitized) > limit:
        return sanitized[: max(0, limit - 3)] + "..."
    return sanitized


def _usage_dict(usage: Any) -> dict[str, int | None] | None:
    if usage is None:
        return None
    data = asdict(usage) if hasattr(usage, "__dataclass_fields__") else dict(usage)
    if not any(value is not None for value in data.values()):
        return None
    return data


def _base_result(*, mode: str, provider: str, model: str | None) -> dict[str, Any]:
    return {
        "mode": mode,
        "provider": provider,
        "model": model,
        "status": "failed_closed",
        "reason": "not_run",
        "smoke_evidence_only": True,
        "behavior_evidence": False,
        "quality_evidence": False,
        "readiness_evidence": False,
        "latency_ms": None,
        "finish_reason": None,
        "usage": None,
        "estimated_cost_usd": None,
        "model_set": None,
        "output_preview": "",
        "redaction_status": "sanitized_no_secrets_printed",
        "errors": [],
    }


def _safe_error(message: str) -> dict[str, str]:
    return {"message": _clip(message, 180)}


def run_local(prompt: str, env: Mapping[str, str] | None = None) -> dict[str, Any]:
    source = os.environ if env is None else env
    model = source.get("ALPHA_LOCAL_LLM_MODEL")
    result = _base_result(mode="local", provider="ollama", model=model)
    started = time.monotonic()
    # Explicitly use only ALPHA_LOCAL_LLM_* env through LocalLLMRuntimeConfig. Hosted keys
    # are rejected by that config and are never read or forwarded here.
    try:
        runtime_config = LocalLLMRuntimeConfig.from_env(source)
        adapter_result = run_configured_local_llm_runtime(prompt, config=runtime_config)
        result.update(
            {
                "model": runtime_config.model,
                "status": "passed" if adapter_result.status == "non_evidence" else "failed_closed",
                "reason": adapter_result.reason,
                "latency_ms": int((time.monotonic() - started) * 1000),
                "output_preview": _clip(adapter_result.output_text),
            }
        )
    except LocalLLMProviderAdapterError as exc:
        result.update(
            {
                "reason": exc.reason_code,
                "latency_ms": int((time.monotonic() - started) * 1000),
                "errors": [_safe_error(exc.reason_code)],
            }
        )
    except Exception as exc:  # fail closed with class only, not raw details
        result.update(
            {
                "reason": f"runner_error:{exc.__class__.__name__}",
                "latency_ms": int((time.monotonic() - started) * 1000),
                "errors": [_safe_error(exc.__class__.__name__)],
            }
        )
    return result


def run_openai(prompt: str, env: Mapping[str, str] | None = None) -> dict[str, Any]:
    source = os.environ if env is None else env
    model = source.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL).strip() or DEFAULT_OPENAI_MODEL
    model_set = source.get("MODEL_SET", "operator_smoke").strip() or "operator_smoke"
    result = _base_result(mode="openai", provider="openai", model=model)
    result["model_set"] = model_set

    if source.get("MODEL_PROVIDER", "").strip().lower() != "openai":
        result.update({"reason": "model_provider_not_openai", "errors": [_safe_error("MODEL_PROVIDER=openai required")]})
        return result
    if source.get("ALPHA_LIVE_OPENAI", "").strip() != "1":
        result.update({"reason": "live_openai_opt_in_required", "errors": [_safe_error("ALPHA_LIVE_OPENAI=1 required")]})
        return result
    if not source.get("OPENAI_API_KEY", "").strip():
        result.update({"reason": "missing_openai_api_key", "errors": [_safe_error("OPENAI_API_KEY required")]})
        return result

    started = time.monotonic()
    try:
        provider_result = OpenAIProviderClient(api_key=source.get("OPENAI_API_KEY")).execute(
            ProviderRequest(
                prompt=prompt,
                system="Answer briefly for a smoke check. Do not echo the prompt.",
                model=model,
                max_tokens=OPENAI_MAX_TOKENS,
                timeout_ms=int(DEFAULT_TIMEOUT_SECONDS * 1000),
                temperature=0.0,
                metadata={"request_id": "operator-smoke-runner", "model_set": model_set},
            )
        )
        result.update(
            {
                "status": "passed" if provider_result.text.strip() else "failed_closed",
                "reason": "openai_smoke_completed" if provider_result.text.strip() else "empty_provider_output",
                "model": provider_result.model,
                "latency_ms": provider_result.latency_ms,
                "finish_reason": provider_result.finish_reason,
                "usage": _usage_dict(provider_result.usage),
                "estimated_cost_usd": provider_result.cost.estimated_usd,
                "output_preview": _clip(provider_result.text),
            }
        )
    except ProviderError as exc:
        result.update(
            {
                "reason": f"openai_{exc.category}",
                "latency_ms": int((time.monotonic() - started) * 1000),
                "errors": [_safe_error(exc.safe_message)],
            }
        )
    except Exception as exc:
        result.update(
            {
                "reason": f"runner_error:{exc.__class__.__name__}",
                "latency_ms": int((time.monotonic() - started) * 1000),
                "errors": [_safe_error(exc.__class__.__name__)],
            }
        )
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one explicit operator smoke check.")
    parser.add_argument("--mode", choices=("local", "openai"), required=True)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    prompt = args.prompt.strip()
    if not prompt:
        print(json.dumps({**_base_result(mode=args.mode, provider=args.mode, model=None), "reason": "prompt_required"}, sort_keys=True))
        return 2
    if len(prompt) > MAX_PROMPT_CHARS:
        print(json.dumps({**_base_result(mode=args.mode, provider=args.mode, model=None), "reason": "prompt_too_long"}, sort_keys=True))
        return 2

    result = run_local(prompt) if args.mode == "local" else run_openai(prompt)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
