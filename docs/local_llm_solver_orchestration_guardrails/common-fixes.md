# Common Fixes That Preserve Guardrails

## Preserve checker intent

Allowed documentation fixes should make the contract clearer without loosening enforcement:

- Correct stale repo-relative links to existing local LLM solver orchestration docs.
- Add explicit evidence-boundary wording near risky phrases.
- Restore a missing selected-next action in the authoritative selected-next file.
- Restore a missing blocker fallback lane in the packet file that owns it.
- Move required decision markers from log-only locations into authoritative decision/status files.
- Clarify that an old lane token is historical, preserved, or closed when it is not the current selected-next action.

## Do not weaken the checker

Do not respond to a failure by changing checker scope, disabling phrase detection, excluding the failing document, or broadening accepted paths. This runbook is docs-only and does not modify checker scripts or tests.

## Do not move claims into logs

`checks-run.md`, command logs, stdout captures, and similar files are not authoritative decision files. Do not fix a missing decision marker by copying it only into a log or checks-run file.

## Do not infer missing fields from memory

If a packet is missing a selected-next action, blocker fallback lane, evidence boundary, or accepted decision marker, use the controlling lane, source-of-truth packet, or accepted spec. Do not reconstruct packet fields from memory.

## Preserve evidence boundaries

When adding boundary wording, be explicit:

- This docs-only runbook does not start the release-readiness ladder.
- This docs-only runbook does not start Level 4.
- This docs-only runbook does not change runtime behavior.
- This docs-only runbook does not change provider behavior.
- This docs-only runbook does not provide benchmark evidence; this is an explicit boundary, not an accepted claim.
- This docs-only runbook does not promote evidence.
