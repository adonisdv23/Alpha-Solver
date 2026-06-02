# EVAL-ARTIFACT-PRESERVE-001 · Preserve Evaluation Artifacts for Comparison Runs

## Status

Documentation/spec-first lane for `OUTPUT-DIFFERENTIATION-PHASE-001`.

This spec defines how future Alpha-vs-plain evaluation runs preserve durable,
citable, sanitized artifacts. It does not change runtime behavior, provider
behavior, dashboard behavior, Cloud Run configuration, OpenAI enablement, or
Google Sheet planning ledgers.

## Purpose

Future higher-headroom evals must be inspectable from the repository instead of
relying on screenshots, chat memory, temporary local files, or operator notes.
This lane creates the preservation contract for summarized artifacts so future
runs can be cited, reviewed, and used for conservative decision-making.

The supervised preview remains operator-test-ready only. This artifact lane does
not validate the MVP, prove Alpha Solver superiority, prove production
readiness, prove benchmark success, or prove provider reasoning orchestration.

## Scope

In scope:

- Define the committed documentation lane for future eval run artifacts.
- Define artifact locations, names, required summary fields, side-by-side fields,
  redaction rules, acceptable artifact types, evidence strength levels, and claim
  boundaries.
- Add a copyable future run-report template under `docs/evals/templates/`.
- Preserve the existing `docs/evals/runs/` path for sanitized, summarized run
  artifacts.

Out of scope:

- Runtime behavior changes.
- Provider behavior changes.
- Dashboard behavior changes.
- Cloud Run config changes.
- Enabling OpenAI or running live provider evals.
- Deployment.
- Google Sheets updates.
- Raw provider payload storage.
- Broad eval platform implementation.

## Source hierarchy

When interpreting future eval artifacts, source authority is:

1. Repo code and tests.
2. Repo specs and docs, including this spec and `docs/evals/ARTIFACT_PRESERVATION.md`.
3. External planning/status ledgers, including Google Sheets.
4. AI-generated outputs and chat summaries, which are advisory unless preserved
   with evidence under this artifact lane.

If artifacts conflict with code/tests, code/tests win. If a planning ledger
conflicts with repo specs/docs, repo specs/docs win until the repo contract is
changed.

## Artifact location

Future eval preservation artifacts should live under:

```text
docs/evals/runs/
```

Copyable templates and instructions should live under:

```text
docs/evals/templates/
docs/evals/ARTIFACT_PRESERVATION.md
```

Artifacts under `docs/evals/runs/` must be sanitized, summary-level, and
appropriate for committing. Large raw traces, raw provider payloads, or local
archives do not belong in this lane.

## Naming conventions

Use stable, lowercase, hyphenated run directories or Markdown/JSON filenames.
Future Alpha-vs-plain comparison runs should use:

```text
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>/
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>/run-summary.md
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>/score-table.csv
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>/defects.md
```

For single-file summarized artifacts, use:

```text
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>-summary.md
```

Examples:

```text
docs/evals/runs/20260602-higher-headroom-eval-001-smoke/run-summary.md
docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain-summary.md
```

Run IDs should match the artifact path stem and include the lane ID when
possible. Do not encode secrets, provider account names, private customer names,
or raw prompt text in file or directory names.

## Required eval run summary fields

Every future run summary must include:

- Run ID.
- Date.
- Operator.
- Branch/commit.
- Provider/mode.
- Prompt set.
- Prompt count.
- Live mode used: yes/no.
- Request cap used.
- Rollback confirmed: yes/no/not applicable.
- Plain output summary.
- Alpha output summary.
- Rubric used.
- Score table or score-table reference.
- Alpha advantages observed.
- Plain advantages observed.
- Defects or regressions.
- Metrics summary.
- Evidence strength.
- Redactions performed.
- Conservative interpretation.
- Follow-up tickets.
- Non-claims.

## Required side-by-side comparison fields

Every Alpha-vs-plain side-by-side artifact must include:

