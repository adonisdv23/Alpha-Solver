# Candidate Views

This file defines possible future dashboard views without creating routes, UI code, API endpoints, frontend components, backend handlers, or data loaders.

## View 1: Evidence packet index

A future view may list accepted or draft packet directories with:

- Packet lane identifier.
- Packet title.
- Selected next action or selected next lane.
- Blocker fallback lane.
- Evidence boundary summary.
- Links to authoritative packet files.

Release gates before implementation:

- A source-of-truth packet index must be designated.
- The view must distinguish accepted packets from draft or historical packets.
- The view must show that displayed evidence does not create dashboard readiness or `/v1/solve` readiness.
- Level 6 must approve use of this design before any route or UI is created.

## View 2: Guardrail status view

A future view may display static guardrail checker names, expected commands, last recorded docs-only check results, and links to runbook pages.

Release gates before implementation:

- The implementation must not run checkers automatically unless separately authorized.
- The implementation must not weaken checker scripts, Makefile targets, tests, or CI.
- The view must label check results as static documentation/check evidence only.
- The view must not imply model quality, provider readiness, benchmark readiness, or production readiness.

## View 3: Claim-boundary view

A future view may present blocked claims, allowed language, risky phrases, and required nearby boundary language for operators reviewing evidence.

Release gates before implementation:

- The claim taxonomy must be accepted in an authoritative spec or packet.
- Risky claim detection must not be treated as proof that unflagged text is safe.
- The view must include explicit "does not create" and "does not expose" boundary statements.
- Level 6 controls whether this design is used.

## View 4: Audit trail view

A future view may display packet lineage, lane transitions, selected next actions, blocker fallback lanes, and checks run.

Release gates before implementation:

- The audit source must be immutable or explicitly versioned for the displayed snapshot.
- The view must show commit or artifact provenance when available.
- The view must preserve historical closed states and must not overwrite them with current selections.
- The view must not provide controls that mutate audit records unless a separate audited mutation design is accepted.

## View 5: Operator decision checklist

A future view may display default-off operator controls, required confirmations, and stop conditions before an operator proceeds to a later lane.

Release gates before implementation:

- All controls must be default-off.
- Any enabled control must require explicit operator intent and visible evidence boundary acceptance.
- Controls must not invoke providers, run models, expose routes, or modify runtime behavior in this design.
- Any future control that can execute work must be specified and accepted in a separate implementation lane.
