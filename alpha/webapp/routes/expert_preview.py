"""Authenticated expert preview UI routes for same-provider comparison."""

from __future__ import annotations

import html
import json
from typing import Any, Dict, Iterable, Mapping
from urllib.parse import parse_qs

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse

router = APIRouter()

DISCLAIMER = (
    "This preview is for supervised operator review. It does not prove Alpha Solver "
    "superiority, MVP validation, production readiness, broad runtime readiness, or "
    "answer-quality benchmark success."
)

_ROUTE = "/dashboard/expert-preview"
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
      <p class="answer">{_escape(_answer(payload))}</p>
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
      <p class="answer">{_escape(_answer(payload))}</p>
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
      .panes {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }}
      .pane h2 {{ margin-top: 0; }}
      .answer, pre {{ white-space: pre-wrap; overflow-wrap: anywhere; }}
      .answer {{ border: 1px solid rgba(86, 97, 246, 0.16); background: rgba(237, 240, 255, 0.65); border-radius: 12px; padding: 1rem; }}
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
      <form method="post" action="{_ROUTE}">
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
      const form = document.querySelector("form");
      function cookieValue(name) {{
        return document.cookie
          .split(";")
          .map((part) => part.trim())
          .find((part) => part.startsWith(name + "="))
          ?.slice(name.length + 1) || "";
      }}
      form.addEventListener("submit", async (event) => {{
        event.preventDefault();
        const response = await fetch(form.action, {{
          method: "POST",
          headers: {{ "X-Alpha-CSRF": cookieValue("alpha_dashboard_csrf") }},
          body: new FormData(form),
        }});
        const html = await response.text();
        document.open();
        document.write(html);
        document.close();
      }});
    </script>
  </body>
</html>"""


async def _extract_prompt(request: Request) -> str:
    content_type = request.headers.get("content-type", "").lower()
    if "application/json" in content_type:
        payload = await request.json()
        if isinstance(payload, Mapping):
            return str(payload.get("prompt", "")).strip()
        return ""
    body = await request.body()
    if not body:
        return ""
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
