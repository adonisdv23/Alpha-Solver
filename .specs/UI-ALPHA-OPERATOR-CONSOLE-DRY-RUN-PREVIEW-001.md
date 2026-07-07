# UI-ALPHA-OPERATOR-CONSOLE-DRY-RUN-PREVIEW-001 · Operator Console Dry-Run Preview

Status: Implemented

Lane: `AOC-B005-DRY-RUN-PREVIEW-001`

## Goal

Add a **display-only** Dry-Run Preview panel to the existing protected,
local-first Operator Console. The console already lists `dry-run` as an available
run mode, but it never explains what dry-run readiness means, what inputs a
dry-run would need, what would be previewed, or why it still is not execution.
This panel answers a single cockpit question: what would a future dry-run prepare,
and what is missing before a separate dry-run execution lane could be considered?

This is a dry-run **preview** lane, not a dry-run **execution** lane. It executes
nothing. It is a status/visibility lane, not a runner lane, not a provider lane,
not a `/v1/solve` lane, not a CLI lane, and not an artifact-mutation lane.

## Motivation

The Run Setup card advertises `dry-run` as an available mode, but the operator has
no way to see what a dry-run would prepare or require. The next cockpit question
is: is dry-run preview available, what input source would a dry-run need, is local
capture present and structurally valid, is an evidence packet present and
self-consistent, are the anchor/lift preflight reports present, are any derived
artifacts stale relative to capture, is provider/live execution still blocked, and
what is explicitly not happening now? This lane answers those from the local
metadata this console already assembles, without adding any execution path.

## Scope

- `alpha/webapp/routes/operator_console.py`: add a new top-level `dry_run_preview`
  status section and a compact "Dry-Run Preview" card.
  - Pure helpers derive everything from the already-assembled, already-safe
    `local_artifacts` and `provider_gate` sub-payloads:
    `_dry_run_input_source_status`, `_dry_run_preflight_status`,
    `_dry_run_freshness_warnings`, `_dry_run_preview_blockers`,
    `_dry_run_preview_readiness`, and `_build_dry_run_preview`. No new input is
    read: no raw artifact content, no secret value, no provider, no CLI, no solve.
  - Fields on `dry_run_preview`: `preview_mode` (`display_only`),
    `dry_run_execution` (`not_enabled`), `would_use` (safe surface names),
    `input_source_status` (`capture_missing` / `capture_invalid` /
    `capture_structurally_valid` / `capture_export_ready`),
    `evidence_packet_status` (the existing packet state: `missing` /
    `invalid_json` / `invalid_structure` / `digest_valid` / `digest_invalid` /
    `digest_unverifiable`), `preflight_status` (`anchor_*` / `lift_*`
    present/missing/invalid), `freshness_warnings` (safe labels drawn only from
    `local_artifacts.freshness.sequence_coherence`), `provider_gate_summary`
    (`live_execution_gate`, `provider_key_status`, `cap_completeness`,
    `live_execution_blockers`), `preview_readiness` (`unavailable` /
    `needs_artifacts` / `preview_ready`), `preview_blockers` (safe labels),
    `boundary`, and `boundary_notes`.
  - The card keeps the disabled live-run button. No POST action, no live-run/
    execute/submit/generate/solve button, and no new endpoint.
- `docs/OPERATOR_CONSOLE.md`: document the panel, define preview readiness in
  operator terms, and preserve the existing no-provider/no-runner/no-secret/
  no-raw/no-readiness/no-validation boundaries.
- `tests/test_operator_console.py`: focused dry-run preview tests.
- `.specs/INDEX.md`: one new row for this spec.

## Non-goals and boundaries

- No dry-run execution. This lane previews prerequisites and missing readiness
  only; it never runs a dry-run.
- No provider, hosted-model, local-model, MCP, tool, browser, or network call; no
  CLI or subprocess execution from the console; no `/v1/solve` call; no call to
  internal solve functions.
- No prompt submission and no generated output. The console does not generate
  route, confidence, SAFE-OUT state, expert trace, shortlist, diagnostics, answer
  text, model output, provider result, billing result, benchmark result, or
  readiness result.
- No credential validation and no provider ping. The provider gate summary reuses
  the existing environment-presence gate; it validates nothing.
- No API pricing lookup and no exact billing or spend calculation.
- No artifact creation, edit, deletion, upload, save, or mutation; no receipt
  store.
- No POST action, no executable action button, and no newly exposed route beyond
  the existing read-only page and status JSON. No page redesign and no new
  dependency.
- No raw or partial API key display, no environment dump, and no raw
  prompt/baseline/routed/route-metadata/system-prompt/provider-payload/full-JSON
  display.
- No change to `alpha_solver_portable.py`, provider runtime, model routing,
  `/v1/solve`, the capture/export/preflight schemas, or the
  `operator_run_capture.py` CLI semantics.
