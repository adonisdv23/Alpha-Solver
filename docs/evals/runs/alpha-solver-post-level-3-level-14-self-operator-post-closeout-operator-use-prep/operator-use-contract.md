# Operator-use contract

This contract governs every future operator use of the narrow operator-only
Self Operator path after release closeout. It restates the exact allowed
claim, fixes the explicit not-claims, and binds future use to the canonical
runbook and the closeout guardrails.

## Exact allowed claim

The narrow operator-only Self Operator path is eligible for the next operator-supervised review stage, based only on the accepted local evidence chain and completed closeout gates.

No other status claim is allowed. This claim is the complete claim surface.

## Explicit not-claims

The allowed claim is not MVP readiness, release readiness, production
readiness, hosted readiness, provider readiness, runtime readiness,
benchmark validation, or autonomous readiness. In particular, this is not:

```
MVP ready
release ready
production ready
runtime ready
provider ready
hosted ready
benchmark validated
autonomous ready
broad user ready
```

None of these phrases may be used as an affirmative status claim in any
future operator-use artifact. They may appear only as quoted forbidden
vocabulary, scan commands, or scan classifications.

## Contract terms for future use

1. Every future use is operator-supervised, local-only, and bounded by the
   canonical runbook
   (`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization/mvp-operator-runbook.md`).
2. Explicit operator confirmation per
   `operator-confirmation-requirements.md` is required before any supervised
   use; missing confirmation is a hard stop.
3. Allowed activity is limited to `allowed-use-scope.md`; everything in
   `forbidden-actions.md` remains forbidden regardless of approval text.
4. Outputs are written only below an explicit local output root per
   `artifact-output-root-plan.md`, redacted per `redaction-and-secrets.md`.
5. Stop states are terminal for the run and are handled per
   `stop-state-response-plan.md`; defects route to the blocker-fix lane, not
   to retries with weakened inputs.
6. Non-execution proof is preserved per
   `non-execution-proof-requirements.md`; source evidence is preserved per
   `evidence-preservation-rules.md`.
7. The final local status CLI is deferred per `status-cli-deferred.md` and is
   not a precondition for any step in this contract.
