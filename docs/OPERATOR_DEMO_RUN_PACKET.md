# Operator Demo Run Packet

Use this one-page packet to run one small manual Alpha Solver preview session.
For the full prompt list and rubric, use the
[Operator Behavioral Demo Checklist](OPERATOR_BEHAVIORAL_DEMO_CHECKLIST.md). For
notes, use the
[Operator Behavioral Demo Evidence Template](OPERATOR_BEHAVIORAL_DEMO_EVIDENCE_TEMPLATE.md).
For the first controlled 3-prompt run's summarized findings, use
[First Operator Demo Findings](evals/FIRST_OPERATOR_DEMO_FINDINGS.md). After the
first demo follow-up fixes are merged and redeployed, use the
[Operator Post-Fix Retest Packet](OPERATOR_POST_FIX_RETEST_PACKET.md) instead of
rerunning this full packet.

## Purpose

- Run one small manual behavioral demo session through `/dashboard/expert-preview`.
- Compare plain same-provider output against the Alpha Solver expert preview.
- Capture only summarized evidence; do not paste raw full outputs or provider
  payloads.
- Do not claim MVP validation, Alpha Solver superiority, production readiness,
  answer-quality benchmark success, or provider reasoning orchestration.

## Before you start

Confirm all of the following before the first prompt:

- Cloud Run URL is known and reachable by the operator.
- Dashboard password is available through the approved operator channel.
- Service is in `MODEL_PROVIDER=local` unless an explicit live test window has
  been approved.
- No secrets, headers, cookies, session values, CSRF tokens, API keys, raw
  provider payloads, or raw full model outputs will be copied into evidence.

## Default local-provider run sequence

1. Open `/dashboard/expert-preview` on the Cloud Run preview URL.
2. Log in with the dashboard password.
3. Select 3 to 5 prompt IDs from the checklist.
4. Submit one prompt at a time.
5. Confirm the loading state appears and duplicate submission is blocked while
   the request is in flight.
6. Confirm both comparison panes render before recording evidence.
7. Record summarized evidence using one evidence-template block per prompt.
8. Create follow-up tickets only for real defects or clear routing/prompt
   weaknesses.

## Recommended first-run prompt subset

Choose 3 to 5 prompt IDs from the checklist that cover the widest operator
signal with the smallest run:

- `P6` for overclaim prevention.
- `P2` for hidden constraints.
- `P4` for execution planning.
- `P7` for corrective next actions.
- `P5` for project-context preservation.

## Optional controlled live-provider sequence

Use this only with explicit approval for a live-provider test window.

1. Confirm the approved prompt count, operator, provider, cap, and rollback
   owner.
2. Set `MODEL_PROVIDER=openai` only for the approved window.
3. Set `ALPHA_LIVE_PREVIEW_ENABLED=true`.
4. Set `ALPHA_LIVE_PREVIEW_MAX_REQUESTS` to a low value, usually `1` or `2`.
5. Confirm `OPENAI_API_KEY` is configured through the approved secret mechanism,
   preferably Secret Manager. Do not paste the API key into this run packet, the
   evidence template, screenshots, logs, Google Sheets, PR comments, or chat. Do
   not proceed if the live key is missing or the operator cannot confirm it is
   mounted safely.
6. Keep Cloud Run `max-instances=1` for the test window if using the current
   per-process cap.
7. Run only the approved prompt count.
8. If cap behavior is part of the test, confirm the cap blocks additional live
   preview submissions as expected.
9. Immediately return the service to `MODEL_PROVIDER=local` when the approved
   prompts or window are complete.
10. Record rollback confirmation in the evidence block.

## Evidence packet

- Use the
  [Operator Behavioral Demo Evidence Template](OPERATOR_BEHAVIORAL_DEMO_EVIDENCE_TEMPLATE.md).
- Copy one evidence block per prompt.
- Summarize plain-provider and Alpha Solver outputs in your own words.
- Include manual scoring and conservative interpretation.
- Do not paste raw full outputs, raw provider request/response payloads, secrets,
  headers, cookies, session values, CSRF tokens, API keys, dashboard passwords,
  or provider account identifiers.

## Stop conditions

Stop the run and file the appropriate follow-up if any of these occur:

- Login fails.
- CSRF or submit errors appear.
- `Preview request failed` appears.
- Live cap behavior is unexpected.
- Secrets or raw payloads appear in the UI, logs, or evidence.
- Output makes unsafe or unsupported claims.
- The service cannot be returned to `MODEL_PROVIDER=local` after live testing.

## Interpretation and claim boundaries

- One run is not validation.
- A promising result only justifies more testing.
- Weak results should become prompt/routing tickets.
- Runtime or UI failures should become defect tickets.
- Do not use run results for public claims, MVP validation claims, Alpha Solver
  superiority claims, production-readiness claims, broad runtime-readiness
  claims, answer-quality benchmark claims, or provider reasoning orchestration
  claims.
