# Failure Triage

## First rule: preserve the checker

Do not fix a failure by weakening the checker, broadening exclusions, moving claims into logs, moving claims into `checks-run.md`, or changing tests. The safe response is to repair the underlying documentation or packet metadata so the existing checker continues to protect the evidence boundary.

## Broken path

A broken path usually means the docs path/link checker found a repo-relative local LLM reference that does not exist. Verify the target path in the checkout, then fix the link or path text in the referring doc. Do not delete preserved artifacts, rename packet directories, or replace a specific path with vague prose to avoid the checker.

## Stale selected-next state

A stale selected-next failure means one doc or packet presents conflicting current next actions, such as a no-further-lanes marker alongside a future selected lane. Keep historical selected-next references clearly labeled as prior, preserved, historical, previous, or closed. Keep the current state authoritative and explicit.

Current guardrail runbook state:

```text
NO_FURTHER_GUARDRAIL_RUNBOOK_LANES_SELECTED
```

## Missing blocker fallback

A missing blocker fallback failure means a packet or doc requires a blocker fallback lane but the expected `blocker-fallback-lane.md` file or explicit fallback section is missing. Add the fallback marker in the appropriate packet or runbook location; do not infer a fallback lane from memory, backlog sheets, or prior conversation.

Guardrail runbook blocker fallback lane:

```text
ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-POST-LEVEL-3-GUARDRAIL-RUNBOOK-FIX-001
```

## Missing evidence boundary

A missing evidence-boundary failure means a packet or doc uses boundary-sensitive material without an authoritative boundary file or nearby boundary language. Add or repair explicit evidence-boundary, blocked-claims, non-actions, or non-claims language in an authoritative doc. Do not move the boundary only into command logs or `checks-run.md`.

## Decision marker present only in logs

If a final decision marker appears only in a log, `checks-run.md`, stdout capture, or recorded command output, it does not satisfy the packet consistency boundary. Place accepted decision markers in authoritative decision files such as packet README, accepted-result, final-status, selected-next, final-boundary, or blocked-claims files according to the packet structure.

## Unsupported readiness or benchmark claim

Unsupported readiness or benchmark language must be either removed or explicitly bounded as a blocked non-claim. Production readiness, MVP readiness, benchmark evidence, local model quality evidence, provider-orchestration evidence, Alpha superiority, billing evidence, dashboard readiness, `/v1/solve` readiness, broad runtime readiness, evidence-model promotion, provider fallback readiness, and hosted fallback readiness remain blocked unless a separate approved lane creates authoritative evidence. Do not create such evidence in this runbook lane.
