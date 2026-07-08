# Workflow Map

## Workflow A: Review packet readiness

The operator selects or lands on a current packet. The workbench shows packet id, path, packet type, lifecycle state, required artifacts, missing artifacts, and whether the packet is ready for output collection, scoring, interpretation, design follow-up, or stop.

## Workflow B: Compare Alpha/routed vs plain/baseline

The operator checks whether both sides exist, whether source identities are hidden or reviewed, whether scoring is blank/locked/interpreted/blocked, and what claim boundary applies. The workbench must distinguish comparison setup from scoring and final interpretation.

## Workflow C: Inspect route/expert context

The operator sees whether task interpretation, route/expert/persona, SAFE-OUT, confidence, shortlist, fallback, or route metadata exists. Missing route metadata should be shown as diagnostic absence, not as failure by itself.

## Workflow D: Decide next safe action

The workbench selects one next safe action. It states why the action is safe, what artifact it will produce, and what it will not authorize.

## Workflow E: Stop or defer

If artifacts are incomplete, source identities are improperly exposed, scoring is unauthorized, claim boundaries are unclear, or route metadata is missing for a route-dependent review, the workbench must show stop/defer with the blocking reason and no execution-style action.
