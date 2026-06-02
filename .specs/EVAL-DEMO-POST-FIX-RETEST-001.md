# EVAL-DEMO-POST-FIX-RETEST-001 · Post-Fix Operator Retest Packet

## Purpose

Add a concise operator retest packet for verifying the fixes merged after the
first controlled operator demo. The packet tells operators how to verify layout,
request metrics, and format-preservation improvements after redeploying latest
`main` without rerunning the full earlier demo process.

The packet must capture summarized evidence only and must not claim MVP
validation, Alpha Solver superiority, production readiness, answer-quality
benchmark success, exact billing accuracy, or provider reasoning orchestration.

## Context

The first controlled 3-prompt operator demo identified follow-up issues. The
post-fix retest assumes these fixes have been implemented or are expected to be
merged before the retest:

- `UI-PREVIEW-RESPONSE-LAYOUT-001`: long response rendering fix.
- `EVAL-DEMO-FINDINGS-001`: first operator demo findings artifact.
- `ALPHA-FORMAT-PRESERVATION-001`: expert answers preserve requested output
  structure better.
- `UI-PREVIEW-REQUEST-METRICS-001`: request metrics panel for latency,
  provider/model/mode, call count, token usage, and estimated cost.

## Scope

In scope:

- Add `docs/OPERATOR_POST_FIX_RETEST_PACKET.md`.
- Add this spec file.
- Register this spec in `.specs/INDEX.md`.
- Add short links from `docs/OPERATOR_DEMO_RUN_PACKET.md` and
  `docs/evals/FIRST_OPERATOR_DEMO_FINDINGS.md`.
- Optionally add a short link from
  `docs/OPERATOR_BEHAVIORAL_DEMO_CHECKLIST.md`.
- Include preconditions, local and optional live retest sequences, 2 to 3
  prompts, verification checklist, evidence block, stop conditions, and claim
  boundaries.

Out of scope:

- Runtime behavior changes.
- Cloud Run config changes.
- Provider behavior changes.
- Expert-preview behavior changes.
- Dashboard auth/session/CSRF behavior changes.
- Enabling OpenAI.
- Deploying Cloud Run.
- Persistent storage.
- Google Sheet or backlog workbook updates.
- MVP validation, Alpha Solver superiority, production-readiness, broad
  runtime-readiness, answer-quality benchmark success, exact billing accuracy,
  or provider reasoning orchestration claims.

## Retest packet requirements

The retest packet must include:

1. Purpose:
   - run a short post-fix operator retest after the first demo follow-up fixes;
   - verify layout, metrics, and format-preservation improvements;
   - capture summarized evidence only;
   - avoid MVP validation, Alpha Solver superiority, production readiness,
     answer-quality benchmark success, exact billing accuracy, and provider
     reasoning orchestration claims.
2. Preconditions:
   - relevant fix PRs are merged into `main`;
   - Cloud Run is redeployed from latest `main`;
   - the service starts in `MODEL_PROVIDER=local` by default;
   - controlled live mode requires explicit approval;
   - live mode uses a low cap, usually `2` or `3`, with `max-instances=1` while
     using the current per-process cap;
   - `OPENAI_API_KEY` is mounted through the approved secret mechanism,
     preferably Secret Manager;
   - no secrets or raw provider payloads are copied into evidence.
3. Retest sequence for local-provider UI smoke, optional controlled
   live-provider retest, prompt submission, evidence capture, and rollback to
   local mode.
4. Exactly 2 or 3 recommended prompts focused on format preservation, request
   metrics, rollout honesty, brevity, and claim boundaries.
5. Verification checklist covering response readability, answer-box reviewability,
   metrics visibility, total latency, provider/model/mode, call count, token
   usage, estimated cost or `not estimated`, estimate labeling, secret/raw
   payload exclusion, Prompt A structure preservation, assumptions not replacing
   deliverables, and live cap/rollback behavior when used.
6. A small copyable evidence block with prompt ID, mode, plain summary, Alpha
   summary, metrics visibility, format preservation, layout readability,
   estimated cost display, defect status, follow-up ticket need, and conservative
   interpretation.
7. Stop conditions for login failure, CSRF or submit errors, `Preview request
   failed`, unexpected live-cap behavior, failed rollback, secrets or raw
   payloads appearing, exact-billing claims, and unsupported readiness or
   superiority claims.
8. Claim boundaries stating the retest does not validate the MVP, prove Alpha
   Solver superiority, prove production readiness, prove broad runtime readiness,
   prove answer-quality benchmark success, prove exact billing accuracy, or prove
   provider reasoning orchestration.

## Acceptance criteria

- `docs/OPERATOR_POST_FIX_RETEST_PACKET.md` exists.
- `.specs/EVAL-DEMO-POST-FIX-RETEST-001.md` exists and is registered in
  `.specs/INDEX.md`.
- The retest packet links to the original run packet and first demo findings.
- The retest packet includes preconditions, local and optional live retest
  sequences, 2 to 3 prompts, verification checklist, evidence block, stop
  conditions, and claim boundaries.
- Runtime behavior is unchanged.
- Cloud Run config is unchanged.
- Provider behavior is unchanged.
- Dashboard auth/session/CSRF behavior is unchanged.
- OpenAI is not enabled.
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

`EVAL-DEMO-POST-FIX-RETEST-001` should be marked Done only if this PR is merged.
This supports post-fix operator verification after the first demo follow-up
fixes.

This does not validate the MVP, prove Alpha Solver superiority, or prove
production readiness. It also does not prove broad runtime readiness,
answer-quality benchmark success, exact billing accuracy, or provider reasoning
orchestration. Backlog spreadsheets and Google Sheets are not edited from this
repo task.
