"""Read-only Alpha Solver Operator Console shell.

This module renders a protected, local-first operator cockpit made of status
cards. It exposes contract/status information for the operator and clearly
marks every not-yet-wired surface. It intentionally does **not** enable live
API execution:

* No provider client is imported, instantiated, or called here.
* No network, model, MCP, tool, or browser call is made.
* Status is assembled only from configuration and environment *presence*.

Secret handling: key status is boolean/categorical only. Raw environment values
(API keys, secrets) are never returned by the JSON endpoint and never rendered
in HTML. Only ``present`` / ``missing`` / ``unknown`` categories are surfaced.

The console is mounted behind the shared dashboard auth/CSRF middleware (see
``alpha/webapp/routes/auth.py``) under the protected ``/dashboard`` prefix, so
it is fail-closed: it is only reachable when the dashboard is enabled with a
non-default password and an explicit signing secret, and only for an
authenticated session.
"""

from __future__ import annotations

import html
import os
from pathlib import Path
from typing import Any, Dict, List, Mapping

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

from alpha.webapp import operator_console_artifacts as artifacts

router = APIRouter()

ROUTE = "/dashboard/operator-console"
STATUS_ROUTE = "/dashboard/operator-console/status"

# ---------------------------------------------------------------------------
# Boundary text. These strings are asserted by tests and must appear verbatim
# in the rendered console so an operator immediately understands the mode and
# the honesty/evidence boundaries.
# ---------------------------------------------------------------------------
LOCAL_FIRST_TEXT = "Local-first operator console"
LIVE_DISABLED_TEXT = "Live provider calls are disabled in this MVP"
ARTIFACT_BOUNDARY_TEXT = (
    "Preflight and capture outputs are structural support artifacts, not "
    "answer-quality, benchmark, readiness, or superiority evidence"
)
NO_KEYS_TEXT = "No API keys are displayed"
CLAIM_BOUNDARY_TEXT = (
    "No benchmark, readiness, production, provider-validation, or "
    "superiority evidence is presented here"
)

# Portable behavior-contract file. We only check for its presence and list
# well-known high-level surface labels. We never parse or expose private
# chain-of-thought or the file's internal prompt content.
_PORTABLE_CONTRACT_PATH = "alpha_solver_portable.py"
_PORTABLE_CONTRACT_SURFACES = (
    "SolverEnvelope",
    "SAFE-OUT",
    "confidence",
    "route/expert trace",
    "local-output honesty",
    "Substantive Lift",
)

# Environment variables inspected for *presence* only. Values are never read
# into any response.
_PROVIDER_ENV = "MODEL_PROVIDER"
_EMERGENCY_STOP_ENV = "ALPHA_PROVIDER_EMERGENCY_STOP"
_LIVE_PREVIEW_ENV = "ALPHA_LIVE_PREVIEW_ENABLED"
_COST_CAP_ENVS = (
    "ALPHA_PROVIDER_MAX_COST_USD",
    "ALPHA_PROVIDER_MAX_INPUT_TOKENS",
    "ALPHA_PROVIDER_MAX_OUTPUT_TOKENS",
    "ALPHA_PROVIDER_MAX_REQUESTS",
)
# Provider credential env var names surfaced as present/missing only. The names
# are shown; the values never are.
_KEY_ENVS = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY")

_TRUTHY = {"1", "true", "yes", "on"}


