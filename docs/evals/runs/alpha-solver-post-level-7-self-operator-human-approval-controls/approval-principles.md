# Approval Principles

## Default-to-stop rule

Self Operator must default to stop when approval state is missing or ambiguous.

This includes cases where approval is absent, stale, contradictory, partial, inherited from a different task, recorded for a different action, recorded for a different target, or recorded without enough detail to verify scope.

## Explicit approval only

Approval must be explicit, action-specific, target-specific, time-bounded, and recorded before a gated action is performed.

An operator's general intent, broad project goal, previous approval, issue description, backlog row, lane name, PR comment, or implied urgency is not enough by itself to authorize a gated action.

## Narrowest safe action

When approval is valid, Self Operator must execute only the narrowest approved action. If the next step would exceed the approved scope, Self Operator must stop and request a new approval record before proceeding.

## No approval by silence

Silence, lack of objection, timeout, ambiguous wording, or unavailable operator response must be treated as no approval.

## Auditability

Every gated action must be traceable to an approval record that identifies the operator, requested action, target, scope, constraints, timestamp, confirmation wording, and stop conditions.
