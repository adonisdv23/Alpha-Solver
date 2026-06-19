#!/usr/bin/env python3
"""Local-only Operator smoke test console.

This console is intentionally local-only and smoke-only. It reuses
``tools.operator_smoke_runner`` for provider execution so the existing fail-closed
checks remain the execution path. The page ships plain HTML, inline CSS, and
inline vanilla JavaScript only. It loads no external scripts, styles, fonts,
images, telemetry, or remote assets, and it persists no results.
"""

from __future__ import annotations

from copy import deepcopy
import html
import json
import os
from typing import Any, Mapping
from urllib.parse import parse_qs

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

from alpha import model_router, tool_router
from tools import operator_smoke_runner as smoke_runner

APP_TITLE = "Alpha Solver local smoke test console"
DEFAULT_LOCAL_MODEL = "qwen2.5:3b"
DEFAULT_OPENAI_MODEL = smoke_runner.DEFAULT_OPENAI_MODEL
DEFAULT_PROMPT = smoke_runner.DEFAULT_PROMPT
MAX_PROMPT_CHARS = smoke_runner.MAX_PROMPT_CHARS
CUSTOM_MODEL_OPTION = "custom"
LOCAL_MODEL_OPTIONS = ("qwen2.5:3b", "gemma3:4b", "llama3.2:1b", "llama3.2:latest", CUSTOM_MODEL_OPTION)
OPENAI_MODEL_OPTIONS = ("gpt-4.1-mini", "gpt-4.1", "gpt-4o-mini", CUSTOM_MODEL_OPTION)
MODEL_OPTIONS: dict[str, tuple[str, ...]] = {"local": LOCAL_MODEL_OPTIONS, "openai": OPENAI_MODEL_OPTIONS}
PROMPT_LIMIT_MESSAGE = (
    f"Prompt is over the {MAX_PROMPT_CHARS}-character smoke-runner limit. Shorten the prompt and retry."
)
LOCAL_ONLY_NOTICE = (
    "Passing smoke does not prove quality, readiness, benchmark success, "
    "provider superiority, local-model superiority, production readiness, "
    "public readiness, security/privacy completion, or Alpha superiority."
)
RUN_COMMAND = "uvicorn tools.operator_test_console:app --host 127.0.0.1 --port 8765"
SECRET_KEYS = ("api_key", "authorization", "bearer", "access_token", "refresh_token", "secret", "password")
SAFE_USAGE_TOKEN_KEYS = ("input_tokens", "output_tokens", "total_tokens", "cached_tokens")

# Bounded, operator-facing explanations for safe failed-closed reasons. These
# explain why a check stopped safely; they are not quality or readiness claims.
REASON_EXPLANATIONS: dict[str, str] = {
    "prompt_too_long": PROMPT_LIMIT_MESSAGE,
    "unsupported_mode": "Mode is not supported. Choose local or openai and retry.",
    "model_provider_not_openai": "OpenAI mode needs MODEL_PROVIDER=openai in the local environment.",
    "live_openai_opt_in_required": "OpenAI mode needs ALPHA_LIVE_OPENAI=1 in the local environment.",
    "missing_openai_api_key": "OpenAI mode needs OPENAI_API_KEY set in the local terminal environment.",
    "endpoint_not_local_non_evidence": "The local LLM endpoint must be a loopback (127.0.0.1) address.",
    "empty_provider_output": "The provider returned no usable text, so the smoke check failed closed.",
    "prompt_required": "Enter a prompt and retry.",
    "not_run": "No smoke check has run yet.",
}

# Setup checklist content. These are local-only, evidence-bounded steps and never
# ask the operator to paste a secret value into the UI.
LOCAL_SETUP_STEPS = (
    "Confirm Ollama is running at 127.0.0.1:11434.",
    "Set ALPHA_LOCAL_LLM_ENABLED=1.",
    "Set ALPHA_LOCAL_LLM_ENDPOINT=http://127.0.0.1:11434/api/chat.",
    "Set ALPHA_LOCAL_LLM_MODEL=qwen2.5:3b.",
)
OPENAI_SETUP_STEPS = (
    "Set MODEL_PROVIDER=openai.",
    "Set ALPHA_LIVE_OPENAI=1.",
    "Set OPENAI_MODEL=gpt-4.1-mini.",
    "Set OPENAI_API_KEY in the local terminal environment.",
    "Never paste API keys into the UI.",
)
ROUTE_PREVIEW_BOUNDARY = (
    "Route preview is metadata-only. Tool recommendation is not tool execution. "
    "Model recommendation is not model validation. Provider or local model execution is not authorized by preview. "
    "Smoke results remain smoke-only evidence, and passing smoke does not prove model quality, provider quality, "
    "local-model quality, readiness, benchmark success, production/public readiness, security/privacy completion, "
    "or Alpha superiority."
)


def _normalize_host(value: str | None) -> str:
    if not value:
        return ""
    normalized = value.strip().lower()
    if normalized.startswith("["):
        end = normalized.find("]")
        return normalized[1:end] if end != -1 else normalized.strip("[]")
    if normalized.count(":") == 1:
        normalized = normalized.rsplit(":", 1)[0]
    return normalized.strip("[]")


def _is_loopback_host(host: str | None) -> bool:
    return _normalize_host(host) in {"127.0.0.1", "localhost", "::1"}


def _is_loopback_request(host_header: str | None, peer_host: str | None) -> bool:
    host_is_safe = True if not host_header else _is_loopback_host(host_header)
    peer_is_safe = _is_loopback_host(peer_host)
    return host_is_safe and peer_is_safe


def assert_loopback_request(request: Request) -> None:
    """Reject requests unless both Host and peer address are loopback."""

    host = request.headers.get("host")
    peer_host = request.client.host if request.client and request.client.host else None
    if not _is_loopback_request(host, peer_host):
        raise HTTPException(status_code=403, detail="operator_test_console_loopback_only")


def _redact_scalar(value: Any) -> Any:
    if isinstance(value, str):
        redacted = value
        lowered = redacted.lower()
        for marker in ("s" + "k-", "bear" + "er ", "bearer-prefix "):
            if marker in lowered:
                return "[REDACTED]"
        return redacted
    return value


