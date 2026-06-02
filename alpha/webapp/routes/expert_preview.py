"""Authenticated expert preview UI routes for same-provider comparison."""

from __future__ import annotations

from email import policy
from email.parser import BytesParser
import html
import json
import logging
import os
from threading import Lock
from typing import Any, Dict, Iterable, Mapping
from urllib.parse import parse_qs

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse

router = APIRouter()
logger = logging.getLogger(__name__)

DISCLAIMER = (
    "This preview is for supervised operator review. It does not prove Alpha Solver "
    "superiority, MVP validation, production readiness, broad runtime readiness, or "
    "answer-quality benchmark success."
)

ROUTE = "/dashboard/expert-preview"
_ROUTE = ROUTE
LIVE_PREVIEW_ENABLED_ENV = "ALPHA_LIVE_PREVIEW_ENABLED"
LIVE_PREVIEW_MAX_REQUESTS_ENV = "ALPHA_LIVE_PREVIEW_MAX_REQUESTS"
_DEFAULT_LIVE_PREVIEW_MAX_REQUESTS = 1
_LIVE_PREVIEW_DISABLED_MESSAGE = (
    "Live OpenAI preview testing is disabled. Set "
    f"{LIVE_PREVIEW_ENABLED_ENV}=true and configure a low "
    f"{LIVE_PREVIEW_MAX_REQUESTS_ENV} only for explicitly approved operator testing."
)
_LIVE_PREVIEW_CAP_MESSAGE = (
    "Live OpenAI preview request cap reached for this service instance. "
    f"Raise {LIVE_PREVIEW_MAX_REQUESTS_ENV} only with explicit operator approval."
)


