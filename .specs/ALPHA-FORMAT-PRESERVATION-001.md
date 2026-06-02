# ALPHA-FORMAT-PRESERVATION-001 · Expert Answer Format Preservation

## Purpose

Improve the expert-route final answer behavior so Alpha Solver preserves a
user's requested output format, structure, headings, sectioning, and time boxes
while still surfacing assumptions, considerations, and conservative claim
boundaries.

## Context

During the first controlled 3-prompt operator demo, Prompt 3 asked:

> Create a two-hour operator test plan for /dashboard/expert-preview that
> separates setup, prompt runs, evidence capture, and rollback.

The plain provider output produced a direct time-boxed operator test plan. The
Alpha Solver expert preview surfaced useful considerations and assumptions, but
its final answer did not preserve the requested two-hour plan structure as
clearly. Investigation indicates the likely root cause is the backend expert
Step 2 prompt: it uses Step 1 considerations and assumptions, but did not
strongly require the final answer to preserve the requested output shape.

## Scope

In scope:

- Update expert-route final-answer prompt construction so requested output shape
  is preserved first.
- Preserve requested section names when present, including setup, prompt runs,
  evidence capture, and rollback.
- Preserve requested time boxes when present, including two-hour plan requests.
- Preserve requested deliverable type when present, including checklist, table,
  plan, release note, email, rubric, and runbook.
- Keep assumptions and considerations available without letting them replace the
  requested deliverable.
- Preserve safety and claim-boundary language.
- Add no-network tests using fake provider clients.

Out of scope:

- Provider selection changes.
- Preview UI changes.
- Dashboard auth/session/CSRF changes.
- Enabling OpenAI.
- Cloud Run deployment.
- Google Sheets or backlog workbook updates.
- Claims of MVP validation, Alpha Solver superiority, production readiness,
  broad runtime readiness, answer-quality benchmark success, or provider
  reasoning orchestration.

## Requirements

1. If the user asks for a specific format, the expert final answer should
   preserve it unless unsafe or impossible.
2. Requested section names should be preserved when present.
3. Requested time boxes should be preserved when present.
4. Requested output type should be preserved when present.
5. Assumptions and considerations should remain useful, but they must not
   replace the requested deliverable.
6. Expert final answers should be answer-first: the requested deliverable comes
   first, and assumptions or considerations can follow or remain in structured
   detail fields.
7. Safety and claim-boundary behavior must not be reduced.
8. Provider selection behavior must not change.
9. Preview UI behavior must not change unless required by the backend contract.

## Acceptance criteria

- Expert Step 2 prompt construction explicitly instructs the provider to preserve
  requested output format, section names, order, time boxes, bullets, tables, and
  named parts unless unsafe or impossible.
- A no-network API test proves the two-hour operator test plan prompt returns a
  final answer with setup, prompt runs, evidence capture, rollback, and time-box
  structure while considerations and assumptions remain available separately.
- A no-network UI preview test proves the same requested plan structure renders
  as the primary expert answer and considerations/assumptions remain visible.
- A no-network API test proves claim-boundary instructions remain present for an
  overclaim-sensitive release-note prompt.
- Existing expert-preview and local-provider tests continue to pass.
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

`ALPHA-FORMAT-PRESERVATION-001` should be marked Done only if this PR is merged.
This was discovered during the first controlled operator demo. It supports MVP
operator testing but does not validate the MVP, prove Alpha Solver superiority,
prove production readiness, prove broad runtime readiness, prove answer-quality
benchmark success, or prove provider reasoning orchestration.
