# ALPHA-LIVE-EXPERT-STEP1-PARSE-001 · Recover Actionable Execution Prompts When Step 1 Metadata Is Missing

## Purpose

Fix the live expert-route fallback where an actionable execution-planning prompt
can enter generic clarify-only behavior when Step 1 provider metadata is empty,
malformed, non-JSON, or missing confidence.

## Context

After `ALPHA-CLARIFY-THRESHOLD-001` and `ALPHA-PRIMARY-ANSWER-EMPTY-001`, a
controlled live retest still showed Alpha Solver expert preview clarifying this
concrete prompt while the plain provider produced a direct plan:

> Create a two-hour operator test plan for /dashboard/expert-preview that
> separates setup, prompt runs, evidence capture, and rollback.

The live response showed mode `clarify`, confidence `unavailable`, no surfaced
considerations, and no surfaced assumptions. This indicates Step 1 metadata was
missing, unavailable, or unparseable, bypassing the existing confidence-band
fallback for actionable execution-planning prompts.

## Scope

In scope:

- Narrowly recover actionable execution-planning prompts when Step 1 confidence
  metadata is unavailable.
- Default to `answer_with_assumptions` only when the prompt is concrete and
  recognized by the existing actionable execution-planning heuristic.
- Add safe default assumptions when Step 1 returns none.
- Preserve the primary-answer fallback so an empty Step 2 answer still returns a
  direct two-hour operator test plan.
- Add no-network API and expert-preview UI coverage.

Out of scope:

- Global clarification disablement.
- Broad routing rewrites.
- Provider selection changes.
- Dashboard auth/session/CSRF changes.
- Request metrics changes.
- Live OpenAI enablement, Cloud Run deployment, or Google Sheets updates.
- Claims of MVP validation, Alpha Solver superiority, production readiness,
  broad runtime readiness, answer-quality benchmark success, exact billing
  accuracy, or provider reasoning orchestration.

## Requirements

1. The retest prompt must not return generic clarify-only behavior solely
   because Step 1 confidence metadata is missing or unparseable.
2. Missing Step 1 confidence for concrete actionable execution-planning prompts
   should use `answer_with_assumptions`.
3. The final answer must include a direct two-hour operator test plan.
4. The answer must preserve setup, prompt runs, evidence capture, and rollback.
5. If Step 1 returns no assumptions, safe defaults should cover supervised
   operator preview only, local rollback availability, claim boundaries, and
   sanitized evidence.
6. Genuinely underspecified prompts must still clarify.
7. Unsafe or high-risk prompts must still block or clarify as appropriate.
8. Existing `ALPHA-CLARIFY-THRESHOLD-001`,
   `ALPHA-PRIMARY-ANSWER-EMPTY-001`, and `ALPHA-FORMAT-PRESERVATION-001`
   behavior must remain intact.

## Acceptance criteria

- No-network `/v1/solve` tests simulate empty, malformed, non-JSON, and
  missing-confidence Step 1 responses for the retest prompt.
- Those tests return `mode=answer_with_assumptions`, a non-empty primary answer,
  the requested plan sections, and default safe assumptions.
- A no-network `/dashboard/expert-preview` test renders the direct deliverable
  rather than the generic clarify message.
- Existing clarify, block/safe-out, request metrics, format-preservation, and
  primary-answer fallback tests continue to pass.

## Validation expectations

```bash
git diff --check
python -m pytest tests/test_api_endpoints.py -q
python -m pytest tests/ui/test_expert_preview.py -q
python -m pytest -q
```

## Backlog impact

`ALPHA-LIVE-EXPERT-STEP1-PARSE-001` should be marked Done only if this PR is
merged. It was discovered during the post-PR #225 controlled live retest and is a
pre-MVP blocker for the supervised live checkpoint. This does not validate the
MVP, prove Alpha Solver superiority, prove production readiness, prove broad
runtime readiness, prove answer-quality benchmark success, prove exact billing
accuracy, or prove provider reasoning orchestration.
