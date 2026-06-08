# Lane 02: local preflight runner code scaffold

## Objective

Create an offline fail-closed local preflight runner scaffold that reports readiness but does not execute implementation tasks.

## Source evidence to verify

Verify the local preflight runner spec: allowed local commands, forbidden commands, required checks, output artifacts, stop-state mapping, and fail-closed failure modes.

## Allowed changes

Local-only preflight orchestration helpers, command allowlist/blocklist data, preflight result schema integration, deterministic tests, inert fixtures if needed, and a lane-completion docs packet.

## Forbidden changes

Use `shared-forbidden-files.md` as the minimum blocklist. This lane must not introduce provider calls, hosted model calls, external API calls, credentials, browser automation, deployment, billing, route exposure, dashboard exposure, fallback, hosted fallback, source-artifact mutation, evidence promotion, autonomous approval, or autonomous merge.

## Tests expected

Preflight blocked-command detection, allowed-command classification, missing required docs stop, unclear branch/status stop, changed-file scope stop, and no provider/network/browser/deployment/billing access.

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

If Lane 01 is merged and GS done, select local preflight runner code scaffold; otherwise return to the blocker fallback lane.

## Blocker fallback lane

`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-10-TO-LEVEL-12-SELF-OPERATOR-IMPLEMENTATION-BRIDGE-FIX-001`
