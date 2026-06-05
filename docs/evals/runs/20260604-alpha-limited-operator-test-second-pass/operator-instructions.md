# Operator Instructions

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-SECOND-PASS-001`

Status: packet prepared, second-pass test not yet executed

## Scope

Run only the tasks in `operator-test-task-set.md` if a separate execution lane authorizes the second-pass manual prompt-contract simulation. This packet itself does not authorize execution, scoring, import, external updates, or Batch C work.

## Before execution

- Confirm the execution lane is separate from this packet-preparation lane.
- Confirm the source context is limited to the files listed in `README.md`.
- Confirm the feedback form and result log are blank before use.
- Confirm no prior evidence packet, interpretation packet, post-results decision packet, or PR #294 refinement packet will be edited during execution.
- Prepare a raw-artifact capture location outside this preparation PR if execution is authorized.

## Execution procedure

For each task:

1. Copy the exact **Prompt to submit** from `operator-test-task-set.md`.
2. Submit only that task prompt to the manual prompt-contract simulation surface.
3. Preserve the raw artifact exactly as returned, including any lead-ins, wrapper labels, `standard:` artifacts, labels, headings, caveats, or malformed output.
4. Do not clean, normalize, trim, rewrite, or repair the raw artifact.
5. Fill the blank result-log fields for that task.
6. Fill the blank feedback-form fields for that task.
7. Record `stop_condition_reached_yes_no` and `stop_condition_id_or_summary` for every task.
8. Do not compare to first-pass feedback until all raw artifacts and task-level feedback entries are preserved.

## Scoring dimensions to preserve

Use the same 0-3 rating dimensions preserved from the earlier imported operator feedback:

- direct usefulness
- brevity
- answer-first
- no over-frame
- claim boundary
- evidence boundary
- no invention
- stop-condition handling
- usable next action
- usable with minor edits

## Stop-condition handling

A stop condition should be recorded when a task asks for missing-result reconstruction, invented ratings, unsupported readiness, unsupported comparative claims, unexecuted-result claims, external updates, Batch C work, or any action outside the authorized evidence boundary.

Stop-condition fields are mandatory for every task, even when the operator records `no`.

## Raw artifact preservation

Preserve raw artifacts exactly. Do not remove:

- visible process-style lead-ins;
- wrapper labels;
- `standard:` artifacts;
- unnecessary `Replacement:` labels;
- memo-style framing;
- extra caveats;
- stop-condition text;
- formatting defects.

These artifacts are the subject of the second-pass packet and must remain available for later review if an execution lane is authorized.

## Non-actions during this packet

Do not:

- run providers or local models as part of this preparation PR;
- call `/v1/solve`;
- score or import results in this preparation PR;
- edit first-pass feedback, ratings, totals, or notes;
- update Google Sheets;
- start Batch C;
- make readiness, validation, superiority, benchmark, provider, runtime, local-model, MVP, or production claims.
