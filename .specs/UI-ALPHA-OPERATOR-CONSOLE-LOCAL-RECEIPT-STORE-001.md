# UI-ALPHA-OPERATOR-CONSOLE-LOCAL-RECEIPT-STORE-001 · Operator Console Local Receipt Store

## Goal

Add a narrow, protected, local-first receipt store to the Alpha Solver Operator
Console so an authenticated operator can save a safe local snapshot of the
current console status and see recent receipt metadata on the console page.

## Motivation

The console can show local status, provider/cost gate state, artifact freshness,
sequence coherence, and dry-run preview state. Operators need a durable local
record of what the cockpit showed at a review checkpoint without storing raw
prompts, outputs, secrets, provider payloads, executable state, or raw artifact
bodies.

## Scope

- Add one protected POST path under `/dashboard/operator-console` that creates
  one local receipt snapshot.
- Add a Local Receipt Store card/subsection to the existing console UI.
- Add a `local_receipts` status section containing safe recent receipt metadata.
- Store receipts as JSON under `local/operator_console/receipts/`, or under
  `<resolved safe artifact root>/receipts/` when the existing inside-repository
  `ALPHA_OPERATOR_CONSOLE_ARTIFACT_ROOT` override is used.
- Whitelist the receipt snapshot fields from the already safe console status.
- List recent receipts as metadata summaries only.

## Non-goals and boundaries

This lane is not a solve lane, provider lane, dry-run execution lane, raw
artifact archive, general file-writing API, receipt editor, validation lane, or
readiness lane.

Local-write-only receipt boundary:

- The only new write is creation of one safe local receipt JSON file.
- No request data may influence the directory, filename, receipt id, or receipt
  body.
- Receipts are never edited or deleted in this lane.
- Receipt files are never uploaded, downloaded, or rendered through a raw viewer.

No-execution/no-solve/no-provider/no-artifact-mutation/no-runtime-output
boundary:

- Saving a receipt does not run a solve.
- Saving a receipt does not call `/v1/solve`.
- Saving a receipt does not call providers, hosted models, local models, MCP,
  browser automation, network, CLI, or subprocesses.
- Saving a receipt does not call internal solve functions and does not submit a
  prompt.
- Saving a receipt does not generate route, confidence, SAFE-OUT, expert trace,
  shortlist, diagnostics, answer text, model output, provider result, billing
  result, benchmark result, or readiness result.
- Saving a receipt does not create, edit, delete, upload, save, or mutate
  capture, evidence-packet, anchor-preflight, lift-preflight, or other existing
  operator artifacts.

No-raw/no-secret/no-readiness/no-validation/no-benchmark/no-superiority
boundary:

- Receipts do not store raw prompts, raw baseline outputs, raw routed outputs,
  raw route metadata, system prompts, provider payloads, raw secrets, partial
  keys, raw environment values, or full artifact JSON.
- Receipts store safe summaries only.
- A receipt is not answer-quality proof, validation, production readiness,
  provider readiness, benchmark evidence, billing accuracy, or superiority
  evidence.
- A receipt does not authorize live execution or dry-run execution.

## Code targets

- `alpha/webapp/operator_console_receipts.py` contains receipt-root resolution,
  schema constants, snapshot whitelisting, safe id generation, digest creation,
  atomic local write, and recent receipt metadata listing.
- `alpha/webapp/routes/operator_console.py` wires the protected POST route,
  status section, and compact UI card.
- `tests/test_operator_console.py` covers receipt status, route protection,
  path/body ignore behavior, safe override policy, digest verification,
  non-leakage, invalid receipt fail-safe handling, newest-first listing, and
  no-artifact-mutation/no-execution boundaries.
- `docs/OPERATOR_CONSOLE.md` documents operator-facing behavior and boundaries.

## Receipt schema

Receipt files use schema version `operator_console_receipt_v1` and receipt type
`status_snapshot`.

Top-level fields:

