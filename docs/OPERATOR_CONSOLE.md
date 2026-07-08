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


## Operator Console First 5 Minutes

The Operator Console helps you review local evidence, understand manual next
steps, and see what is blocked. It does not run Alpha Solver or call providers.

Alpha Solver remains a discrimination and operator-control layer, not a generic
dashboard or runner. Use this page as a local-first cockpit for reading bounded
metadata and choosing manual next steps outside the console.

### First five-minute checklist

1. Confirm the console is protected and local-first under
   `/dashboard/operator-console`.
2. Check **Local Artifact Status** to see which local support files are present.
3. Check **Freshness and Sequence Coherence** to see local file-time hints and
   possible derived-artifact mismatches.
4. Check **Provider, Model, and Cost Gate** to see configuration visibility and
   why provider use remains blocked here.
5. Read **Dry-Run Preview** as metadata only. It does not run a dry-run.
6. Use **Manual Next Step Guide** to decide what is reviewable, manual-only, or
   blocked.
7. Use **ChatGPT Copy/Paste Capture** guidance only if you are manually
   collecting outputs outside the console.
8. Create a local receipt only if you need a bounded metadata snapshot of the
   current console state.

### Card-by-card interpretation

#### Local Artifact Status

- **What it shows:** compact states, counts, schema versions, packet ids, and
  digests for local capture, evidence packet, and preflight support files.
- **What it does not do:** it does not create, repair, delete, or rewrite those
  files, and it does not show raw prompts or raw outputs.
- **Mistake to avoid:** do not treat a present file or valid structure as proof
  of answer quality or proof that the evidence is current.

#### Freshness and Sequence Coherence

- **What it shows:** local filesystem modified-time metadata and metadata-only
  comparisons between capture and derived artifacts.
- **What it does not do:** it does not prove the true order of manual work, and
  it does not inspect raw prompt or output content.
- **Mistake to avoid:** do not treat newer timestamps as quality evidence; copied
  or restored files can carry misleading times.

#### Provider, Model, and Cost Gate

- **What it shows:** configured provider labels, key presence categories, cap
  presence categories, and the display-only reason provider use stays blocked
  inside this console.
- **What it does not do:** it does not validate credentials, estimate spend, call
  providers, or call ChatGPT.
- **Mistake to avoid:** do not treat a present key or cap as provider readiness,
  billing accuracy, or permission to run anything from the console.

#### Dry-Run Preview

- **What it shows:** a display-only summary of local metadata that a future lane
  might use: capture state, evidence state, preflight state, freshness hints,
  and provider-gate blockers.
- **What it does not do:** it does not run a dry-run, call `/v1/solve`, call a
  provider, generate answer text, or prove execution readiness.
- **Mistake to avoid:** do not read `preview_ready` as a product readiness claim;
  it means only local metadata completeness for this preview panel.

#### Local Receipt Store

- **What it shows:** recent local receipt metadata and a protected action to save
  one bounded status snapshot.
- **What it does not do:** it does not save raw prompts, raw outputs, pasted
  model output, provider payloads, or arbitrary files.
- **Mistake to avoid:** do not treat a receipt as validation, answer-quality
  proof, benchmark evidence, or production readiness.

#### ChatGPT Copy/Paste Capture

- **What it shows:** manual-only guidance for collecting plain ChatGPT output and
  routed Alpha output outside the console, then updating the local capture file
  outside the console.
- **What it does not do:** it does not call ChatGPT, automate a browser, provide
  a paste box, store pasted output, or edit capture files.
- **Mistake to avoid:** do not paste model output into the console; use the
  operator-owned local capture workflow outside this page.

#### Manual Next Step Guide

- **What it shows:** bounded labels for what can be reviewed now, what must be
  done manually outside the console, and what is blocked inside the console.
- **What it does not do:** it does not create tasks, start work, run commands,
  call services, or mutate artifacts.
- **Mistake to avoid:** do not treat guide labels as instructions that the
  console will perform; they are only operator-safety labels.

#### Route/Trace placeholders

- **What it shows:** placeholder route, trace, confidence, SAFE-OUT, expert/team,
  shortlist, and diagnostics fields that say no run has happened here.
- **What it does not do:** it does not invent route output, expose raw route
  metadata, select outputs, or imply a solve occurred.
- **Mistake to avoid:** do not treat placeholders as hidden results or pending
  work; they are empty until a separately authorized lane wires real metadata.

