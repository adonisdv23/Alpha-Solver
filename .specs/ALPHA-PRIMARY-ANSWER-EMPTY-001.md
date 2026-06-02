# ALPHA-PRIMARY-ANSWER-EMPTY-001 · Ensure Answer-with-Assumptions Returns a Primary Deliverable

## Purpose

Fix the expert-route defect where Step 1 can correctly select
`answer_with_assumptions` for an actionable operator planning prompt while the
primary answer returned to `/v1/solve` and rendered in `/dashboard/expert-preview`
is empty or not meaningfully populated.

## Context

During the controlled live retest after `ALPHA-CLARIFY-THRESHOLD-001`, this
prompt no longer entered clarify-only mode:

> Create a two-hour operator test plan for /dashboard/expert-preview that
> separates setup, prompt runs, evidence capture, and rollback.

The remaining blocker was that the expert preview displayed mode
`answer_with_assumptions` and surfaced considerations/assumptions, but the
primary Alpha answer box did not contain the requested two-hour operator test
plan.

## Scope

In scope:

- Preserve the `answer_with_assumptions` mode selected by
  `ALPHA-CLARIFY-THRESHOLD-001` for actionable execution-planning prompts.
- Ensure primary expert answers are non-empty when the expert route answers with
  assumptions.
- Preserve the requested setup, prompt runs, evidence capture, and rollback
  sections for the retest prompt.
- Keep considerations and assumptions available as metadata; they must not
  replace the primary deliverable.
- Add no-network API and expert-preview UI regression coverage.

Out of scope:

- Provider selection changes.
- OpenAI enablement, Cloud Run deployment, or live retesting.
- Dashboard auth/session/CSRF changes.
- Request metrics behavior changes.
- Google Sheets or backlog workbook updates.
- Claims of MVP validation, Alpha Solver superiority, production readiness,
  broad runtime readiness, answer-quality benchmark success, exact billing
  accuracy, or provider reasoning orchestration.

## Requirements

1. The retest prompt returns `mode=answer_with_assumptions` when confidence falls
   in the clarify band but the prompt is actionable.
2. `answer` and `final_answer` are non-empty for that mode.
3. The primary answer contains a direct two-hour operator test plan with setup,
   prompt runs, evidence capture, and rollback sections.
4. Considerations and assumptions remain available in their metadata fields.
5. Genuinely underspecified prompts may still clarify.
6. SAFE-OUT, claim-boundary, format-preservation, request metrics, live spend
   guard, dashboard auth/session/CSRF, and provider selection behavior are
   preserved.
7. No live provider calls are required for validation.

## Acceptance criteria

- API regression coverage proves an empty Step 2 provider answer in
  `answer_with_assumptions` mode is converted into a safe, direct primary
  operator test-plan deliverable for the retest prompt.
- Expert-preview UI regression coverage proves the primary answer pane renders
  that direct deliverable and still renders considerations and assumptions.
- Preview rendering prefers a non-empty final-answer compatibility alias when an
  `answer` key is present but blank.
- Existing clarify, metrics, format-preservation, SAFE-OUT, and claim-boundary
  tests continue to pass.

## Backlog impact

`ALPHA-PRIMARY-ANSWER-EMPTY-001` should be marked Done only if this PR is merged.
This defect was discovered during the clarify-threshold live retest after PR
#224. It remains a pre-MVP blocker until the fix is merged and live-retested.
This does not validate the MVP, prove Alpha Solver superiority, or prove
production readiness.
