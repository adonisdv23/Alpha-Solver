# Post-Results Decision Framework

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-POST-RESULTS-DECISION-FRAMEWORK-001`

Status: allowed decisions defined before results import or interpretation.

## Preconditions before using this framework

This framework may be applied only after a separate, explicit lane has:

1. imported actual limited operator-test artifacts from the manual operator run;
2. preserved the evidence chain without mutating source artifacts;
3. interpreted the imported feedback and defects within the portable-surface claim boundary; and
4. documented the interpretation without scoring, rescoring, unblinding, provider calls, runtime measurement, or Batch C execution unless separately authorized by a later spec.

If those preconditions are not satisfied, the only allowed decision is to continue treating the operator-test packet as prepared but not yet usable for post-results decisions.

## Decision principles

Post-results decisions must be grounded in imported and interpreted operator feedback only. They must not convert operator feedback into benchmark proof, MVP validation, production readiness, broad Alpha superiority, `/v1/solve` behavior, provider behavior, routing behavior, or exact billing evidence.

The decision maker must select the narrowest lane that addresses the interpreted evidence. If evidence is incomplete, inconsistent, missing provenance, or outside the portable surface, the decision must prefer evidence repair or pause over progression.

## Allowed decisions

### 1. Keep current portable contract for a second operator pass

Allowed when interpreted feedback indicates the current portable contract is usable enough to preserve unchanged for another manual operator pass, but the evidence is still too limited for readiness claims.

This decision may authorize a second-pass operator-test lane that repeats or extends manual portable-surface feedback collection. It must not authorize Batch C execution, runtime wiring, provider orchestration, `/v1/solve` measurement, or production-readiness claims.

### 2. Targeted refinement

Allowed when interpreted feedback identifies specific, bounded defects in answer-first behavior, brevity/control, claim-boundary handling, evidence discipline, stop-condition behavior, artifact handling, or next-action quality.

This decision may authorize a narrow portable-contract follow-up refinement. It must preserve existing useful behavior and must not broaden into runtime, provider, model, routing, capture, scoring, rescoring, or unblinding changes.

### 3. Rerun limited operator test

Allowed when the operator run is procedurally incomplete, affected by execution ambiguity, missing required task coverage, missing required feedback fields, or otherwise insufficient to support a stable interpretation.

This decision may authorize rerunning the limited manual operator test or a tightly corrected version of it. It must not fill gaps by memory, inference, invented results, or external planning-ledger claims.

### 4. Repair evidence chain

Allowed when artifacts, provenance, preservation notes, result logs, defect logs, or claim-boundary records are incomplete, inconsistent, or not repo-preserved enough to support a decision.

This decision may authorize an evidence-repair lane limited to artifact preservation, provenance clarification, missing-template correction, or documentation reconciliation. It must not reinterpret absent evidence as results and must not alter protected raw/scored artifacts or operator maps.

### 5. Pause progression

Allowed when interpreted feedback reveals serious defects, unsafe claim behavior, fabricated-result risk, stop-condition failure, artifact-discipline failure, or any ambiguity that makes progression unsafe.

This decision blocks progression until a later approved lane resolves the issue. It may recommend a repair, refinement, or rerun lane, but it must not proceed to readiness review or Batch C review.

### 6. Prepare readiness-review lane only if evidence is strong and defects are low

Allowed only when imported and interpreted operator-test evidence is strong, internally consistent, repo-preserved, portable-surface bounded, and shows low defect severity/frequency.

This decision may prepare a readiness-review lane. Readiness review means review only: it may assess whether future progression should be considered, but it does not execute Batch C, validate MVP readiness, prove benchmark success, establish production readiness, or authorize runtime/provider/model/routing changes.

## Decision output requirements

Every post-results decision must state:

- selected decision;
- source interpretation artifact used;
- evidence boundary;
- defects or evidence gaps that drove the decision;
- explicitly blocked lanes and claims;
- exact next lane, if any; and
- confirmation that no scoring, rescoring, unblinding, provider calls, `/v1/solve` measurement, Batch C execution, Google Sheets update, or runtime/provider/model/routing change is authorized by the decision itself.

## Tie-breakers

When more than one decision seems plausible:

1. choose evidence repair over interpretation if provenance is weak;
2. choose rerun over refinement if task coverage or feedback completeness is insufficient;
3. choose targeted refinement over readiness review if defects are material but bounded;
4. choose second pass over readiness review if feedback is positive but sample/evidence breadth remains limited; and
5. choose pause if any decision would require inventing results, expanding claims, or crossing protected surfaces.
