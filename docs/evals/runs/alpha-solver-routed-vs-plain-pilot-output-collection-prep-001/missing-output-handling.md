# Missing output handling

If operator-provided outputs are missing for any task, leave the task fields blank and mark the task as missing in `per-task-capture-index.md` during a future authorized collection update.

Do not backfill missing outputs by simulation, inference, Codex generation, prompt-contract drafting, provider calls, hosted-model calls, local-model calls, tool execution, browsing, or `/v1/solve` execution unless a separate later authorization explicitly permits that source.

A future collection lane must distinguish:

- operator-provided output present;
- operator-provided output missing;
- separately authorized execution output present;
- separately authorized execution failed or stopped.