### What to do manually outside the console

Do terminal commands from a terminal. Edit capture files outside the console.
Collect ChatGPT copy/paste outputs manually outside the console. Review local
evidence files outside the console when you need the raw local material. Decide
manually whether a local receipt is useful for the current review.

The console can show bounded metadata about those surfaces, but it does not
perform the manual steps for you.

### When to create a local receipt

Create a local receipt when you need a bounded metadata snapshot of the current
console state. A receipt is useful when you want a local timestamped summary of
what the console showed at that moment.

A receipt is not validation, not answer-quality proof, not benchmark evidence,
and not production readiness. It is a local metadata snapshot only.

### How to interpret Dry-Run Preview

Dry-Run Preview is a display-only summary of local metadata that a future lane
might use. It does not run a dry-run and does not prove execution readiness.

Treat the preview as a checklist of visible local metadata and blockers. If it
points to missing artifacts or blocked provider use, handle those items manually
outside the console or wait for a separately authorized lane.

### What the console does not prove

The console does not prove:

- answer quality
- route correctness
- model superiority
- provider readiness
- billing accuracy
- benchmark validity
- production readiness
- validation success

### Do not expect this console to...

- run providers
- call ChatGPT
- run `/v1/solve`
- run terminal commands
- automate a browser
- store pasted model output
- edit capture files
- display raw prompts or outputs
- score, rank, or select winners


## Operator Console Daily-Use Walkthrough

Use this walkthrough as a manual operator comprehension check. It helps an
operator confirm they can use the current console and docs without confusing
metadata, manual steps, and blocked behavior. It does not run Alpha Solver, call
providers, validate outputs, or show readiness.

Time box: about 5 to 10 minutes. Stop if this is confusing and record the first
confusion point outside the console.

### Before you start

- You can access the protected `/dashboard/operator-console` page.
- You have read the **Operator Console First 5 Minutes** section above.
- You understand the console is local-first and non-executing.
- You have local artifacts only if you want to inspect artifact-dependent
  states. Missing local artifacts are still useful for seeing how the console
  describes absent metadata.

### Walkthrough steps

1. Open `/dashboard/operator-console`.
2. Confirm the page says local-first and live provider calls are disabled.
3. Read the First 5 Minutes checklist in `docs/OPERATOR_CONSOLE.md`.
4. Inspect **Local Artifact Status** and write down what is present, missing, or
   stale. Look at this first when you need to understand the local evidence
   surface.
5. Inspect **Freshness and Sequence Coherence** and identify whether there are
   warnings. This is only metadata.
6. Inspect **Provider, Model, and Cost Gate** and confirm provider use remains
   blocked in the console.
7. Inspect **Dry-Run Preview** and state whether you are reading it as
   metadata-only or mistaking it for execution readiness. It is metadata-only.
8. Inspect **Manual Next Step Guide** and identify one reviewable item, one
   manual-only item, and one blocked item.
9. Inspect **ChatGPT Copy/Paste Capture** and confirm output collection happens
   outside the console. This must be done manually.
10. Decide whether a **Local Receipt** is useful. If it is not useful, explicitly
    skip it. A receipt is local metadata, not proof of answer quality.
11. Confirm the console did not run providers, call ChatGPT, run `/v1/solve`,
    execute commands, edit capture files, or store pasted outputs. These are
    blocked in the console.
12. Record the first point of confusion, if any, outside the console.

### Expected operator-understanding outcomes

- The operator can name the first thing to inspect.
- The operator can separate reviewable, manual-only, and blocked behavior.
- The operator does not interpret receipt metadata as validation.
- The operator does not interpret Dry-Run Preview as execution readiness.
- The operator knows when to stop instead of asking the console to perform work.

### Failure signals

These signals mean the docs or UI may need future refinement:

- The operator cannot identify what to inspect first.
- The operator thinks the console can run a dry-run.
- The operator thinks provider calls are enabled.
- The operator thinks a receipt proves quality.
- The operator thinks route/trace placeholders are hidden results.
- The operator expects a queue, runner, scheduler, or action button; those are
  not console behavior.
- The operator wants to paste model output into the console.
- The operator cannot explain what is blocked.

### Manual notes template

Fill out this template outside the console. The console must not store this
manual note.

