# MVP-READINESS-CHECKPOINT-001 · Operator-Test-Ready MVP Preview Checkpoint

## Purpose

Create a final documentation checkpoint for the Alpha Solver supervised preview.
The checkpoint marks the preview as ready for disciplined operator testing only
and records the final live retest evidence after PR #226.

## Scope

In scope:

- add `docs/MVP_READINESS_CHECKPOINT.md`;
- add this spec;
- register this spec in `.specs/INDEX.md`;
- summarize the final capped live OpenAI retest evidence;
- distinguish repo-backed evidence from backlog or planning-ledger-only rows;
- track `POST-MVP-COST-LATENCY-OPTIMIZATION-001` as important but
  post-MVP/non-blocking for this checkpoint;
- preserve strict claim boundaries.

Out of scope:

- runtime behavior changes;
- Cloud Run configuration changes;
- provider behavior changes;
- request metrics changes;
- dashboard auth/session/CSRF changes;
- enabling OpenAI;
- deploying Cloud Run;
- Google Sheet or backlog workbook updates;
- MVP validation, Alpha Solver superiority, production-readiness, broad
  runtime-readiness, answer-quality benchmark success, exact billing accuracy,
  or provider reasoning orchestration claims.

## Requirements

The checkpoint document must:

1. State that Alpha Solver supervised preview is ready for disciplined operator
   testing only.
2. Avoid claims that the MVP is validated, production-ready, superior to plain
   providers, broadly runtime-ready, answer-quality benchmark successful,
   exact-billing accurate, or provider reasoning orchestrated.
3. Record what is true now: hosted Cloud Run preview, dashboard login/session
   flow, local safe default, controlled live OpenAI mode only with explicit
   operator approval, capped live mode with rollback, request metrics, readable
   long output, final gate direct answer-with-assumptions behavior, and existing
   operator packets/findings.
4. Summarize final PR #226 live retest evidence for the prompt:
   `Create a two-hour operator test plan for /dashboard/expert-preview that separates setup, prompt runs, evidence capture, and rollback.`
5. Include the observed final gate metrics as estimates only.
6. Provide an evidence ledger that does not invent missing repo artifacts.
7. Distinguish repo-backed evidence, backlog/planning-ledger evidence, and
   post-MVP/non-blocking tasks.
8. State the default operating posture as `MODEL_PROVIDER=local`.
9. State that live provider mode requires explicit operator approval, low caps,
   and confirmed rollback to local mode.
10. State that secrets, raw provider payloads, headers, cookies, CSRF tokens,
    session values, API keys, bearer tokens, and provider account identifiers
    must not be exposed.
11. Define operator-test-ready Go and No-Go conditions.
12. Include strict non-claims.
13. Recommend next-stage work using conservative release language.
14. State that Google Sheet updates are handled separately by the
    Sheet-maintainer workflow after merge.

## Acceptance criteria

- `docs/MVP_READINESS_CHECKPOINT.md` exists.
- `.specs/MVP-READINESS-CHECKPOINT-001.md` exists and is registered in
  `.specs/INDEX.md`.
- The checkpoint says operator-test-ready only.
- The checkpoint includes final live retest evidence.
- The checkpoint includes strict non-claims.
- The checkpoint distinguishes repo-backed evidence from
  backlog/planning-ledger-only items.
- The checkpoint tracks cost/latency as post-MVP/non-blocking.
- Runtime behavior is unchanged.
- Cloud Run config is unchanged.
- Provider behavior is unchanged.
- Dashboard auth/session/CSRF behavior is unchanged.
- OpenAI is not enabled by Codex.
- No deployment is performed by Codex.
- No Google Sheet update is performed by Codex.

## Evidence and non-claims

Evidence is limited to repo-backed specs/docs and summarized operator-reported
final gate observations. Planning-ledger-only rows may be named only when clearly
labeled as not represented by a repo artifact in this checkout.

This checkpoint does not validate the MVP, prove Alpha Solver superiority, prove
production readiness, prove broad runtime readiness, prove answer-quality
benchmark success, prove exact billing accuracy, or prove provider reasoning
orchestration.

## Validation expectations

Because this is documentation/spec-only work, validation should include:

```bash
git diff --check
python -m pytest -q
```

If the full pytest suite is skipped or cannot complete, report why and still run
`git diff --check`.

## Backlog impact

`MVP-READINESS-CHECKPOINT-001` should be marked Done only if this PR is merged.
This marks the supervised preview as ready for disciplined operator testing only.

This does not validate the MVP. This does not prove Alpha Solver superiority.
This does not prove production readiness. This does not prove broad runtime
readiness. This does not prove answer-quality benchmark success. This does not
prove exact billing accuracy. This does not prove provider reasoning
orchestration.

Post-MVP or non-blocking rows remain tracked separately:

- `POST-MVP-COST-LATENCY-OPTIMIZATION-001`
- `TESTER-ONBOARDING-001`
- `TESTER-FEEDBACK-TEMPLATE-001`
- `UI-PREVIEW-EXPORT-EVIDENCE-001`
- `PERSISTENT-QUOTA-001`
- `ALPHA-BREVITY-CONTROL-001`
- `ALPHA-CONFIDENCE-CALIBRATION-001`

Google Sheets and external backlog workbooks are not updated from this repo task.
