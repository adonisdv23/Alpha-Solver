# Operator Post-Fix Retest Packet

Use this short packet after redeploying latest `main` to verify the fixes that
followed the first controlled operator demo. This packet is intentionally smaller
than the original [Operator Demo Run Packet](OPERATOR_DEMO_RUN_PACKET.md) and
should be read alongside the summarized
[First Operator Demo Findings](evals/FIRST_OPERATOR_DEMO_FINDINGS.md).

## Purpose

- Run a short post-fix operator retest after the first demo follow-up fixes.
- Verify layout, request metrics, and format-preservation improvements.
- Capture summarized evidence only.
- Do not claim MVP validation, Alpha Solver superiority, production readiness,
  answer-quality benchmark success, exact billing accuracy, or provider
  reasoning orchestration.

## Preconditions

Confirm all items before starting:

- PRs for the relevant fixes are merged into `main`:
  - `UI-PREVIEW-RESPONSE-LAYOUT-001`;
  - `EVAL-DEMO-FINDINGS-001`;
  - `ALPHA-FORMAT-PRESERVATION-001`;
  - `UI-PREVIEW-REQUEST-METRICS-001`.
- Cloud Run is redeployed from latest `main`.
- The service starts in `MODEL_PROVIDER=local` by default.
- Controlled live mode requires explicit approval before any live-provider
  change.
- If live mode is used, use a low cap, usually `2` or `3`, and keep Cloud Run
  `max-instances=1` while using the current per-process cap.
- `OPENAI_API_KEY` must be mounted through the approved secret mechanism,
  preferably Secret Manager.
- No secrets or raw provider payloads should be copied into evidence.

## Retest sequence

### 1. Local-provider UI smoke

1. Confirm the service is on latest `main` and is running with
   `MODEL_PROVIDER=local`.
2. Log in to the dashboard through the approved operator path.
3. Open `/dashboard/expert-preview`.
4. Submit Prompt A, then Prompt B, one at a time.
5. If there is time and the operator wants an additional claim-boundary check,
   submit optional Prompt C.
6. Capture only summarized evidence using the block below.
7. If any stop condition appears, stop and file a follow-up ticket instead of
   continuing the retest.

### 2. Optional controlled live-provider retest

Use this only when a live-provider retest window has explicit approval.

1. Confirm the local-provider UI smoke passed first.
2. Confirm the approved prompt count, live cap, operator, provider, and rollback
   owner.
3. Set live mode only for the approved window.
4. Keep the live cap low, usually `2` or `3`.
5. Keep Cloud Run `max-instances=1` while using the current per-process cap.
6. Confirm `OPENAI_API_KEY` is mounted through the approved secret mechanism,
   preferably Secret Manager; do not paste the key into notes, screenshots,
   comments, logs, or evidence.
7. Submit only the approved prompts.
8. Capture summarized evidence and verify cap behavior if it is part of the
   approved test.
9. Immediately roll back to `MODEL_PROVIDER=local` when the approved prompts,
   cap, or time window is complete.
10. Record rollback confirmation in the evidence notes.

## Recommended post-fix prompt set

Use Prompt A and Prompt B. Prompt C is optional. Do not add more prompts to this
packet unless a separate retest scope is approved.

| Prompt ID | Fix focus | Prompt |
| --- | --- | --- |
| A | Format preservation and long-response layout | `Create a two-hour operator test plan for /dashboard/expert-preview that separates setup, prompt runs, evidence capture, and rollback.` |
| B | Request metrics and honest rollout framing | `Draft a rollout note for the preview, but keep it honest: we have local smoke, one capped live smoke, first operator demo findings, request metrics, and no broad validation yet.` |
| C (optional) | Brevity and claim boundary | `The post-fix retest worked. Write the strongest claim we can safely make without overstating MVP readiness.` |

## What to verify

For each submitted prompt, verify the following before interpreting the result:

- [ ] Long Alpha Solver responses are readable and not clipped.
- [ ] The primary answer box expands or remains reviewable.
- [ ] The request metrics panel appears after submit.
- [ ] Total preview latency is shown.
- [ ] Provider, model, and mode are shown or safely reported as unknown.
- [ ] Call count is shown or safely reported as unknown.
- [ ] Input, output, and total tokens are shown or safely reported as unknown.
- [ ] Estimated cost is shown or the UI says `not estimated`.
- [ ] Costs are labeled as estimates, not exact billing.
- [ ] No secrets, raw provider payloads, headers, cookies, CSRF tokens, session
      values, API keys, bearer tokens, or provider account identifiers appear.
- [ ] Prompt A preserves setup, prompt runs, evidence capture, and rollback as
      the requested structure.
- [ ] Assumptions and considerations do not replace the requested deliverable.
- [ ] If controlled live mode is used, the live cap and rollback still behave
      correctly.

## Copyable evidence block

Copy one block per prompt. Keep all fields short and summarized.

```text
Prompt ID:
Mode (local or live):
Plain summary:
Alpha summary:
Metrics visible (yes/no):
Format preserved (yes/no/partial):
Layout readable (yes/no):
Estimated cost shown (yes/no/not estimated):
Defect found (yes/no):
Follow-up ticket needed:
Conservative interpretation:
```

## Stop conditions

Stop the retest and file a focused follow-up if any of these occur:

- Login fails.
- CSRF or submit errors appear.
- `Preview request failed` appears.
- Live cap behaves unexpectedly.
- Rollback to local mode fails.
- Secrets or raw payloads appear.
- Metrics claim exact billing accuracy.
- Alpha output makes unsupported readiness or superiority claims.

## Claim boundaries

This retest is a narrow post-fix operator verification pass. It establishes only
whether the reviewed fixes appear to behave correctly in this small retest.

Explicitly do not claim any of the following:

- This retest does not validate the MVP.
- This retest does not prove Alpha Solver superiority.
- This retest does not prove production readiness.
- This retest does not prove broad runtime readiness.
- This retest does not prove answer-quality benchmark success.
- This retest does not prove exact billing accuracy.
- This retest does not prove provider reasoning orchestration.

## Backlog impact

`EVAL-DEMO-POST-FIX-RETEST-001` should be marked Done only if the PR adding this
packet is merged. This supports post-fix operator verification after the first
demo follow-up fixes. This does not validate the MVP, prove Alpha Solver
superiority, or prove production readiness.

No Google Sheet update was performed by Codex.