- No scoring, ranking, winner fields, or model-comparison UI.
- The console must not synthesize Alpha Solver runtime fields when no solve has
  run from the console: no route, expert trace, confidence, SAFE-OUT state,
  shortlist, SolverEnvelope output, provider model choice, provider result,
  billing result, benchmark result, readiness result, generated answer, or
  dry-run output is invented.

## Preview-only boundary

The Dry-Run Preview panel is display-only. It previews what a future dry-run would
prepare or require; it does not run a dry-run and does not enable one.
`preview_mode` is always `display_only` and `dry_run_execution` is always
`not_enabled`. A future dry-run execution lane must be separately authorized.

## No-execution / no-solve / no-provider / no-artifact-mutation / no-runtime-output boundary

This lane adds no execution path. It performs no provider/model/MCP/network/
browser/CLI/subprocess call, no `/v1/solve` call, no internal solve-function call,
no dry-run execution, and no prompt submission. It creates, edits, deletes,
uploads, and mutates no artifact, and stores no receipt. It generates no route,
confidence, SAFE-OUT, expert trace, shortlist, diagnostics, answer text, model
output, provider result, billing result, benchmark result, or readiness result. It
displays no raw or partial secret and no raw prompt/output/route-metadata/provider
payload.

## No-readiness / no-validation / no-benchmark / no-superiority boundary

`preview_readiness` means only whether the preview has enough local metadata to
explain the next step. It is not answer quality, route readiness, provider
readiness, production readiness, validation, benchmark evidence, billing accuracy,
or superiority evidence. A `preview_ready` state does not claim any of those and
does not authorize execution. Evidence-packet `digest_valid` is packet
self-integrity only, not freshness or answer quality. Freshness warnings are local
filesystem metadata only. The provider gate summary reports that live execution is
blocked; it does not claim provider readiness and does not authorize live
execution.

## Code Targets

- `alpha/webapp/routes/operator_console.py`
- `tests/test_operator_console.py`
- `docs/OPERATOR_CONSOLE.md`
- `.specs/INDEX.md`
- `.specs/UI-ALPHA-OPERATOR-CONSOLE-DRY-RUN-PREVIEW-001.md`

## Test Plan

`tests/test_operator_console.py`: the status JSON includes the new
`dry_run_preview` section; preview mode is `display_only`; dry-run execution is
`not_enabled`; the live-run button stays disabled; no POST/action route is added;
missing capture and invalid capture each produce safe preview blockers and still
render; structurally valid and export-ready capture produce a local input status
without exposing raw prompts or outputs; a missing evidence packet produces a safe
blocker; a digest-valid packet is treated as self-integrity only (not
quality/readiness); digest-invalid and digest-unverifiable states produce safe
warnings/blockers; missing anchor/lift reports produce a safe blocker while present
reports are shown as local metadata; stale evidence-packet/anchor/lift artifacts vs
capture each produce a safe freshness warning; the provider gate summary is
included but live execution stays blocked; complete provider/cap configuration does
not enable dry-run execution; fake API keys never appear in HTML, JSON, or reprs;
raw prompt/baseline/routed/route-metadata/system-prompt/provider-payload sentinels
never appear; provider client constructors patched to raise still allow both routes
to return; a source scan confirms no provider client, httpx, requests, subprocess,
socket, browser, MCP, CLI, or solve imports are introduced in the route module; the
UI contains the dry-run preview boundary text; the UI contains no misleading
execution/claim language; and existing provider gate, artifact status, and freshness
surfaces persist alongside the panel.

## Validation

- `python -m pytest tests/test_operator_console.py -q`
- `python -m pytest tests/test_operator_console.py tests/test_operator_run_capture.py tests/test_api_endpoints.py -q`
- `python -m pytest -q`
- `ruff check alpha/webapp/routes/operator_console.py tests/test_operator_console.py`
- `python scripts/check_narrative_claim_safety.py docs/OPERATOR_CONSOLE.md .specs/UI-ALPHA-OPERATOR-CONSOLE-DRY-RUN-PREVIEW-001.md`

## Definition of Done

The route addition, docs, tests, and this spec merged; all validation commands
pass; the dry-run preview reads only the existing safe `local_artifacts` and
`provider_gate` sub-payloads; `preview_mode` stays `display_only` and
`dry_run_execution` stays `not_enabled` under every configuration; the live-run
button stays disabled; no POST/action route or new endpoint is added; no provider,
model, MCP, network, browser, CLI, subprocess, `/v1/solve`, internal solve, or
dry-run execution path is added; no credential is validated and no provider is
pinged; no exact billing or spend is claimed; no artifact is mutated; no raw or
partial secret and no raw prompt/output/route-metadata/provider payload is
displayed; and no schema is changed. Reporting `preview_ready` means only that the
local metadata is complete enough to explain the next step; it is not
answer-quality, validation, production, provider readiness, benchmark, billing, or
superiority evidence, and it does not authorize live or dry-run execution, which
remains a separate future lane.
