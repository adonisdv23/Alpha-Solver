# First Operator Demo Findings

## Purpose

This document records safe, summarized findings from the first controlled
3-prompt Alpha Solver operator demo through `/dashboard/expert-preview`. It is a
repo-tracked signal artifact for follow-up work, not a benchmark, validation
report, or release-readiness claim.

The hosted MVP preview had already passed local-provider smoke and one capped
live OpenAI smoke before this operator demo. The operator then used the operator
demo flow to compare plain same-provider output with Alpha Solver expert-preview
output for three prompts.

## Evidence safety

This artifact intentionally records only summarized observations. It does not
store raw provider payloads, full raw provider traces, secrets, headers, cookies,
session values, CSRF tokens, API keys, dashboard passwords, provider account
identifiers, or full raw model outputs.

## Claim boundaries

This first run is a signal source for follow-up tickets, not a benchmark.

After the follow-up fixes are merged and latest `main` is redeployed, use the
[Operator Post-Fix Retest Packet](../OPERATOR_POST_FIX_RETEST_PACKET.md) for a
short verification pass focused on layout, metrics, and format preservation.
When that retest is complete, keep only summarized outcomes in the
[Post-Fix Operator Retest Findings](POST_FIX_OPERATOR_RETEST_FINDINGS.md)
artifact.

It does not establish any of the following claims:

- This does not validate the MVP.
- This does not prove Alpha Solver superiority.
- This does not prove production readiness.
- This does not prove broad runtime readiness.
- This does not prove answer-quality benchmark success.
- This does not prove provider reasoning orchestration.

## Demo prompt comparisons

### Prompt 1: release-note claim boundary

**Prompt**

```text
The demo worked once. Write the strongest claim we can safely make in release notes without overstating readiness.
```

**Plain output summary**

- The plain provider output was concise and directly usable.
- It framed the result as a single successful controlled demo showing
  end-to-end feasibility while still calling the system an experimental
  prototype that is not production-ready.

**Alpha Solver output summary**

- Alpha Solver expert preview produced several strong-but-safe release-note
  alternatives.
- The Alpha response was useful, but more verbose than needed for this simple
  claim-boundary request.
- The preview displayed `mode=direct`, `complexity=trivial`, `call_count=1`, and
  `confidence=0.0`.

**Provisional interpretation**

- Plain output was the better fit for immediate release-note copy because the
  task favored brevity and a single safe claim.
- Alpha still contributed useful alternatives, but its extra volume was less
  helpful for this prompt.

**Finding**

Alpha may overproduce for simple claim-boundary prompts, and the `confidence=0.0`
display on a usable answer may need calibration.

### Prompt 2: honest preview rollout note

**Prompt**

```text
Draft a rollout note for the preview, but keep it honest: we have local smoke, one capped live smoke, and no broad validation yet.
```

**Plain output summary**

- The plain provider output was a strong rollout note.
- It covered summary, validation status, scope, expectations, enablement,
  support, success criteria, risks, and compliance.

**Alpha Solver output summary**

- Alpha Solver expert preview was more operationally complete.
- It added status expectations, scope boundaries, supported
  platforms/environments, known gaps, risk disclosure, usage guidance,
  assumptions, and considerations.

**Provisional interpretation**

- Alpha appeared more useful for this more complex operational planning and risk
  disclosure prompt.
- The added structure and caveats were valuable, but long-response rendering in
  the UI made the result hard to review.

**Finding**

Alpha appears useful for operational planning and risk disclosure, but long
responses in the expert-preview UI need clearer rendering and review ergonomics.

### Prompt 3: two-hour operator test plan

**Prompt**

```text
Create a two-hour operator test plan for /dashboard/expert-preview that separates setup, prompt runs, evidence capture, and rollback.
```

**Plain output summary**

- The plain provider output gave a direct time-boxed operator test plan.
- It included purpose, success criteria, stop/rollback criteria, roles, setup,
  and environment validation.

**Alpha Solver output summary**

- Alpha Solver expert preview produced strong considerations and assumptions
  around objectives, prompt coverage, observability, rollback, privacy, and risk
  management.
- Alpha surfaced useful hidden constraints, but did not preserve the requested
  two-hour plan format as clearly as the plain output.

**Provisional interpretation**

- Plain output was easier to use as an execution plan because it preserved the
  requested time-boxed format more clearly.
- Alpha added valuable risk and constraint analysis that could inform a revised
  plan, but the response shape was less directly executable.

**Finding**

Alpha may need stronger output-format preservation for execution-plan prompts
when the user asks for a specific plan, checklist, or time-boxed structure.

## Follow-up tickets identified

1. `UI-PREVIEW-RESPONSE-LAYOUT-001`
   - Long Alpha Solver expert-preview responses did not visually expand or read
     cleanly in the main response container.
2. `UI-PREVIEW-REQUEST-METRICS-001`
   - The preview should show request duration, provider/model/mode, call count,
     token usage, and estimated API cost.
3. `ALPHA-FORMAT-PRESERVATION-001`
   - Alpha should better preserve requested output shape when the user asks for
     a specific plan/checklist format.
4. `ALPHA-BREVITY-CONTROL-001`
   - Alpha may overproduce on simple prompts where a concise answer is better.
5. `ALPHA-CONFIDENCE-CALIBRATION-001`
   - `confidence=0.0` on a usable answer looks suspicious and should be
     investigated.

## Safety and scope boundaries

This findings artifact is documentation/spec-only. It makes no runtime changes
and requires no environment changes.

The following are explicitly out of scope:

- Runtime behavior changes.
- Cloud Run config changes.
- Provider behavior changes.
- Expert-preview behavior changes.
- Dashboard auth/session/CSRF behavior changes.
- Enabling live OpenAI.
- Deploying Cloud Run.
- Adding persistent storage.
- Adding automated benchmark claims.
- Updating Google Sheets or backlog workbooks.

## Backlog impact

`EVAL-DEMO-FINDINGS-001` should be marked Done only if the PR that adds this
artifact is merged. This finding supports follow-up tickets
`UI-PREVIEW-RESPONSE-LAYOUT-001`, `UI-PREVIEW-REQUEST-METRICS-001`,
`ALPHA-FORMAT-PRESERVATION-001`, `ALPHA-BREVITY-CONTROL-001`, and
`ALPHA-CONFIDENCE-CALIBRATION-001`.

No Google Sheet update was performed by Codex.
