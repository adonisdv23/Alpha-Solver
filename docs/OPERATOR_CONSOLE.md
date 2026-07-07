# Alpha Solver Operator Console

Lane: `UI-ALPHA-OPERATOR-CONSOLE-MVP-001`

A protected, local-first operator console shell. It is a read-only cockpit of
status cards, not a runner and not a public dashboard. Opening it is a status
read: it starts no run, calls no provider, and spends no API credits.

## What it is

The console summarizes, on one protected page, the answers to:

- What mode am I in? (**local-first**, live provider calls **disabled**.)
- Which contract/status surfaces exist?
- Where will route, SAFE-OUT, confidence, expert/team, shortlist, preflight,
  capture, and evidence receipts appear once wired?
- What stays blocked until future lanes?

**Live provider calls are disabled in this MVP.** The console does not enable
live API execution. The live-run control is rendered disabled.

## How to reach it

The console mounts behind the shared dashboard auth/CSRF middleware, under the
protected `/dashboard` prefix, and is fail-closed exactly like the bundled
expert-preview page. It is served only when both of these are set:

- a non-default `ALPHA_DASHBOARD_PASSWORD`, and
- an explicit `ALPHA_DASHBOARD_SECRET_KEY`.

When either is missing the dashboard is not mounted and the console routes
return 404. When mounted, an unauthenticated `GET` redirects to `/login`.

- Page: `GET /dashboard/operator-console`
- Read-only status JSON: `GET /dashboard/operator-console/status`

## Cards

1. **Operator Console Header** — title, `local-first` mode, live provider calls
   disabled, and the claim boundary.
2. **Portable Contract Status** — that `alpha_solver_portable.py` is present,
   its source path, that it is a portable standalone behavior contract, and a
   high-level surface list (SolverEnvelope, SAFE-OUT, confidence, route/expert
   trace, local-output honesty, Substantive Lift). Private chain-of-thought is
   not parsed or exposed, and the contract file is not modified.
3. **Run Setup** — a disabled prompt input and the visible run modes (dry-run,
   local-only, ChatGPT copy/paste, and live-provider shown disabled). The
   live-run button is disabled; this MVP does not enable live API execution.
4. **Route and Trace** — placeholder fields for route, confidence, SAFE-OUT
   state, expert/team, shortlist, and diagnostics. They read "not run yet"; the
   console does not invent route output or imply a solve ran.
5. **Provider and Cost Gate** — the configured provider, that the console does
   not call providers, emergency-stop and cost-cap status, the live-preview
   surface state, and API key **presence** only (`present` / `missing`). No raw
   or partial key values are shown.
6. **Preflight and Capture Entry** — the local workflows (anchor-preflight,
   lift-preflight, init capture, validate capture, export evidence packet) with
   command snippets and a docs pointer. These run from a terminal, not from the
   console.
7. **Evidence and Receipt** — placeholders for a future receipt id, export
   digest, and validation status.

## Secret handling

- Key status is boolean/categorical only (`present` / `missing` / `unknown`).
- **No API keys are displayed.** Raw environment values are never returned by
  the JSON endpoint and never rendered in HTML.

## Boundaries

- No provider, hosted-model, local-model, MCP, tool, browser, or network call
  is made by the console.
- The console does not change model routing, provider runtime, `/v1/solve`
  execution, or the capture/export schemas, and it does not change the
  `operator_run_capture.py` CLI.
- Preflight and capture outputs are structural support artifacts, not
  answer-quality, benchmark, readiness, or superiority evidence. Reporting a
  surface as present means only that the named surface exists in the codebase;
  it does not claim any answer-quality result. This page is not a benchmark,
  readiness, production, or superiority claim, and it does not validate the
  product.
