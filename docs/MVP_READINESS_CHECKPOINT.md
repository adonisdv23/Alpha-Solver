# MVP Readiness Checkpoint

## Status statement

Alpha Solver supervised preview is ready for disciplined operator testing only.
This checkpoint is an operator-test-ready preview checkpoint, not an MVP
validation checkpoint.

This document must not be read as a claim that Alpha Solver is MVP-validated,
production-ready, superior to plain providers, broadly runtime-ready,
answer-quality benchmark successful, exact-billing accurate, or provider
reasoning orchestrated.

## What is true now

- A hosted Cloud Run preview lane exists for `/dashboard/expert-preview`.
- The dashboard login/session flow exists and is part of the preview operating
  surface.
- `MODEL_PROVIDER=local` works and remains the default safe posture.
- Controlled live OpenAI mode works only under explicit operator approval.
- Live mode is capped and should be rolled back to `MODEL_PROVIDER=local` after
  approved tests.
- The request metrics panel is available for preview requests.
- Long Alpha Solver outputs are readable in the expert preview.
- The expert preview can produce a direct `answer_with_assumptions` plan for the
  final gate prompt recorded below.
- Operator testing packets and findings artifacts exist for the initial demo,
  post-fix retest, and post-fix findings.

## Final gate evidence

After PR #226, latest `main` was redeployed to controlled live OpenAI mode with
cap `1`. The operator ran exactly this prompt:

```text
Create a two-hour operator test plan for /dashboard/expert-preview that separates setup, prompt runs, evidence capture, and rollback.
```

Observed result:

- Alpha Solver expert preview returned a direct plan.
- Alpha primary answer was non-empty.
- Alpha was not clarify-only.
- Alpha mode showed `answer_with_assumptions`.
- Alpha confidence showed `0.72`.
- Alpha call count showed `2`.
- Request metrics were visible.
- Layout was readable.
- Estimated API cost was visible.
- No secrets or raw provider payloads were visible.
- The service was rolled back to `MODEL_PROVIDER=local` afterward.

Observed metrics, recorded as estimates only:

| Surface | Provider / model | Mode | Calls | Tokens | Estimated cost |
| --- | --- | --- | ---: | ---: | ---: |
| Total preview | n/a | n/a | n/a | n/a | Latency about `106.43 s` |
| Plain provider | OpenAI / `gpt-5-2025-08-07` | `tot` | 1 | 32 input, 2048 output, 2080 total | about `$0.030880` |
| Alpha Solver | OpenAI / `gpt-5-2025-08-07` | `answer_with_assumptions` | 2 | 959 input, 3997 output, 4956 total | about `$0.064750` |

The cost/latency tradeoff is visible and remains tracked as
`POST-MVP-COST-LATENCY-OPTIMIZATION-001`. It is not a blocker for this
operator-test-ready checkpoint because live mode is capped, operator-controlled,
and the preview now exposes the tradeoff through request metrics.

## Evidence ledger

Repo code, tests, specs, and docs are higher authority than the external backlog
or planning ledger. Rows below marked repo-backed have a repo artifact in this
checkout. Rows marked planning-ledger-only are not invented as repo evidence.

| Item | Repo evidence status | Repo artifact or note |
| --- | --- | --- |
| `DEPLOY-CLOUDRUN-SMOKE-001` | Planning-ledger-only / not found as a spec in this repo | Mentioned by related deployment specs, but no `.specs/DEPLOY-CLOUDRUN-SMOKE-001.md` artifact exists in this checkout. |
| `DEPLOY-CLOUDRUN-LIVE-OPENAI-001` | Planning-ledger-only / not found as a spec in this repo | Mentioned as held/inconclusive by related specs, but no `.specs/DEPLOY-CLOUDRUN-LIVE-OPENAI-001.md` artifact exists in this checkout. |
| `DEPLOY-LIVE-SPEND-GUARD-001` | Repo-backed | `.specs/DEPLOY-LIVE-SPEND-GUARD-001.md` |
| `UI-PREVIEW-LOADING-STATE-001` | Repo-backed | `.specs/UI-PREVIEW-LOADING-STATE-001.md` |
| `UI-PREVIEW-RESPONSE-LAYOUT-001` | Repo-backed | `.specs/UI-PREVIEW-RESPONSE-LAYOUT-001.md` |
| `UI-PREVIEW-REQUEST-METRICS-001` | Repo-backed | `.specs/UI-PREVIEW-REQUEST-METRICS-001.md` |
| `EVAL-BEHAVIORAL-DEMO-001` | Repo-backed | `.specs/EVAL-BEHAVIORAL-DEMO-001.md` |
| `EVAL-DEMO-EVIDENCE-001` | Repo-backed | `.specs/EVAL-DEMO-EVIDENCE-001.md` |
| `EVAL-DEMO-RUN-PACKET-001` | Repo-backed | `.specs/EVAL-DEMO-RUN-PACKET-001.md` |
| `EVAL-DEMO-FINDINGS-001` | Repo-backed | `.specs/EVAL-DEMO-FINDINGS-001.md` |
| `EVAL-DEMO-POST-FIX-RETEST-001` | Repo-backed | `.specs/EVAL-DEMO-POST-FIX-RETEST-001.md` |
| `EVAL-DEMO-POST-FIX-FINDINGS-001` | Repo-backed | `.specs/EVAL-DEMO-POST-FIX-FINDINGS-001.md` |
| `ALPHA-FORMAT-PRESERVATION-001` | Repo-backed | `.specs/ALPHA-FORMAT-PRESERVATION-001.md` |
| `ALPHA-CLARIFY-THRESHOLD-001` | Repo-backed | `.specs/ALPHA-CLARIFY-THRESHOLD-001.md` |
| `ALPHA-PRIMARY-ANSWER-EMPTY-001` | Repo-backed | `.specs/ALPHA-PRIMARY-ANSWER-EMPTY-001.md` |
| `ALPHA-LIVE-EXPERT-STEP1-PARSE-001` | Repo-backed | `.specs/ALPHA-LIVE-EXPERT-STEP1-PARSE-001.md` |

