# Failure Triage

## Broken path

Symptoms:

- The docs path/link checker reports a missing repo-relative local LLM path.

Safe response:

- Confirm whether the referenced path should exist.
- Correct the link to the current authoritative path if the document reference is stale.
- Create documentation only when the spec or accepted packet requires that artifact and the current lane permits it.
- Do not move or rename preserved source artifacts to satisfy a link.

## Stale selected-next state

Symptoms:

- The docs path/link checker or packet consistency checker reports contradictory selected-next state.
- A document says no further lanes are selected while also selecting a future implementation lane.

Safe response:

- Update the authoritative selected-next file to the accepted state.
- For this runbook lane, the required selected next action is:

```text
NO_FURTHER_GUARDRAIL_RUNBOOK_LANES_SELECTED
```

- Do not leave historical implementation lane text in a current selected-next section.
- If historical lane text must remain, clearly mark it as historical or closed context outside the current selected-next state.

## Missing blocker fallback

Symptoms:

- The packet consistency checker reports `missing required blocker-fallback-lane.md`.

Safe response:

- Add or restore the authoritative blocker fallback lane file when the packet requires one.
- For this runbook lane, the blocker fallback lane is:

```text
ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-POST-LEVEL-3-GUARDRAIL-RUNBOOK-FIX-001
```

- Do not infer a fallback lane from memory; use the lane value supplied by the accepted controlling lane or packet contract.

## Missing evidence boundary

Symptoms:

- The evidence-boundary checker reports risky language without nearby boundary wording.
- The packet consistency checker reports a missing evidence-boundary, blocked-claims, non-actions, or equivalent boundary file.

Safe response:

- Add explicit evidence-boundary language in the authoritative doc.
- State what the artifact does not prove.
- Keep the boundary close to any risky phrase.
- Do not use boundary language to imply the claim is accepted.

## Decision marker present only in logs

Symptoms:

- A required marker appears in `checks-run.md`, command output, or a log file but the checker still fails.

Safe response:

- Put required decision markers in authoritative decision/status files such as accepted-result, final-status, selected-next-action, final-boundary, blocked-claims, or the corresponding packet file required by the lane.
- Keep command logs as logs only.
- Do not fix by moving claims into logs or checks-run files.

## Unsupported readiness or benchmark claim boundary

Symptoms:

- The evidence-boundary checker reports language that sounds like unsupported readiness, quality, or benchmark evidence.

Safe response:

- Rewrite the statement as a non-claim, blocked claim, or explicit boundary.
- State that the docs-only artifact does not prove runtime readiness, model quality, provider behavior, benchmark results, billing behavior, dashboard behavior, or `/v1/solve` behavior.
- If the claim is intended to be made, stop and route it to the proper future evidence lane instead of changing this runbook.

## Checker failure that seems too strict

Safe response:

- Do not fix by weakening the checker.
- First update the documentation so the evidence boundary, path reference, selected-next state, fallback lane, or packet field is explicit.
- If the checker itself is truly wrong, use the blocker fallback lane instead of changing checker behavior in this docs-only runbook PR.
