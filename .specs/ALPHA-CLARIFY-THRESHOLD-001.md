# ALPHA-CLARIFY-THRESHOLD-001 · Answer Execution Prompts with Assumptions When Sufficient

## Purpose

Improve expert-route mode selection so Alpha Solver answers actionable
execution-planning prompts with reasonable assumptions instead of replacing the
requested deliverable with clarify-only behavior.

## Context

During the post-fix controlled live retest, Prompt A asked:

> Create a two-hour operator test plan for /dashboard/expert-preview that
> separates setup, prompt runs, evidence capture, and rollback.

Plain provider output produced a direct two-hour operator test plan, but Alpha
Solver expert preview entered clarify mode with a generic clarification message.
The request already contained a concrete deliverable, route target, time box, and
required sections, so a useful answer with explicit assumptions was preferable.

`ALPHA-FORMAT-PRESERVATION-001` strengthened the final-answer prompt after the
expert route chooses to answer. This spec covers the earlier mode-selection
threshold so answerable execution-planning prompts are not blocked by unnecessary
clarification.

## Scope

In scope:

- Narrowly adjust expert-route clarify threshold behavior for actionable
  execution-planning prompts.
- Prefer `answer_with_assumptions` over `clarify` when a prompt includes an
  explicit execution-style deliverable and concrete target/context.
- Preserve requested sections for the retest prompt: setup, prompt runs,
  evidence capture, and rollback.
- Keep clarifying questions available for genuinely underspecified, unsafe,
  impossible, or high-risk requests.
- Add no-network API and expert-preview UI coverage using fake provider clients.

Out of scope:

- Global clarification disablement.
- Broad routing rewrites.
- Provider selection changes.
- Preview UI changes unless strictly necessary.
- Request metrics behavior changes.
- Dashboard auth/session/CSRF changes.
- Enabling OpenAI.
- Cloud Run deployment.
- Google Sheets or backlog workbook updates.
- Claims of MVP validation, Alpha Solver superiority, production readiness,
  broad runtime readiness, answer-quality benchmark success, exact billing
  accuracy, or provider reasoning orchestration.

## Requirements

1. Actionable execution-planning prompts with enough context should answer with
   assumptions instead of entering clarify mode.
2. The retest prompt should produce a direct two-hour plan, not a
   clarification-only response.
3. The answer should preserve setup, prompt runs, evidence capture, and rollback.
4. Assumptions and considerations may appear, but they must not replace the
   requested deliverable.
5. Clarifying questions should still be allowed when requests are genuinely
   underspecified, unsafe, impossible, or high-risk.
6. SAFE-OUT behavior must be preserved.
7. Claim-boundary behavior must be preserved.
8. `ALPHA-FORMAT-PRESERVATION-001` behavior must be preserved.
9. Provider selection, preview UI, request metrics, dashboard auth/session/CSRF,
   and deployment behavior must not change.

## Acceptance criteria

- A no-network API test proves the retest prompt does not return clarify-only
  behavior when the expert preview confidence is in the clarify band.
- The API response includes setup, prompt runs, evidence capture, and rollback
  in the primary answer.
- A no-network expert-preview UI test proves the primary Alpha answer is not the
  generic clarify message for the retest prompt.
- Existing control coverage still proves genuinely underspecified expert-route
  prompts can clarify.
- Existing format-preservation, claim-boundary, SAFE-OUT, request metrics, and
  expert-preview tests continue to pass.
- No live provider calls are required or made by the tests.

## Validation expectations

```bash
git diff --check
python -m pytest tests/test_api_endpoints.py -q
python -m pytest tests/ui/test_expert_preview.py -q
python -m pytest -q
```

If the full suite cannot complete, report the exact failure or environment
limitation and still report the focused checks.

## Backlog impact

`ALPHA-CLARIFY-THRESHOLD-001` should be marked Done only if this PR is merged.
This was discovered during the post-fix controlled live retest. It supports MVP
readiness by preventing answerable execution prompts from being blocked by
unnecessary clarification, but it does not validate the MVP, prove Alpha Solver
superiority, prove production readiness, prove broad runtime readiness, prove
answer-quality benchmark success, prove exact billing accuracy, or prove provider
reasoning orchestration.