- `schema_version`
- `receipt_id`
- `created_at_utc`
- `source` (`operator_console`)
- `receipt_type` (`status_snapshot`)
- `content_digest`
- `snapshot`

`content_digest` is a `sha256:<hex>` digest over the safe receipt body with the
`content_digest` field excluded. It is self-integrity only.

The `snapshot` is a whitelisted subset of current console status:

- `console`: mode, live-provider-call status, claim boundary, boundary notes.
- `portable_contract`: presence, source path, contract mode, high-level
  surfaces.
- `run_setup`: run modes, disabled live-run button flag, note.
- `route_trace`: placeholder states only.
- `provider_gate`: configured provider, provider mode label, disabled live
  provider calls, console-calls-providers flag, emergency stop, live preview
  surface, categorical key status, required provider key names, provider key
  status, cap completeness, categorical cap status, cost cap status,
  token/request cap status, live execution gate, blockers, and gate boundary.
- `dry_run_preview`: display-only preview mode, dry-run execution status,
  would-use labels, input/evidence/preflight/freshness statuses, provider-gate
  summary, preview readiness/blockers, and boundary notes.
- `local_artifacts`: artifact-root label only; detected flag; status timestamp;
  capture/evidence/preflight states, schema versions, ids, counts, digests, and
  freshness/sequence-coherence metadata; boundary texts.
- `evidence_receipt`: existing placeholder fields and note only.

## Receipt path policy

- Fixed default root: `local/operator_console/receipts/` below the repository
  root.
- If `ALPHA_OPERATOR_CONSOLE_ARTIFACT_ROOT` resolves inside the repository root,
  receipts are written under that safe root's `receipts/` child directory.
- Outside-root or traversal overrides are rejected by the existing artifact-root
  policy and cannot redirect receipt writes outside the repository.
- Receipt ids are generated internally as bounded ids with no path separators.
- Filenames are derived internally as `<receipt_id>.json`.
- Collision handling does not overwrite an existing receipt silently.
- Writes use a temporary file in the receipt directory followed by an atomic
  rename/replace to the final path.
- Symlink receipt roots are rejected.

## Test plan

- Verify status JSON includes `local_receipts` with safe labels and zero-count
  behavior.
- Verify unauthenticated POST and missing-CSRF POST follow dashboard protection.
- Verify authenticated POST creates exactly one receipt under the fixed/safe
  receipt directory.
- Verify query/body attempts to supply path, filename, receipt id, or receipt
  body are ignored.
- Verify outside-root override cannot write outside the repository and inside
  override writes only below the safe root.
- Verify receipt id, filename, schema version, and digest shape/verification.
- Verify receipt snapshots include provider/dry-run/local-artifact summaries but
  no raw prompts, outputs, raw route metadata, provider payloads, raw secrets,
  partial keys, or raw env values.
- Verify recent receipt metadata appears in status/page without exposing full
  receipt bodies.
- Verify invalid/corrupt receipt files fail safe.
- Verify multiple receipts list newest-first with a safe limit.
- Verify receipt creation does not mutate capture/evidence/preflight artifacts.
- Verify provider-client constructors patched to raise do not affect page,
  status, or receipt POST.
- Verify no provider/network/subprocess/browser/MCP/solve imports are added to
  the route or helper.
- Run focused, related, full, lint, and narrative-claim-safety validation.

## Definition of Done

- The protected console exposes a Local Receipt Store card with receipt-root
  label, recent count, recent metadata summaries, boundary text, and exactly one
  `Save local receipt snapshot` action.
- Status JSON exposes `local_receipts` metadata and never exposes full receipt
  bodies.
- POST `/dashboard/operator-console/receipts` creates one safe receipt JSON from
  internally assembled status only.
- Receipts stay confined to `local/operator_console/receipts/` or the safe
  override root's `receipts/` child.
- Existing no-provider, no-runner, no-secret, no-raw, no-readiness, and
  no-validation boundaries remain intact.
- Focused and required validation commands pass or any missing evidence is
  reported exactly.
