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



def build_route_preview(task: str, mode: str, model: str) -> dict[str, Any]:
    """Build a deterministic metadata-only route preview from existing routers."""

    cleaned_task = (task or "").strip()
    selected_mode = mode if mode in {"local", "openai"} else "local"
    requested_model = (model or "").strip() or _model_default(selected_mode)
    model_preview = model_router.preview_route(
        model_router.RoutingPreviewRequest(
            requested_mode=selected_mode,
            requested_model=requested_model,
            allow_hosted_providers=False,
            allow_local=True,
            prompt_length=len(cleaned_task),
            local_only=True,
        )
    ).as_dict()
    tool_preview = tool_router.recommend_tool(
        tool_router.ToolRecommendationRequest(task_text=cleaned_task, untrusted_context="operator_console_task")
    ).as_dict()
    return {
        "status": "preview_only",
        "task": cleaned_task,
        "task_family": tool_preview.get("recommended_tool_family"),
        "model_route": model_preview,
        "tool_route": tool_preview,
        "fallback_path": model_preview.get("fallbacks", []),
        "evidence_boundary": ROUTE_PREVIEW_BOUNDARY,
        "provider_or_local_execution_authorized": False,
        "tool_execution_authorized": False,
        "preview_only": True,
    }


def _route_list(values: Any) -> str:
    if not values:
        return '<span class="muted-inline">none</span>'
    if isinstance(values, Mapping):
        values = [f"{key}={value}" for key, value in values.items()]
    items = "".join(f"<li>{html.escape(str(value))}</li>" for value in values)
    return f'<ul class="mini">{items}</ul>'


def _route_preview_rows(route_preview: Mapping[str, Any] | None) -> str:
    rows: list[str] = []

    def add(label: str, value: Any) -> None:
        if isinstance(value, (list, tuple, dict)):
            value_html = _route_list(value)
        else:
            value_html = html.escape(str(value))
        rows.append(
            f'<div class="kv"><div class="kv-k">{html.escape(label)}</div>'
            f'<div class="kv-v">{value_html}</div></div>'
        )

    if not route_preview:
        add("Status", "No route preview yet")
        add("Evidence boundary", ROUTE_PREVIEW_BOUNDARY)
        add("Provider/local execution authorized", "false")
        add("Tool execution authorized", "false")
        return "".join(rows)

    model_route = route_preview.get("model_route", {}) if isinstance(route_preview.get("model_route"), Mapping) else {}
    tool_route = route_preview.get("tool_route", {}) if isinstance(route_preview.get("tool_route"), Mapping) else {}
    add("Status", route_preview.get("status", "preview_only"))
    add("Task family", route_preview.get("task_family") or "not_available")
    add(
        "Recommended model path",
        f"{model_route.get('recommended_mode') or 'none'} / {model_route.get('recommended_model') or 'none'}",
    )
    add(
        "Recommended tool family",
        f"{tool_route.get('recommended_tool_family') or 'none'} / {tool_route.get('recommended_tool_id') or 'none'}",
    )
    add("Route reasons", list(model_route.get("reasons", [])) + list(tool_route.get("reasons", [])))
    add("Route warnings", list(model_route.get("warnings", [])) + list(tool_route.get("warnings", [])))
    add("Fallback path", route_preview.get("fallback_path", []))
    add("Evidence boundary", route_preview.get("evidence_boundary", ROUTE_PREVIEW_BOUNDARY))
    add(
        "Provider/local execution authorized",
        str(route_preview.get("provider_or_local_execution_authorized", False)).lower(),
    )
    add("Tool execution authorized", str(route_preview.get("tool_execution_authorized", False)).lower())
    return "".join(rows)

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
.json-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
pre#sanitized-json {
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
  var copyButton = document.getElementById("copy-json");
  if (modeSelect) { modeSelect.addEventListener("change", rebuildModelOptions); }
  if (modelSelect) { modelSelect.addEventListener("change", toggleCustomModel); }
  if (promptInput) { promptInput.addEventListener("input", updatePromptCounter); }
  if (copyButton) { copyButton.addEventListener("click", copySanitizedJson); }
  toggleCustomModel();
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
        <input type="hidden" name="mode" value="{html.escape(state["mode"])}">
        <input type="hidden" name="model" value="{html.escape(state["model_option"])}">
        <input type="hidden" name="custom_model" value="{html.escape(state["custom_model"])}">
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