def _truthy_env(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _model_provider() -> str:
    return os.getenv("MODEL_PROVIDER", "local").strip().lower()


def _live_preview_max_requests() -> int:
    raw = os.getenv(LIVE_PREVIEW_MAX_REQUESTS_ENV, "").strip()
    if not raw:
        return _DEFAULT_LIVE_PREVIEW_MAX_REQUESTS
    try:
        return int(raw)
    except ValueError:
        logger.warning(
            "live_preview_guard blocked reason=invalid_cap provider=openai env=%s",
            LIVE_PREVIEW_MAX_REQUESTS_ENV,
        )
        return 0


def _live_preview_lock(request: Request) -> Lock:
    lock = getattr(request.app.state, "live_preview_guard_lock", None)
    if lock is None:
        lock = Lock()
        request.app.state.live_preview_guard_lock = lock
    return lock


def _check_live_preview_guard(request: Request) -> str | None:
    """Return a safe user-facing error when the live preview must fail closed."""

    provider = _model_provider()
    if provider != "openai":
        return None

    if not _truthy_env(LIVE_PREVIEW_ENABLED_ENV):
        logger.warning(
            "live_preview_guard blocked reason=disabled provider=openai env=%s",
            LIVE_PREVIEW_ENABLED_ENV,
        )
        return _LIVE_PREVIEW_DISABLED_MESSAGE

    max_requests = _live_preview_max_requests()
    if max_requests <= 0:
        logger.warning(
            "live_preview_guard blocked reason=cap_not_positive provider=openai max_requests=%s",
            max_requests,
        )
        return _LIVE_PREVIEW_CAP_MESSAGE

    with _live_preview_lock(request):
        count = int(getattr(request.app.state, "live_preview_request_count", 0))
        if count >= max_requests:
            logger.warning(
                "live_preview_guard blocked reason=cap_reached provider=openai count=%s max_requests=%s",
                count,
                max_requests,
            )
            return _LIVE_PREVIEW_CAP_MESSAGE
        request.app.state.live_preview_request_count = count + 1
        logger.warning(
            "live_preview_guard allowed provider=openai count=%s max_requests=%s",
            count + 1,
            max_requests,
        )
    return None


def _escape(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _answer(payload: Mapping[str, Any]) -> str:
    value = payload.get("answer", payload.get("final_answer", ""))
    return str(value) if value is not None else ""


def _public_meta(payload: Mapping[str, Any]) -> Dict[str, Any]:
    meta = payload.get("meta")
    if not isinstance(meta, Mapping):
        return {}
    allowed = (
        "route",
        "complexity",
        "provider",
        "model",
        "model_set",
        "call_count",
        "preview_parse_status",
        "confidence_available",
    )
    return {key: meta[key] for key in allowed if key in meta}


def _render_list(items: Iterable[str]) -> str:
    values = list(items)
    if not values:
        return '<p class="empty">None surfaced.</p>'
    return "<ul>" + "".join(f"<li>{_escape(item)}</li>" for item in values) + "</ul>"


def _render_plain_payload(payload: Mapping[str, Any] | None) -> str:
    if payload is None:
        return '<p class="empty">Submit a prompt to render the plain same-provider output.</p>'
    meta = _public_meta(payload)
    details = json.dumps(meta, indent=2, sort_keys=True) if meta else "{}"
    return f"""
      <div class="answer response-text" aria-label="Primary response">{_escape(_answer(payload))}</div>
      <details>
        <summary>Details</summary>
        <pre>{_escape(details)}</pre>
      </details>
    """


def _render_expert_payload(payload: Mapping[str, Any] | None) -> str:
    if payload is None:
        return '<p class="empty">Submit a prompt to render the Alpha Solver expert preview.</p>'
    meta = _public_meta(payload)
    confidence = (
        "unavailable"
        if meta.get("confidence_available") is False
        else payload.get("confidence", "—")
    )
    rows = [
        ("Mode", payload.get("mode", "—")),
        ("Confidence", confidence),
        ("Complexity", meta.get("complexity", "—")),
        ("Call count", meta.get("call_count", "—")),
    ]
    details = json.dumps(meta, indent=2, sort_keys=True) if meta else "{}"
    rows_html = "".join(
        f"<div><dt>{_escape(label)}</dt><dd>{_escape(value)}</dd></div>" for label, value in rows
    )
    return f"""
      <div class="answer response-text" aria-label="Primary response">{_escape(_answer(payload))}</div>
      <dl class="metadata">{rows_html}</dl>
      <h3>Considerations</h3>
      {_render_list(_as_list(payload.get('considerations')))}
      <h3>Assumptions</h3>
      {_render_list(_as_list(payload.get('assumptions')))}
      <h3>Clarifying questions</h3>
      {_render_list(_as_list(payload.get('clarifying_questions')))}
      <details>
        <summary>Details</summary>
        <pre>{_escape(details)}</pre>
      </details>
    """


def _render_page(
    *,
    prompt: str = "",
    plain: Mapping[str, Any] | None = None,
    expert: Mapping[str, Any] | None = None,
    error: str = "",
) -> str:
    error_html = f'<p class="error" role="alert">{_escape(error)}</p>' if error else ""
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Alpha Solver · Expert Preview</title>
    <style>
      :root {{ color-scheme: light dark; font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.5; }}
      body {{ margin: 0; min-height: 100vh; background: radial-gradient(circle at top, #f6f8ff, #e4e8f4); color: #1d2038; }}
      .container {{ max-width: 1080px; margin: 0 auto; padding: 2.5rem 1.25rem 4rem; }}
      h1 {{ margin-bottom: 0.5rem; }}
      .disclaimer {{ border: 1px solid #c7d2fe; background: rgba(238, 242, 255, 0.9); border-radius: 14px; padding: 1rem; color: #30365f; }}
      form, .pane {{ background: rgba(255, 255, 255, 0.92); border-radius: 16px; padding: 1.25rem; box-shadow: 0 18px 55px rgba(31, 35, 71, 0.08); }}
      form {{ display: grid; gap: 0.85rem; margin: 1.5rem 0; }}
      label {{ font-weight: 700; }}
      textarea {{ min-height: 130px; resize: vertical; border: 1px solid #cdd5ef; border-radius: 12px; padding: 0.85rem 1rem; font: inherit; color: inherit; background: rgba(255,255,255,0.78); }}
      button {{ justify-self: start; border: 0; border-radius: 999px; padding: 0.7rem 1.25rem; font: inherit; font-weight: 700; color: white; background: linear-gradient(135deg, #5661f6, #7b5ff4); cursor: pointer; }}
      button:disabled {{ cursor: wait; opacity: 0.72; }}
      .panes {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); align-items: start; gap: 1rem; }}
      .pane {{ min-width: 0; }}
      .pane h2 {{ margin-top: 0; }}
      .answer, pre {{ white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; }}
      .answer {{ display: block; margin: 0 0 1rem; max-height: none; overflow: visible; border: 1px solid rgba(86, 97, 246, 0.16); background: rgba(237, 240, 255, 0.65); border-radius: 12px; padding: 1rem; }}
      .metadata {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.75rem; }}
      dt {{ color: #565b8f; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }}
      dd {{ margin: 0; font-weight: 600; }}
      details {{ margin-top: 1rem; }}
      summary {{ cursor: pointer; font-weight: 700; }}
      pre {{ background: #111827; color: #e5e7eb; border-radius: 12px; padding: 0.85rem; }}
      .empty {{ color: #5f668f; }}
      .error {{ padding: 0.85rem 1rem; border-radius: 12px; background: rgba(244, 67, 54, 0.12); color: #9f1239; }}
      @media (max-width: 760px) {{ .panes {{ grid-template-columns: 1fr; }} }}
    </style>
  </head>
  <body>
    <main class="container">
      <h1>Supervised preview only</h1>
      <p class="disclaimer">{_escape(DISCLAIMER)}</p>
      {error_html}
      <form method="post" action="{_ROUTE}" id="expert-preview-form">
        <label for="prompt">Prompt</label>
        <textarea id="prompt" name="prompt" required>{_escape(prompt)}</textarea>
        <button type="submit">Compare same-provider outputs</button>
      </form>
      <section class="panes" aria-label="same-provider comparison">
        <article class="pane" id="plain-pane">
          <h2>Plain provider output</h2>
          {_render_plain_payload(plain)}
        </article>
        <article class="pane" id="expert-pane">
          <h2>Alpha Solver expert preview</h2>
          {_render_expert_payload(expert)}
        </article>
      </section>
    </main>
    <script>
      function cookieValue(name) {{
        return document.cookie
          .split(";")
          .map((part) => part.trim())
          .find((part) => part.startsWith(name + "="))
          ?.slice(name.length + 1) || "";
      }}
      function initExpertPreviewForm() {{
        const form = document.querySelector("#expert-preview-form");
        if (!form || form.dataset.alphaSubmitBound === "true") {{
          return;
        }}
        form.dataset.alphaSubmitBound = "true";
        let previewInFlight = false;
        form.addEventListener("submit", async (event) => {{
          event.preventDefault();
          if (previewInFlight) {{
            return;
          }}
          previewInFlight = true;
          const submitButton = form.querySelector('button[type="submit"]');
          const originalButtonText = submitButton?.textContent || "Compare same-provider outputs";
          if (submitButton) {{
            submitButton.disabled = true;
            submitButton.textContent = "Running preview...";
          }}
          form.setAttribute("aria-busy", "true");
          try {{
            const response = await fetch(form.action, {{
              method: "POST",
              headers: {{
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "X-Alpha-CSRF": cookieValue("alpha_dashboard_csrf"),
              }},
              body: new URLSearchParams(new FormData(form)),
            }});
            const html = await response.text();
            const nextDocument = new DOMParser().parseFromString(html, "text/html");
            document.title = nextDocument.title;
            document.body.innerHTML = nextDocument.body.innerHTML;
            initExpertPreviewForm();
          }} finally {{
            previewInFlight = false;
            if (document.body.contains(form)) {{
              form.removeAttribute("aria-busy");
              if (submitButton) {{
                submitButton.disabled = false;
                submitButton.textContent = originalButtonText;
              }}
            }}
          }}
        }});
      }}
      initExpertPreviewForm();
    </script>
  </body>
</html>"""


def _prompt_from_multipart_body(content_type: str, body: bytes) -> str:
    message = BytesParser(policy=policy.default).parsebytes(
        b"Content-Type: "
        + content_type.encode("latin-1", errors="ignore")
        + b"\r\nMIME-Version: 1.0\r\n\r\n"
        + body
    )
    if not message.is_multipart():
        return ""
    for part in message.iter_parts():
        params = dict(part.get_params(header="content-disposition", failobj=[]))
        if params.get("name") != "prompt":
            continue
        payload = part.get_payload(decode=True)
        if payload is None:
            return str(part.get_payload()).strip()
        charset = part.get_content_charset() or "utf-8"
        return payload.decode(charset, errors="replace").strip()
    return ""


async def _prompt_from_form(request: Request) -> str:
    form = await request.form()
    value = form.get("prompt", "")
    return str(value).strip()


async def _extract_prompt(request: Request) -> str:
    content_type_header = request.headers.get("content-type", "")
    content_type = content_type_header.lower()
    if "application/json" in content_type:
        payload = await request.json()
        if isinstance(payload, Mapping):
            return str(payload.get("prompt", "")).strip()
        return ""

    if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        try:
            return await _prompt_from_form(request)
        except AssertionError:
            # Starlette requires the optional python-multipart package even for
            # URL-encoded form parsing. Keep the preview route compatible with
            # minimal no-network installs by falling back to the raw body parser.
            pass

    body = await request.body()
    if not body:
        return ""
    if "multipart/form-data" in content_type:
        return _prompt_from_multipart_body(content_type_header, body)
    parsed = parse_qs(body.decode())
    return (parsed.get("prompt") or [""])[0].strip()


async def _solve_preview(request: Request, prompt: str, *, expert: bool) -> Dict[str, Any]:
    # Import lazily so tests can monkeypatch service.app without importing the
    # API application when they only render the page.
    from service.app import SolveRequest, solve

    context: Dict[str, Any] = {}
    if expert:
        context["route"] = "expert"
    response = await solve(SolveRequest(query=prompt, context=context), request)
    body = response.body.decode("utf-8")
    payload = json.loads(body) if body else {}
    if not isinstance(payload, dict):
        return {"final_answer": str(payload)}
    return payload


@router.get(_ROUTE, response_class=HTMLResponse)
async def expert_preview_page() -> HTMLResponse:
    return HTMLResponse(content=_render_page())


@router.post(_ROUTE, response_class=HTMLResponse)
async def expert_preview_submit(request: Request) -> HTMLResponse:
    prompt = await _extract_prompt(request)
    if not prompt:
        return HTMLResponse(
            content=_render_page(error="Prompt is required."),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    guard_error = _check_live_preview_guard(request)
    if guard_error:
        return HTMLResponse(
            content=_render_page(prompt=prompt, error=guard_error),
            status_code=status.HTTP_403_FORBIDDEN,
        )
    try:
        plain = await _solve_preview(request, prompt, expert=False)
        expert = await _solve_preview(request, prompt, expert=True)
    except Exception:
        return HTMLResponse(
            content=_render_page(prompt=prompt, error="Preview request failed."),
            status_code=status.HTTP_502_BAD_GATEWAY,
        )
    return HTMLResponse(content=_render_page(prompt=prompt, plain=plain, expert=expert))


__all__ = ["router", "DISCLAIMER"]
