# Decision Templates

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-POST-RESULTS-DECISION-FRAMEWORK-001`

Status: post-results decision templates prepared before results import or interpretation.

## Template: keep

```md
# Post-Results Decision: Keep Current Portable Contract

Decision: keep current portable contract for a second operator pass.

Source interpretation artifact: `<path-to-post-results-interpretation>`

Evidence boundary: imported and interpreted limited operator-test feedback only; portable surface only.

Rationale:
- `<summarize interpreted support without adding new results>`
- `<summarize why defects do not require immediate refinement>`

Next lane: `ALPHA-LIMITED-OPERATOR-TEST-SECOND-PASS-001`

Blocked:
- Batch C execution
- runtime wiring
- `/v1/solve` measurement
- provider orchestration
- production readiness
- MVP validation
- public user testing
- benchmark success
- exact billing claims

Confirmation: this decision does not score, rescore, unblind, call providers, update Sheets, execute Batch C, or modify runtime/provider/model/routing behavior.
```

## Template: refine

```md
# Post-Results Decision: Targeted Portable-Contract Refinement

Decision: targeted refinement.

Source interpretation artifact: `<path-to-post-results-interpretation>`

Evidence boundary: imported and interpreted limited operator-test feedback only; portable surface only.

Defects to address:
- `<bounded defect family>`
- `<bounded defect family>`

Out of scope:
- runtime/provider/model/routing changes
- capture, scoring, rescoring, or unblinding changes
- Batch C execution
- readiness, benchmark, MVP, production, or public-testing claims

Next lane: `ALPHA-PORTABLE-CONTRACT-FOLLOWUP-REFINEMENT-001`

Confirmation: this decision authorizes only a narrow follow-up refinement lane and does not invent results or broaden the evidence boundary.
```

## Template: rerun

```md
# Post-Results Decision: Rerun Limited Operator Test

Decision: rerun limited operator test.

Source interpretation artifact: `<path-to-post-results-interpretation>`

Evidence boundary: imported artifacts were insufficient for a stable post-results decision.

Reason rerun is required:
- `<first run incomplete, wrong/blocked surface, incomplete evidence bundle, stop-condition rerun requirement, insufficient completed tasks, or equivalent issue>`

Next lane: `ALPHA-LIMITED-OPERATOR-TEST-RERUN-001`

Blocked:
- filling gaps from memory
- fabricating feedback, defects, outcomes, or scores
- Batch C execution
- runtime, provider, `/v1/solve`, production, MVP, public-testing, benchmark, or exact-billing claims

Confirmation: this decision does not treat incomplete artifacts as results and does not authorize protected-surface changes.
```

## Template: pause

```md
# Post-Results Decision: Pause Progression

Decision: pause progression.

Source interpretation artifact: `<path-to-post-results-interpretation>`

Evidence boundary: imported and interpreted limited operator-test feedback only; portable surface only.

Reason progression is paused:
- `<serious defect, unsafe claim behavior, stop-condition failure, artifact-discipline failure, or unresolved ambiguity>`

Required before progression resumes:
- `<repair, refinement, rerun, or explicit future spec>`

Next lane: `<none, ALPHA-OPERATOR-TEST-EVIDENCE-REPAIR-001, or ALPHA-PORTABLE-CONTRACT-FOLLOWUP-REFINEMENT-001>`

Confirmation: no readiness-review, Batch C review, Batch C execution, runtime work, provider work, `/v1/solve` measurement, scoring, rescoring, unblinding, or claims expansion is authorized.
```

## Template: readiness review

```md
# Post-Results Decision: Prepare Readiness Review

Decision: prepare readiness-review lane only.

Source interpretation artifact: `<path-to-post-results-interpretation>`

Evidence boundary: imported and interpreted limited operator-test feedback only; portable surface only.

Why review is allowed:
- `<interpreted evidence is strong>`
- `<defects are low>`
- `<provenance is preserved>`

Next lane: `ALPHA-PORTABLE-SURFACE-READINESS-REVIEW-001` or `ALPHA-BATCH-C-READINESS-REVIEW-001`

Review-only limits:
- no Batch C execution
- no runtime wiring
- no `/v1/solve` measurement
- no provider orchestration
- no production-readiness claim
- no MVP-validation claim
- no benchmark-success claim
- no exact-billing claim

Confirmation: this decision prepares review only and does not execute or validate the reviewed lane.
```

## Template: blocked

```md
# Post-Results Decision: Blocked Request

Requested lane or claim: `<requested blocked lane or claim>`

Decision: blocked unless separately justified by a future evidence-backed spec.

Reason blocked:
- `<explain why imported operator feedback does not authorize this activity or claim>`

Allowed alternative, if any: `<one allowed lane from allowed-next-lanes.md or none>`

Blocked activities and claims preserved:
- Batch C execution
- runtime wiring
- `/v1/solve` measurement
- provider orchestration
- production readiness
- MVP validation
- public user testing
- benchmark success
- exact billing claims

Confirmation: this blocked decision does not import, invent, score, rescore, unblind, call providers, update Sheets, execute Batch C, or modify runtime/provider/model/routing behavior.
```
