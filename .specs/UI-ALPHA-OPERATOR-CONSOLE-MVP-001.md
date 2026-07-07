# UI-ALPHA-OPERATOR-CONSOLE-MVP-001 · Alpha Solver Operator Console Shell (MVP)

Status: Implemented

## Goal

Give the operator a protected, local-first console shell that exposes Alpha
Solver contract/status surfaces as a cockpit of read-only cards, so an operator
can open one protected page and immediately understand the current mode,
which contract/status surfaces exist, and what stays blocked until future
lanes — without spending API credits and without weakening the honesty or
evidence boundaries.

## Motivation

The bundled dashboard mounts login plus the supervised expert-preview page, but
there is no single read-only surface that summarizes the local-first operating
mode, the portable behavior contract's presence, the provider/cost gate state,
and the existing capture/preflight entry points. Operators had to read code and
docs to answer "what mode am I in, are live providers off, and where will
route/SAFE-OUT/confidence/receipts appear." This lane adds that summary as a
protected shell. It reports status only; it starts no run and calls no provider.

## Scope

- `alpha/webapp/routes/operator_console.py`: read-only route module mounted
  under the protected `/dashboard` prefix.
  - `GET /dashboard/operator-console` renders an HTML cockpit of seven cards:
    header, portable contract status, run setup, route/trace, provider/cost
    gate, preflight/capture entry, and evidence/receipt.
  - `GET /dashboard/operator-console/status` returns the same information as
    read-only JSON.
  - `build_console_status()` assembles the payload purely from configuration
    and environment *presence*. It performs no provider, network, model, or
    tool call and never reads a secret value into the returned structure.
- `service/app.py`: include the operator console router in `_mount_dashboard`
  alongside auth and expert-preview, so the console inherits the same
  fail-closed mount (non-default `ALPHA_DASHBOARD_PASSWORD` plus explicit
  `ALPHA_DASHBOARD_SECRET_KEY`) and session/CSRF middleware.
- `docs/OPERATOR_CONSOLE.md`: what the console is, how to reach it, the
  no-provider boundary, and the honesty/evidence boundary.
- Tests in `tests/test_operator_console.py`.

## Non-goals and boundaries

- Live provider calls stay disabled. This shell does not enable live API
  execution; the live-run button is rendered disabled.
- No provider, hosted-model, local-model, MCP, tool, browser, or network call.
  No provider client is imported, instantiated, or executed by this module.
- No API key storage. Key status is boolean/categorical (`present` / `missing`
  / `unknown`) only; raw environment values are never returned by the JSON
  endpoint and never rendered in HTML.
- No change to `alpha_solver_portable.py` behavior. The portable contract is
  read for presence only; private chain-of-thought is not parsed or exposed.
- No change to provider runtime, model routing, `/v1/solve` execution, or the
  capture/export schemas. No change to `operator_run_capture.py` CLI semantics.
- No scoring, ranking, winner fields, blind labels, source maps, identity maps,
  A/B identity keys, or model-comparison UI.
- No benchmark, readiness, production, provider-validation, local-model, or
  superiority claims. Preflight/capture outputs are described as structural
  support artifacts, not answer-quality evidence.

## Code Targets

- `alpha/webapp/routes/operator_console.py`
- `service/app.py`
- `docs/OPERATOR_CONSOLE.md`
- `tests/test_operator_console.py`

## Test Plan

`tests/test_operator_console.py`: the page and status routes are registered on
the real app and on a freshly mounted app; both are protected (a logged-out GET
redirects to `/login`) and are not served by an unmounted app; an authenticated
page renders all seven cards and the required boundary text; the live-run
button is disabled; the status JSON has the expected sections with
`live_provider_calls` disabled and `live_run_button_enabled` false; key status
is categorical only; a fake secret placed in the environment never appears in
the HTML or JSON (and `build_console_status()` never embeds it); and rendering
never constructs or executes a provider client (the module references no
provider client class).

## Validation

- `python -m pytest tests/test_operator_console.py -q`
- `python -m pytest tests/ui/test_expert_preview_real_app.py tests/ui/test_auth.py -q`
- `python -m pytest tests/test_operator_run_capture.py -q`
- `python -m pytest tests/test_api_endpoints.py -q`
- `python -m pytest -q`
- `python scripts/check_narrative_claim_safety.py docs/OPERATOR_CONSOLE.md`
- `python scripts/check_narrative_claim_safety.py .specs/UI-ALPHA-OPERATOR-CONSOLE-MVP-001.md`
- `ruff check service alpha scripts tests`

## Definition of Done

The console route module, app wiring, docs, tests, and this spec merged; all
validation commands pass; the console is reachable only behind the fail-closed
`/dashboard` auth mount; live provider calls stay disabled; no raw secret is
exposed; and no provider-call path is exercised. Opening the console is a status
read, not a run: it presents no benchmark, readiness, production, or superiority
evidence, and reporting a surface as present means only that the named surface
exists in the codebase, not that any answer-quality judgment has been made.
