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

### Running the lift preflight CLI

After filling a capture and before qualitative review, the operator can run
the read-only preflight over the capture file:

```bash
python scripts/operator_run_capture.py lift-preflight \
  --capture local/pr646_substantive_lift_capture.json \
  --report-out local/pr646_lift_preflight_report.json
```

The command loads the capture, and for every case that has both a prompt and
a routed output it runs the local checker over the solution body and prints one
state per case. If the pasted routed output begins with a full-response
`SOLUTION:` label, the preflight strips that leading label before checking so
operators may paste the collected routed output rather than hand-editing it
down to only the six-line body.

- `structural_pass` / `structural_fail` — the configured structural wording
  checks held or did not hold for the supplied routed output and prompt. When
  the prompt has no extractable anchors, the line says the anchor-specific
  checks were vacuous, so anchor-free prompts do not create false failures.
- `missing_prompt` / `missing_routed_output` — the case cannot be preflighted
  yet; fill the capture first.
- `excluded_case` — excluded cases are skipped, never checked.
- `safe_out_not_applicable` — the routed output is a bounded `SAFE-OUT:`
  response; the lift wording contract does not apply to honest non-answers.

Exit code 0 means no case needed attention; exit code 1 means at least one
case was a structural fail, had missing text, or was malformed. The optional
`--report-out` file is a local JSON report for the operator's own notes. It
is not a capture file, not an evidence packet, and not an input to `export`;
it carries no score, rank, winner, blind-label, source-map, or identity-map
fields, and writing it never modifies the capture.

The preflight is structural wording only. Its output must not be described
as answer quality, benchmark validation, readiness, or Alpha superiority; a
`structural_pass` means only that the configured local structural checks held
for the supplied text and prompt. Comparative interpretation of baseline
versus routed outputs remains out of scope for this harness.

### Checking prompt anchors before you capture

The lift preflight above runs on routed outputs, so it can only run after the
operator has already done the manual ghost-chat work. To catch anchoring
problems at authoring time — before spending a manual run — run the anchor
preflight over the case packet itself:

```bash
python scripts/operator_run_capture.py anchor-preflight \
  --case-packet tests/fixtures/operator_run_capture/pr646_substantive_lift_case_packet.json
```

For each case it reports one state:

- `anchor_bearing` — the prompt carries extractable case anchors (files, PR or
  issue numbers, lane IDs, backticked spans, identifier tokens), so the lift
  contract's anchoring checks will be meaningful for that prompt.
- `anchor_free` — the prompt has no extractable anchors, so the lift anchoring
  checks would be vacuous. This is **informational, not a defect**: a
  low-headroom prompt is legitimately anchor-free. If the prompt is meant to be
  high-headroom, add the concrete objects it should force the answer to engage.
- `invalid_case` — the case is malformed or has an empty prompt.

By default the command exits 0 for a well-formed packet (anchor-free cases are
reported but not treated as errors), and exits 1 only when a case is
malformed. Pass `--require-anchors` to opt into a stricter authoring gate that
also lists anchor-free prompts as needing attention (exit 1) — useful when a
packet is intended to be entirely high-headroom. The optional `--report-out`
writes a local JSON report; like the lift-preflight report it is not a capture
file, not an evidence packet, not an input to `export`, and carries no score,
rank, winner, blind-label, source-map, or identity-map fields. The command
never modifies the case packet.

This is a structural anchor-presence check only. Reporting a prompt as
`anchor_bearing` says nothing about answer quality, benchmark validation,
readiness, or Alpha superiority; it means only that the prompt contains the
kind of concrete objects the lift anchoring checks look for.

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
