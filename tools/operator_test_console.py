#!/usr/bin/env python3
"""Local-only Operator smoke test console.

This console is intentionally local-only and smoke-only. It reuses
``tools.operator_smoke_runner`` for provider execution so the existing fail-closed
checks remain the execution path.
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

from tools import operator_smoke_runner as smoke_runner

APP_TITLE = "Alpha Solver local smoke test console"
DEFAULT_LOCAL_MODEL = "qwen2.5:3b"
DEFAULT_OPENAI_MODEL = smoke_runner.DEFAULT_OPENAI_MODEL
DEFAULT_PROMPT = smoke_runner.DEFAULT_PROMPT
LOCAL_ONLY_NOTICE = (
    "Passing smoke does not prove quality, readiness, benchmark success, "
    "provider superiority, local-model superiority, production readiness, "
    "public readiness, security/privacy completion, or Alpha superiority."
)
SECRET_KEYS = ("api_key", "authorization", "bearer", "token", "secret", "password")


def _is_loopback_host(host: str | None) -> bool:
    if not host:
        return False
    normalized = host.strip().lower().strip("[]")
    if normalized.startswith("localhost:") or normalized.startswith("127.0.0.1:"):
        normalized = normalized.rsplit(":", 1)[0]
    if normalized.startswith("[::1]:"):
        normalized = "::1"
    return normalized in {"127.0.0.1", "localhost", "::1"}


def assert_loopback_request(request: Request) -> None:
    """Reject non-loopback Host headers for the local console."""

    host = request.headers.get("host", "")
    if not _is_loopback_host(host):
        raise HTTPException(status_code=403, detail="operator_test_console_loopback_only")


def _redact_scalar(value: Any) -> Any:
    if isinstance(value, str):
        redacted = value
        for marker in ("sk-", "bearer-prefix "):
            if marker in redacted:
                return "[REDACTED]"
        return redacted
    return value


def sanitize_result(result: Mapping[str, Any]) -> dict[str, Any]:
    """Return a JSON-safe result with secret-like fields redacted or removed."""

    def walk(value: Any, key: str = "") -> Any:
        lowered = key.lower()
        if any(marker in lowered for marker in SECRET_KEYS):
            return "[REDACTED]"
        if isinstance(value, Mapping):
            return {str(k): walk(v, str(k)) for k, v in value.items()}
        if isinstance(value, list):
            return [walk(item, key) for item in value]
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
    if len(cleaned_prompt) > smoke_runner.MAX_PROMPT_CHARS:
        result = smoke_runner._base_result(mode=mode, provider=mode, model=model)  # noqa: SLF001
        result["reason"] = "prompt_too_long"
        return sanitize_result(result)

    execution_env = _env_for_mode(mode, model, env)
    if mode == "local":
        return sanitize_result(smoke_runner.run_local(cleaned_prompt, env=execution_env))
    if mode == "openai":
        return sanitize_result(smoke_runner.run_openai(cleaned_prompt, env=execution_env))
    result = smoke_runner._base_result(mode=mode, provider=mode, model=model)  # noqa: SLF001
    result["reason"] = "unsupported_mode"
    return sanitize_result(result)


def render_result_html(result: Mapping[str, Any] | None = None) -> str:
    display_result = sanitize_result(result) if result else {}
    result_json = json.dumps(display_result, indent=2, sort_keys=True)
    escaped_json = html.escape(result_json)
    status = html.escape(str(display_result.get("status", "not_run")))
    provider = html.escape(str(display_result.get("provider", "not_run")))
    model = html.escape(str(display_result.get("model", "not_run")))
    latency = html.escape(str(display_result.get("latency_ms", "not_run")))
    usage = html.escape(json.dumps(display_result.get("usage"), sort_keys=True))
    cost = display_result.get("estimated_cost_usd")
    cost_html = "" if cost is None else f"<li>Estimated cost: {html.escape(str(cost))}</li>"
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>{APP_TITLE}</title></head>
<body>
  <h1>{APP_TITLE}</h1>
  <p><strong>Local-only:</strong> run with <code>uvicorn tools.operator_test_console:app --host 127.0.0.1 --port 8765</code>.</p>
  <p><strong>Evidence boundary:</strong> {LOCAL_ONLY_NOTICE}</p>
  <form method="post" action="/run">
    <label>Mode
      <select name="mode">
        <option value="local">local</option>
        <option value="openai">openai</option>
      </select>
    </label><br>
    <label>Model <input name="model" value="{html.escape(DEFAULT_LOCAL_MODEL)}"></label>
    <p>Defaults: local <code>{html.escape(DEFAULT_LOCAL_MODEL)}</code>, OpenAI <code>{html.escape(DEFAULT_OPENAI_MODEL)}</code>.</p>
    <label>Prompt<br><textarea name="prompt" rows="5" cols="80">{html.escape(DEFAULT_PROMPT)}</textarea></label><br>
    <button type="submit">Run bounded smoke check</button>
  </form>
  <h2>Result</h2>
  <ul>
    <li>Status: {status}</li>
    <li>Provider: {provider}</li>
    <li>Model: {model}</li>
    <li>Latency ms: {latency}</li>
    <li>Usage: {usage}</li>
    {cost_html}
    <li>smoke_evidence_only: {str(display_result.get('smoke_evidence_only', True)).lower()}</li>
    <li>behavior_evidence: {str(display_result.get('behavior_evidence', False)).lower()}</li>
    <li>quality_evidence: {str(display_result.get('quality_evidence', False)).lower()}</li>
    <li>readiness_evidence: {str(display_result.get('readiness_evidence', False)).lower()}</li>
  </ul>
  <pre id="sanitized-json">{escaped_json}</pre>
  <p>No API key field is provided. OpenAI mode reads <code>OPENAI_API_KEY</code> from the local environment only.</p>
</body></html>"""


app = FastAPI(title=APP_TITLE)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    assert_loopback_request(request)
    return HTMLResponse(render_result_html())


@app.post("/run", response_class=HTMLResponse)
async def run_from_form(request: Request) -> HTMLResponse:
    assert_loopback_request(request)
    body = (await request.body()).decode("utf-8", errors="replace")
    form = parse_qs(body, keep_blank_values=True)
    mode = form.get("mode", [""])[0]
    model = form.get("model", [""])[0]
    prompt = form.get("prompt", [DEFAULT_PROMPT])[0]
    selected_model = model.strip() or (DEFAULT_LOCAL_MODEL if mode == "local" else DEFAULT_OPENAI_MODEL)
    if mode == "openai" and selected_model == DEFAULT_LOCAL_MODEL:
        selected_model = DEFAULT_OPENAI_MODEL
    result = run_console_smoke(mode=mode, model=selected_model, prompt=prompt)
    return HTMLResponse(render_result_html(result))


@app.post("/api/run")
async def run_from_api(request: Request) -> JSONResponse:
    assert_loopback_request(request)
    payload = await request.json()
    mode = str(payload.get("mode", ""))
    model = str(payload.get("model", ""))
    prompt = str(payload.get("prompt", DEFAULT_PROMPT))
    selected_model = model.strip() or (DEFAULT_LOCAL_MODEL if mode == "local" else DEFAULT_OPENAI_MODEL)
    if mode == "openai" and selected_model == DEFAULT_LOCAL_MODEL:
        selected_model = DEFAULT_OPENAI_MODEL
    return JSONResponse(run_console_smoke(mode=mode, model=selected_model, prompt=prompt))
