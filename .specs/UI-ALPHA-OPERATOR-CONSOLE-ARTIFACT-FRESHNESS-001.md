# UI-ALPHA-OPERATOR-CONSOLE-ARTIFACT-FRESHNESS-001 · Operator Console Artifact Freshness and Sequence Coherence

Status: Implemented

## Goal

Extend the protected, read-only Operator Console so the existing local artifact
status cards also show read-only temporal metadata and simple
dependency-coherence warnings for the four fixed local artifacts introduced by
`UI-ALPHA-OPERATOR-CONSOLE-LOCAL-ARTIFACT-STATUS-001`. This lane infers
freshness from local filesystem modified-time metadata and the existing safe
summaries only. It executes no workflow, provider, model, `/v1/solve`, MCP,
browser automation, network call, or CLI command, and it changes no artifact and
no schema.

## Motivation

After the local-artifact-status lane the console can show whether local
artifacts exist and whether they are structurally valid, but it cannot tell the
operator whether the artifacts are current relative to each other. The next
cockpit question is: am I looking at a fresh capture and matching derived
artifacts, or stale evidence/preflight files from an older local run? A valid
evidence-packet digest proves only packet self-integrity; it does not prove that
`evidence_packet.json` reflects the latest `capture.json` on disk. This lane adds
read-only freshness and sequence-coherence metadata so an operator can spot stale
or out-of-sequence local artifacts.

## Scope

- `alpha/webapp/operator_console_artifacts.py`: extend the read-only helper.
  - Preserve the fixed-root policy: default `local/operator_console/`, optional
    `ALPHA_OPERATOR_CONSOLE_ARTIFACT_ROOT` override honored only when it resolves
    inside the repository root, path-traversal and outside-root values rejected,
    and no path taken from query params, form data, request bodies, cookies, or
    headers.
  - Preserve the exact four fixed filenames.
  - Add `status_generated_at_utc` (UTC ISO-8601) generated when
    `build_artifact_status` runs. `build_artifact_status` accepts an injectable
    `now` so freshness labels are deterministic in tests.
  - Add safe per-file metadata for each fixed file via `file_freshness`:
    `path_label` (safe relative label), `exists`, `modified_at_utc`,
    `age_seconds`, `metadata_state` (`missing` / `present` / `unavailable`), and
    a deterministic `age_label` (`missing` / `just_updated` / `recent` /
    `older` / `unknown`) via the pure `age_label` helper and fixed thresholds
    (5 minutes, 24 hours).
  - Add derived-vs-capture ordering under `sequence_coherence`:
    `evidence_packet_vs_capture`, `anchor_preflight_vs_capture`, and
    `lift_preflight_vs_capture`, each with a `state`
    (`not_comparable` / `same_or_newer_than_capture` / `older_than_capture`) and
    a `flags` list of safe mismatch signals (`packet_id_mismatch`,
    `counts_mismatch`, `digest_invalid`, `digest_unverifiable`,
    `metadata_only_no_claim`) drawn only from existing safe summaries.
- `alpha/webapp/routes/operator_console.py`: add a compact
  "Artifact Freshness and Sequence Coherence" subsection to the existing
  Evidence and Receipt card (status generation time, per-file freshness rows,
  derived-vs-capture ordering rows, and the freshness boundary statements), plus
  a "Refresh" link that only reloads the current read-only `GET` page. No new
  endpoint is added; the freshness data extends the existing `local_artifacts`
  payload returned by the read-only status JSON.
- `docs/OPERATOR_CONSOLE.md`: artifact freshness and sequence-coherence section,
  per-state operator definitions, and the freshness boundaries.
- `tests/test_operator_console.py`: focused freshness/coherence tests.
- `.specs/INDEX.md`: one new row for this spec.

## Non-goals and boundaries

- No provider, hosted-model, local-model, MCP, tool, browser, network, or
  `/v1/solve` call; no CLI or subprocess execution from the console.
- No create, modify, delete, upload, edit, or save of any artifact; the four
  files are read-only inputs. No receipt store and no workbench action buttons.
- The Refresh affordance is a plain `GET` page reload; it never POSTs, runs a
  workflow, calls providers/models/CLI, mutates artifacts, or creates receipts.
- No raw prompts, baseline outputs, routed outputs, raw route metadata, system
  prompts, provider payloads, or full artifact JSON are displayed. Only counts,
  states, schema versions, ids, the content digest (a hash), and safe filesystem
  metadata (labels, timestamps, ages, ordering states) are surfaced. No raw JSON
  viewer is added.
