# Operator-Only Boundary

Lane: `ALPHA-SOLVER-POST-LEVEL-7-SELF-OPERATOR-MVP-SCOPE-MATRIX-PACKET-001`

## Operator-only decisions

The following decisions must remain operator-only in the earliest safe Self Operator MVP:

- Approving task scope, acceptance criteria, and evidence labels.
- Deciding whether a generated artifact is accurate, sufficient, or accepted.
- Authorizing any file creation or modification beyond an explicitly approved local docs/artifact scope.
- Authorizing tests or checks with side effects beyond local deterministic validation.
- Providing, changing, validating, or using credentials, tokens, secrets, or environment variables.
- Selecting or enabling providers, model routes, fallback paths, hosted execution, or `/v1/solve` exposure.
- Approving external communication, browser use, account actions, purchases, billing, deployments, release work, merges, or evidence promotion.
- Resolving conflicts between specs, packets, guardrails, product boundaries, and operator instructions.

## Operator-only actions

The Self Operator MVP may prepare local drafts for operator review, but the operator must perform or explicitly authorize:

- Any external action.
- Any irreversible action.
- Any cost-incurring action.
- Any credential-affecting action.
- Any provider-backed action.
- Any production, deployment, merge, release, or publication action.
- Any action that changes accepted evidence status.

## Required stop behavior

The Self Operator MVP must stop when:

- Confirmation is missing, ambiguous, or stale.
- The requested action is outside approved local artifact scope.
- A credential, provider, billing, deployment, browser, merge, or external-action boundary is implicated.
- Evidence labels or readiness claims would exceed accepted source evidence.
- Traceability cannot be preserved without exposing secrets or unreviewed payloads.
- Required checks fail or cannot be run.
