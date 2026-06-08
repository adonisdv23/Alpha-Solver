# Lane 06: local harness dry-run wrapper

## Objective

Create a local dry-run wrapper that exercises only offline preflight, approval, stop-state, and artifact-writing paths without provider, route, dashboard, browser, deployment, billing, or runtime production behavior.

## Source evidence to verify

Verify Level 8 local harness/UX acceptance boundaries if present through source packets, plus Level 9 artifact, preflight, approval, and stop-state specs.

## Allowed changes

Local-only dry-run wrapper, deterministic tests, inert fixtures, redacted local review artifacts, and a lane-completion docs packet.

## Forbidden changes

Use `shared-forbidden-files.md` as the minimum blocklist. This lane must not introduce provider calls, hosted model calls, external API calls, credentials, browser automation, deployment, billing, route exposure, dashboard exposure, fallback, hosted fallback, source-artifact mutation, evidence promotion, autonomous approval, or autonomous merge.

## Tests expected

Dry-run writes local redacted review artifacts only, no provider/network/browser/deployment/billing access, missing confirmation stop, forbidden surface stop, and no route/dashboard exposure.

Also run static safety regression checks proving no provider/network/browser/deployment/billing/credential access and no forbidden surface exposure.

## Stop conditions

Use `shared-stop-conditions.md`, including: stop if explicit operator confirmation is missing; stop if Level 10 static-test scaffold is not merged and GS done before runtime-adjacent scaffolds; stop if scope is unclear; stop if changed files exceed allowed scope.

## Required outputs

- Focused code scaffold only for this lane's local-only responsibility.
- Deterministic local tests or static checks for this lane's behavior.
- Lane-completion docs packet with changed-file proof, commands run, and evidence boundary.
- Stop-state or blocker note instead of partial implementation if any hard stop is hit.

## PR body requirements

- Lane ID and objective.
- Source evidence verified.
- Changed-file list and changed-file scope proof.
- Tests/checks run and results.
- Forbidden-surface proof.
- Evidence boundary and explicit non-actions.
- Selected next action and blocker fallback lane.

## Evidence boundary

The lane may create local-only redacted review artifacts only when explicitly authorized. It must not promote evidence, mutate source artifacts, claim production readiness, call providers, call external APIs, use credentials, automate browsers, deploy, bill, expose routes, or approve itself.

## Selected next action

If Lane 05 is merged and GS done, select local harness dry-run wrapper; otherwise split or fall back.

## Blocker fallback lane

`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-10-TO-LEVEL-12-SELF-OPERATOR-IMPLEMENTATION-BRIDGE-FIX-001`