```text
Date:
Operator:
Console state summary:
First thing inspected:
Reviewable item found:
Manual-only item found:
Blocked item found:
Receipt created: yes/no
Dry-Run Preview interpretation:
Confusion point:
Stop condition triggered: yes/no
Follow-up needed:
```

### What this walkthrough does not prove

This walkthrough does not prove:

- answer quality
- route correctness
- model superiority
- provider readiness
- billing accuracy
- benchmark validity
- production readiness
- validation success
- execution safety beyond the currently documented console boundaries

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
4. **Dry-Run Preview** — a display-only read of what a future dry-run would
   prepare or require, derived only from the local artifact status and provider
   gate below. It runs no dry-run and enables none (see below).
5. **Route and Trace** — placeholder fields for route, confidence, SAFE-OUT
   state, expert/team, shortlist, and diagnostics. They read "not run yet"; the
   console does not invent route output or imply a solve ran.
6. **Provider and Cost Gate** — the configured provider and mode label, that the
   console does not call providers, emergency-stop and live-preview surface
   state, API key **presence** only (`present` / `missing`), and a display-only
   Live Execution Gate that reports whether live execution is blocked, the
   blockers, and cap completeness (see below). No raw or partial key values are
   shown.
7. **Preflight and Capture Entry** — the local workflows (anchor-preflight,
   lift-preflight, init capture, validate capture, export evidence packet) with
   command snippets and a docs pointer. These run from a terminal, not from the
   console.
8. **Local Receipt Store** — a narrow local audit-snapshot store with a
   receipt-root label, recent receipt count, recent receipt metadata, boundary
   text, and one `Save local receipt snapshot` action.
9. **Evidence and Receipt** — placeholders for a future receipt id, export
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
model, calls a CLI, or mutates an artifact. Receipt creation is available only
through the separate protected Local Receipt Store action described below, and
that action writes only a safe receipt JSON.

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

## Local Receipt Store

Lane: `UI-ALPHA-OPERATOR-CONSOLE-LOCAL-RECEIPT-STORE-001`

The Local Receipt Store card lets an authenticated operator save a safe local
audit snapshot of the current console status and then see recent receipt
metadata. A local receipt is a JSON status snapshot for later comparison or
audit. It is local-only and summary-only; it is not an answer, proof, validation
result, readiness result, benchmark result, billing result, or superiority
claim.

### Routes and protection

- Page: `GET /dashboard/operator-console`
- Read-only status JSON: `GET /dashboard/operator-console/status`
- Receipt creation: `POST /dashboard/operator-console/receipts`

The receipt creation route is under the same protected `/dashboard` surface as
the console. Unauthenticated POST requests fail under dashboard protection, and
authenticated POST requests must satisfy the dashboard CSRF guard. The route
takes no user-supplied path, filename, receipt id, or receipt body. Query-string
and request-body attempts to provide any of those values are ignored.

### Receipt root and path policy

Receipts are stored only under the existing safe local artifact root:

- Default: `local/operator_console/receipts/` under the repository root.
- Safe override: if `ALPHA_OPERATOR_CONSOLE_ARTIFACT_ROOT` resolves inside the
  repository root, receipts are written under that resolved root's `receipts/`
  child.
- Outside-root, traversal, or invalid overrides are rejected by the same safe
  root policy used for local artifacts, so they cannot redirect receipt writes
  outside the repository.

Receipt ids are generated internally as bounded safe identifiers with no path
separators. Filenames are derived internally from the receipt id and end in
`.json`. Receipt creation writes a temporary file inside the receipt directory
and then atomically renames it to the final receipt path. It does not overwrite
an existing receipt silently and does not use a request-supplied path.

### Receipt schema and safe fields

Receipt files use schema version `operator_console_receipt_v1` and receipt type
`status_snapshot`. Top-level fields are:

- `schema_version`
- `receipt_id`
- `created_at_utc`
- `source` (`operator_console`)
- `receipt_type` (`status_snapshot`)
- `content_digest`
- `snapshot`

`content_digest` is a `sha256:<hex>` digest over the safe receipt body excluding
the digest field itself. It is self-integrity only. It is not proof that the
receipt is correct, current, answer-quality evidence, validation evidence, or a
readiness signal.

The `snapshot` stores only whitelisted safe status summaries:

- Console mode, disabled live-provider-call status, claim boundary, and boundary
  notes.
- Portable-contract presence, source path, contract mode, and high-level surface
  labels.
