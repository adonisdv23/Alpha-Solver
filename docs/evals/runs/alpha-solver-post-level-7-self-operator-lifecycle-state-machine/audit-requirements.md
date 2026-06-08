# Audit Requirements

## Minimum audit fields

A future Self Operator implementation should record:

- Lifecycle run identifier.
- Current state and prior state.
- Transition timestamp.
- Actor or system component requesting the transition.
- Operator approval identifier when applicable.
- Scope statement.
- Evidence references.
- Credentials boundary.
- Fallback boundary.
- External visibility classification.
- Non-actions and blocked claims.
- Failure or blocked reason.
- Checks run and check results.

## Approval audit

Every approval-gated transition must preserve the exact approval context. A future implementation must be able to answer who approved, what was approved, when it was approved, which evidence was reviewed, and which actions remained prohibited.

## Failure audit

For `blocked` and `failed`, the audit record must identify the fail-closed trigger, the last safe state, and the required fallback path. Missing audit data is itself a fail-closed condition.

## Immutability expectation

Archived lifecycle records should be append-only or immutable. Corrections should be separate, timestamped, and clearly identified as metadata corrections rather than edits to historical facts.
