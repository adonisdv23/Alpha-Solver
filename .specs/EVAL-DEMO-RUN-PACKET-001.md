# EVAL-DEMO-RUN-PACKET-001 · One-Page Operator Demo Run Packet

## Purpose

Add a concise operator-facing run packet for one manual Alpha Solver preview test
session. The packet bundles the behavioral demo checklist and evidence template
into a practical step-by-step procedure for comparing plain same-provider output
against the Alpha Solver expert preview while capturing only summarized evidence.

The packet must not claim MVP validation, Alpha Solver superiority, production
readiness, answer-quality benchmark success, broad runtime readiness, or provider
reasoning orchestration.

## Context

The Cloud Run preview lane already has local-provider smoke, controlled one-call
live OpenAI smoke, live-provider opt-in/cap guard, expert-preview loading state,
an operator behavioral demo checklist, and an evidence template. Operators still
need a short run packet that says exactly what to do in one manual session
without rereading all supporting documents.

## Scope

In scope:

- Add `docs/OPERATOR_DEMO_RUN_PACKET.md`.
- Register this spec in `.specs/INDEX.md`.
- Link the run packet to the checklist and evidence template.
- Link the checklist and evidence template back to the run packet.
- Optionally add a deployment-doc pointer.

Out of scope:

- Runtime behavior changes.
- Cloud Run config changes.
- Provider behavior changes.
- Expert-preview behavior changes.
- Dashboard auth, session, or CSRF behavior changes.
- Enabling OpenAI or running live OpenAI from Codex.
- Deploying Cloud Run.
- Persistent storage.
- Automated benchmark claims.
- Google Sheet or backlog workbook updates.

## Run packet requirements

The operator run packet must include:

1. Purpose: run one small manual behavioral demo session, compare plain
   same-provider output against Alpha Solver expert preview, capture summarized
   evidence only, and avoid validation or superiority claims.
2. Before-you-start checks for Cloud Run URL, dashboard password,
   `MODEL_PROVIDER=local` by default unless a live test window is approved, and
   no copying of secrets or raw provider payloads.
3. Default local-provider run sequence for opening `/dashboard/expert-preview`,
   logging in, selecting 3 to 5 checklist prompt IDs, submitting one prompt at a
   time, confirming loading state and both panes, recording evidence, and filing
   follow-up tickets only for real defects or clear routing/prompt weaknesses.
4. Optional controlled live-provider sequence requiring explicit approval,
   `MODEL_PROVIDER=openai`, `ALPHA_LIVE_PREVIEW_ENABLED=true`, a low
   `ALPHA_LIVE_PREVIEW_MAX_REQUESTS` such as `1` or `2`, and a safe-key
   prerequisite that `OPENAI_API_KEY` is configured through the approved secret
   mechanism, preferably Secret Manager. The sequence must warn operators not to
   paste the API key into the run packet, evidence template, screenshots, logs,
   Google Sheets, PR comments, or chat, and not to proceed if the live key is
   missing or cannot be confirmed as mounted safely. It must also include
   `max-instances=1` for the test window when using the current per-process cap,
   approved prompt count only, cap confirmation when in scope, immediate return
   to `MODEL_PROVIDER=local`, and rollback confirmation.
5. Recommended first-run prompt subset covering overclaim prevention, hidden
   constraints, execution planning, corrective next actions, and project-context
   preservation.
6. Evidence packet instructions linking to the evidence template, copying one
   block per prompt, summarizing outputs instead of pasting raw full outputs,
   scoring, and conservative interpretation.
7. Stop conditions for login failure, CSRF or submit errors,
   `Preview request failed`, unexpected live cap behavior, secrets or raw
   payloads appearing in UI/logs/evidence, unsafe or unsupported claims, and
   inability to return to local mode after live testing.
8. Interpretation boundaries: one run is not validation, promising results only
   justify more testing, weak results become prompt/routing tickets, runtime/UI
   failures become defect tickets, and run results must not be used for public
   claims.

## Acceptance criteria

- `docs/OPERATOR_DEMO_RUN_PACKET.md` exists.
- `.specs/EVAL-DEMO-RUN-PACKET-001.md` exists and is registered in
  `.specs/INDEX.md`.
- The run packet links to the checklist and evidence template.
- The checklist and evidence template link back to the run packet.
- The run packet includes local-provider sequence, optional controlled
  live-provider sequence, prompt subset guidance, evidence instructions, stop
  conditions, and claim boundaries.
- Runtime behavior is unchanged.
- Cloud Run config is unchanged.
- Provider behavior is unchanged.
- Dashboard auth/session/CSRF behavior is unchanged.
- Live OpenAI is not enabled.
- No Google Sheet or backlog workbook update is performed by Codex.

## Validation expectations

Because this is docs/spec-only, validation should include:

```bash
git diff --check
python -m pytest -q
```

If the full pytest suite is not practical, report why and still run
`git diff --check`.

## Backlog impact

`EVAL-DEMO-RUN-PACKET-001` should be marked Done only if this PR is merged. This
supports `EVAL-BEHAVIORAL-DEMO-001` and `EVAL-DEMO-EVIDENCE-001`. It does not
validate the MVP, prove Alpha Solver superiority, prove production readiness,
prove broad runtime readiness, prove answer-quality benchmark success, or prove
provider reasoning orchestration. Backlog spreadsheets are not edited from this
repo task.

## Non-goals

- No runtime behavior change.
- No OpenAI enablement.
- No Cloud Run deployment.
- No provider behavior change.
- No expert-preview behavior change.
- No dashboard auth/session/CSRF change.
- No persistent storage.
- No automated benchmark claims.
- No Google Sheets or backlog workbook update.
- No MVP validation claim.
- No Alpha Solver superiority claim.
- No production-readiness claim.
- No broad runtime-readiness claim.
- No answer-quality benchmark success claim.
- No provider reasoning orchestration claim.
