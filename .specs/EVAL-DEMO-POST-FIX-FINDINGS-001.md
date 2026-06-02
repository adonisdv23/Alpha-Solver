# EVAL-DEMO-POST-FIX-FINDINGS-001 · Post-Fix Operator Retest Findings

## Purpose

Add a repo-tracked, safe, summarized findings artifact for the post-fix Alpha
Solver operator retest through `/dashboard/expert-preview`.

The artifact must record local-smoke and controlled live-provider retest
observations after the first demo follow-up fixes without storing raw provider
payloads, secrets, sensitive runtime values, full raw traces, or full raw model
outputs.

## Context

The first controlled 3-prompt operator demo surfaced follow-up issues around
long-response layout, request metrics, and format preservation. Follow-up fixes
were implemented under these work items:

- `UI-PREVIEW-RESPONSE-LAYOUT-001`;
- `ALPHA-FORMAT-PRESERVATION-001`;
- `UI-PREVIEW-REQUEST-METRICS-001`;
- `EVAL-DEMO-POST-FIX-RETEST-001`.

The operator redeployed latest `main`, confirmed local mode, ran a local UI
smoke, then ran a controlled live-provider retest with a low cap. The service was
rolled back to `MODEL_PROVIDER=local` afterward.

## Scope

In scope:

- Add `docs/evals/POST_FIX_OPERATOR_RETEST_FINDINGS.md`.
- Add this spec file.
- Register this spec in `.specs/INDEX.md`.
- Add short pointers from the post-fix retest packet and first demo findings.
- Record summarized local smoke observations.
- Record summarized controlled live retest observations for Prompt A and Prompt
  B.
- Compare pre-fix issues against post-fix retest results for layout, request
  metrics, format preservation, and clarification threshold behavior.
- Identify follow-up tickets `ALPHA-CLARIFY-THRESHOLD-001` and
  `POST-MVP-COST-LATENCY-OPTIMIZATION-001`.

Out of scope:

- Runtime behavior changes.
- Cloud Run config changes.
- Provider behavior changes.
- Expert-preview behavior changes.
- Dashboard auth/session/CSRF behavior changes.
- Enabling live OpenAI.
- Deploying Cloud Run.
- Persistent storage.
- Google Sheet or backlog workbook updates.
- MVP validation, Alpha Solver superiority, production-readiness, broad
  runtime-readiness, answer-quality benchmark success, exact billing accuracy,
  or provider reasoning orchestration claims.

## Findings artifact requirements

The findings artifact must include:

1. Local smoke findings for `MODEL_PROVIDER=local`, including dashboard load,
   metrics rendering, provider display, unknown or not-estimated token/cost
   handling, absence of secrets/raw payloads, and local-mode limitations.
2. Controlled live retest findings for the two approved prompts, including
   summarized plain and Alpha Solver observations, layout readability, metrics
   visibility, estimated cost visibility, defect status, and follow-up need.
3. Summarized metrics for each prompt: total preview latency, provider/model,
   route or mode, call count, token counts, and estimated cost. Costs must be
   framed as estimates, not exact billing.
4. A comparison of pre-fix issue versus post-fix result for:
   - long response layout;
   - request metrics visibility;
   - format preservation;
   - clarification threshold behavior.
5. Follow-up ticket `ALPHA-CLARIFY-THRESHOLD-001` for Prompt A entering clarify
   mode instead of producing the requested two-hour plan with reasonable
   assumptions.
6. Follow-up ticket `POST-MVP-COST-LATENCY-OPTIMIZATION-001` for post-MVP or
   shortly-after-MVP latency and estimated-cost optimization. This must not be
   marked as a blocker for the current MVP readiness checkpoint.
7. A final conservative interpretation that:
   - layout is fixed or improved;
   - request metrics are fixed and verified live;
   - format preservation is partially improved;
   - clarify threshold still needs a targeted fix;
   - cost/latency needs post-MVP optimization;
   - MVP is not validated by this retest.
8. Strict claim boundaries stating this retest does not validate the MVP, prove
   Alpha Solver superiority, prove production readiness, prove broad runtime
   readiness, prove answer-quality benchmark success, prove exact billing
   accuracy, or prove provider reasoning orchestration.
9. Safety and scope boundaries stating runtime behavior, Cloud Run config,
   provider behavior, expert-preview behavior, dashboard auth/session/CSRF
   behavior, live OpenAI enablement, persistent storage, and Google Sheets are
   unchanged by this work.

## Acceptance criteria

- `docs/evals/POST_FIX_OPERATOR_RETEST_FINDINGS.md` exists.
- `.specs/EVAL-DEMO-POST-FIX-FINDINGS-001.md` exists and is registered in
  `.specs/INDEX.md`.
- The findings artifact records only summarized observations and summarized
  metrics.
- The findings artifact does not store raw provider payloads, full raw outputs,
  secrets, headers, cookies, CSRF tokens, session values, API keys, bearer
  tokens, provider account identifiers, dashboard passwords, or full raw traces.
- The findings artifact compares pre-fix issues against post-fix results for
  layout, metrics, format preservation, and clarification threshold behavior.
- Follow-up tickets `ALPHA-CLARIFY-THRESHOLD-001` and
  `POST-MVP-COST-LATENCY-OPTIMIZATION-001` are included.
- Cost/latency optimization is marked post-MVP or shortly-after-MVP and not a
  blocker for the current MVP readiness checkpoint.
- Runtime behavior is unchanged.
- Cloud Run config is unchanged.
- Provider behavior is unchanged.
- Dashboard auth/session/CSRF behavior is unchanged.
- Live OpenAI is not enabled by Codex.
- No Google Sheet update is performed by Codex.

## Validation expectations

Because this is documentation/spec-only work, validation should include:

```bash
git diff --check
python -m pytest -q
```

If the full pytest suite is skipped or cannot complete, report why and still run
`git diff --check`.

## Backlog impact

`EVAL-DEMO-POST-FIX-FINDINGS-001` should be marked Done only if this PR is
merged. This supports `MVP-READINESS-CHECKPOINT-001`, creates follow-up
`ALPHA-CLARIFY-THRESHOLD-001`, and creates post-MVP task
`POST-MVP-COST-LATENCY-OPTIMIZATION-001`.

This does not validate the MVP, prove Alpha Solver superiority, or prove
production readiness. It also does not prove broad runtime readiness,
answer-quality benchmark success, exact billing accuracy, or provider reasoning
orchestration. Backlog spreadsheets and Google Sheets are not edited from this
repo task.

## Non-goals

- No runtime behavior change.
- No Cloud Run configuration change.
- No Cloud Run deployment.
- No provider behavior change.
- No expert-preview behavior change.
- No dashboard auth/session/CSRF change.
- No live OpenAI enablement.
- No persistent storage.
- No Google Sheets or backlog workbook update.
- No MVP validation claim.
- No Alpha Solver superiority claim.
- No production-readiness claim.
- No broad runtime-readiness claim.
- No answer-quality benchmark success claim.
- No exact billing accuracy claim.
- No provider reasoning orchestration claim.
