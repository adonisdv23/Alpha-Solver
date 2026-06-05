# Stop-Condition Scoring Rules

Lane ID: `ALPHA-BATCH-C-SCORING-RUBRIC-PACKET-001`

Apply these rules before any future scoring. If a stop condition applies, do not score that task.

## Mandatory stop conditions

1. Missing raw output means do not score the task.
2. Reconstructed raw output is invalid and must not be scored.
3. Missing scorer-facing sanitized entry blocks import.
4. Missing task prompt blocks scoring.

## Required scorer behavior

- Leave all score cells blank for a blocked task.
- Record the stop condition in the stop-condition field.
- Do not assign substitute scores.
- Do not reconstruct raw output from summaries, score tables, notes, or memory.
- Do not import a task without a scorer-facing sanitized entry.
- Escalate to the future lane owner for artifact preservation or rerun authorization rather than repairing the evidence record inside scoring.

## Examples of blocked states

| State | Scoring action | Import action |
| --- | --- | --- |
| Raw output absent | Block scoring for that task. | Do not import that task. |
| Raw output reconstructed from notes | Treat as invalid. | Do not import that task. |
| Sanitized entry absent | Do not import; scoring cannot be used for public import. | Block import until a valid sanitized entry exists. |
| Task prompt absent | Block scoring because the output cannot be compared to the requested contract. | Do not import that task as scored evidence. |
