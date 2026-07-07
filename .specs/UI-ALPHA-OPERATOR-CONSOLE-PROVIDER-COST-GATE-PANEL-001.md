# UI-ALPHA-OPERATOR-CONSOLE-PROVIDER-COST-GATE-PANEL-001 · Operator Console Provider, Model, and Cost Gate Panel

Status: Implemented

## Goal

Expand the existing protected local-first Operator Console Provider and Cost Gate
card into a clearer **display-only** safety panel that tells the operator whether
live-provider execution remains blocked and why. This is a status and
safety-gate visibility lane. It is not a live-provider lane, not a cost-metering
lane, not a credential-validation lane, not a smoke-test lane, not a
workbench-action lane, and not a `/v1/solve` lane.

## Motivation

The current Provider and Cost Gate card is shallow: it shows that provider calls
are disabled and whether caps are configured, partially configured, or missing,
but it does not clearly explain whether live-provider execution remains blocked,
which safety gates are missing, or what would need to be present before any
future live lane could even be considered. The next cockpit question is: can
live execution even be considered later, and if not, what safety gate is missing?
This lane answers that from configuration presence only, without enabling any
execution path.

## Scope

- `alpha/webapp/routes/operator_console.py`: expand the `provider_gate` payload
  and rendered card into a display-only gate-readiness panel.
  - New safe derived fields on `provider_gate`: `provider_mode_label`,
    `cap_status` (per cap `present`/`missing`), `cap_completeness`
    (`none_configured` / `partially_configured` / `configured`),
    `cost_cap_status` (`missing` / `present`), `token_request_cap_status`
    (`missing` / `partial` / `present`), `live_execution_gate` (always
    `blocked`), `live_execution_blockers` (safe blocker labels), and
    `gate_boundary` (display-only note). Existing fields
    (`configured_provider`, `live_provider_calls`, `console_calls_providers`,
    `emergency_stop`, `live_preview_surface`, `key_status`, `cost_caps`, `note`)
    are preserved.
  - Pure helpers derive everything from environment *presence* and truthiness
    only: `_cap_status`, `_cap_completeness`, `_cost_cap_status`,
    `_token_request_cap_status`, `_provider_mode_label`,
    `_live_execution_blockers`, and `_build_provider_gate`. No secret value is
    read, no credential is validated, and no provider is contacted.
  - The card keeps the disabled live-run button, adds a compact "Live Execution
    Gate" subsection (gate result, cap completeness, cost cap, token/request
    caps), a blockers list, per-cap presence rows, key presence rows, and the
    gate boundary statements. No POST action, no executable live-run button, no
    new endpoint.
- `docs/OPERATOR_CONSOLE.md`: document the expanded panel, define each visible
  gate state in operator terms, and state that caps are configured limits (not
  billing truth), key status is categorical only, and complete configuration
  does not authorize live execution.
- `tests/test_operator_console.py`: focused provider/cost gate tests.
- `.specs/INDEX.md`: one new row for this spec.

## Non-goals and boundaries

- No provider, hosted-model, local-model, MCP, tool, browser, network, or
  `/v1/solve` call; no CLI or subprocess execution from the console.
- No provider ping and no credential validation. Key and cap status are
  environment *presence* only.
- No API pricing lookup, exact billing, or spend calculation. Caps are
  configured limits, not billing accuracy or spend verification.
- No POST action, no executable live-run button, no newly exposed route beyond
  the existing read-only status JSON, and no page redesign.
- No raw or partial API key display, no environment dump, and no raw
  prompt/output/route-metadata/provider-payload/full-JSON display.
- No artifact creation, edit, deletion, upload, or mutation; no receipt store; no
  workbench action buttons.
- No change to `alpha_solver_portable.py`, provider runtime, model routing,
  `/v1/solve` execution, the capture/export/preflight schemas, or the
  `operator_run_capture.py` CLI semantics.
- No scoring, ranking, winner fields, or model-comparison UI.
- The console must not synthesize Alpha Solver runtime fields when no solve has
  run from the console: no route, expert trace, confidence, SAFE-OUT state,
  shortlist, SolverEnvelope output, provider model choice, provider result,
  billing result, benchmark result, or readiness result is invented.

## Display-only provider/cost boundary

Provider and cost gate status is configuration visibility only. It does not imply
route confidence, SAFE-OUT confidence, answer quality, validation, production
readiness, public/API readiness, autonomous readiness, model superiority,
provider readiness, benchmark evidence, or exact billing accuracy. Environment
presence is not credential validity, and a configured cap is not billing truth.

## No-execution / no-secret / no-billing-claim / no-readiness boundary

This lane adds no execution path. It performs no provider/model/MCP/network/
browser/CLI/subprocess call, no `/v1/solve` call, no provider ping, and no
credential validation. It displays no raw or partial secret and no raw
prompt/output/route metadata/provider payload. It performs no pricing lookup and
no exact spend calculation. `live_execution_gate` is always `blocked`: complete
cap or key configuration does not authorize live execution, which remains blocked
unless a separate future live-provider lane explicitly authorizes it. A complete
display-only gate is not provider readiness, production readiness, validation,
benchmark evidence, or superiority evidence.

## Code Targets

- `alpha/webapp/routes/operator_console.py`
- `tests/test_operator_console.py`
- `docs/OPERATOR_CONSOLE.md`
- `.specs/INDEX.md`

## Test Plan

`tests/test_operator_console.py`: the status JSON includes the expanded
`provider_gate` fields; the default gate stays blocked and display-only; live
provider calls stay disabled and the live-run button stays disabled; emergency
stop engaged appears as a blocker; a missing provider key appears as a safe
blocker without displaying any value; a present key reports `present` only (no
raw or partial value); a missing cost cap appears as a safe blocker; partial cap
configuration reports `partially_configured` / `partial`; complete cap
configuration reports `configured` / `present` yet stays blocked; live-preview
enabled does not by itself permit execution; the gate never validates
credentials and never calls provider clients; provider client constructors
patched to raise still allow both routes to return; fake API keys never appear
in HTML, JSON, or reprs; the status JSON contains no raw environment values for
any inspected env var; the rendered HTML contains the gate boundary text; a
source scan confirms no provider/network/subprocess/browser/CLI execution
imports in the route module; no scoring/ranking/winner/billing/model-comparison
claim language appears in the gate UI; and existing artifact status and freshness
surfaces persist alongside the gate.

## Validation

- `python -m pytest tests/test_operator_console.py -q`
- `python -m pytest tests/test_operator_console.py tests/test_operator_run_capture.py tests/test_api_endpoints.py -q`
- `python -m pytest -q`
- `ruff check alpha/webapp/routes/operator_console.py tests/test_operator_console.py`
- `python scripts/check_narrative_claim_safety.py docs/OPERATOR_CONSOLE.md .specs/UI-ALPHA-OPERATOR-CONSOLE-PROVIDER-COST-GATE-PANEL-001.md`

## Definition of Done

The route expansion, docs, tests, and this spec merged; all validation commands
pass; the provider/cost gate reads environment presence only; `live_execution_gate`
stays `blocked` under every configuration; no credential is validated, no provider
is contacted, no raw or partial secret is displayed, no raw env value is exposed,
and no schema is changed. Reporting a key or cap as `present`, or a gate as
complete, means only that the named environment variable is set; it is not
credential validity, billing truth, provider readiness, production readiness,
validation, benchmark, or superiority evidence, and it does not authorize live
execution.
