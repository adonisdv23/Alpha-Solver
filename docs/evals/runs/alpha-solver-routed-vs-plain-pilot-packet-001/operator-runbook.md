# Operator runbook for a later pilot

1. Pre-run checks: confirm authorization, clean source-of-truth state, no open conflicting PRs, no secrets in prompts, and no readiness or superiority claims planned.
2. Task order: use `task-set.md` task ids in ascending order unless a separately recorded randomization plan is authorized.
3. Plain output collection: collect one plain single-model response per task without route metadata.
4. Alpha-routed output collection: collect one Alpha-routed response per task with classification, recommendations, reasons, warnings, fallback, boundary, confidence or answerability notes, and next action.
5. Preserve task ids exactly in every filename, note, and capture row.
6. Avoid revealing identities or route assignments prematurely by using neutral labels until authorized unblinding.
7. Capture evidence with timestamps, model/tool settings, prompt text, response summaries, and artifact paths; do not paste sensitive raw content into repo docs.
8. Stop if outputs contain sensitive data, secrets, credentials, private raw outputs, or unexpectedly identifying details; quarantine outside the repo and ask the operator for direction.
9. Avoid readiness and superiority claims; describe the exercise as a bounded pilot only.
10. After completion, run any separately authorized scoring pass, preserve raw output custody boundaries, update evidence indexes only with approved summaries, and keep claims bounded.

## Protocol boundaries

This packet does not execute the pilot. It does not call providers, run hosted models, run local models, execute tools, browse the web, generate Alpha outputs, generate baseline outputs, score outputs, change scores, unblind, inspect raw Alpha outputs, inspect raw baseline outputs, perform source-map work, mutate Google Sheets, add dependencies, expose `/v1/solve`, or expose dashboard or public API behavior. It makes no readiness, benchmark, production, public, security/privacy, provider, local-model, tool-quality, or Alpha-superiority claims.
