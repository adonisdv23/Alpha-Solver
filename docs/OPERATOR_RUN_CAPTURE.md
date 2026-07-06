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

## Substantive Lift capture preflight

Before reviewing a PR646/post-652 qualitative capture packet, operators should
confirm the packet preserves the evidence needed to evaluate the run without
turning the harness into a scorer:

- Preserve prompt/context parity between baseline and Alpha threads, including
  the same task wording, constraints, and any operator-provided context used to
  generate each pasted output.
- Preserve raw export provenance when available, such as the raw exported
  transcript or capture artifact that the pasted fields came from.
- Preserve explicit high-headroom prompt anchors when the prompt expects
  case-specific reasoning, including files, PR numbers, issue numbers, named
  artifacts, implementation lanes, or other concrete task objects.
- Keep `route_metadata` limited to route and provenance facts. It is not a
  place for quality judgments, comparative conclusions, or reviewer scoring.
- Do not add score, rank, winner, blind label, source map, identity map, A/B
  identity key, readiness, benchmark, or superiority fields to the capture,
  export, `route_metadata`, or surrounding packet notes.

`check_substantive_lift(solution, prompt=prompt)` may be used only as a
non-scoring structural preflight for the Substantive Lift wording contract. A
passing result must not be described as answer quality, benchmark validation,
readiness, production suitability, or Alpha superiority; it only means the
checked text satisfied the local structural wording rules for that prompt.

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
