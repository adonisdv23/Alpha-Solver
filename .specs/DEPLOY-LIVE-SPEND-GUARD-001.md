# DEPLOY-LIVE-SPEND-GUARD-001 · Live Provider Spend Guard for Expert Preview

## Purpose

Add a narrow fail-closed spend guard before any live OpenAI-backed operator
testing of `/dashboard/expert-preview` on Cloud Run. The guard applies only to
the authenticated dashboard preview route and does not enable live OpenAI.

## Scope

In scope:

- keep `MODEL_PROVIDER=local` preview behavior unchanged;
- require an explicit `ALPHA_LIVE_PREVIEW_ENABLED=true` opt-in before preview
  submissions may use `MODEL_PROVIDER=openai`;
- enforce a per-process preview request cap via
  `ALPHA_LIVE_PREVIEW_MAX_REQUESTS`;
- block before provider client construction or provider calls when the opt-in is
  absent/false or the cap has been reached;
- render safe user-facing block messages that preserve the submitted prompt;
- log server-side allow/block decisions without secrets, prompts, raw headers,
  raw request bodies, or provider payloads;
- document the environment variables required for approved live-provider preview
  testing.

Out of scope:

- enabling live OpenAI in Cloud Run;
- deploying to Cloud Run;
- making real OpenAI calls in tests;
- persistent quota storage or billing dashboards;
- changes to dashboard auth/session/CSRF behavior;
- changes to provider expert-pass behavior after a request is allowed;
- Google Sheets/backlog workbook updates.

## Guard design

The guard lives in the `/dashboard/expert-preview` POST route because that route
is the immediate Cloud Run live-testing surface. It checks `MODEL_PROVIDER` after
CSRF/session middleware has accepted the request and before the route calls the
shared solve path.

When `MODEL_PROVIDER` is not `openai`, the guard is bypassed so local-provider
smoke testing remains unchanged. When `MODEL_PROVIDER=openai`, submissions are
blocked unless `ALPHA_LIVE_PREVIEW_ENABLED` is truthy (`1`, `true`, `yes`, or
`on`). Allowed live-preview submissions consume one per-process cap slot. The
cap comes from `ALPHA_LIVE_PREVIEW_MAX_REQUESTS`; if unset, the default is `1`
allowed preview submission per service instance. Invalid, zero, or negative caps
fail closed.

## Environment variables

| Variable | Default | Meaning |
| --- | --- | --- |
| `MODEL_PROVIDER` | `local` | `openai` selects the live provider path guarded by this spec. |
| `ALPHA_LIVE_PREVIEW_ENABLED` | unset/false | Must be truthy before `/dashboard/expert-preview` may call the OpenAI provider path. |
| `ALPHA_LIVE_PREVIEW_MAX_REQUESTS` | `1` | Per-process cap for allowed live preview submissions. |
| `OPENAI_API_KEY` | unset | Required only for explicitly approved live-provider testing; never committed. |

## Acceptance criteria

- Local-provider preview submit still returns `200` and renders both panes.
- OpenAI-provider preview submit is blocked before provider calls when
  `ALPHA_LIVE_PREVIEW_ENABLED` is absent or false.
- OpenAI-provider preview submit is allowed when live preview is enabled and the
  cap permits, using fake-provider tests only.
- Further preview submits are blocked before provider calls once the configured
  cap is reached.
- Blocked responses preserve the submitted prompt and do not render secrets, raw
  headers, bearer tokens, API keys, raw request bodies, or raw provider payloads.
- CSRF rejection and dashboard login/session behavior remain unchanged.
- Provider expert-pass behavior remains unchanged when the guard allows a
  request.

## Backlog impact

`DEPLOY-LIVE-SPEND-GUARD-001` should be marked Done only if the PR implementing
this spec is merged. `DEPLOY-CLOUDRUN-LIVE-OPENAI-001` remains Held until the
operator explicitly approves live-provider testing after this guard is merged and
deployed. This spec does not validate the MVP, claim production readiness, or
claim provider reasoning orchestration.