Supporting docs include the Cloud Run preview deployment guide, operator demo
run packet, post-fix retest packet, and post-fix findings artifact.

## Backlog alignment

### Repo-backed evidence

Repo-backed evidence includes the specs and docs listed in the evidence ledger,
plus the final gate retest summarized in this checkpoint. This is the evidence
used to mark the supervised preview operator-test-ready only.

### Backlog / planning-ledger evidence

The external backlog or Google Sheet may contain planning rows, status labels,
and next-action notes. Those ledgers do not override repo artifacts. If a row is
not represented by a repo spec, code, test, or doc artifact, treat it as
planning-ledger evidence only until a PR creates or updates repo evidence.

Google Sheet updates are handled separately by the Sheet-maintainer workflow
after this PR merges. This repo task does not update the Sheet.

### Post-MVP / non-blocking tasks

The following rows remain post-MVP or non-blocking for this operator-test-ready
checkpoint:

- `POST-MVP-COST-LATENCY-OPTIMIZATION-001`
- `TESTER-ONBOARDING-001`
- `TESTER-FEEDBACK-TEMPLATE-001`
- `UI-PREVIEW-EXPORT-EVIDENCE-001`
- `PERSISTENT-QUOTA-001`
- `ALPHA-BREVITY-CONTROL-001`
- `ALPHA-CONFIDENCE-CALIBRATION-001`

`POST-MVP-COST-LATENCY-OPTIMIZATION-001` remains important but non-blocking for
operator-test-ready MVP preview status because the live path is capped,
operator-approved, and observable. Broader trusted tester onboarding should not
begin until the operator approves the next stage. Persistent/global quota may be
needed before broader live testing, depending on the selected architecture.

## Operating posture

- Default posture: `MODEL_PROVIDER=local`.
- Live provider mode requires explicit operator approval.
- Live tests should use low request caps.
- Rollback to `MODEL_PROVIDER=local` must be confirmed after live tests.
- Do not expose secrets, raw provider payloads, headers, cookies, CSRF tokens,
  session values, API keys, bearer tokens, or provider account identifiers.

## Go / no-go

### Go: operator-test-ready

The supervised preview is operator-test-ready when all of these are true:

- latest `main` deploys;
- local mode works;
- controlled live mode works under cap;
- the final gate prompt produces a direct Alpha answer;
- request metrics render;
- layout is readable;
- rollback to `MODEL_PROVIDER=local` is confirmed;
- known non-blockers are tracked.

### No-Go

The preview is not operator-test-ready if any of these occur:

- login/session fails;
- submit/CSRF fails;
- Alpha returns clarify-only for the final gate prompt;
- primary Alpha answer is blank;
- metrics are missing in live test;
- secrets or raw payloads appear;
- rollback fails;
- live mode cannot be capped.

## Explicit non-claims

- This checkpoint does not validate the MVP.
- This checkpoint does not prove Alpha Solver superiority.
- This checkpoint does not prove production readiness.
- This checkpoint does not prove broad runtime readiness.
- This checkpoint does not prove answer-quality benchmark success.
- This checkpoint does not prove exact billing accuracy.
- This checkpoint does not prove provider reasoning orchestration.

## Output differentiation rubric

Future Alpha-vs-plain comparison work should use the universal response-quality rubric in `docs/evals/RESPONSE_QUALITY_RUBRIC.md` to score visible output quality, preserve reviewer calibration, and avoid unsupported superiority, validation, production-readiness, benchmark, billing-accuracy, or provider-reasoning-orchestration claims.

## Next stage

Recommended next-stage work, only after operator approval where applicable:

- optional trusted tester onboarding after the operator approves that stage;
- cost/latency optimization;
- more behavioral eval prompts;
- evidence export if needed;
- persistent/global quota before broader live testing if required by the chosen
  architecture;
- continuing conservative release language that avoids unsupported validation,
  production-readiness, superiority, benchmark, billing-accuracy, or provider
  reasoning-orchestration claims.
