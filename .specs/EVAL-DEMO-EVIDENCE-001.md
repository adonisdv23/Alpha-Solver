# EVAL-DEMO-EVIDENCE-001 · Operator Demo Evidence Template

## Purpose

Add a lightweight, repo-tracked evidence template for manual Alpha Solver
operator behavioral demo runs. The template supports the existing
`EVAL-BEHAVIORAL-DEMO-001` checklist by giving operators a consistent way to
record summarized findings without storing raw provider payloads or secrets.

## Background

`docs/OPERATOR_BEHAVIORAL_DEMO_CHECKLIST.md` defines a safe manual protocol for
comparing plain same-provider output against the Alpha Solver expert preview.
Operators need a copyable note format for each run so findings are consistent,
bounded, and safe to share without creating benchmark or validation claims.

## Scope

This spec is documentation-only. It adds:

- `docs/OPERATOR_BEHAVIORAL_DEMO_EVIDENCE_TEMPLATE.md`;
- this spec file;
- registration in `.specs/INDEX.md`;
- a short pointer from the operator behavioral demo checklist to the evidence
  template.

## Requirements

The evidence template must include the following sections.

### Run metadata

- Run ID.
- Date/time.
- Operator.
- Environment.
- Cloud Run URL or service label, summarized or redacted if needed.
- Mode: local-provider smoke, controlled live-provider, or side-by-side
  comparison.
- Provider/model if known, otherwise `unknown`.
- Confirmation that the service was returned to `MODEL_PROVIDER=local` if live
  mode was used.

### Prompt record

- Prompt ID from the checklist.
- Prompt text or short prompt summary.
- Reason the prompt was selected.
- Expected behavior target.

### Output summaries

- Plain provider output summary.
- Alpha Solver expert preview summary.
- The template must not require or encourage raw full-output capture.
- The template must explicitly forbid raw provider payloads, headers, cookies,
  session values, CSRF tokens, API keys, dashboard passwords, and secrets.

### Scoring

Use the same checklist rubric categories and a simple `0` to `2` score for both
plain provider output and Alpha Solver output:

- hidden constraints;
- intent preservation;
- concrete next actions;
- unsupported-claim avoidance;
- clarifying-question discipline;
- useful structure;
- claim-boundary respect;
- assumption visibility;
- operator confidence;
- practical usefulness.

### Defects and follow-up

Capture:

- UI defect found;
- runtime defect found;
- prompt/routing weakness found;
- documentation confusion found;
- suggested backlog item;
- severity;
- evidence summary;
- owner or next reviewer, if known.

### Interpretation

Include conservative outcome options:

- Inconclusive.
- Promising, needs more runs.
- Weak, needs prompt/routing improvement.
- Defect found, create ticket.
- Do not use for claims.

### Claim boundaries

The template must explicitly state:

- One run is not validation.
- This evidence does not prove Alpha Solver superiority.
- This evidence does not prove MVP validation.
- This evidence does not prove production readiness.
- This evidence does not prove answer-quality benchmark success.
- This evidence does not prove provider reasoning orchestration.

## Acceptance criteria

- Evidence template file exists.
- Spec file exists and is registered in `.specs/INDEX.md`.
- Checklist links to the evidence template.
- Template includes metadata, prompt record, output summaries, scoring, defect
  capture, interpretation, and claim boundaries.
- Template forbids storing secrets, raw provider payloads, headers, cookies,
  CSRF tokens, session values, or API keys.
- Runtime behavior is unchanged.
- Cloud Run config is unchanged.
- Provider behavior is unchanged.
- Dashboard auth/session/CSRF behavior is unchanged.
- Live OpenAI is not enabled.
- No Google Sheet update is performed by Codex.

## Validation

Because this is documentation/spec-only work, validation should include:

```bash
git diff --check
python -m pytest -q
```

If the full pytest suite is skipped or cannot complete, report why and include
any focused checks that were run.

## Backlog impact

`EVAL-DEMO-EVIDENCE-001` should be marked Done only if the PR implementing this
spec is merged. This supports `EVAL-BEHAVIORAL-DEMO-001`. This does not validate
the MVP, prove Alpha Solver superiority, or prove production readiness. Backlog
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
