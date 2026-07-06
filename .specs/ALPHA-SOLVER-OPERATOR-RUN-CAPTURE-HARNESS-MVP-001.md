# ALPHA-SOLVER-OPERATOR-RUN-CAPTURE-HARNESS-MVP-001 · Operator Run Capture Harness (MVP)

## Goal

Give the operator a local, deterministic harness that turns manually generated
routed-vs-plain runs into a normalized, machine-validated JSON evidence packet,
replacing hand-assembled per-run markdown files as the capture substrate for
later (separately authorized) blind scoring, replay, and audit lanes.

## Motivation

Operator evidence currently lives in loose markdown files per run directory
(for example `raw/baseline/<task>.md` and `raw/alpha/<task>.md`), with
consistency enforced only by regex documentation checkers. There is no
machine-readable capture format, no required-field validation before an
evidence packet exists, and no byte-stable export a replay or scoring lane can
digest. Every downstream evidence lane (packet normalizer, scorer packet
validator, blind-scoring bridge) needs that substrate first.

## Scope

- Case packet ingestion: `packet_id`, optional `description`, cases with
  unique non-empty `task_id`, `prompt`, optional `notes`.
- Capture scaffolding with one empty slot per task; task IDs and prompts are
  preserved verbatim.
- Operator-filled fields per case: `baseline_output` (plain), `routed_output`
  (routed Alpha), `route_metadata` (non-empty object), `validation_status`
  (`pending` / `captured` / `excluded`, with `exclusion_reason` required for
  excluded cases).
- Strict validation before export: unknown fields are rejected at every level,
  so score, rank, winner, blind-label, or identity-map fields cannot enter a
  packet; export additionally requires no pending cases and at least one
  captured case.
- Deterministic export: keys sorted, cases ordered by `task_id`, LF endings,
  no timestamps, byte-identical re-export, and a `content_digest` (SHA-256
  over the canonical body) for tamper detection.
- Embedded `harness_boundaries` attestation block covering only what the
  harness itself did (no provider/model/tool calls, no network, no scoring,
  no blinding or unblinding).

## Non-goals

- Do not call providers, hosted models, or local models.
- Do not execute tools or use the network.
- Do not touch `/v1/solve`, dashboards, or any external service.
- Do not score, rank, blind, or unblind outputs.
- Do not write any source map or A/B identity key.
- Do not claim readiness, benchmark results, provider or local-model quality,
  or that routed output is better than baseline; comparative interpretation is
  out of scope for this lane.

## Code Targets

- `alpha/eval/operator_run_capture.py` — validation, scaffolding, packet
  build, digest, deterministic rendering.
- `scripts/operator_run_capture.py` — `init` / `validate` / `export` CLI with
  distinct exit codes (0 ok, 1 validation failure, 2 usage/IO) and overwrite
  protection.
- `tests/fixtures/operator_run_capture/` — synthetic case packet and filled
  capture fixtures (all content invented; no provider or model output).
- `docs/OPERATOR_RUN_CAPTURE.md` — process doc with explicit non-claims.

## Test Plan

`tests/test_operator_run_capture.py` covers: case-packet validation (missing
keys, duplicates, unknown keys, empty case lists), scaffolding preservation,
capture validation (output/metadata requirements, exclusion reasons, schema
version, export completeness), packet structure and counts, task-ID ordering,
byte-identical deterministic export, digest verification and tamper detection,
and CLI roundtrip plus exit codes via subprocess.

## Acceptance Criteria

- `python -m pytest tests/test_operator_run_capture.py -q` passes.
- `python scripts/check_narrative_claim_safety.py docs/OPERATOR_RUN_CAPTURE.md`
  passes.
- Re-exporting an unchanged capture produces byte-identical packet files.
- A validation pass means only that the configured structural rules held for
  that capture file; it does not claim readiness or output quality.

## Definition of Done

Module, CLI, fixtures, tests, and process doc merged; all listed checks pass;
boundaries above hold with no provider/model/tool/network usage anywhere in
the lane.