- Comparison ID.
- Parent Run ID.
- Prompt ID or sanitized prompt label.
- Prompt category or capability being tested.
- Plain provider/mode and configuration summary.
- Alpha provider/mode and configuration summary.
- Plain output summary, not raw provider output.
- Alpha output summary, not raw provider output.
- Rubric dimensions used for this comparison.
- Per-dimension scores for plain output.
- Per-dimension scores for Alpha output.
- Winner/tie/no-decision field, if the rubric permits that conclusion.
- Explanation limited to evidence preserved in the artifact.
- Defects or regressions for each side.
- Redactions performed.
- Evidence strength.
- Non-claims.

## Redaction and storage rules

Before committing any eval artifact, redact or omit:

- Secrets and credentials.
- Runtime account metadata that could identify provider accounts or private
  tenants.
- Private user data unless explicitly sanitized and necessary for the eval.
- Raw prompts when they contain private, sensitive, or proprietary material.
- Raw output text when it contains private, sensitive, or proprietary material.
- Screenshots unless they are sanitized and referenced with a clear description
  of what was redacted.

Artifacts must state what redactions were performed. If a safe summary cannot be
created without preserving sensitive data, do not commit the artifact.

## Material that must never be stored

The following must never be committed or intentionally preserved in this lane:

- API keys.
- Bearer tokens.
- Dashboard passwords.
- Cookies.
- CSRF tokens.
- Session values.
- Raw provider payloads.
- Provider account identifiers.
- Full unredacted request/response traces.
- Private user data unless explicitly sanitized and needed.

## Acceptable artifact types

The preservation lane accepts only sanitized, summary-level artifacts such as:

- Summarized run report.
- Prompt set manifest.
- Scoring rubric reference.
- Summarized plain output.
- Summarized Alpha output.
- Score table.
- Defect list.
- Conservative interpretation.
- Screenshot reference if sanitized.

## Evidence strength levels

Future artifacts must label evidence strength using one or more of these levels:

1. `operator-reported-summary` — operator reported the result, but the repo does
   not preserve supporting artifacts.
2. `screenshot-backed-summary` — summary is backed by sanitized screenshots or
   screenshot references.
3. `repo-preserved-summarized-artifact` — sanitized summary artifacts are
   preserved in the repo.
4. `automated-test-backed-artifact` — artifact generation or validation is backed
   by automated tests.
5. `live-provider-artifact-with-sanitized-metrics` — live provider run metrics
   are preserved in sanitized form without raw payloads or sensitive material.

Higher evidence strength improves reviewability, but none of these levels alone
turns an eval into proof of superiority or production readiness.

## Claim boundaries

Artifact preservation does not prove or imply:

- MVP validation.
- Alpha Solver superiority.
- Production readiness.
- Broad runtime readiness.
- Benchmark success.
- Exact billing accuracy.
- Provider reasoning orchestration.

Future run reports must include a `Non-claims` section carrying these boundaries
unless a later, explicit spec narrows or extends them with evidence.

## Supported next-phase lanes

This lane supports the next phase by making future evidence durable and citable:

- `HIGHER-HEADROOM-EVAL-001` can preserve sanitized run summaries before more
  live eval spend.
- `DISC-MRG-069` and `DISC-MRG-068` can cite preserved artifacts instead of chat
  memory or temporary operator notes.
- `ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001` can assemble side-by-side evidence
  packets from sanitized preserved comparisons.
- Future `EVAL-DIFFERENTIATION-RUN-001` can record Alpha-vs-plain output
  summaries, score tables, defects, metrics, redactions, evidence strength, and
  conservative interpretation in a consistent form.

## Validation expectations

For this docs/spec-first lane:

- Run `git diff --check`.
- Run `python -m pytest -q` when practical.
- If full pytest is skipped for a docs-only change, explain why and still run
  `git diff --check`.

No live provider calls are required or allowed by this lane.

## Backlog impact

`EVAL-ARTIFACT-PRESERVE-001` should be marked Done only after the implementing PR
is merged. This is P0 for `OUTPUT-DIFFERENTIATION-PHASE-001` and enables future
higher-headroom evals and Alpha-vs-plain evidence packets.

This lane does not prove Alpha Solver superiority, validate the MVP, or prove
production readiness. Backlog spreadsheets are not edited from this repo task.
