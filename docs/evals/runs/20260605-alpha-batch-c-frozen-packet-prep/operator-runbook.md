# Operator Runbook

Lane ID: `ALPHA-BATCH-C-OPERATOR-RUNBOOK-PACKET-001`

## Scope

This runbook supports a future manual Batch C prompt-contract simulation using the frozen packet. It is not an execution record.

## Before execution

- Confirm a later approval explicitly authorizes the manual run.
- Confirm the task set has not changed after this packet was committed.
- Confirm the operator understands that raw outputs must be preserved before scoring or sanitization.
- Confirm private URLs, private transcripts, provider identifiers, private endpoints, keys, secrets, credentials, and operator-only notes must not enter public docs.
- Confirm the run is manual prompt-contract simulation only.

## Execution sequence for a future approved run

1. Create a private raw-capture workspace outside the public docs tree if sensitive material may appear.
2. Record run metadata in the raw artifact capture template.
3. Prompt tasks BC-001 through BC-012 in order.
4. Save each raw output immediately and immutably enough for reviewer inspection.
5. Record anomalies without editing the raw output.
6. Complete operator feedback after raw capture is complete.
7. Produce scorer-facing sanitized entries using the sanitization template.
8. Complete the redaction log and preservation checklist.
9. Only after all required artifacts exist, ask for a separate result-import lane.

## Raw output preservation rules

- Preserve the exact generated text for each task.
- Preserve task ID, prompt text, timestamp or run-order marker, and any anomaly note.
- Do not rewrite, normalize, summarize, or trim raw output before preservation.
- Do not replace raw output with a scored summary.
- If raw output is missing, mark a stop condition rather than reconstructing it.

## Operator stop conditions

Stop and do not import results if any required artifact is missing:

- raw output for any task;
- task prompt text used by the operator;
- operator feedback for any task;
- scorer-facing sanitized entry for any task;
- redaction log for sensitive removals;
- reviewer checklist.

## Out of scope for the operator runbook

- provider calls beyond any separately approved manual prompt-contract context;
- endpoint tests;
- source code changes;
- test changes;
- Google Sheets updates;
- scoring without raw artifacts;
- result interpretation in the execution packet.