- Run modes, disabled live-run button flag, and run-setup note.
- Route/trace placeholder states only.
- Provider/cost gate summary: configured provider, provider mode label, disabled
  live provider calls, console-calls-providers flag, emergency-stop state, live
  preview surface state, categorical key status (`present` / `missing` only),
  required provider key names, categorical provider-key status, cap
  completeness, categorical cap statuses, cost cap status, token/request cap
  status, live execution gate, blockers, and gate boundary.
- Dry-run preview summary: display-only preview mode, dry-run execution status,
  would-use labels, input/evidence/preflight/freshness states, provider-gate
  summary, preview readiness/blockers, and boundary notes.
- Local artifact status summaries: artifact-root label only; detected flag;
  status timestamp; capture/evidence/preflight states, schema versions, packet
  ids, counts, content digest, route-metadata presence count, freshness metadata,
  sequence-coherence states/flags, and boundary texts.
- Existing evidence/receipt placeholder fields and note.

### What receipts do not store

Receipts do **not** store raw prompts, raw baseline outputs, raw routed outputs,
raw route metadata, system prompts, provider payloads, raw secrets, partial API
keys, raw environment values, arbitrary request bodies, full artifact JSON, or
future unsafe status fields. The recent receipt list in the page/status JSON
shows metadata only: receipt id, creation time, schema version, receipt type,
content digest, safe path label, state, and a compact snapshot summary. It does
not return or render the full receipt body by default.

### Receipt boundaries

- Local receipts are local audit snapshots only.
- Saving a receipt does not run a solve.
- Saving a receipt does not call `/v1/solve`.
- Saving a receipt does not call providers, models, MCP, browser automation,
  network, CLI, or subprocesses.
- Saving a receipt does not create, edit, delete, upload, save, or mutate
  capture/evidence/preflight artifacts.
- Saving a receipt writes only a safe local receipt JSON under the fixed receipt
  directory.
- Receipts store safe summaries only.
- Receipts do not store raw prompts, raw outputs, raw route metadata, system
  prompts, provider payloads, raw secrets, partial keys, or raw environment
  values.
- A receipt is not answer-quality proof, validation, production readiness,
  provider readiness, benchmark evidence, billing accuracy, or superiority
  evidence.
- A receipt does not authorize live execution or dry-run execution.

The Local Receipt Store does not add receipt delete, edit, upload, download, or
raw-viewer support. Any future receipt management or export behavior requires a
separate lane.

## Provider, model, and cost gate panel

Lane: `UI-ALPHA-OPERATOR-CONSOLE-PROVIDER-COST-GATE-PANEL-001`

The Provider and Cost Gate card is a **display-only** view of provider, model,
and cost-gate configuration. It answers a single cockpit question: can live
execution even be considered later, and if not, what safety gate is missing? It
reads environment-variable *presence* and truthiness only. It never reads a
secret value, never validates a credential, never contacts a provider, and never
authorizes live execution.

### Configuration rows

- `configured_provider` / `provider_mode_label` — the configured provider mode
  (from `MODEL_PROVIDER`, default `local`). The label always notes that live
  provider execution is not enabled from this console.
- `live_provider_calls` — always `disabled`; `console_calls_providers` is always
  `false`.
- `emergency_stop` — `engaged` / `not engaged` (from
  `ALPHA_PROVIDER_EMERGENCY_STOP`).
- `live_preview_surface` — `enabled` / `disabled` (from
  `ALPHA_LIVE_PREVIEW_ENABLED`).
