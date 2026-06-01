# EVAL-BEHAVIORAL-DEMO-001 · Operator Behavioral Demo Checklist for MVP Preview

## Purpose

Create a repo-tracked operator checklist for a small, disciplined behavioral demo
of the deployed Alpha Solver MVP preview at:

```text
/dashboard/expert-preview
```

The checklist helps an operator compare plain same-provider output against the
Alpha Solver expert preview and decide whether the preview is promising enough
for further testing. It is not an answer-quality benchmark and does not validate
Alpha Solver, the MVP, production readiness, provider reasoning orchestration, or
superiority over a provider.

## Context

The Cloud Run preview lane has demonstrated that the hosted path can be exercised
under guardrails: local-provider smoke, dashboard login, expert-preview loading,
browser submit, login redirect, duplicate-submit loading state, live-provider
spend guard, one controlled live OpenAI preview smoke, cap blocking on a second
live submit, and return to `MODEL_PROVIDER=local`.

The remaining gap for this lane is an operator-facing protocol for judging
whether Alpha Solver provides noticeable behavioral value over plain output from
the same provider.

## Scope

In scope:

- Add `docs/OPERATOR_BEHAVIORAL_DEMO_CHECKLIST.md`.
- Register this spec in `.specs/INDEX.md`.
- Optionally add short documentation pointers from deployment/readiness docs.
- Keep all instructions operator-facing and manually executable.
- Preserve strict claim boundaries and secret-handling rules.

Out of scope:

- Runtime behavior changes.
- Cloud Run config changes.
- Provider behavior changes.
- Dashboard auth, session, CSRF, or expert-preview behavior changes.
- Enabling OpenAI or running live OpenAI from Codex.
- Persistent storage, benchmark infrastructure, or automated scoring.
- Google Sheet or backlog workbook updates.

## Checklist requirements

The operator checklist must include:

1. Preconditions:
   - Cloud Run URL is available.
   - Dashboard password is available.
   - Service is in `MODEL_PROVIDER=local` by default.
   - Live OpenAI testing requires explicit approval.
   - Live mode, if used, has a low cap and returns to local mode afterward.
2. Test modes:
   - Local-provider UI smoke mode.
   - Controlled live-provider mode.
   - Manual side-by-side operator comparison mode.
3. A prompt set of 8 to 12 non-high-stakes demo prompts covering ambiguity,
   hidden constraints, risk/safety boundaries, execution planning,
   project-context preservation, overclaim prevention, corrective next actions,
   concise answers under uncertainty, and refusal or safe-out boundaries where
   applicable.
4. A simple manual rubric comparing plain provider output and Alpha Solver expert
   preview output using criteria such as hidden constraints, intent preservation,
   next actions, unsupported-claim avoidance, clarifying-question discipline,
   useful structure, claim boundaries, assumptions, operator confidence, and
   practical usefulness.
5. Evidence capture guidance for date/time, mode, provider/model if known,
   prompt, plain-output summary, Alpha-output summary, score, operator notes,
   defects, and whether to create a backlog item.
6. Explicit prohibition on storing raw provider payloads, secrets, headers,
   cookies, or API keys as required evidence.
7. Strict pass/fail interpretation: one good result is not validation; promising
   outputs justify only further testing; Done means the checklist exists; no
   claims of superiority, MVP validation, production readiness, answer-quality
   benchmark success, or provider reasoning orchestration.
8. Recommended next actions for defect tickets, prompt/routing tickets,
   documentation updates, and blocking broader testers until repeatable demo
   results are acceptable.

## Acceptance criteria

- `.specs/EVAL-BEHAVIORAL-DEMO-001.md` exists and is registered in
  `.specs/INDEX.md`.
- `docs/OPERATOR_BEHAVIORAL_DEMO_CHECKLIST.md` exists.
- The checklist includes preconditions, test modes, prompt set, scoring rubric,
  evidence capture template, pass/fail interpretation, and next actions.
- The checklist preserves strict claim boundaries.
- The checklist does not require secrets or raw provider payload capture.
- Runtime behavior is unchanged.
- Cloud Run config is unchanged.
- Provider behavior is unchanged.
- Dashboard auth/session/CSRF behavior is unchanged.
- Live OpenAI is not enabled.
- No Google Sheet or backlog workbook update is performed by Codex.

## Validation expectations

Because this is a docs/spec-only lane, validation should include:

```bash
git diff --check
python -m pytest -q
```

If the full pytest suite is not practical in the execution environment, report
what was run and why the full suite was skipped or could not complete.

## Backlog impact

`EVAL-BEHAVIORAL-DEMO-001` should be marked Done only if the PR implementing this
spec is merged. This enables disciplined operator testing after Cloud Run local
and controlled live-provider smoke. It does not validate the MVP, prove Alpha
Solver superiority, or prove production readiness. Backlog spreadsheets are not
edited from this repo task.

## Non-goals

- No MVP validation claim.
- No Alpha Solver superiority claim.
- No answer-quality superiority claim.
- No production-readiness claim.
- No broad runtime-readiness claim.
- No answer-quality benchmark success claim.
- No provider reasoning orchestration claim.
- No runtime behavior change.
- No Cloud Run deployment.
- No provider behavior change.
- No expert-preview behavior change.
- No dashboard auth/session/CSRF change.
- No persistent storage.
- No live OpenAI enablement.
- No Google Sheets or backlog workbook edit.
