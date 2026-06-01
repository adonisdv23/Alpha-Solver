# UI-PREVIEW-001 · Authenticated Expert Preview UI

## Purpose

Add a compact authenticated dashboard preview that lets an operator compare an ordinary same-provider answer with the Alpha Solver expert-framed answer for the same prompt.

The preview is for supervised operator review only. It is not evidence of benchmarked answer quality or broad runtime readiness.

## Scope

- Add a protected dashboard route at `/dashboard/expert-preview`.
- Reuse the existing dashboard password/session/CSRF middleware.
- Reuse the existing `/v1/solve` request model and solve logic internally.
- Submit the plain pane as a same-provider request without `context.route == "expert"`.
- Submit the expert pane as a same-provider request with `context.route == "expert"`.
- Render the result as two compact panes:
  - `Plain provider output`
  - `Alpha Solver expert preview`
- Surface operator-friendly expert fields where present:
  - mode
  - confidence
  - complexity
  - call count
  - considerations
  - assumptions
  - clarifying questions
- Keep raw or engineering metadata out of the default view; details are limited to a small public metadata subset.
- Display an explicit supervised-preview disclaimer near the top of the page.

## Auth boundary

The preview route is under `/dashboard`, which is included in the existing dashboard protected prefixes. Logged-out users follow the existing dashboard auth-block behavior. State-changing preview submissions continue to require the existing CSRF header.

No second authentication mechanism is added.

## UI fields

The UI includes:

- prompt input box;
- compare submit button;
- required supervised-preview disclaimer;
- plain same-provider output pane;
- Alpha Solver expert preview pane;
- mode, confidence, complexity, and call-count labels;
- considerations list;
- assumptions list;
- clarifying questions list when present;
- a `Details` disclosure for limited public metadata.

## Validation expectations

No-network route-level tests should prove:

- logged-out users are blocked by the existing auth convention;
- logged-in users can load the preview page;
- the disclaimer is visible;
- fake provider calls render both plain and expert outputs;
- the plain pane uses the non-expert route;
- the expert pane uses `context.route == "expert"`;
- expert fields are surfaced;
- raw provider metadata, secrets, auth headers, API keys, raw request bodies, and raw response bodies are not displayed;
- UI copy stays within claim boundaries;
- existing `/v1/solve` behavior remains covered by existing endpoint tests.

## Backlog impact

`UI-PREVIEW-001` should be marked Done only after the PR implementing this spec is merged. The PR should be added as implementation evidence for this lane. Backlog spreadsheets are not edited from this repo task.

`PROVIDER-EXPERT-PASS-001` remains Done from PR #199. `CLARIFY-SURFACE-001`, `EVAL-ARTIFACT-PRESERVE-001`, and `EVAL-BEHAVIORAL-DEMO-001` remain separate lanes and should only be marked Done if their corresponding PRs were merged.

## Non-goals

- No MVP validation claim.
- No Alpha Solver superiority claim.
- No answer-quality superiority claim.
- No production-readiness claim.
- No broad runtime-readiness claim.
- No answer-quality benchmark success claim.
- No provider reasoning orchestration claim.
- No live provider tests.
- No broad eval benchmark.
- No provider orchestration, loops, fan-out, verify-revise behavior, or re-synthesis.
- No provider expert-pass behavior changes.
- No clarify behavior changes.
- No eval artifact preservation behavior changes.
- No behavioral demo checklist changes.
- No backlog workbook edits.