- `key_status` — per credential env (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`,
  `GOOGLE_API_KEY`), `present` / `missing` only.
- `required_provider_keys` — the credential env var name(s) the **configured
  provider** would require (names only, never values).
- `provider_key_status` — the categorical status of that specific requirement:
  `not_required` (`local` / `none`), `not_evaluated` (`local_llm`, whose local
  runtime configuration this display-only gate does not assess), `present` (all
  required keys present), or `missing` (a required key is absent). This mirrors
  the provider-key mapping in `scripts/check_env.py` categorically: `openai`
  requires `OPENAI_API_KEY`, `anthropic` requires `ANTHROPIC_API_KEY`, and
  `google` / `gemini` require `GOOGLE_API_KEY`.

### Live Execution Gate (display-only)

- `live_execution_gate` — always `blocked` from this console. This lane does not
  enable live execution under any configuration.
- `live_execution_blockers` — safe labels explaining why live execution stays
  blocked. `display_only_lane` and `live_provider_calls_disabled` are always
  present. The rest describe what a future, separately authorized live-provider
  lane would still need in place: `emergency_stop_engaged`,
  `missing_provider_key` (derived from the **configured provider's** required
  key, not from any key), `local_llm_configuration_not_evaluated` (for
  `local_llm`, which is never satisfied by a hosted-provider key),
  `missing_cost_cap`, `missing_token_or_request_cap`,
  `live_preview_surface_disabled`.
- `gate_boundary` — `display-only; no provider call or credential validation
  performed`.

### Cap completeness

Cost, token, and request caps are inspected for presence only:

- `cap_status` — per cap (`max_cost_usd`, `max_input_tokens`,
  `max_output_tokens`, `max_requests`), `present` / `missing`.
- `cap_completeness` — `none_configured` / `partially_configured` /
  `configured` across the four caps.
- `cost_cap_status` — `missing` / `present` for the spend cap only.
- `token_request_cap_status` — `missing` / `partial` / `present` across the
  token and request caps.

Caps are **configured limits, not billing truth**. Presence of a cap does not
verify spend, pricing, or billing accuracy, and this console performs no spend
estimation.

### Gate boundaries

- Provider and cost gate status is configuration visibility only.
- This console does not validate credentials.
- This console does not call providers, models, /v1/solve, MCP, tools, browser
  automation, network, CLI, or subprocesses.
- Cost caps are configured limits, not billing accuracy or spend verification.
- Key status is present/missing only; no raw or partial key values are displayed.
- A complete display-only gate is not provider readiness, production readiness,
  validation, benchmark evidence, or superiority evidence.
- Live execution remains blocked unless a separate future live-provider lane
  explicitly authorizes it. Complete cap or key configuration does not authorize
  live execution — the gate result stays `blocked`.

Environment presence is not credential validity: a key reported `present` may
still be invalid, and the console does not check. A cap reported `present` is a
configured limit only, not proof of billing behavior.

## Dry-Run Preview panel

Lane: `UI-ALPHA-OPERATOR-CONSOLE-DRY-RUN-PREVIEW-001`

The Run Setup card lists `dry-run` as an available mode, but it does not explain
what dry-run readiness means or what a dry-run would need. The **Dry-Run Preview**
card answers that one cockpit question: what would a future dry-run prepare, and
what is missing before a separate dry-run execution lane could be considered? It is
**display-only**. It runs no dry-run and enables none: `preview_mode` is always
`display_only` and `dry_run_execution` is always `not_enabled`. Every value is
derived from the local artifact status and provider gate described above; nothing
here executes, submits, mutates, or generates output.

### What the panel reports

- `preview_mode` / `dry_run_execution` — always `display_only` and `not_enabled`.
- `would_use` — safe names of the existing local metadata a dry-run would read
  (`local_capture_summary`, `local_artifact_status`, `artifact_freshness_metadata`,
  `provider_cost_gate_status`). These are surface names only, not contents.
- `input_source_status` — the local capture's readiness as an input source:
  `capture_missing`, `capture_invalid`, `capture_structurally_valid`, or
  `capture_export_ready`, mapped from the existing capture summary.
- `evidence_packet_status` — the existing evidence-packet state (`missing`,
  `invalid_json`, `invalid_structure`, `digest_valid`, `digest_invalid`,
  `digest_unverifiable`).
- `preflight_status` — whether the anchor and lift preflight reports are
  `*_present`, `*_missing`, or `*_invalid`, as local metadata only.
- `freshness_warnings` — safe labels drawn only from the existing
  `local_artifacts.freshness.sequence_coherence` (for example
  `evidence_packet_older_than_capture`, `anchor_preflight_older_than_capture`,
  `lift_preflight_older_than_capture`, `packet_id_mismatch`, `counts_mismatch`,
  `digest_invalid`, `digest_unverifiable`).
- `provider_gate_summary` — the existing gate's `live_execution_gate` (always
  `blocked`), `provider_key_status`, `cap_completeness`, and
  `live_execution_blockers`.
- `preview_readiness` — `unavailable`, `needs_artifacts`, or `preview_ready`.
- `preview_blockers` — safe labels naming what is missing before a future dry-run
  lane (for example `missing_capture`, `invalid_capture`,
  `missing_evidence_packet`, `invalid_or_unverified_evidence_packet`,
  `stale_derived_artifacts`, `missing_preflight_reports`,
  `provider_live_execution_blocked`, `display_only_lane`).

### What preview readiness means

Preview readiness is local metadata completeness only: whether the panel has enough
local metadata to explain the operator's next step. `preview_ready` requires that
local capture is structurally valid or export-ready, the evidence packet's own
digest is valid, both preflight reports are present, and no stale-or-mismatched
freshness warnings apply. If capture is missing or a prerequisite is absent the
panel reports `needs_artifacts` and still renders; if capture cannot be read it
reports `unavailable` and still renders.

A preview-ready state does not claim answer quality, route readiness, provider
readiness, production readiness, validation, benchmark evidence, billing accuracy,
or superiority, and it does not authorize execution. It is not a readiness claim
about the product.

### Input source status

`input_source_status` reflects only the local capture file already summarized by
the artifact status card. `capture_structurally_valid` and `capture_export_ready`
expose local counts that the artifact summary already surfaces; they never expose
raw prompts or raw outputs. `capture_missing` and `capture_invalid` mean the local
capture is absent or cannot be read; the panel says so and does not invent input.

### Evidence packet digest status is self-integrity only

`digest_valid` means the evidence packet's recorded digest matches its own body. It
is packet self-integrity only. It is not freshness, not answer quality, and not a
readiness or validation claim, and it does not prove the packet reflects the latest
capture file. `digest_invalid` and `digest_unverifiable` are surfaced as safe
warnings and blockers, never as failure claims about answer quality.

### Freshness warnings are local metadata only

Freshness warnings come only from local filesystem modified-time metadata and the
existing sequence-coherence flags. They are hints, not guarantees: copied or
restored files can carry misleading modified times. A stale warning is not a
failure claim and does not validate or invalidate any answer; it just flags that a
derived file's timestamp appears older than capture on disk.

### Provider gate summary blocks live execution

The provider gate summary reuses the existing display-only gate. `live_execution_gate`
is always `blocked` and `provider_live_execution_blocked` is always a preview
blocker. Provider/live execution stays blocked regardless of preview readiness: a
`preview_ready` panel does not authorize live execution, and complete provider or
cap configuration does not authorize it either. The summary validates no credential
and contacts no provider.

### Dry-Run Preview boundaries

The following boundary statements appear in the panel:

- Dry-run preview is display-only.
- This console does not execute a solve from this panel.
- This console does not call /v1/solve.
- This console does not call providers, models, MCP, browser automation, network,
  CLI, or subprocesses.
- This console does not create, edit, delete, upload, save, or mutate artifacts.
- This console does not generate route, confidence, SAFE-OUT, expert trace,
  shortlist, diagnostics, answer text, model output, provider result, billing
  result, benchmark result, or readiness result.
- Preview readiness is local metadata completeness only.
- A preview-ready state is not answer-quality, validation, production, provider
  readiness, benchmark evidence, billing accuracy, or superiority evidence.
- A future dry-run execution lane must be separately authorized.

A preview-ready panel is not a readiness, validation, benchmark, production, or
superiority claim. This lane does not enable dry-run execution; that remains a
separate future lane that must be separately authorized.

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

## ChatGPT Copy/Paste Capture card

The `ChatGPT Copy/Paste Capture` card explains the `chatgpt-copy-paste` run mode as a manual-only workflow. The operator generates plain ChatGPT output and routed Alpha output outside the console, then pastes those outputs into the operator-owned local `capture.json` lab notebook outside this panel. Pasted outputs belong in the local capture file, not in the console card.

The card adds a `chatgpt_copy_paste_capture` status section with fixed boundary fields: `mode=manual_only`, automation disabled, browser automation disabled, provider calls disabled, live execution disabled, `capture_storage=external_capture_file_only`, `console_writes_capture=false`, and `console_stores_pasted_outputs=false`.

### Capture stages and next manual steps

The current capture stage is derived only from safe local artifact summaries that the console already exposes. It does not read or display raw prompts, raw baseline output, raw routed output, or raw route metadata.

- `no_capture` means the safe capture summary reports no local capture file. Suggested manual steps are to author the case packet, run anchor preflight from a terminal, and scaffold the capture from a terminal.
- `capture_invalid` means the safe capture summary reports invalid JSON or invalid structure. Suggested manual steps are to inspect/repair the local file outside the console and validate from a terminal.
- `capture_scaffolded` means a structurally valid capture exists with pending slots. Suggested manual steps are to manually collect plain ChatGPT output, manually collect routed Alpha output, paste outputs into the local capture file, and record observed route/provenance facts.
- `capture_in_progress` means the safe counts show captured or excluded slots while pending work remains. Suggested manual steps are to finish pending slots, record observed route/provenance facts, and validate from a terminal.
- `capture_all_excluded` means the capture is structurally valid but has no pending slots and no captured cases, so it is not export-ready. Suggested manual steps are to add at least one captured case, revise the case packet or capture file outside the console, and validate from a terminal.
- `capture_export_ready` means the safe summary reports an export-ready capture and no digest-valid evidence packet. Suggested manual steps are to run lift preflight from a terminal, export the evidence packet from a terminal, and optionally save a local receipt snapshot through the existing receipt store.
- `evidence_packet_available` means the evidence packet summary reports a digest-valid packet. This is packet self-integrity only, not answer quality, validation, readiness, benchmark, production, billing, or superiority evidence.

### Placeholder-only capture slot template

The card shows placeholders only:

- `task_id: <task_id>`
- `baseline_output: <paste plain ChatGPT output into local capture file>`
- `routed_output: <paste routed Alpha output into local capture file>`
- `route_metadata: <observed route/provenance facts only>`
- `validation_status: captured or excluded`
- `exclusion_reason: <required only when excluded>`

The card does not provide a paste textarea, capture editor, upload form, save button, or artifact mutation route.

### Copy/paste checklist

The checklist is made of bounded safe labels only: author the case packet, run anchor preflight from a terminal, scaffold capture from a terminal, collect plain ChatGPT output manually, collect routed Alpha output manually, paste outputs into the local capture file, record observed route metadata, validate capture from a terminal, run lift preflight from a terminal, export the evidence packet from a terminal, and optionally save a local receipt snapshot through the existing B006 receipt store.

### Route metadata guidance

Route metadata is for observed route/provenance facts only. Route metadata is not scoring, ranking, winner selection, quality judgment, readiness, benchmark, validation, production, billing, or superiority evidence. The console does not use route metadata to select a winner, compare models, score answers, rank outputs, validate quality, or claim production readiness.

### Terminal command snippets are text only

The card repeats the existing local harness command snippets for anchor preflight, init capture, validate capture, lift preflight, and export evidence packet. These snippets are terminal instructions only. The console does not execute them, start a subprocess, call the CLI, call network, call providers, call ChatGPT, call models, call MCP, automate a browser, submit prompts, call `/v1/solve`, or call internal solve functions.

### Manual-only boundaries

ChatGPT copy/paste capture is manual-only. This console does not call ChatGPT. This console does not call providers, models, `/v1/solve`, MCP, browser automation, network, CLI, or subprocesses. This console does not automate a browser. This console does not submit prompts. This console does not store pasted model outputs in this lane. This console does not create, edit, delete, upload, save, or mutate `capture.json`, evidence packets, preflight reports, or receipts from this panel.

The capture harness remains a local lab notebook, not a runner. Receipts may be saved separately through the existing local receipt store, but the ChatGPT Copy/Paste Capture card does not auto-save receipts and does not mutate receipts. Any future paste-storage, capture-editor, browser-automation, or API-automation behavior must be separately authorized.

## Manual Next Step Guide

Lane: `AOC-B008A-OPERATOR-NEXT-STEP-CLARITY-001`

The **Manual Next Step Guide** is a display-only clarity panel in the protected Operator Console. It summarizes safe labels for what the operator can review now, what remains manual-only outside the console, and what is blocked inside the console.

The panel is not a queue, not a runner, and not a workbench. It does not execute anything, call providers, call ChatGPT, call `/v1/solve`, automate a browser, run CLI/subprocess commands, submit prompts, or mutate capture/evidence/preflight artifacts.

The guide does not add write paths. The existing Local Receipt Store remains the only controlled local write action on the Operator Console surface. The guide does not store pasted output and does not add a paste editor, capture editor, raw prompt viewer, raw output viewer, or raw route metadata viewer.

The guide also makes no readiness, validation, benchmark, production, scoring, ranking, winner, or superiority claims. Its labels are operator-safety labels only; they are not evidence of output quality, provider availability, billing accuracy, or launch suitability.