def sanitize_result(result: Mapping[str, Any]) -> dict[str, Any]:
    """Return a JSON-safe result with secret-like fields redacted or removed."""

    def is_safe_numeric_usage_counter(key: str, value: Any) -> bool:
        lowered = key.lower()
        return (
            isinstance(value, (int, float))
            and (lowered in SAFE_USAGE_TOKEN_KEYS or lowered.endswith("_tokens") or lowered.endswith("_token_count"))
        )

    def walk(value: Any, key: str = "", parent_key: str = "") -> Any:
        lowered = key.lower()
        parent_lowered = parent_key.lower()
        if any(marker in lowered for marker in SECRET_KEYS):
            return "[REDACTED]"
        if parent_lowered == "usage" and is_safe_numeric_usage_counter(lowered, value):
            return value
        if isinstance(value, Mapping):
            return {str(k): walk(v, str(k), key) for k, v in value.items()}
        if isinstance(value, list):
            return [walk(item, key, parent_key) for item in value]
        return _redact_scalar(value)

    sanitized = walk(deepcopy(dict(result)))
    sanitized["smoke_evidence_only"] = True
    sanitized["behavior_evidence"] = False
    sanitized["quality_evidence"] = False
    sanitized["readiness_evidence"] = False
    sanitized["redaction_status"] = "sanitized_no_secrets_rendered_or_saved"
    return sanitized


def _env_for_mode(mode: str, model: str, base_env: Mapping[str, str] | None = None) -> dict[str, str]:
    source = dict(os.environ if base_env is None else base_env)
    if mode == "local":
        source["ALPHA_LOCAL_LLM_MODEL"] = model.strip() or DEFAULT_LOCAL_MODEL
    elif mode == "openai":
        source["OPENAI_MODEL"] = model.strip() or DEFAULT_OPENAI_MODEL
    else:
        raise ValueError("unsupported_mode")
    return source


