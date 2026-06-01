# DASHBOARD-LOGIN-REDIRECT-001 · Configurable Dashboard Login Redirect

## Objective

Fix the bundled `service.app:app` Cloud Run/operator preview login landing so a
successful dashboard login redirects to `/dashboard/expert-preview` instead of
`/requests`, while preserving the shared dashboard auth router's default landing
behavior for existing/custom consumers.

## Scope

- Add app-local configurability for the dashboard post-login redirect in
  `alpha.webapp.routes.auth`.
- Configure only the bundled `service.app:app` dashboard mount to use
  `/dashboard/expert-preview` after successful login.
- Keep the bundled app mounted only for login/auth and expert preview; do not
  mount `/requests`, `/settings`, `/run`, or `/jobs`.
- Keep dashboard session cookies, CSRF checks, lockout behavior, and fail-closed
  mount guard semantics unchanged.
- Update operator documentation that previously described the `/requests`
  post-login redirect as a known limitation.

## Acceptance criteria

- Successful login in bundled `service.app:app` redirects to
  `/dashboard/expert-preview`.
- Successful login still sets the dashboard session and CSRF cookies.
- Incorrect passwords still render the login page with `Invalid credentials`.
- Logged-out requests to `/dashboard/expert-preview` still redirect to `/login`.
- Logged-in requests to `/dashboard/expert-preview` render successfully.
- `/requests`, `/settings`, `/run`, and `/jobs` remain unmounted in the bundled
  Cloud Run/operator preview app unless independently mounted by future approved
  work.
- The default shared auth router login redirect remains `/requests` unless an
  application explicitly configures a different redirect target.
- No provider, OpenAI, expert-pass, clarify/eval, or Cloud Run Docker behavior
  changes.

## Backlog impact

`DASHBOARD-LOGIN-REDIRECT-001` should be marked Done only after the implementing
PR is merged. This is a UX cleanup after `DEPLOY-CLOUDRUN-SMOKE-001`; it does
not change Cloud Run deployment status, enable live OpenAI, validate the MVP, or
claim production readiness.

## Non-goals

- No mounting `/requests`, `/settings`, `/run`, or `/jobs` in the bundled app.
- No dashboard redesign.
- No auth/session/CSRF weakening.
- No dashboard fail-closed behavior changes.
- No OpenAI or provider behavior changes.
- No expert-pass, clarify, or eval behavior changes.
- No JWT flake fixes.
- No live spend guard changes.
- No Google Sheets or backlog workbook updates.
- No MVP-validation, Alpha Solver superiority, production-readiness, broad
  runtime-readiness, answer-quality benchmark success, or provider reasoning
  orchestration claims.
