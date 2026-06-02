# Post-Fix Operator Retest Findings

This artifact records summarized findings from the post-fix Alpha Solver
operator retest for `/dashboard/expert-preview`. It is a documentation-only
findings record, not a benchmark, validation report, production-readiness
assessment, or raw evidence store.

The retest followed the [Operator Post-Fix Retest Packet](../OPERATOR_POST_FIX_RETEST_PACKET.md)
after follow-up fixes for the first controlled operator demo:

- `UI-PREVIEW-RESPONSE-LAYOUT-001`;
- `ALPHA-FORMAT-PRESERVATION-001`;
- `UI-PREVIEW-REQUEST-METRICS-001`;
- `EVAL-DEMO-POST-FIX-RETEST-001`.

## Evidence handling and redaction boundary

This artifact records only summarized operator observations and summarized
request metrics. It intentionally does not store raw model outputs, raw provider
payloads, full raw provider traces, secrets, headers, cookies, CSRF tokens,
session values, API keys, bearer tokens, provider account identifiers, dashboard
passwords, or other sensitive runtime material.

The prompt text is included because it is the controlled retest input. Provider
responses are summarized only.

## Local smoke

- **Mode used:** `local`.
- **Environment sequence:** Cloud Run was redeployed from latest `main`, and the
  service was confirmed on `MODEL_PROVIDER=local` before the local smoke.
- **Dashboard route:** `/dashboard/expert-preview` loaded.
- **Metrics rendering:** The request metrics panel rendered.
- **Metrics provider:** Metrics showed provider as `local`.
- **Token and cost handling:** Token usage and cost were safely shown as
  `unknown` or `not estimated`.
- **Sensitive data check:** No secrets or raw payloads appeared.
- **Local-mode limitation:** Local mode remained simple and deterministic and
  mostly echoed the prompt, so it could verify UI and metrics rendering but not
  true live-provider behavior.

**Interpretation:** local smoke passed.

## Controlled live retest

- **Mode used:** `live`, controlled OpenAI mode with a low cap.
- **Rollback:** The service was rolled back to `MODEL_PROVIDER=local` after the
  live retest.
- **Evidence scope:** The observations below summarize behavior and metrics only;
  they do not include raw provider payloads or full raw outputs.

### Prompt A: two-hour operator test plan

**Prompt**

```text
Create a two-hour operator test plan for /dashboard/expert-preview that separates setup, prompt runs, evidence capture, and rollback.
```

**Operator observations**

- Plain output summary: produced a direct two-hour operator test plan with
  objectives, scope, success criteria, prerequisites, test prompts,
  safety/guardrails, and a 120-minute run-of-show.
- Alpha Solver output summary: did not produce the requested two-hour plan. It
  entered clarify mode and asked for details before answering.
- Format preserved: no.
- Layout readable: yes.
- Metrics visible: yes.
- Estimated cost shown: yes.
- Defect found: yes.
- Follow-up needed: `ALPHA-CLARIFY-THRESHOLD-001`.

**Metrics summary**

| Surface | Provider/model | Route or mode | Calls | Tokens | Estimated cost |
| --- | --- | --- | ---: | ---: | ---: |
| Plain | OpenAI `gpt-5-2025-08-07` | `tot` | 1 | 32 input / 2048 output / 2080 total | about `$0.030880` |
| Alpha Solver | OpenAI `gpt-5-2025-08-07` | `clarify` | 2 | 266 input / 4096 output / 4362 total | about `$0.062770` |

Total preview latency was about 121.27 seconds. Costs are UI/request estimates,
not exact billing claims.

**Interpretation**

Prompt A found a post-fix defect. Layout and metrics were readable and visible,
but Alpha Solver did not preserve the requested time-boxed plan structure because
it entered clarify mode instead of answering with reasonable assumptions.

### Prompt B: honest rollout note

**Prompt**

```text
Draft a rollout note for the preview, but keep it honest: we have local smoke, one capped live smoke, first operator demo findings, request metrics, and no broad validation yet.
```

**Operator observations**

- Plain output summary: produced a detailed preview rollout note with status,
  scope, validation status, metrics placeholders, risks, rollout gates,
  enablement, support, and timeline.
- Alpha Solver output summary: produced a structured preview rollout note with
  non-GA positioning, scope/audience, risk containment controls, limited
  evidence, included features, considerations, assumptions, and honest validation
  boundaries.
- Format preserved or appropriate structure: yes.
- Layout readable: yes.
- Metrics visible: yes.
- Estimated cost shown: yes.
- Defect found: no.
- Follow-up needed: none for this prompt, though cost and latency should be
  tracked for post-MVP optimization.