def run_console_smoke(mode: str, model: str, prompt: str, env: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Run one smoke check through the existing smoke runner path."""

    cleaned_prompt = prompt.strip() or DEFAULT_PROMPT
    if mode not in {"local", "openai"}:
        result = smoke_runner._base_result(mode=mode, provider=mode, model=model)  # noqa: SLF001
        result["reason"] = "unsupported_mode"
        return sanitize_result(result)
    if len(cleaned_prompt) > smoke_runner.MAX_PROMPT_CHARS:
        result = smoke_runner._base_result(mode=mode, provider=mode, model=model)  # noqa: SLF001
        result["reason"] = "prompt_too_long"
        return sanitize_result(result)

    execution_env = _env_for_mode(mode, model, env)
    if mode == "local":
        return sanitize_result(smoke_runner.run_local(cleaned_prompt, env=execution_env))
    return sanitize_result(smoke_runner.run_openai(cleaned_prompt, env=execution_env))


def _model_default(mode: str) -> str:
    return DEFAULT_OPENAI_MODEL if mode == "openai" else DEFAULT_LOCAL_MODEL


def _resolve_effective_model(mode: str, model_option: str, custom_model: str) -> str:
    """Resolve the model id used for execution from a dropdown option plus custom text."""

    option = (model_option or "").strip()
    default = _model_default(mode)
    if option == CUSTOM_MODEL_OPTION:
        return (custom_model or "").strip() or default
    if not option:
        return default
    if mode == "openai" and option == DEFAULT_LOCAL_MODEL:
        return DEFAULT_OPENAI_MODEL
    return option


def _form_state(
    mode: str = "local",
    model: str = "",
    prompt: str = DEFAULT_PROMPT,
    model_option: str | None = None,
    custom_model: str = "",
) -> dict[str, str]:
    """Resolve the form fields to re-render after a submit.

    Accepts either an explicit ``model_option`` plus ``custom_model`` (used by the
    form handler) or a resolved effective ``model`` (used by render callers and
    tests). The returned dict preserves the selected mode, the selected model
    option, the custom model value, the effective model, and the prompt.
    """

    selected_mode = mode if mode in {"local", "openai"} else "local"
    options = MODEL_OPTIONS[selected_mode]
    known = [option for option in options if option != CUSTOM_MODEL_OPTION]

    if model_option is not None and str(model_option).strip() != "":
        chosen_option = str(model_option).strip()
        if chosen_option not in options:
            chosen_custom = chosen_option
            chosen_option = CUSTOM_MODEL_OPTION
        else:
            chosen_custom = (custom_model or "").strip()
    else:
        effective = (model or "").strip()
        if not effective:
            chosen_option = _model_default(selected_mode)
            chosen_custom = ""
        elif effective in known:
            chosen_option = effective
            chosen_custom = ""
        else:
            chosen_option = CUSTOM_MODEL_OPTION
            chosen_custom = effective

    if chosen_option == CUSTOM_MODEL_OPTION:
        effective_model = (chosen_custom or "").strip() or _model_default(selected_mode)
    else:
        effective_model = chosen_option

    selected_prompt = prompt if prompt else DEFAULT_PROMPT
    return {
        "mode": selected_mode,
        "model_option": chosen_option,
        "custom_model": chosen_custom,
        "model": effective_model,
        "prompt": selected_prompt,
    }


TASK_SIGNAL_KEYWORDS: dict[str, tuple[str, ...]] = {
    "privacy": ("private", "secret", "credential", "pii", "confidential"),
    "current_facts": ("latest", "today", "current", "news", "recent"),
    "tool": ("tool", "run", "execute", "call", "browse", "github"),
    "repo": ("repo", "repository", "codebase", "pytest", "file"),
    "document": ("document", "doc", "pdf", "markdown", "summarize"),
    "spreadsheet": ("sheet", "spreadsheet", "csv", "excel"),
    "computation": ("calculate", "compute", "math", "sum", "average"),
}


def _task_signals(task: str, tool_preview: Mapping[str, Any]) -> dict[str, Any]:
    lowered = task.lower()
    indicators = {name: any(keyword in lowered for keyword in keywords) for name, keywords in TASK_SIGNAL_KEYWORDS.items()}
    family = tool_preview.get("recommended_tool_family") or "not_available"
    return {
        "task_family": family,
        "privacy_indicator": indicators["privacy"],
        "current_facts_indicator": indicators["current_facts"],
        "tool_indicator": indicators["tool"],
        "repo_indicator": indicators["repo"],
        "document_indicator": indicators["document"],
        "spreadsheet_indicator": indicators["spreadsheet"],
        "computation_indicator": indicators["computation"],
        "source": "existing_metadata_router_plus_keyword_signals",
    }


def build_route_preview(task: str, mode: str, model: str) -> dict[str, Any]:
    """Build a deterministic metadata-only route preview from existing routers."""

    cleaned_task = (task or "").strip()
    selected_mode = mode if mode in {"local", "openai"} else "local"
    requested_model = (model or "").strip() or _model_default(selected_mode)
    model_preview = model_router.preview_route(
        model_router.RoutingPreviewRequest(
            requested_mode=selected_mode,
            requested_model=requested_model,
            allow_hosted_providers=True,
            allow_local=True,
            prompt_length=len(cleaned_task),
            local_only=False,
        )
    ).as_dict()
    tool_preview = tool_router.recommend_tool(
        tool_router.ToolRecommendationRequest(task_text=cleaned_task, untrusted_context="operator_console_task")
    ).as_dict()
    interpretation = _task_signals(cleaned_task, tool_preview)
    preview = {
        "status": "preview_only",
        "task": cleaned_task,
        "task_family": interpretation["task_family"],
        "task_interpretation": interpretation,
        "model_route": model_preview,
        "tool_route": tool_preview,
        "fallback_path": model_preview.get("fallbacks", []),
        "evidence_boundary": ROUTE_PREVIEW_BOUNDARY,
        "provider_or_local_execution_authorized": False,
        "tool_execution_authorized": False,
        "preview_only": True,
    }
    preview["best_path_summary"] = build_best_path_summary(preview)
    return preview


def build_best_path_summary(route_preview: Mapping[str, Any] | None) -> dict[str, Any]:
    """Build bounded metadata-only best-path recommendation from route preview."""

    if not route_preview:
        return {
            "status": "recommend_only",
            "recommended_route_type": "clarification_needed",
            "primary_option": "none",
            "why_this_route": ["No route preview has been requested yet."],
            "safe_next_action": "preview_only",
            "fallback_summary": [],
            "risk_flags": ["unsupported/no eligible route"],
            "evidence_boundary": "Catalog inclusion is not quality evidence; recommendation is not execution authorization.",
            "manual_override_summary": "Mode/model controls are available; route/tool overrides are unavailable in this lane.",
            "metadata_only": True,
            "provider_or_local_execution_authorized": False,
            "tool_execution_authorized": False,
        }

    model_route = route_preview.get("model_route", {}) if isinstance(route_preview.get("model_route"), Mapping) else {}
    tool_route = route_preview.get("tool_route", {}) if isinstance(route_preview.get("tool_route"), Mapping) else {}
    interpretation = route_preview.get("task_interpretation", {}) if isinstance(route_preview.get("task_interpretation"), Mapping) else {}
    model_ok = model_route.get("status") == "preview_only" and bool(model_route.get("recommended_model"))
    tool_ok = tool_route.get("status") == "preview_only" and bool(tool_route.get("recommended_tool_id"))
    tool_no_match = (
        tool_route.get("status") == "failed_closed"
        and not tool_route.get("recommended_tool_id")
        and "no_matching_tool_family" in set(map(str, tool_route.get("reasons", [])))
    )
    failed = (
        route_preview.get("status") == "failed_closed"
        or model_route.get("status") == "failed_closed"
        or (tool_route.get("status") == "failed_closed" and not tool_no_match)
    )

    risk_flags: list[str] = []
    if interpretation.get("privacy_indicator") or "privacy" in " ".join(map(str, tool_route.get("warnings", []))):
        risk_flags.append("privacy-sensitive")
    if interpretation.get("current_facts_indicator"):
        risk_flags.append("current facts")
    if interpretation.get("repo_indicator") or interpretation.get("tool_indicator"):
        risk_flags.append("repo/tool action")
    if interpretation.get("document_indicator") or interpretation.get("spreadsheet_indicator"):
        risk_flags.append("document/spreadsheet")
    if len(str(route_preview.get("task", ""))) > 350:
        risk_flags.append("long context")
    if failed or not (model_ok or tool_ok or (model_ok and tool_no_match)):
        risk_flags.append("unsupported/no eligible route")
    if not risk_flags:
        risk_flags.append("none detected")

    if failed or not (model_ok or tool_ok):
        route_type = "no eligible route"
        primary = "none"
        status = "failed_closed"
        safe_next = "do_not_execute"
    elif tool_ok and (
        interpretation.get("current_facts_indicator")
        or tool_route.get("recommended_tool_id") == "web_current_research"
    ):
        route_type = "hybrid route" if model_ok else "tool route"
        primary = str(tool_route.get("recommended_tool_id"))
        status = "recommend_only"
        safe_next = "preview_only"
    elif interpretation.get("computation_indicator") and model_ok and not interpretation.get("tool_indicator"):
        route_type = "model route"
        primary = str(model_route.get("recommended_model"))
        status = "recommend_only"
        safe_next = "smoke_run_allowed_through_existing_smoke_path" if model_route.get("selected_smoke_eligible") else "preview_only"
    elif tool_ok and (interpretation.get("tool_indicator") or interpretation.get("repo_indicator") or interpretation.get("document_indicator") or interpretation.get("spreadsheet_indicator")):
        route_type = "hybrid route" if model_ok else "tool route"
        primary = str(tool_route.get("recommended_tool_id"))
        status = "recommend_only"
        safe_next = "preview_only"
    elif model_ok:
        route_type = "model route"
        primary = str(model_route.get("recommended_model"))
        status = "recommend_only"
        safe_next = "smoke_run_allowed_through_existing_smoke_path" if model_route.get("selected_smoke_eligible") else "preview_only"
    else:
        route_type = "clarification_needed"
        primary = "none"
        status = "recommend_only"
        safe_next = "ask_operator_to_clarify"

    reasons = list(model_route.get("reasons", []))[:3] + list(tool_route.get("reasons", []))[:3]
    warnings = list(model_route.get("warnings", []))[:2] + list(tool_route.get("warnings", []))[:2]
    why = reasons + warnings
    if interpretation.get("privacy_indicator"):
        why.insert(0, "local/privacy caveat: privacy-sensitive task signal detected; preview does not prove privacy completion.")
    if not why:
        why = ["Metadata preview has insufficient route reasons; keep recommendation preview-only."]
    fallbacks = []
    for item in route_preview.get("fallback_path", [])[:2]:
        if isinstance(item, Mapping):
            fallbacks.append(f"model:{item.get('model')} ({item.get('mode')})")
    for item in tool_route.get("candidates", [])[:2]:
        fallbacks.append(f"tool:{item}")

    return {
        "status": status,
        "recommended_route_type": route_type,
        "primary_option": primary,
        "why_this_route": why[:8],
        "safe_next_action": safe_next,
        "fallback_summary": fallbacks[:4],
        "risk_flags": risk_flags,
        "evidence_boundary": "Catalog inclusion is not quality evidence; recommendation is not execution authorization.",
        "manual_override_summary": "Mode/model controls are reflected in preview; route/tool overrides are unavailable in this lane.",
        "metadata_only": True,
        "provider_or_local_execution_authorized": False,
        "tool_execution_authorized": False,
    }

def _route_list(values: Any) -> str:
    if not values:
        return '<span class="muted-inline">none</span>'
    if isinstance(values, Mapping):
        values = [f"{key}={value}" for key, value in values.items()]
    rendered: list[str] = []
    for value in values:
        if isinstance(value, Mapping):
            parts = [f"{key}: {item}" for key, item in value.items()]
            rendered.append("; ".join(parts))
        else:
            rendered.append(str(value))
    items = "".join(f"<li>{html.escape(item)}</li>" for item in rendered)
    return f'<ul class="mini">{items}</ul>'


def _grouped_route_reasons(model_route: Mapping[str, Any], tool_route: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "model route reasons": list(model_route.get("reasons", [])),
        "model route warnings": list(model_route.get("warnings", [])),
        "tool route reasons": list(tool_route.get("reasons", [])),
        "tool route caveats": list(tool_route.get("warnings", [])),
    }


def _route_section(title: str, body: str, section_id: str | None = None) -> str:
    section_attr = f' id="{html.escape(section_id)}"' if section_id else ""
    return f'<section class="route-card"{section_attr}><h3>{html.escape(title)}</h3>{body}</section>'


def _route_flow_html() -> str:
    steps = (
        ("1", "Read task", "Use the task text only as untrusted local input."),
        ("2", "Pick route", "Preview model and tool route metadata without calls."),
        ("3", "Explain route", "Show reasons, warnings, caveats, and fallbacks."),
        ("4", "Run or recommend safe path", "Keep preview separate from bounded local/OpenAI smoke execution."),
        ("5", "Capture evidence", "Copy route evidence JSON with no-call and non-quality boundaries."),
    )
    items = "".join(
        f'<li><span class="step-num">{num}</span><strong>{html.escape(label)}</strong><p>{html.escape(copy)}</p></li>'
        for num, label, copy in steps
    )
    return f'<ol class="route-flow">{items}</ol>'


def _route_kv_rows(items: tuple[tuple[str, Any], ...]) -> str:
    rows: list[str] = []
    for label, value in items:
        value_html = _route_list(value) if isinstance(value, (list, tuple, dict)) else html.escape(str(value))
        rows.append(f'<div class="kv"><div class="kv-k">{html.escape(label)}</div><div class="kv-v">{value_html}</div></div>')
    return "".join(rows)


def _best_path_summary_html(summary: Mapping[str, Any]) -> str:
    summary_json = html.escape(json.dumps(dict(summary), indent=2, sort_keys=True))
    rows = _route_kv_rows((
        ("Best path status", summary.get("status", "recommend_only")),
        ("Recommended route type", summary.get("recommended_route_type", "clarification_needed")),
        ("Primary option", summary.get("primary_option", "none")),
        ("Why this route", summary.get("why_this_route", [])),
        ("Safe next action", summary.get("safe_next_action", "preview_only")),
        ("Fallback summary", summary.get("fallback_summary", [])),
        ("Risk flags", summary.get("risk_flags", [])),
        ("Evidence boundary", summary.get("evidence_boundary", "Catalog inclusion is not quality evidence; recommendation is not execution authorization.")),
        ("Manual override availability", summary.get("manual_override_summary", "Mode/model controls are available; route/tool overrides are unavailable in this lane.")),
        ("Provider/local execution authorized", str(summary.get("provider_or_local_execution_authorized", False)).lower()),
        ("Tool execution authorized", str(summary.get("tool_execution_authorized", False)).lower()),
    ))
    rows += f'<div class="json-head"><h3>Copyable best-path JSON</h3></div><pre id="best-path-json">{summary_json}</pre>'
    return _route_section("Best Path Summary", rows, "best-path-summary-card")


def _route_preview_rows(route_preview: Mapping[str, Any] | None) -> str:
    if not route_preview:
        empty_rows = _route_kv_rows((
            ("Status", "No route preview yet"),
            ("No eligible route display", "Friendly fail-closed/no-eligible-route preview will render here without execution."),
            ("Evidence boundary", ROUTE_PREVIEW_BOUNDARY),
            ("Provider/local execution authorized", "false"),
            ("Tool execution authorized", "false"),
        ))
        override_rows = _route_kv_rows((
            ("Route override", "Unavailable in this local console lane; route is selected by existing metadata routers."),
            ("Mode override", "Use the Mode dropdown; preview reads the current selection."),
            ("Model override", "Use the Model dropdown or custom model input; preview and smoke use existing parameters."),
            ("Tool override", "Unavailable in this lane; metadata-only tool recommendation remains router selected."),
        ))
        return (
            _best_path_summary_html(build_best_path_summary(None))
            + _route_section("Route flow timeline", _route_flow_html(), "route-flow-card")
            + _route_section("Manual override controls", override_rows, "manual-override-card")
            + _catalog_snapshot_html({}, {})
            + _target_status_html()
            + _target_difference_html()
            + _improvement_loop_html()
            + _route_section("Evidence boundary", empty_rows, "route-evidence-card")
        )

    model_route = route_preview.get("model_route", {}) if isinstance(route_preview.get("model_route"), Mapping) else {}
    tool_route = route_preview.get("tool_route", {}) if isinstance(route_preview.get("tool_route"), Mapping) else {}
    interpretation = route_preview.get("task_interpretation", {}) if isinstance(route_preview.get("task_interpretation"), Mapping) else {}
    evidence_json = html.escape(json.dumps(route_preview, indent=2, sort_keys=True))
    status = route_preview.get("status", "preview_only")
    best_path = route_preview.get("best_path_summary")
    if not isinstance(best_path, Mapping):
        best_path = build_best_path_summary(route_preview)

    task_rows = _route_kv_rows((
        ("Task family", interpretation.get("task_family", route_preview.get("task_family") or "not_available")),
        ("Privacy indicator", interpretation.get("privacy_indicator", False)),
        ("Current-facts indicator", interpretation.get("current_facts_indicator", False)),
        ("Tool indicator", interpretation.get("tool_indicator", False)),
        ("Repo indicator", interpretation.get("repo_indicator", False)),
        ("Document indicator", interpretation.get("document_indicator", False)),
        ("Spreadsheet indicator", interpretation.get("spreadsheet_indicator", False)),
        ("Computation indicator", interpretation.get("computation_indicator", False)),
        ("Signal source", interpretation.get("source", "existing_metadata_router")),
    ))
    model_rows = _route_kv_rows((
        ("Model route status", model_route.get("status", "not_available")),
        ("Recommended mode", model_route.get("recommended_mode") or "none"),
        ("Recommended model", model_route.get("recommended_model") or "none"),
        ("Selected backend type", model_route.get("selected_backend_type") or "not_available"),
        ("Selected cost tier", model_route.get("selected_cost_tier") or "not_available"),
        ("Selected latency tier", model_route.get("selected_latency_tier") or "not_available"),
        ("Selected context tier", model_route.get("selected_context_tier") or "not_available"),
        ("Selected privacy tier", model_route.get("selected_privacy_tier") or "not_available"),
        ("Smoke eligibility", model_route.get("selected_smoke_eligible", "not_available")),
        ("Confidence label", model_route.get("confidence_label", "metadata_only")),
        ("Operator caveat", model_route.get("operator_caveat", "Catalog inclusion is not model quality evidence.")),
        ("Fallback candidates", route_preview.get("fallback_path", [])),
        ("Warnings", model_route.get("warnings", [])),
    ))
    tool_rows = _route_kv_rows((
        ("Tool route status", tool_route.get("status", "not_available")),
        ("Recommended tool route", tool_route.get("recommended_tool_id") or "none"),
        ("Tool category", tool_route.get("recommended_tool_family") or "none"),
        ("Execution authorization status", tool_route.get("execution_authorized", False)),
        ("Caveats", tool_route.get("warnings", [])),
        ("Tool fallback or alternative routes", tool_route.get("candidates", [])),
    ))
    override_rows = _route_kv_rows((
        ("Route override", "Unavailable in this local console lane; route is selected by existing metadata routers."),
        ("Mode override", "Use the Mode dropdown; preview reads the current selection."),
        ("Model override", "Use the Model dropdown or custom model input; preview and smoke use existing parameters."),
        ("Tool override", "Unavailable in this lane; metadata-only tool recommendation remains router selected."),
    ))
    evidence_rows = _route_kv_rows((
        ("Status", status),
        ("No-call evidence flag", model_route.get("no_call_evidence", True)),
        ("Preview-vs-execution boundary", route_preview.get("evidence_boundary", ROUTE_PREVIEW_BOUNDARY)),
        ("Catalog-not-quality evidence caveat", "Catalog inclusion is not model/tool quality evidence."),
        ("Provider/local execution authorized", str(route_preview.get("provider_or_local_execution_authorized", False)).lower()),
        ("Tool execution authorized", str(route_preview.get("tool_execution_authorized", False)).lower()),
        ("Route reasons (grouped)", _grouped_route_reasons(model_route, tool_route)),
    ))
    evidence_rows += f'<div class="json-head"><h3>Copyable route evidence JSON</h3></div><pre id="route-evidence-json">{evidence_json}</pre>'
    fail_closed = ""
    if status == "failed_closed" or model_route.get("status") == "failed_closed" or tool_route.get("status") == "failed_closed":
        fail_closed = _route_section("Friendly fail-closed / no eligible route", _route_kv_rows((("Safe display", "No eligible route preview remains visible and non-executing."),)), "route-fail-closed-card")

    return (
        _best_path_summary_html(best_path)
        + _route_section("Route flow timeline", _route_flow_html(), "route-flow-card")
        + _route_section("Task interpretation signals", task_rows, "task-interpretation-card")
        + _route_section("Model route card", model_rows, "model-route-card")
        + _route_section("Tool route card", tool_rows, "tool-route-card")
        + _catalog_snapshot_html(model_route, tool_route)
        + _route_section("Manual override controls", override_rows, "manual-override-card")
        + _target_status_html()
        + _target_difference_html()
        + _improvement_loop_html()
        + _route_section("Evidence boundary card", evidence_rows, "route-evidence-card")
        + fail_closed
    )



def _target_status_html() -> str:
    groups = (
        ("Built now", ("smoke runner", "local/OpenAI test console", "model catalog metadata", "routing preview", "best-path summary", "bounded JSON")),
        ("Next", ("operator review", "additional UI polish", "model cost/capability metadata refinements", "routed-vs-plain eval authorization")),
        ("Future", ("benchmark-backed routing", "model sync", "full tool execution", "release readiness review")),
    )
    columns = []
    for title, items in groups:
        body = "".join(f"<li>{html.escape(item)}</li>" for item in items)
        columns.append(f'<div class="status-column"><h3>{html.escape(title)}</h3><ul class="mini">{body}</ul></div>')
    return _route_section("Built now / next / future", '<div class="status-grid">' + ''.join(columns) + '</div>', "target-status-card")


def _target_difference_html() -> str:
    rows = _route_kv_rows((
        ("Closer to target", ("explicit best-path recommendation", "task interpretation signals", "model/tool catalog metadata", "fail-closed safety copy", "copyable bounded JSON")),
        ("Still bounded", ("no provider/local model execution from preview", "no tool execution", "no public dashboard/API", "no scoring or benchmark claims")),
        ("Operator review need", "Manual review should compare this local console preview against the target guide/diagrams before any broader product claim."),
    ))
    return _route_section("Target parity difference panel", rows, "target-difference-card")


def _catalog_snapshot_html(model_route: Mapping[str, Any], tool_route: Mapping[str, Any]) -> str:
    model_rows = _route_kv_rows((
        ("Hosted model metadata", "OpenAI-family catalog entries can render as hosted metadata; preview does not call them."),
        ("Local model metadata", "Ollama/local catalog entries can render as local metadata; preview does not run them."),
        ("Displayed tiers", (model_route.get("selected_cost_tier", "not_available"), model_route.get("selected_latency_tier", "not_available"), model_route.get("selected_context_tier", "not_available"), model_route.get("selected_privacy_tier", "not_available"))),
        ("Smoke eligible", model_route.get("selected_smoke_eligible", "not_available")),
    ))
    tool_rows = _route_kv_rows((
        ("Tool families", ("web/current research", "Python/computation", "GitHub/code", "docs/spreadsheets", "file parsing", "specialized tools")),
        ("Recommended tool", tool_route.get("recommended_tool_id") or "none"),
        ("Execution authorized", str(tool_route.get("execution_authorized", False)).lower()),
        ("Catalog caveat", "Tool recommendation is metadata-only and not tool execution."),
    ))
    return _route_section("Model and tool catalog snapshot", model_rows + tool_rows, "catalog-snapshot-card")


def _improvement_loop_html() -> str:
    steps = ("operator testing", "compare route evidence", "update catalog metadata", "update routing policy", "review better future routes")
    body = '<ol class="route-flow">' + ''.join(
        f'<li><span class="step-num">{idx}</span><strong>{html.escape(step)}</strong><p>review-only loop step; no scoring or benchmark claim.</p></li>'
        for idx, step in enumerate(steps, 1)
    ) + '</ol>'
    return _route_section("Improvement loop (review-only)", body, "improvement-loop-card")

def _reason_explanation(reason: str) -> str:
    if reason in REASON_EXPLANATIONS:
        return REASON_EXPLANATIONS[reason]
    if reason.startswith("openai_"):
        return "The OpenAI smoke check stopped safely. See the sanitized reason and errors below."
    if reason.startswith("runner_error:"):
        return "The runner stopped safely on an internal error class. No raw details are shown."
    return ""


def _model_option_tags(mode: str, selected_option: str) -> str:
    tags: list[str] = []
    for option in MODEL_OPTIONS[mode]:
        label = "custom (enter below)" if option == CUSTOM_MODEL_OPTION else option
        selected = " selected" if option == selected_option else ""
        tags.append(f'<option value="{html.escape(option)}"{selected}>{html.escape(label)}</option>')
    return "".join(tags)


def _status_presentation(status: str) -> tuple[str, str]:
    if status == "passed":
        return "state-passed", "Passed (smoke only)"
    if status == "failed_closed":
        return "state-failed", "Failed closed (safe)"
    if status == "not_run":
        return "state-neutral", "No run yet"
    return "state-neutral", status


def _friendly_result_rows(display_result: Mapping[str, Any]) -> str:
    rows: list[str] = []

    def add(label: str, value_html: str) -> None:
        rows.append(
            f'<div class="kv"><div class="kv-k">{html.escape(label)}</div>'
            f'<div class="kv-v">{value_html}</div></div>'
        )

    add("Status", html.escape(str(display_result.get("status", "not_run"))))

    reason = display_result.get("reason")
    if reason is not None:
        explanation = _reason_explanation(str(reason))
        reason_html = html.escape(str(reason))
        if explanation:
            reason_html += f'<div class="hint">{html.escape(explanation)}</div>'
        add("Reason", reason_html)

    add("Provider", html.escape(str(display_result.get("provider", "not_run"))))
    add("Model", html.escape(str(display_result.get("model", "not_run"))))

    latency = display_result.get("latency_ms")
    add("Latency (ms)", html.escape(str(latency if latency is not None else "not_run")))

    usage = display_result.get("usage")
    if isinstance(usage, Mapping) and usage:
        items = "".join(
            f"<li>{html.escape(str(key))}: {html.escape(str(value))}</li>" for key, value in usage.items()
        )
        add("Usage tokens", f'<ul class="mini">{items}</ul>')

    cost = display_result.get("estimated_cost_usd")
    if cost is not None:
        add("Estimated cost (USD)", html.escape(str(cost)))

    preview = display_result.get("output_preview")
    if preview:
        add("Output preview", html.escape(str(preview)))

    errors = display_result.get("errors")
    if errors:
        if isinstance(errors, list):
            items = "".join(
                "<li>"
                + html.escape(str(item.get("message", item) if isinstance(item, Mapping) else item))
                + "</li>"
                for item in errors
            )
            add("Errors", f'<ul class="mini">{items}</ul>')
        else:
            add("Errors", html.escape(str(errors)))

    flags = (
        f'smoke_evidence_only={str(display_result.get("smoke_evidence_only", True)).lower()}, '
        f'behavior_evidence={str(display_result.get("behavior_evidence", False)).lower()}, '
        f'quality_evidence={str(display_result.get("quality_evidence", False)).lower()}, '
        f'readiness_evidence={str(display_result.get("readiness_evidence", False)).lower()}'
    )
    add("Evidence flags", html.escape(flags))
    return "".join(rows)


def _checklist_html(title: str, steps: tuple[str, ...]) -> str:
    items = "".join(f"<li>{html.escape(step)}</li>" for step in steps)
    return f'<div class="checklist-group"><h3>{html.escape(title)}</h3><ol>{items}</ol></div>'


_PAGE_CSS = """
:root {
  color-scheme: light;
  --bg: #f4f5f7;
  --panel: #ffffff;
  --ink: #1f2430;
  --muted: #5a6271;
  --line: #d8dce4;
  --accent: #2f5bd1;
  --warn-bg: #fdf3d8;
  --warn-line: #d9b84a;
  --pass-bg: #e7f6ec;
  --pass-line: #3f9d63;
  --fail-bg: #fbe9e9;
  --fail-line: #c0504d;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.5;
}
.container { max-width: 920px; margin: 0 auto; padding: 24px 18px 48px; }
header.app-header {
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
  border-bottom: 1px solid var(--line); padding-bottom: 14px; margin-bottom: 18px;
}
header.app-header h1 { font-size: 1.35rem; margin: 0; }
.badge {
  font-size: 0.72rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
  background: #eaeefb; color: var(--accent); border: 1px solid #c3cef3;
  border-radius: 999px; padding: 3px 10px;
}
.card {
  background: var(--panel); border: 1px solid var(--line); border-radius: 10px;
  padding: 18px; margin-bottom: 18px;
}
.card h2 { margin: 0 0 12px; font-size: 1.05rem; }
.card h3 { margin: 0 0 8px; font-size: 0.95rem; }
.notice {
  border-radius: 8px; padding: 12px 14px; border: 1px solid var(--line); margin-bottom: 12px;
}
.notice-boundary { background: #eef1f6; border-color: var(--line); color: var(--muted); }
.notice-warn { background: var(--warn-bg); border-color: var(--warn-line); color: #7a5c08; }
label.field { display: block; margin-bottom: 14px; font-weight: 600; }
label.field span.field-label { display: block; margin-bottom: 5px; }
select, input[type="text"], textarea {
  width: 100%; font: inherit; color: inherit; background: #fff;
  border: 1px solid var(--line); border-radius: 7px; padding: 9px 10px;
}
textarea { resize: vertical; min-height: 110px; }
.counter { font-size: 0.82rem; color: var(--muted); font-weight: 500; margin-top: 5px; }
.help { font-size: 0.82rem; color: var(--muted); font-weight: 500; margin-top: 4px; }
button {
  font: inherit; font-weight: 600; cursor: pointer;
  border: 1px solid var(--accent); background: var(--accent); color: #fff;
  border-radius: 7px; padding: 9px 16px;
}
button.secondary { background: #fff; color: var(--accent); }
button[disabled] { opacity: 0.5; cursor: not-allowed; }
.result-banner {
  border-radius: 8px; padding: 10px 14px; font-weight: 700; margin-bottom: 14px; border: 1px solid var(--line);
}
.state-passed { background: var(--pass-bg); border-color: var(--pass-line); color: #1f6b3c; }
.state-failed { background: var(--fail-bg); border-color: var(--fail-line); color: #8f302d; }
.state-neutral { background: #eef1f6; border-color: var(--line); color: var(--muted); }
.kv {
  display: grid; grid-template-columns: 170px 1fr; gap: 10px;
  padding: 8px 0; border-bottom: 1px solid #eef0f4;
}
.kv:last-child { border-bottom: 0; }
.kv-k { color: var(--muted); font-weight: 600; }
.kv-v { word-break: break-word; }
.kv-v .hint { font-size: 0.84rem; color: var(--muted); margin-top: 4px; }
ul.mini { margin: 0; padding-left: 18px; }
.route-card { border: 1px solid #eef0f4; border-radius: 8px; padding: 14px; margin-top: 14px; }
.route-flow { display: grid; grid-template-columns: repeat(auto-fit, minmax(145px, 1fr)); gap: 10px; padding-left: 0; list-style: none; }
.route-flow li { border: 1px solid var(--line); border-radius: 8px; padding: 10px; background: #fbfcff; }
.status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; }
.status-column { border: 1px solid var(--line); border-radius: 8px; padding: 10px; background: #fbfcff; }
.route-flow p { margin: 6px 0 0; color: var(--muted); font-size: 0.84rem; }
.step-num { display: inline-block; width: 1.55rem; height: 1.55rem; border-radius: 999px; background: var(--accent); color: #fff; text-align: center; margin-right: 6px; }
.json-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
pre#sanitized-json, pre#route-evidence-json, pre#best-path-json {
  background: #1f2430; color: #eef0f4; border-radius: 8px; padding: 14px;
  overflow-x: auto; font-size: 0.86rem; margin: 10px 0 0;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
}
.copy-status { font-size: 0.82rem; color: var(--muted); font-weight: 500; }
.checklist-group { margin-bottom: 14px; }
.checklist-group:last-child { margin-bottom: 0; }
footer.app-footer { font-size: 0.82rem; color: var(--muted); margin-top: 6px; }
code { background: #eef1f6; border-radius: 4px; padding: 1px 5px; }
"""


_PAGE_SCRIPT_TEMPLATE = """
<script>
"use strict";
var MODEL_OPTIONS = __MODEL_OPTIONS__;
var PROMPT_LIMIT = __PROMPT_LIMIT__;
var CUSTOM_OPTION = "custom";

function rebuildModelOptions() {
  var modeSelect = document.getElementById("mode-select");
  var modelSelect = document.getElementById("model-select");
  if (!modeSelect || !modelSelect) { return; }
  var previous = modelSelect.value;
  var options = MODEL_OPTIONS[modeSelect.value] || [];
  modelSelect.innerHTML = "";
  options.forEach(function (opt) {
    var node = document.createElement("option");
    node.value = opt;
    node.textContent = (opt === CUSTOM_OPTION) ? "custom (enter below)" : opt;
    modelSelect.appendChild(node);
  });
  if (options.indexOf(previous) !== -1) { modelSelect.value = previous; }
  toggleCustomModel();
}

function toggleCustomModel() {
  var modelSelect = document.getElementById("model-select");
  var row = document.getElementById("custom-model-row");
  if (!modelSelect || !row) { return; }
  if (modelSelect.value === CUSTOM_OPTION) { row.removeAttribute("hidden"); }
  else { row.setAttribute("hidden", "hidden"); }
  syncPreviewInputs();
}

function syncPreviewInputs() {
  var modeSelect = document.getElementById("mode-select");
  var modelSelect = document.getElementById("model-select");
  var customModel = document.getElementById("custom-model");
  var previewMode = document.getElementById("preview-mode");
  var previewModel = document.getElementById("preview-model");
  var previewCustomModel = document.getElementById("preview-custom-model");
  if (modeSelect && previewMode) { previewMode.value = modeSelect.value; }
  if (modelSelect && previewModel) { previewModel.value = modelSelect.value; }
  if (customModel && previewCustomModel) { previewCustomModel.value = customModel.value; }
}

function updatePromptCounter() {
  var prompt = document.getElementById("prompt-input");
  var count = document.getElementById("prompt-count");
  var warning = document.getElementById("prompt-warning");
  var button = document.getElementById("run-button");
  if (!prompt || !count || !warning || !button) { return; }
  var length = prompt.value.length;
  count.textContent = length;
  if (length > PROMPT_LIMIT) {
    warning.removeAttribute("hidden");
    button.setAttribute("disabled", "disabled");
  } else {
    warning.setAttribute("hidden", "hidden");
    button.removeAttribute("disabled");
  }
}

function copySanitizedJson() {
  var panel = document.getElementById("sanitized-json");
  var status = document.getElementById("copy-status");
  var text = panel ? panel.textContent : "";
  function done(ok) {
    if (status) {
      status.textContent = ok ? "Copied sanitized JSON." : "Copy failed. Select the JSON and copy manually.";
    }
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
    return;
  }
  try {
    var area = document.createElement("textarea");
    area.value = text;
    document.body.appendChild(area);
    area.select();
    var ok = document.execCommand("copy");
    document.body.removeChild(area);
    done(ok);
  } catch (err) {
    done(false);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  var modeSelect = document.getElementById("mode-select");
  var modelSelect = document.getElementById("model-select");
  var promptInput = document.getElementById("prompt-input");
  var customModel = document.getElementById("custom-model");
  var copyButton = document.getElementById("copy-json");
  if (modeSelect) { modeSelect.addEventListener("change", rebuildModelOptions); }
  if (modelSelect) { modelSelect.addEventListener("change", toggleCustomModel); }
  if (customModel) { customModel.addEventListener("input", syncPreviewInputs); }
  if (promptInput) { promptInput.addEventListener("input", updatePromptCounter); }
  if (copyButton) { copyButton.addEventListener("click", copySanitizedJson); }
  toggleCustomModel();
  syncPreviewInputs();
  updatePromptCounter();
});
</script>
"""


def _script_html() -> str:
    options_json = json.dumps({mode: list(values) for mode, values in MODEL_OPTIONS.items()}, sort_keys=True)
    return _PAGE_SCRIPT_TEMPLATE.replace("__MODEL_OPTIONS__", options_json).replace(
        "__PROMPT_LIMIT__", str(MAX_PROMPT_CHARS)
    )


def render_result_html(
    result: Mapping[str, Any] | None = None,
    form_state: Mapping[str, str] | None = None,
    route_preview: Mapping[str, Any] | None = None,
) -> str:
    display_result = sanitize_result(result) if result else {}
    state = _form_state(**dict(form_state or {}))

    result_json = json.dumps(display_result, indent=2, sort_keys=True)
    escaped_json = html.escape(result_json)

    status = str(display_result.get("status", "not_run"))
    state_class, headline = _status_presentation(status)
    reason = str(display_result.get("reason", ""))

    limit_block = ""
    if reason == "prompt_too_long":
        limit_block = f'<div class="notice notice-warn">{html.escape(PROMPT_LIMIT_MESSAGE)}</div>'

    if display_result:
        result_body = (
            f'<div class="result-banner {state_class}">{html.escape(headline)}</div>'
            f"{limit_block}"
            f"{_friendly_result_rows(display_result)}"
        )
    else:
        result_body = (
            '<div class="result-banner state-neutral">No run yet</div>'
            '<p class="help">Submit the form to run one bounded local-only smoke check.</p>'
        )

    mode_options = (
        f'<option value="local"{" selected" if state["mode"] == "local" else ""}>local</option>'
        f'<option value="openai"{" selected" if state["mode"] == "openai" else ""}>openai</option>'
    )
    model_options = _model_option_tags(state["mode"], state["model_option"])
    custom_hidden = "" if state["model_option"] == CUSTOM_MODEL_OPTION else " hidden"
    prompt_value = html.escape(state["prompt"])
    prompt_length = len(state["prompt"])

    local_checklist = _checklist_html("Local / Ollama", LOCAL_SETUP_STEPS)
    openai_checklist = _checklist_html("OpenAI", OPENAI_SETUP_STEPS)
    route_task = html.escape(str((route_preview or {}).get("task", state["prompt"])))
    route_rows = _route_preview_rows(route_preview)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(APP_TITLE)}</title>
  <style>{_PAGE_CSS}</style>
</head>
<body>
  <div class="container">
    <header class="app-header">
      <h1>{html.escape(APP_TITLE)}</h1>
      <span class="badge">Local only</span>
    </header>

    <div class="notice notice-boundary">
      <strong>Evidence boundary:</strong> {html.escape(LOCAL_ONLY_NOTICE)}
      Run locally with <code>{html.escape(RUN_COMMAND)}</code>.
    </div>

    <div class="card" id="route-preview-panel">
      <h2>Route preview (metadata-only)</h2>
      <div class="notice notice-boundary">{html.escape(ROUTE_PREVIEW_BOUNDARY)}</div>
      <form method="post" action="/preview">
        <label class="field">
          <span class="field-label">Task for route preview</span>
          <textarea name="task" id="route-task-input" rows="4">{route_task}</textarea>
        </label>
        <input type="hidden" name="mode" id="preview-mode" value="{html.escape(state["mode"])}">
        <input type="hidden" name="model" id="preview-model" value="{html.escape(state["model_option"])}">
        <input type="hidden" name="custom_model" id="preview-custom-model" value="{html.escape(state["custom_model"])}">
        <button type="submit" id="preview-route-button" class="secondary">Preview route only</button>
      </form>
      <div class="help">Preview does not call providers, run local models, execute tools, validate model quality, or run smoke checks.</div>
      <div class="route-preview-result">{route_rows}</div>
    </div>

    <div class="card">
      <h2>Run a bounded smoke check</h2>
      <form method="post" action="/run">
        <label class="field">
          <span class="field-label">Mode</span>
          <select name="mode" id="mode-select">{mode_options}</select>
        </label>
        <label class="field">
          <span class="field-label">Model</span>
          <select name="model" id="model-select">{model_options}</select>
        </label>
        <div id="custom-model-row" class="field"{custom_hidden}>
          <label class="field">
            <span class="field-label">Custom model</span>
            <input type="text" name="custom_model" id="custom-model" value="{html.escape(state["custom_model"])}" placeholder="Enter a custom model id">
          </label>
        </div>
        <label class="field">
          <span class="field-label">Prompt</span>
          <textarea name="prompt" id="prompt-input" rows="5">{prompt_value}</textarea>
        </label>
        <div class="counter"><span id="prompt-count">{prompt_length}</span> / {MAX_PROMPT_CHARS} characters (max length: {MAX_PROMPT_CHARS})</div>
        <div id="prompt-warning" class="notice notice-warn" hidden>{html.escape(PROMPT_LIMIT_MESSAGE)}</div>
        <button type="submit" id="run-button">Run bounded smoke check</button>
      </form>
    </div>

    <div class="card">
      <h2>Result summary</h2>
      {result_body}
    </div>

    <div class="card">
      <div class="json-head">
        <h2>Sanitized JSON</h2>
        <button type="button" id="copy-json" class="secondary">Copy sanitized JSON</button>
      </div>
      <span class="copy-status" id="copy-status" aria-live="polite"></span>
      <pre id="sanitized-json">{escaped_json}</pre>
    </div>

    <div class="card">
      <h2>Setup checklist</h2>
      {local_checklist}
      {openai_checklist}
    </div>

    <footer class="app-footer">
      No API key field is provided. OpenAI mode reads <code>OPENAI_API_KEY</code> from the local environment only.
      This console is local-only, persists no results, and loads no external assets.
    </footer>
  </div>
  {_script_html()}
</body>
</html>"""


app = FastAPI(title=APP_TITLE)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    assert_loopback_request(request)
    return HTMLResponse(render_result_html())


@app.post("/preview", response_class=HTMLResponse)
async def preview_from_form(request: Request) -> HTMLResponse:
    assert_loopback_request(request)
    body = (await request.body()).decode("utf-8", errors="replace")
    form = parse_qs(body, keep_blank_values=True)
    mode = form.get("mode", ["local"])[0]
    model_option = form.get("model", [""])[0]
    custom_model = form.get("custom_model", [""])[0]
    task = form.get("task", [DEFAULT_PROMPT])[0]
    effective_model = _resolve_effective_model(mode, model_option, custom_model)
    preview = build_route_preview(task=task, mode=mode, model=effective_model)
    form_state = {"mode": mode, "model_option": model_option, "custom_model": custom_model, "prompt": task}
    return HTMLResponse(render_result_html(form_state=form_state, route_preview=preview))


@app.post("/api/preview")
async def preview_from_api(request: Request) -> JSONResponse:
    assert_loopback_request(request)
    payload = await request.json()
    mode = str(payload.get("mode", "local"))
    model = str(payload.get("model", ""))
    custom_model = str(payload.get("custom_model", ""))
    task = str(payload.get("task", DEFAULT_PROMPT))
    effective_model = _resolve_effective_model(mode, model, custom_model)
    return JSONResponse(build_route_preview(task=task, mode=mode, model=effective_model))


@app.post("/run", response_class=HTMLResponse)
async def run_from_form(request: Request) -> HTMLResponse:
    assert_loopback_request(request)
    body = (await request.body()).decode("utf-8", errors="replace")
    form = parse_qs(body, keep_blank_values=True)
    mode = form.get("mode", [""])[0]
    model_option = form.get("model", [""])[0]
    custom_model = form.get("custom_model", [""])[0]
    prompt = form.get("prompt", [DEFAULT_PROMPT])[0]
    effective_model = _resolve_effective_model(mode, model_option, custom_model)
    result = run_console_smoke(mode=mode, model=effective_model, prompt=prompt)
    form_state = {
        "mode": mode,
        "model_option": model_option,
        "custom_model": custom_model,
        "prompt": prompt,
    }
    return HTMLResponse(render_result_html(result, form_state=form_state))


@app.post("/api/run")
async def run_from_api(request: Request) -> JSONResponse:
    assert_loopback_request(request)
    payload = await request.json()
    mode = str(payload.get("mode", ""))
    model = str(payload.get("model", ""))
    custom_model = str(payload.get("custom_model", ""))
    prompt = str(payload.get("prompt", DEFAULT_PROMPT))
    effective_model = _resolve_effective_model(mode, model, custom_model)
    return JSONResponse(run_console_smoke(mode=mode, model=effective_model, prompt=prompt))
