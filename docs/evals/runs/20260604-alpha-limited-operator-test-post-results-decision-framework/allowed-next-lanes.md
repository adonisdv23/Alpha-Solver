# Allowed Next Lanes

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-POST-RESULTS-DECISION-FRAMEWORK-001`

Status: allowed post-results lane menu defined before results import or interpretation.

## Use boundary

These lanes become selectable only after a separate lane imports and interprets actual limited operator-test results. This file does not choose a lane, import results, interpret feedback, or claim readiness.

## Lane menu

### `ALPHA-LIMITED-OPERATOR-TEST-SECOND-PASS-001`

Use when the interpreted evidence supports keeping the current portable contract unchanged for another manual operator pass.

Allowed scope:

- prepare or run a second portable-surface operator pass under a separately approved lane;
- preserve operator feedback and defects;
- maintain claim boundaries from the limited operator-test packet.

Not allowed:

- Batch C execution;
- runtime or `/v1/solve` measurement;
- provider orchestration;
- production, MVP, or benchmark claims.


### `ALPHA-LIMITED-OPERATOR-TEST-RERUN-001`

Use when the first limited operator-test run cannot support interpretation because it was incomplete, blocked, or invalid.

Applies when:

- the first operator run was incomplete;
- the tested surface was wrong or blocked;
- the evidence bundle was too incomplete for interpretation;
- a stop condition requires rerun after repair; or
- the operator did not complete enough tasks.

Allowed scope:

- redo the limited portable-surface operator test under a separately approved rerun lane;
- preserve corrected execution notes, operator feedback, defects, and evidence-chain records;
- document why the prior run cannot be used as a valid first pass.

Not allowed:

- filling gaps in the prior run by memory, inference, external ledgers, or invented results;
- treating an incomplete, blocked, or invalid first run as a valid pass;
- Batch C execution, runtime work, provider calls, `/v1/solve` measurement, or readiness claims.

Distinction from second pass:

- `ALPHA-LIMITED-OPERATOR-TEST-SECOND-PASS-001` is a follow-up run after a valid first pass.
- `ALPHA-LIMITED-OPERATOR-TEST-RERUN-001` is a redo because the first run was incomplete, blocked, or invalid.

### `ALPHA-PORTABLE-CONTRACT-FOLLOWUP-REFINEMENT-001`

Use when interpreted feedback identifies bounded portable-contract defects that warrant targeted refinement.

Allowed scope:

- refine portable contract wording or docs within the interpreted defect boundary;
- add or update focused portable-surface tests if code changes are separately authorized;
- preserve answer-first, brevity/control, evidence-boundary, stop-condition, and artifact-discipline goals.

Not allowed:

- runtime, provider, model, routing, capture, scoring, rescoring, or unblinding changes;
- broad refactors;
- readiness, benchmark, or validation claims.

### `ALPHA-OPERATOR-TEST-EVIDENCE-REPAIR-001`

Use when imported artifacts, provenance, logs, preservation notes, or claim-boundary records are incomplete or inconsistent.

Allowed scope:

- repair documentation of the evidence chain;
- reconcile missing or inconsistent preservation records;
- document why a decision cannot yet be made.

Not allowed:

- fabricating feedback, defects, outcomes, scores, or conclusions;
- mutating protected raw/scored artifacts or operator maps;
- using external ledgers as source evidence when repo artifacts conflict.

### `ALPHA-PORTABLE-SURFACE-READINESS-REVIEW-001`

Use only when interpreted limited operator-test evidence is strong, defects are low, and the review remains portable-surface bounded.

Allowed scope:

- prepare a review of whether the portable surface is ready for a later, separately approved progression decision;
- enumerate remaining evidence gaps and blocked claims;
- preserve limited-evidence language.

Not allowed:

- production-readiness conclusion;
- MVP validation;
- runtime or provider readiness;
- `/v1/solve` claims;
- Batch C execution.

### `ALPHA-BATCH-C-READINESS-REVIEW-001`

Use only as review, not execution, and only if imported and interpreted evidence is strong, defects are low, and the review explicitly preserves all blocked execution boundaries.

Allowed scope:

- evaluate whether a future Batch C execution proposal should be drafted;
- list prerequisites, evidence gaps, and stop conditions;
- confirm what remains unproven.

Not allowed:

- executing Batch C;
- preparing scored packets, capture runs, unblinding, rescoring, or provider calls;
- claiming Batch C readiness as established by operator feedback alone.

## Selection rule

Select exactly one next lane per post-results decision. If the evidence supports more than one lane, choose the narrowest lane that resolves the immediate blocker before considering broader review.
