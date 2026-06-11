# Forbidden actions

Everything below remains forbidden for the Self Operator path after
closeout, in this prep lane and in every future operator-use lane, at all
times, regardless of approval text. This restates the canonical runbook
(sections 15-16) and the closeout guardrails; nothing here is new policy.

## Forbidden execution surfaces

- Provider calls and hosted model calls.
- Local model execution, unless a later explicit operator-supervised use
  lane authorizes it.
- External API calls.
- Browser automation.
- Exposure of `/v1/solve` or dashboard routes.
- Deployment actions of any kind.
- Billing actions of any kind.
- Credential or secret access, storage, display, or use.
- Execution of proposed task commands (the pipeline classifies proposed
  command text; it never executes it).

## Forbidden evidence actions

- Mutating, moving, rewriting, or deleting source artifacts.
- Recreating earlier evidence.
- Promoting evidence by summarizing it in place of re-reading it.
- Editing prior packets to make a defect disappear.
- Updating Google Sheets or any external ledger from repo lanes.

## Forbidden process actions

- Autonomous approval and autonomous merge.
- Reusing an operator confirmation across a different lane ID, run ID, or
  scope.
- Retrying a stopped run by weakening inputs.
- Implementing the final local status CLI in this lane (see
  `status-cli-deferred.md`).

## Forbidden claims

- Any affirmative readiness claim, including every phrase listed in
  `operator-use-contract.md` under "Explicit not-claims".
- Any claim that depends on missing evidence; report the missing evidence
  instead.

A violation of any item here is a stop condition: stop the lane, preserve
the evidence, and route per `stop-state-response-plan.md`.
