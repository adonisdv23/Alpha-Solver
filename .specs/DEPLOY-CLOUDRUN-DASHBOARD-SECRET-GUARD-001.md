# DEPLOY-CLOUDRUN-DASHBOARD-SECRET-GUARD-001 · Require Dashboard Secret for Bundled Cloud Run Preview Mount

## Objective

Tighten the bundled `service.app:app` dashboard mount guard so the Cloud Run MVP
preview dashboard mounts only when both required dashboard deployment values are
explicitly configured:

- `ALPHA_DASHBOARD_PASSWORD` is set and is not the documented default
  `alpha-dashboard`; and
- `ALPHA_DASHBOARD_SECRET_KEY` is set to a non-empty value.

This closes the deployment safety gap where a non-default password alone could
mount the bundled preview while dashboard auth fell back to a random runtime
session-signing secret.

## Scope

- Update only the bundled app's dashboard mount guard and warning text.
- Keep the shared dashboard auth/session/CSRF implementation unchanged after the
  dashboard is mounted.
- Document that the bundled Cloud Run preview dashboard fails closed if either
  required dashboard environment variable is missing or invalid.
- Add no-network tests for the password and secret-key mount matrix.

## Acceptance criteria

- Dashboard routes do not mount when `ALPHA_DASHBOARD_PASSWORD` is unset.
- Dashboard routes do not mount when `ALPHA_DASHBOARD_PASSWORD` is
  `alpha-dashboard`.
- Dashboard routes do not mount when `ALPHA_DASHBOARD_PASSWORD` is non-default
  but `ALPHA_DASHBOARD_SECRET_KEY` is unset or empty.
- Dashboard routes mount when `ALPHA_DASHBOARD_PASSWORD` is non-default and
  `ALPHA_DASHBOARD_SECRET_KEY` is non-empty.
- When dashboard routes do not mount, the JSON API remains available.
- Existing dashboard auth/session/CSRF behavior remains unchanged after mount.
- Provider behavior, expert-pass behavior, clarify behavior, eval behavior,
  preview behavior, and Cloud Run Docker behavior do not change.

## Backlog impact

`DEPLOY-CLOUDRUN-DASHBOARD-SECRET-GUARD-001` should be marked Done only after the
PR implementing this spec is merged. It is a deployment safety follow-up under
`DEPLOY-CLOUDRUN-EPIC-001`, should be completed before
`DEPLOY-CLOUDRUN-SMOKE-001`, and does not deploy Cloud Run, enable live OpenAI,
validate the MVP, or claim production readiness.

## Non-goals

- No Cloud Run deployment.
- No committed secrets or real secret requests.
- No Google Sheets or backlog workbook updates.
- No live OpenAI enablement.
- No Firebase Hosting.
- No custom domain support.
- No login redirect configurability.
- No JWT flake fixes.
- No live spend guard changes.
- No MVP validation claim.
- No Alpha Solver superiority claim.
- No production-readiness claim.
- No broad runtime-readiness claim.
- No answer-quality benchmark success claim.
- No provider reasoning orchestration claim.
