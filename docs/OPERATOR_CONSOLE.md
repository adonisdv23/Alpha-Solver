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
   digest, and validation status, plus local artifact status and a read-only
   artifact freshness / sequence-coherence subsection (see below).

## Local artifact status

The console reads a narrow, fixed local directory and shows compact status for
local operator artifacts. It is read-only: it never creates, modifies, deletes,
or writes any artifact, and it never runs a workflow.

### Artifact root and path policy

- Fixed root: `local/operator_console/` under the repository root (kept
  untracked via `.gitignore`).
- Optional override env `ALPHA_OPERATOR_CONSOLE_ARTIFACT_ROOT` is honored only
  when it resolves to a path **inside** the repository root. Path-traversal and
  outside-root values are rejected and the fixed default is used.
- The console never reads a path from query parameters, form data, request
  bodies, cookies, or headers.
- If the directory does not exist, the console renders normally and shows
  "No local operator artifacts detected."

### Files and states

Inside the root, these optional files are summarized:

- `capture.json` — `missing` / `invalid_json` / `invalid_structure` /
  `structurally_valid` / `export_ready`, with schema version, packet id, and
  total/captured/excluded/pending counts plus a route-metadata presence count.
- `evidence_packet.json` — `missing` / `invalid_json` / `invalid_structure` /
  `digest_valid` / `digest_invalid` / `digest_unverifiable`, with schema
  version, packet id, content digest, and counts. Digest verification reuses
  `operator_run_capture.verify_packet_digest`.
- `anchor_preflight_report.json` and `lift_preflight_report.json` — `missing` /
  `invalid_json` / `invalid_structure` / `present`, with a needs-attention count
  and state counts.

### What is not shown

Only counts, states, schema versions, ids, and the content digest (a hash) are
surfaced. Raw prompts, baseline outputs, routed outputs, raw route metadata,
system prompts, and provider payloads are **not** displayed by default. The
following boundary statements appear in both the page and the status JSON:

- Local artifacts are structural support artifacts only.
- This console does not execute providers, models, /v1/solve, MCP, tools,
  browser automation, or CLI commands.
- No raw prompts or raw outputs are displayed by default.
- No answer-quality, benchmark, readiness, production, validation, or
  superiority claim is made.

A preflight report being present is not a quality or readiness signal.

## Artifact freshness and sequence coherence

Lane: `UI-ALPHA-OPERATOR-CONSOLE-ARTIFACT-FRESHNESS-001`

Structural validity answers "does this artifact exist and is it well formed."
It does not answer "am I looking at a fresh capture and matching derived
artifacts, or stale evidence/preflight files from an older local run." The
console adds a small, read-only **Artifact Freshness and Sequence Coherence**
subsection to the Evidence and Receipt card to help answer that second
question. It infers everything from local filesystem modified-time metadata and
the existing safe summaries above; it changes no schema and reads no raw
content.

### Status generation time

The status payload includes `status_generated_at_utc`, a UTC ISO-8601 timestamp
recorded when the status is assembled. It is the reference point the console
uses to describe how old each file is.

### Per-file freshness

For each of the four fixed files the console surfaces only safe metadata:

- `path_label` — the fixed filename (never an absolute local path).
- `exists` — whether the file is present.
- `modified_at_utc` — the file's modified time as a UTC ISO-8601 string, or
  `null`.
- `age_seconds` — a nonnegative integer age relative to the status time, or
  `null`.
- `metadata_state` — `missing`, `present`, or `unavailable`.
- `age_label` — a deterministic bounded label:
  - `missing` — the file is not present.
  - `just_updated` — modified within the last 5 minutes.
  - `recent` — modified within the last 24 hours.
  - `older` — modified more than 24 hours ago.
  - `unknown` — the file exists but its modified time could not be read.

### Sequence coherence (derived vs capture)

`capture.json` is treated as the source. Each derived artifact is compared to it
under `sequence_coherence`:

- `evidence_packet_vs_capture`
- `anchor_preflight_vs_capture`
- `lift_preflight_vs_capture`

Each comparison reports an ordering `state`:

- `not_comparable` — one or both modified times are unavailable (for example a
  missing file).
- `same_or_newer_than_capture` — the derived file's timestamp is at or after the
  capture timestamp.
- `older_than_capture` — the derived file's timestamp appears older than the
  capture timestamp, so it may reflect an earlier local run.

Each comparison also carries a `flags` list of safe mismatch signals drawn only
from the existing summaries: `packet_id_mismatch` (packet ids differ),
`counts_mismatch` (evidence-packet counts differ from capture counts),
`digest_invalid` / `digest_unverifiable` (the evidence packet's own digest
state), and `metadata_only_no_claim` (always present as a reminder that this is
metadata, not a quality claim).

A "Refresh" affordance on the page is a plain link that reloads the current
read-only `GET` page. It never POSTs, runs a workflow, calls a provider or
model, calls a CLI, mutates an artifact, or creates a receipt.

### Freshness boundaries

- Freshness is local filesystem metadata only.
- A newer artifact is not answer-quality, benchmark, readiness, production,
  validation, or superiority evidence.
- An older derived artifact means only that the local file timestamp appears
  older than the capture timestamp.
- Digest validity is packet self-integrity only, not proof that the packet
  reflects the latest capture file.
- Copied or restored files can carry misleading modified times, so freshness and
  ordering are hints for the operator, not guarantees about run order.

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
