# POST657 Qualitative Run Packet Runbook

Lane: `POST657-QUALITATIVE-RUN-PACKET-001`

## Purpose and boundary

Prepare one local manual qualitative capture after PR #655 and PR #657 using
the current operator-run capture stack. This runbook is operator-facing setup
for capture, structural preflight, export, and reviewer handoff only. It does
not execute the manual review and does not change runtime behavior.

## Required files

- `tests/fixtures/operator_run_capture/post657_qualitative_case_packet.json`
- `docs/OPERATOR_RUN_CAPTURE.md`
- `alpha/eval/operator_run_capture.py`
- `scripts/operator_run_capture.py`
- `tests/fixtures/operator_run_capture/post655_lift_preflight_smoke_capture.json`
- `tests/fixtures/operator_run_capture/post655_lift_preflight_smoke_report.json`
- `.specs/OPERATOR-RUN-CAPTURE-SUBSTANTIVE-LIFT-PREFLIGHT-CLI-001.md`

## Exact command sequence

Run these commands from the repository root:

```bash
python scripts/operator_run_capture.py init \
  --case-packet tests/fixtures/operator_run_capture/post657_qualitative_case_packet.json \
  --out local/post657_qualitative_capture.json
```

After manually filling the capture file as described below:

```bash
python scripts/operator_run_capture.py validate \
  --capture local/post657_qualitative_capture.json

python scripts/operator_run_capture.py lift-preflight \
  --capture local/post657_qualitative_capture.json \
  --report-out local/post657_qualitative_lift_preflight_report.json

python scripts/operator_run_capture.py validate \
  --capture local/post657_qualitative_capture.json \
  --for-export

python scripts/operator_run_capture.py export \
  --capture local/post657_qualitative_capture.json \
  --out local/post657_qualitative_capture_packet.json
```

## Manual paste instructions

For each case in `local/post657_qualitative_capture.json`:

1. Paste the plain baseline answer into `baseline_output`.
2. Paste the full routed Alpha answer into `routed_output`.
3. Do not manually trim a full routed Alpha answer only because it has a
   leading `SOLUTION:` label; after PR #657, full routed answers may include
   that label and `lift-preflight` handles the leading envelope label.
4. Fill `route_metadata` only with route and provenance facts, such as the
   route observed, capture method, source artifact, prompt identifier, and
   relevant transcript provenance.
5. Keep qualitative notes, reviewer interpretations, concerns, and follow-up
   ideas outside `route_metadata`.
6. Set `validation_status` to `captured` only after both outputs are present
   and `route_metadata` is a non-empty object.
7. Set `validation_status` to `excluded` only when `exclusion_reason` is
   non-empty and explains why that case should not move to handoff.

## Preflight interpretation

`lift-preflight` is a local structural wording preflight over the routed output
and prompt. It is not answer quality, not scoring, not a benchmark, not readiness evidence, and not superiority evidence.

- `structural_pass` means only that configured local structural wording checks
  held for the supplied routed text and prompt.
- `structural_fail` means the answer should be reviewed or recaptured before
  qualitative review.
- `safe_out_not_applicable` is allowed for bounded `SAFE-OUT:` responses
  because the Substantive Lift answer-body contract does not apply to an honest
  non-answer.
- `anchor_checks_vacuous` means the prompt did not expose extractable anchors;
  this should usually be treated as packet-design feedback rather than as a
  finding about the routed answer.
- Missing prompt text, missing routed output, malformed cases, or excluded
  cases should be resolved according to `docs/OPERATOR_RUN_CAPTURE.md` before
  reviewer handoff.

## Export instructions

Run `validate --for-export` only after every non-excluded case has both pasted
outputs, a non-empty `route_metadata` object, and `validation_status:
captured`. Then run `export` to produce
`local/post657_qualitative_capture_packet.json`. The exported packet is the
handoff artifact; the preflight report is local operator context and is not an
input to export.

## Reviewer handoff instructions

Hand off these local artifacts together:

- `local/post657_qualitative_capture_packet.json`
- `local/post657_qualitative_lift_preflight_report.json`
- this runbook
- the case packet fixture

Ask the reviewer to read the captured outputs qualitatively against the case
prompts and the six requested moves: Intent, Assumes, Tradeoff,
Recommendation, Fails if, and Next. The reviewer should keep notes outside the
capture/export schema and should not add score, rank, winner, blind-label,
source-map, identity-map, or A/B identity-key fields.

## Explicit non-claims

This packet and runbook do not claim answer quality, benchmark results,
production suitability, public suitability, provider validation, local-model
validation, or Alpha superiority. They do not claim that a `structural_pass`
means a good answer. They do not make identity comparisons and do not ask the operator
or reviewer to score, rank, select winners, or turn the packet into a
benchmark.

## Stop conditions

Stop and report instead of proceeding if any of these conditions is observed:

- PR #655 is not merged on `main`.
- PR #657 is not merged on `main`.
- Issue #656 is not closed as completed.
- An open conflicting PR changes the same capture, preflight, packet, or
  runbook surface.
- `main` does not contain `scripts/operator_run_capture.py lift-preflight`.
- `main` does not contain
  `tests/fixtures/operator_run_capture/post655_lift_preflight_smoke_capture.json`.
- `python scripts/operator_run_capture.py validate --capture local/post657_qualitative_capture.json`
  reports schema errors that cannot be corrected by local paste edits.
- `lift-preflight` reports `structural_fail` for a non-excluded case and the
  operator cannot decide whether to review or recapture before handoff.
- The operator needs scoring, ranking, provider calls, local-model calls,
  runtime `/v1/solve` wiring, route/persona changes, or dashboard/API changes
  to proceed.
