# Operator Roles

## Role boundary goals

Future product-surface work must define role boundaries before exposure. The goal is to prevent accidental enablement, unsupported claims, uncontrolled costs, hidden provider calls, and unreviewed manual overrides.

## Proposed roles

### Operator

The operator executes approved procedures within the approved scope. The operator may request enablement, perform checks, monitor audit output, and trigger stop conditions, but must not unilaterally broaden scope beyond the approved lane.

### Reviewer

The reviewer verifies that default-off behavior, explicit enablement, confirmation gates, audit requirements, and stop conditions are satisfied before exposure. The reviewer must be distinct from the person relying solely on convenience or speed to justify exposure.

### Release owner

The release owner records whether a future surface is eligible for a release milestone. The release owner must not treat this packet as product-readiness evidence.

### Emergency override owner

The emergency override owner may authorize a time-limited manual override only under documented override rules. The override owner must also ensure audit capture, rollback, and follow-up review.

### Level 6 control owner

Level 6 controls whether and how these controls are adopted. No role in this packet bypasses Level 6 adoption authority.

## Separation expectations

Future implementation lanes should avoid combining request, approval, operation, and override authority in a single undocumented action. Where one person must hold multiple roles, the overlap must be explicitly recorded and audited.