**Metrics summary**

| Surface | Provider/model | Route or mode | Calls | Tokens | Estimated cost |
| --- | --- | --- | ---: | ---: | ---: |
| Plain | OpenAI `gpt-5-2025-08-07` | `tot` | 1 | 43 input / 1784 output / 1827 total | about `$0.026975` |
| Alpha Solver | OpenAI `gpt-5-2025-08-07` | `direct` | 2 | 699 input / 3443 output / 4142 total | about `$0.055140` |

Total preview latency was about 79.69 seconds. Costs are UI/request estimates,
not exact billing claims.

**Interpretation**

Prompt B passed the narrow post-fix checks for readable layout, visible metrics,
and useful output structure. It also showed that Alpha Solver expert preview was
materially slower and more expensive than the plain output for this capped live
sample.

## Pre-fix issue vs post-fix result

| Area | Pre-fix issue from first demo | Post-fix retest result | Status |
| --- | --- | --- | --- |
| Long response layout | Long Alpha responses were hard to review and appeared clipped or poorly expanded. | Long live responses were readable and not clipped in the retest. | Fixed or improved. |
| Request metrics visibility | The preview lacked enough request-level latency, provider/model/mode, call count, token, and cost visibility. | The metrics panel showed latency, provider/model/mode, call count, tokens, cost source, and estimated API cost during live retest. | Fixed and verified live. |
| Format preservation | Alpha did not always preserve requested plan/checklist/time-boxed structure. | Prompt B preserved a useful rollout-note structure, but Prompt A did not produce the requested two-hour plan because Alpha entered clarify mode. | Partially improved. |
| Clarification threshold behavior | The first demo emphasized format preservation; clarify-threshold behavior was not the primary identified fix. | Prompt A exposed a new defect where Alpha asked for clarification instead of answering a sufficiently actionable planning prompt with reasonable assumptions. | Still open; targeted follow-up needed. |

## Follow-up tickets

1. `ALPHA-CLARIFY-THRESHOLD-001`
   - Targeted fix for cases where Alpha Solver should answer a sufficiently
     actionable prompt with reasonable assumptions instead of entering clarify
     mode and blocking the requested deliverable.
   - This is relevant to MVP readiness because it affected Prompt A's requested
     operator test-plan format.
2. `POST-MVP-COST-LATENCY-OPTIMIZATION-001`
   - Post-MVP or shortly-after-MVP optimization task for reducing and/or better
     explaining the materially higher latency and estimated API cost observed for
     Alpha Solver expert preview versus plain output.
   - This is not a blocker for the current MVP readiness checkpoint because the
     request metrics panel now exposes the tradeoff for operator review.

## Final conservative interpretation

- Long response layout is fixed or improved in this narrow retest.
- Request metrics are fixed and verified live for the retested prompts.
- Format preservation is partially improved, not fully resolved.
- Clarify threshold behavior still needs a targeted fix through
  `ALPHA-CLARIFY-THRESHOLD-001`.
- Cost and latency need post-MVP or shortly-after-MVP optimization through
  `POST-MVP-COST-LATENCY-OPTIMIZATION-001`.
- This retest does not validate the MVP.

## Strict claim boundaries

This retest establishes only narrow post-fix observations for the local smoke and
two controlled live prompts summarized above. It does not establish any of the
following claims:

- This does not validate the MVP.
- This does not prove Alpha Solver superiority.
- This does not prove production readiness.
- This does not prove broad runtime readiness.
- This does not prove answer-quality benchmark success.
- This does not prove exact billing accuracy.
- This does not prove provider reasoning orchestration.

## Safety and scope boundaries

This findings artifact is documentation/spec-only. The following were not changed
by this work:

- Runtime behavior.
- Cloud Run configuration.
- Provider behavior.
- Expert-preview behavior.
- Dashboard auth/session/CSRF behavior.
- Live OpenAI enablement.
- Persistent storage.
- Google Sheets or backlog workbooks.

No Cloud Run deployment was performed by Codex. No Google Sheet update was
performed by Codex.

## Backlog impact

`EVAL-DEMO-POST-FIX-FINDINGS-001` should be marked Done only if the PR adding
this artifact is merged. This artifact supports `MVP-READINESS-CHECKPOINT-001`,
creates follow-up `ALPHA-CLARIFY-THRESHOLD-001`, and creates post-MVP task
`POST-MVP-COST-LATENCY-OPTIMIZATION-001`.

This does not validate the MVP, prove Alpha Solver superiority, or prove
production readiness.
