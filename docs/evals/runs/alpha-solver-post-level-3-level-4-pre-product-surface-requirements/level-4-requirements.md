# Level 4 Requirements

Level 4 must establish prerequisites before Alpha Solver can begin any product-surface or downstream readiness lane.

## Product-surface preconditions

Before product surface design, dashboard planning, or `/v1/solve` planning can begin, a later lane must have:

1. A bounded quality evaluation design that defines target tasks, excluded tasks, datasets or fixtures, scoring rules, human review expectations, and failure thresholds.
2. A claim-boundary matrix mapping each possible user-facing statement to required evidence.
3. A safety gate proving the proposed surface cannot present local orchestration artifacts as production, MVP, benchmark, or superiority evidence.
4. A route-exposure plan that remains design-only until a separate implementation lane explicitly authorizes route changes.
5. Operator controls for default-off behavior, explicit enablement, bounded inputs, bounded outputs, and safe stop behavior.
6. Observability requirements for traceable artifacts, run identifiers, decision logs, failure logs, and reproducible review records.

## Safety and claim-boundary requirements

Before any downstream lane proceeds, the lane must state:

- what evidence it can create;
- what evidence it cannot create;
- which claims are blocked;
- which artifacts are preserved source evidence;
- which artifacts are new design documents;
- which execution activities are forbidden;
- which stop conditions require fallback instead of continuation.

## Evidence categories required before downstream lanes

Later lanes must define required evidence for:

- quality evaluation design and later quality execution;
- API and `/v1/solve` design;
- dashboard design;
- provider orchestration design;
- provider fallback and hosted fallback design;
- billing design;
- MVP readiness review.

Each category must identify the minimum artifacts, pass/fail criteria, review owner, freshness expectation, contradiction handling, and rollback or blocker fallback path.

## Artifact preservation requirements

Later lanes must preserve accepted Level 2 and Level 3 artifacts as source evidence. They must not rewrite preserved artifacts, change closed decisions, or use command logs as substitutes for authoritative decision files.

## Operator controls and observability requirements

Later lanes must require default-off controls, explicit operator intent, finite timeouts or bounded execution where execution is later authorized, audit logs, reproducible check commands, and clear stop conditions. Observability requirements must be design prerequisites before any runtime or user-facing lane starts.

## Future pass/fail criteria requirements

Future packets must define pass/fail criteria before running or designing work that depends on those criteria. Criteria must be measurable, bounded to the lane, and unable to promote evidence outside the lane's scope.

## Rollback and fallback planning requirements

Every later lane must define a blocker fallback path and a rollback or non-promotion rule before it starts. A lane must stop rather than continue if evidence is missing, stale, contradictory, incomplete, or broader than the lane can safely interpret.

## Design-only versus execution evidence

Design-only packets define requirements and plans. They do not create execution evidence. Execution evidence requires a separate explicit lane that states the exact execution scope, safety limits, artifacts, and stop conditions.