def _escape(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _truthy_env(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in _TRUTHY


def _key_presence(name: str) -> str:
    """Return only a categorical presence marker, never the value."""

    raw = os.getenv(name)
    if raw is None:
        return "missing"
    return "present" if raw.strip() else "missing"


def _contract_present() -> bool:
    root = Path(__file__).resolve().parents[3]
    return (root / _PORTABLE_CONTRACT_PATH).is_file()


def _cost_caps_status() -> str:
    present = sum(1 for name in _COST_CAP_ENVS if os.getenv(name, "").strip())
    if present == 0:
        return "not configured"
    if present == len(_COST_CAP_ENVS):
        return "configured"
    return "partially configured"


def build_console_status() -> Dict[str, Any]:
    """Assemble the read-only operator console status payload.

    Pure function over configuration and environment *presence*. Performs no
    provider, network, model, or tool call, and never reads a secret value into
    the returned structure.
    """

    provider = os.getenv(_PROVIDER_ENV, "local").strip().lower() or "local"
    local_artifacts = artifacts.build_artifact_status()

    return {
        "console": {
            "title": "Alpha Solver Operator Console",
            "mode": "local-first",
            "live_provider_calls": "disabled",
            "claim_boundary": (
                "no benchmark/readiness/superiority evidence"
            ),
            "boundary_notes": [
                LOCAL_FIRST_TEXT,
                LIVE_DISABLED_TEXT,
                NO_KEYS_TEXT,
            ],
        },
        "portable_contract": {
            "present": _contract_present(),
            "source_path": _PORTABLE_CONTRACT_PATH,
            "contract_mode": "portable standalone behavior contract",
            "surfaces": list(_PORTABLE_CONTRACT_SURFACES),
            "note": (
                "High-level surfaces only. Private chain-of-thought is not "
                "parsed or exposed and this console does not modify the "
                "contract file."
            ),
        },
        "run_setup": {
            "run_modes": [
                {"id": "dry-run", "available": True},
                {"id": "local-only", "available": True},
                {"id": "chatgpt-copy-paste", "available": True},
                {"id": "live-provider", "available": False},
            ],
            "live_run_button_enabled": False,
            "note": (
                "This MVP does not enable live API execution. "
                + LIVE_DISABLED_TEXT
                + "."
            ),
        },
        "route_trace": {
            "route": "not run yet",
            "confidence": "not run yet",
            "safe_out_state": "not run yet",
            "expert_team": "not run yet",
            "shortlist": "not run yet",
            "diagnostics": "not run yet",
            "note": "No solve has run from this console; fields are placeholders.",
        },
        "provider_gate": {
            "configured_provider": provider,
            "live_provider_calls": "disabled",
            "console_calls_providers": False,
            "emergency_stop": (
                "engaged" if _truthy_env(_EMERGENCY_STOP_ENV) else "not engaged"
            ),
            "cost_caps": _cost_caps_status(),
            "live_preview_surface": (
                "enabled" if _truthy_env(_LIVE_PREVIEW_ENV) else "disabled"
            ),
            "key_status": {name: _key_presence(name) for name in _KEY_ENVS},
            "note": NO_KEYS_TEXT + ". Key status is present/missing only.",
        },
        "preflight_capture": {
            "workflows": [
                {
                    "id": "anchor-preflight",
                    "command": (
                        "python scripts/operator_run_capture.py anchor-preflight "
                        "--case-packet <case_packet.json>"
                    ),
                },
                {
                    "id": "lift-preflight",
                    "command": (
                        "python scripts/operator_run_capture.py lift-preflight "
                        "--capture <capture.json>"
                    ),
                },
                {
                    "id": "init-capture",
                    "command": (
                        "python scripts/operator_run_capture.py init "
                        "--case-packet <case_packet.json> --out <capture.json>"
                    ),
                },
                {
                    "id": "validate-capture",
                    "command": (
                        "python scripts/operator_run_capture.py validate "
                        "--capture <capture.json>"
                    ),
                },
                {
                    "id": "export-evidence-packet",
                    "command": (
                        "python scripts/operator_run_capture.py export "
                        "--capture <capture.json> --out <packet.json>"
                    ),
                },
            ],
            "docs": "docs/OPERATOR_RUN_CAPTURE.md",
            "note": ARTIFACT_BOUNDARY_TEXT + ".",
        },
        "evidence_receipt": {
            "receipt_id": "not generated yet",
            "export_digest": "not generated yet",
            "validation_status": "not run yet",
            "note": (
                "Receipts are structural support artifacts, not answer-quality "
                "proof."
            ),
        },
        "local_artifacts": local_artifacts,
    }


# ---------------------------------------------------------------------------
# Rendering. All rendering runs through ``_escape`` so no assembled value can
# inject markup, and the status payload never carries a secret value.
# ---------------------------------------------------------------------------
def _kv_rows(pairs: Mapping[str, Any]) -> str:
    return "".join(
        f'<div class="kv"><dt>{_escape(key)}</dt>'
        f"<dd>{_escape(value)}</dd></div>"
        for key, value in pairs.items()
    )


def _list_items(items: List[Any]) -> str:
    return "".join(f"<li>{_escape(item)}</li>" for item in items)


def _render_page(status: Mapping[str, Any]) -> str:
    console = status["console"]
    contract = status["portable_contract"]
    run_setup = status["run_setup"]
    trace = status["route_trace"]
    gate = status["provider_gate"]
    capture = status["preflight_capture"]
    receipt = status["evidence_receipt"]

    run_mode_rows = "".join(
        '<li class="mode">'
        f'<span class="mode-id">{_escape(mode["id"])}</span>'
        f'<span class="badge {"ok" if mode["available"] else "off"}">'
        f'{"available" if mode["available"] else "disabled"}</span>'
        "</li>"
        for mode in run_setup["run_modes"]
    )

    key_rows = "".join(
        f'<div class="kv"><dt>{_escape(name)}</dt>'
        f'<dd><span class="badge {"ok" if state == "present" else "muted"}">'
        f"{_escape(state)}</span></dd></div>"
        for name, state in gate["key_status"].items()
    )

    workflow_rows = "".join(
        "<li class=\"workflow\">"
        f'<code class="wf-id">{_escape(item["id"])}</code>'
        f'<pre class="wf-cmd">{_escape(item["command"])}</pre>'
        "</li>"
        for item in capture["workflows"]
    )

    contract_badge = "present" if contract["present"] else "missing"

    # Local artifact status (read-only; counts/states/digests only).
    local = status["local_artifacts"]
    no_artifacts_msg = local["no_artifacts_message"]
    cap = local["capture"]
    pkt = local["evidence_packet"]
    anchor = local["anchor_preflight"]
    lift = local["lift_preflight"]

    def _state_badge(state: Any) -> str:
        good = {"structurally_valid", "export_ready", "digest_valid", "present"}
        bad = {"invalid_json", "invalid_structure", "digest_invalid"}
        text = str(state)
        cls = "ok" if text in good else "off" if text in bad else "muted"
        return f'<span class="badge {cls}">{_escape(text)}</span>'

    def _no_artifacts_note() -> str:
        return f'<p class="note">{_escape(no_artifacts_msg)}</p>'

    # Route and Trace: local capture counts + route metadata presence count.
    if cap.get("state") in {"structurally_valid", "export_ready"}:
        cap_counts = cap.get("counts", {})
        trace_artifact_html = _kv_rows(
            {
                "captured (local)": cap_counts.get("captured", 0),
                "excluded (local)": cap_counts.get("excluded", 0),
                "pending (local)": cap_counts.get("pending", 0),
                "route metadata present": cap.get("route_metadata_present_count", 0),
            }
        )
    elif cap.get("state") == "missing":
        trace_artifact_html = _no_artifacts_note()
    else:
        trace_artifact_html = (
            f'<div class="kv"><dt>local capture</dt><dd>'
            f'{_state_badge(cap.get("state"))}</dd></div>'
        )

    # Preflight and Capture: whether reports exist and need attention.
    def _preflight_rows(label: str, summary: Mapping[str, Any]) -> str:
        state = summary.get("state")
        if state == "present":
            return (
                f'<div class="kv"><dt>{_escape(label)}</dt><dd>'
                f'{_state_badge(state)} · needs attention: '
                f'{_escape(summary.get("needs_attention_count", 0))}</dd></div>'
            )
        return (
            f'<div class="kv"><dt>{_escape(label)}</dt><dd>'
            f'{_state_badge(state)}</dd></div>'
        )

    preflight_artifact_html = _preflight_rows(
        "anchor preflight report", anchor
    ) + _preflight_rows("lift preflight report", lift)

    # Evidence and Receipt: root, capture/packet states, digest, id, counts.
    pkt_counts = pkt.get("counts", {})
    evidence_artifact_html = _kv_rows(
        {
            "artifact root": local["artifact_root"],
            "local artifacts detected": "yes" if local["detected"] else "no",
        }
    ) + (
        f'<div class="kv"><dt>capture state</dt><dd>'
        f'{_state_badge(cap.get("state"))}</dd></div>'
        f'<div class="kv"><dt>evidence packet state</dt><dd>'
        f'{_state_badge(pkt.get("state"))}</dd></div>'
        + _kv_rows(
            {
                "packet id": pkt.get("packet_id") or "—",
                "content digest": pkt.get("content_digest") or "—",
                "packet captured": pkt_counts.get("captured", "—"),
                "packet excluded": pkt_counts.get("excluded", "—"),
                "packet total": pkt_counts.get("total", "—"),
            }
        )
    )
    boundary_html = "".join(
        f"<li>{_escape(text)}</li>" for text in local["boundaries"]
    )
    evidence_no_artifacts = "" if local["detected"] else _no_artifacts_note()

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Alpha Solver · Operator Console</title>
    <style>
      :root {{ color-scheme: light dark; font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.5; }}
      body {{ margin: 0; min-height: 100vh; background: radial-gradient(circle at top, #f6f8ff, #e4e8f4); color: #1d2038; }}
      .container {{ max-width: 1120px; margin: 0 auto; padding: 2.5rem 1.25rem 4rem; }}
      h1 {{ margin: 0 0 0.35rem; font-size: 1.75rem; }}
      .subtitle {{ color: #565b8f; margin: 0 0 1.25rem; font-weight: 600; }}
      .banner {{ border: 1px solid #c7d2fe; background: rgba(238, 242, 255, 0.9); border-radius: 14px; padding: 1rem 1.15rem; color: #30365f; margin-bottom: 1.5rem; }}
      .banner ul {{ margin: 0.5rem 0 0; padding-left: 1.1rem; }}
      .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.1rem; align-items: start; }}
      .card {{ background: rgba(255, 255, 255, 0.94); border-radius: 16px; padding: 1.15rem 1.25rem; box-shadow: 0 18px 55px rgba(31, 35, 71, 0.08); min-width: 0; }}
      .card h2 {{ margin: 0 0 0.75rem; font-size: 1.08rem; }}
      .kv {{ display: grid; grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr); gap: 0.4rem 0.75rem; padding: 0.25rem 0; border-bottom: 1px solid rgba(86, 97, 246, 0.1); }}
      dt {{ color: #565b8f; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.03em; text-transform: uppercase; margin: 0; }}
      dd {{ margin: 0; font-weight: 600; overflow-wrap: anywhere; }}
      ul {{ margin: 0; padding-left: 1.1rem; }}
      li {{ margin: 0.2rem 0; overflow-wrap: anywhere; }}
      li.mode, li.workflow {{ list-style: none; }}
      ul.modes, ul.workflows {{ padding-left: 0; }}
      .mode {{ display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; padding: 0.35rem 0; border-bottom: 1px solid rgba(86, 97, 246, 0.1); }}
      .mode-id {{ font-weight: 700; }}
      .badge {{ display: inline-block; border-radius: 999px; padding: 0.12rem 0.6rem; font-size: 0.76rem; font-weight: 800; }}
      .badge.ok {{ background: rgba(16, 185, 129, 0.16); color: #047857; }}
      .badge.off {{ background: rgba(244, 63, 94, 0.14); color: #9f1239; }}
      .badge.muted {{ background: rgba(100, 116, 139, 0.16); color: #475569; }}
      .surfaces li {{ font-weight: 600; }}
      .workflow {{ padding: 0.4rem 0; border-bottom: 1px solid rgba(86, 97, 246, 0.1); }}
      .wf-id {{ font-weight: 800; color: #3730a3; }}
      pre.wf-cmd {{ white-space: pre-wrap; overflow-wrap: anywhere; background: #111827; color: #e5e7eb; border-radius: 10px; padding: 0.55rem 0.7rem; margin: 0.35rem 0 0; font-size: 0.82rem; }}
      .note {{ color: #5f668f; font-size: 0.85rem; margin: 0.65rem 0 0; }}
      .disabled-btn {{ margin-top: 0.75rem; border: 0; border-radius: 999px; padding: 0.6rem 1.15rem; font: inherit; font-weight: 700; color: #475569; background: rgba(100, 116, 139, 0.16); cursor: not-allowed; }}
      a.status-link {{ display: inline-block; margin-top: 0.75rem; color: #4f46e5; font-weight: 700; }}
    </style>
  </head>
  <body>
    <main class="container">
      <h1>{_escape(console["title"])}</h1>
      <p class="subtitle">{_escape(LOCAL_FIRST_TEXT)}</p>
      <section class="banner" aria-label="Operator console mode and boundaries">
        <strong>{_escape(LIVE_DISABLED_TEXT)}.</strong>
        <ul>
          <li>Mode: {_escape(console["mode"])}</li>
          <li>Live provider calls: {_escape(console["live_provider_calls"])}</li>
          <li>Claim boundary: {_escape(console["claim_boundary"])}</li>
          <li>{_escape(CLAIM_BOUNDARY_TEXT)}.</li>
          <li>{_escape(NO_KEYS_TEXT)}.</li>
          {boundary_html}
        </ul>
      </section>

      <div class="cards">
        <article class="card" id="card-portable-contract">
          <h2>Portable Contract Status</h2>
          {_kv_rows({
              "present": contract_badge,
              "source path": contract["source_path"],
              "contract mode": contract["contract_mode"],
          })}
          <p class="note">Surfaces (high-level only):</p>
          <ul class="surfaces">{_list_items(contract["surfaces"])}</ul>
          <p class="note">{_escape(contract["note"])}</p>
        </article>

        <article class="card" id="card-run-setup">
          <h2>Run Setup</h2>
          <p class="note">Prompt input is disabled in this MVP shell.</p>
          <textarea placeholder="Prompt entry is disabled in this MVP" disabled aria-disabled="true" style="width:100%;min-height:70px;border-radius:10px;border:1px solid #cdd5ef;padding:0.6rem;font:inherit;background:rgba(255,255,255,0.6);"></textarea>
          <ul class="modes">{run_mode_rows}</ul>
          <button type="button" class="disabled-btn" disabled aria-disabled="true">Live run (disabled)</button>
          <p class="note">{_escape(run_setup["note"])}</p>
        </article>

        <article class="card" id="card-route-trace">
          <h2>Route and Trace</h2>
          {_kv_rows({
              "route": trace["route"],
              "confidence": trace["confidence"],
              "SAFE-OUT state": trace["safe_out_state"],
              "expert/team": trace["expert_team"],
              "shortlist": trace["shortlist"],
              "diagnostics": trace["diagnostics"],
          })}
          <p class="note">{_escape(trace["note"])}</p>
          <p class="note">Local capture counts (structural only):</p>
          {trace_artifact_html}
        </article>

        <article class="card" id="card-provider-gate">
          <h2>Provider and Cost Gate</h2>
          {_kv_rows({
              "configured provider": gate["configured_provider"],
              "live provider calls": gate["live_provider_calls"],
              "console calls providers": gate["console_calls_providers"],
              "emergency stop": gate["emergency_stop"],
              "cost caps": gate["cost_caps"],
              "live preview surface": gate["live_preview_surface"],
          })}
          <p class="note">Key presence (categorical only):</p>
          {key_rows}
          <p class="note">{_escape(gate["note"])}</p>
        </article>

        <article class="card" id="card-preflight-capture">
          <h2>Preflight and Capture Entry</h2>
          <p class="note">Local workflows (run from a terminal, not from this console):</p>
          <ul class="workflows">{workflow_rows}</ul>
          <p class="note">Docs: {_escape(capture["docs"])}</p>
          <p class="note">{_escape(capture["note"])}</p>
          <p class="note">Local preflight report status:</p>
          {preflight_artifact_html}
        </article>

        <article class="card" id="card-evidence-receipt">
          <h2>Evidence and Receipt</h2>
          {_kv_rows({
              "receipt id": receipt["receipt_id"],
              "export digest": receipt["export_digest"],
              "validation status": receipt["validation_status"],
          })}
          <p class="note">{_escape(receipt["note"])}</p>
          <p class="note">Local artifact status:</p>
          {evidence_artifact_html}
          {evidence_no_artifacts}
          <ul class="surfaces">{boundary_html}</ul>
          <p class="note">{_escape(ARTIFACT_BOUNDARY_TEXT)}.</p>
        </article>
      </div>

      <a class="status-link" href="{STATUS_ROUTE}">Read-only status JSON</a>
    </main>
  </body>
</html>"""


@router.get(ROUTE, response_class=HTMLResponse)
async def operator_console_page() -> HTMLResponse:
    """Render the read-only operator console shell."""

    return HTMLResponse(content=_render_page(build_console_status()))


@router.get(STATUS_ROUTE)
async def operator_console_status() -> JSONResponse:
    """Return the read-only operator console status as JSON.

    The payload is assembled by :func:`build_console_status` and never contains
    a raw secret value.
    """

    return JSONResponse(content=build_console_status())