- No API key storage or raw/partial key display; existing categorical key status
  is preserved.
- No change to `alpha_solver_portable.py`, provider runtime, model routing,
  `/v1/solve` execution, the capture/export/preflight schemas, or the
  `operator_run_capture.py` CLI semantics. Freshness is inferred from filesystem
  metadata and existing safe summaries only.
- No scoring, ranking, winner fields, or model-comparison UI.
- The console must not synthesize Alpha Solver runtime fields when no solve has
  run from the console: no route, expert trace, confidence, SAFE-OUT state,
  shortlist, SolverEnvelope output, model choice, provider result, benchmark
  result, or readiness result is invented.

## Freshness / no-claim boundary

Freshness and sequence coherence are local filesystem metadata only. They do not
imply route confidence, SAFE-OUT confidence, answer quality, validation,
production readiness, public/API readiness, autonomous readiness, model
superiority, provider readiness, or benchmark evidence. Specifically:

- Freshness is local filesystem metadata only.
- A newer artifact is not answer-quality, benchmark, readiness, production,
  validation, or superiority evidence.
- An older derived artifact means only that the local file timestamp appears
  older than the capture timestamp.
- Digest validity is packet self-integrity only, not proof that the packet
  reflects the latest capture file.
- Copied or restored files can carry misleading modified times, so these are
  operator hints, not guarantees.

## No-execution / no-raw / no-schema-change boundary

This lane adds no execution path. It performs no provider/model/MCP/network/
browser/CLI/subprocess call and no `/v1/solve` call. It displays no raw prompt,
raw baseline output, raw routed output, raw route metadata, provider payload, or
full artifact JSON, and adds no raw viewer. It changes no capture, export, or
preflight schema and does not modify any artifact.

## Code Targets

- `alpha/webapp/operator_console_artifacts.py`
- `alpha/webapp/routes/operator_console.py`
- `tests/test_operator_console.py`
- `docs/OPERATOR_CONSOLE.md`
- `.specs/INDEX.md`

## Test Plan

`tests/test_operator_console.py`: the status JSON includes
`status_generated_at_utc`; each of the four fixed files exposes safe metadata
when present; missing files return safe missing states and still render; invalid
JSON and invalid UTF-8 fail safe without a server error while still surfacing
filesystem metadata; file mtimes surface only as safe metadata (ISO string and
integer age, no absolute path or raw epoch); freshness labels are deterministic
under injected time and controlled mtimes; `evidence_packet.json`,
`anchor_preflight_report.json`, and `lift_preflight_report.json` older than
`capture.json` each report `older_than_capture`; a derived artifact at or newer
than capture reports `same_or_newer_than_capture`; a packet id mismatch is
reported without raw artifact display; a valid digest older than capture still
reports the stale sequence state; digest invalid/unverifiable are not hidden by
freshness metadata; fake API keys and recognizable raw prompt/baseline/routed/
route-metadata strings never appear in HTML or JSON; provider client
constructors patched to raise still allow both console routes to succeed; a
source scan confirms no provider/network/subprocess/browser/CLI execution
imports are introduced; the outside-root override remains rejected and an
inside-repo override remains honored; and no path is taken from request data.

## Validation

- `python -m pytest tests/test_operator_console.py -q`
- `python -m pytest tests/test_operator_console.py tests/test_operator_run_capture.py tests/test_api_endpoints.py -q`
- `python -m pytest -q`
- `ruff check alpha/webapp/operator_console_artifacts.py alpha/webapp/routes/operator_console.py tests/test_operator_console.py`
- `python scripts/check_narrative_claim_safety.py docs/OPERATOR_CONSOLE.md .specs/UI-ALPHA-OPERATOR-CONSOLE-ARTIFACT-FRESHNESS-001.md`

## Definition of Done

The helper extension, console wiring, docs, tests, and this spec merged; all
validation commands pass; the console reads only the fixed local directory (or a
safe inside-repo override) plus filesystem metadata for the four fixed files;
missing and malformed artifacts fail safe; no raw prompt, output, route
metadata, provider payload, full artifact JSON, or secret is displayed; no
schema is changed; and no provider/model/MCP/network/browser/CLI/subprocess or
`/v1/solve` path is exercised. Reporting an artifact as fresh, or a derived
artifact as older than capture, means only what the local file timestamps and
recorded summaries show; it is not an answer-quality, benchmark, readiness,
production, validation, or superiority judgment.
