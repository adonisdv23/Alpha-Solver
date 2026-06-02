# EVAL-DEMO-FINDINGS-001 · First Operator Demo Findings

## Purpose

Add a repo-tracked, safe, summarized findings artifact for the first controlled
3-prompt Alpha Solver operator demo through `/dashboard/expert-preview`.

The artifact must be a signal source for follow-up tickets, not a benchmark,
validation report, or production-readiness claim.

## Context

The hosted Alpha Solver MVP preview had passed local-provider smoke and one
controlled capped live OpenAI smoke. The operator then ran a 3-prompt controlled
live demo through `/dashboard/expert-preview` using the operator demo flow.

The run compared plain same-provider output against Alpha Solver expert-preview
output. Findings must be summarized only and must avoid raw provider payloads,
secrets, headers, cookies, session values, CSRF tokens, API keys, dashboard
passwords, full raw provider traces, and full raw model outputs.

## Scope

In scope:

- Add `docs/evals/FIRST_OPERATOR_DEMO_FINDINGS.md`.
- Add this spec file.
- Register this spec in `.specs/INDEX.md`.
- Optionally add a short pointer from `docs/OPERATOR_DEMO_RUN_PACKET.md`.
- Record the three demo prompts and summarized observations.
- Record discovered follow-up ticket IDs and conservative interpretation.

Out of scope:

- Runtime behavior changes.
- Cloud Run config changes.
- Provider behavior changes.
- Expert-preview behavior changes.
- Dashboard auth/session/CSRF behavior changes.
- Enabling live OpenAI.
- Deploying Cloud Run.
- Persistent storage.
- Automated benchmark claims.
- Google Sheet or backlog workbook updates.

## Findings artifact requirements

The findings artifact must include:

1. The three prompts used in the first controlled operator demo.
2. Only summarized observations, not raw provider payloads or full raw outputs.
3. A concise comparison for each prompt:
   - plain output summary;
   - Alpha Solver output summary;
   - provisional winner or interpretation;
   - finding.
4. The discovered follow-up tickets:
   - `UI-PREVIEW-RESPONSE-LAYOUT-001`;
   - `UI-PREVIEW-REQUEST-METRICS-001`;
   - `ALPHA-FORMAT-PRESERVATION-001`;
   - `ALPHA-BREVITY-CONTROL-001`;
   - `ALPHA-CONFIDENCE-CALIBRATION-001`.
5. Strict claim boundaries stating that this first run:
   - does not validate the MVP;
   - does not prove Alpha Solver superiority;
   - does not prove production readiness;
   - does not prove broad runtime readiness;
   - does not prove answer-quality benchmark success;
   - does not prove provider reasoning orchestration.
6. A clear statement that the first run is a signal source for follow-up tickets,
   not a benchmark.

## Acceptance criteria

- `docs/evals/FIRST_OPERATOR_DEMO_FINDINGS.md` exists.
- `.specs/EVAL-DEMO-FINDINGS-001.md` exists and is registered in
  `.specs/INDEX.md`.
- The findings artifact records the three prompts.
- The findings artifact records only summarized observations.
- The findings artifact includes a plain-vs-Alpha summary, provisional
  interpretation, and finding for each prompt.
- The findings artifact lists the five follow-up tickets.
- The findings artifact includes the required claim boundaries.
- Runtime behavior is unchanged.
- Cloud Run config is unchanged.
- Provider behavior is unchanged.
- Dashboard auth/session/CSRF behavior is unchanged.
- Live OpenAI is not enabled by this work.
- No Google Sheet or backlog workbook update is performed by Codex.

## Validation expectations

Because this is documentation/spec-only work, validation should include:

```bash
git diff --check
python -m pytest -q
```

If the full pytest suite is skipped or cannot complete, report why and still run
`git diff --check`.

## Backlog impact

`EVAL-DEMO-FINDINGS-001` should be marked Done only if this PR is merged. The
finding supports follow-up tickets `UI-PREVIEW-RESPONSE-LAYOUT-001`,
`UI-PREVIEW-REQUEST-METRICS-001`, `ALPHA-FORMAT-PRESERVATION-001`,
`ALPHA-BREVITY-CONTROL-001`, and `ALPHA-CONFIDENCE-CALIBRATION-001`.

This does not validate the MVP, prove Alpha Solver superiority, or prove
production readiness. It also does not prove broad runtime readiness,
answer-quality benchmark success, or provider reasoning orchestration. Backlog
spreadsheets and Google Sheets are not edited from this repo task.

## Non-goals

- No runtime behavior change.
- No Cloud Run configuration change.
- No Cloud Run deployment.
- No provider behavior change.
- No expert-preview behavior change.
- No dashboard auth/session/CSRF change.
- No live OpenAI enablement.
- No persistent storage.
- No automated benchmark claims.
- No Google Sheets or backlog workbook update.
- No MVP validation claim.
- No Alpha Solver superiority claim.
- No production-readiness claim.
- No broad runtime-readiness claim.
- No answer-quality benchmark success claim.
- No provider reasoning orchestration claim.
