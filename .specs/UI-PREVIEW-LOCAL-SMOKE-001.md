# UI-PREVIEW-LOCAL-SMOKE-001 · Local-provider Expert Preview Smoke Fix

## Purpose

Fix the Cloud Run smoke failure where `/dashboard/expert-preview` returns `Preview request failed.` when the deployment is intentionally configured with `MODEL_PROVIDER=local`.

## Scope

- Preserve the authenticated expert-preview flow from `UI-PREVIEW-001`.
- Keep OpenAI disabled for the smoke path; the fix must pass with `MODEL_PROVIDER=local`.
- Keep the preview route submitting a plain request and an expert request through the shared `/v1/solve` logic.
- Treat `context.route` as a service/provider routing seam, not as a local solver runtime kwarg.
- Preserve deterministic local/offline solver execution for local provider mode.

## Non-goals

- No OpenAI enablement.
- No live provider smoke test.
- No answer-quality or superiority claim.
- No dashboard redesign.
- No broad solver refactor.

## Validation expectations

No-network tests should prove:

- `/v1/solve` in `MODEL_PROVIDER=local` accepts `context.route == "expert"` without invoking a provider.
- `/dashboard/expert-preview` in `MODEL_PROVIDER=local` can render both panes for `Define alpha in one sentence.`.
- The prompt remains preserved after submit.
- Existing OpenAI/fake-provider expert preview behavior remains covered by existing tests.
