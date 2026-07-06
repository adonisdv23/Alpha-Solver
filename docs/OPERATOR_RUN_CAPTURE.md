# Operator Run Capture Harness

Lane: `ALPHA-SOLVER-OPERATOR-RUN-CAPTURE-HARNESS-MVP-001`

A local-only harness that turns manually generated routed-vs-plain operator
runs into a normalized, machine-validated, byte-stable JSON evidence packet.
It replaces hand-assembled per-run markdown files with a format that later
(separately authorized) blind-scoring, replay, and audit lanes can consume.

The harness is a lab notebook, not a runner: the operator generates and pastes
all outputs; the harness only scaffolds, validates, and exports.

## Workflow

1. **Author a case packet** (JSON) listing the tasks to capture. See
   `tests/fixtures/operator_run_capture/case_packet.json` for the shape:
   `packet_id`, optional `description`, and `cases` with unique `task_id`,
   `prompt`, optional `notes`.

2. **Scaffold a capture file** with one empty slot per task:

   ```bash
   python scripts/operator_run_capture.py init \
     --case-packet my_cases.json --out my_capture.json
   ```

3. **Fill in each case by hand.** For every task the operator pastes:
   - `baseline_output` — the plain (non-routed) output they collected
   - `routed_output` — the routed Alpha output they collected
   - `route_metadata` — a non-empty JSON object of route facts they observed
   - `validation_status` — `captured`, or `excluded` with a non-empty
     `exclusion_reason` when a task is dropped

   Task IDs and prompts are preserved from the case packet. Unknown keys are
   rejected on the case-packet and capture schema fields, so schema-level
   score, rank, winner, blind-label, source-map, or identity-map fields are
   invalid. `route_metadata` is intentionally schema-light in this MVP: it is
   accepted as a non-empty JSON object and exported verbatim, and operators
   must use it only for route facts they observed.

4. **Validate** at any time (structural), or with `--for-export`
   (completeness: no `pending` cases, at least one `captured`):

   ```bash
   python scripts/operator_run_capture.py validate --capture my_capture.json --for-export
   ```

5. **Export the evidence packet**:

   ```bash
   python scripts/operator_run_capture.py export \
     --capture my_capture.json --out my_packet.json
   ```

   The export is deterministic: keys sorted, cases ordered by `task_id`, LF
   line endings, no timestamps, and a `content_digest` (SHA-256 over the
   canonical body) so replay or review lanes can detect any post-export edit.
   Re-exporting the same capture yields byte-identical output.

## Packet contents

Every exported packet embeds a `harness_boundaries` block recording, as
machine-readable booleans, that the harness itself made no provider calls, no
hosted or local model calls, executed no tools, used no network access,
performed no scoring, and performed no blinding or unblinding. These
statements cover only what the harness did; they say nothing about how the
operator produced the pasted outputs — record that provenance in the run's
own docs.

## Non-claims and boundaries

- Local files only. Nothing here calls providers, models, or tools, touches
  `/v1/solve`, dashboards, or any external service.
- No scoring, ranking, blinding, or unblinding. Blind scoring is a separate
  lane; no source map or A/B identity key is ever written by this harness.
- `route_metadata` remains schema-light for this MVP. Its keys are route-fact
  notes only and must not be interpreted as scoring, ranking, winner,
  blinding, unblinding, source-map, identity-map, benchmark, readiness,
  quality, production, public-MVP, or Alpha-superiority evidence.
- A passing validation means only that the configured structural rules held
  for that capture file. It does not claim readiness, benchmark results,
  provider or local-model quality, or that routed output is better than the
  baseline. Comparative interpretation is out of scope for this lane.
