# EVAL-ARTIFACT-PRESERVE-001 · Preserve Eval Summary Artifacts

## Purpose

Add a safe committed-documentation path for no-live answer-quality eval summary artifacts so future eval and behavioral-demo review can cite durable repo artifacts rather than ignored local outputs or operator-reported summaries.

## Scope

- Applies only to `scripts/run_answer_quality_eval.py` answer-quality eval summary preservation.
- Adds an opt-in `--save-summary` CLI path for no-live runs.
- Writes the safe summary artifact under `docs/evals/runs/` by default.
- Keeps existing no-live behavior safe and non-live by default.
- Keeps live provider execution behind the existing `--live`, `ALPHA_LIVE_ANSWER_QUALITY=1`, key, and cost-ceiling gates.

## Artifact path

The default committed artifact path is:

```text
docs/evals/runs/answer_quality_no_live_summary.json
```

Tests and local checks may override the destination with `--summary-output PATH` to avoid mutating committed evidence files during automated runs.

## Artifact safety exclusions

The no-live summary artifact must include only summary-level fields such as schema version, no-live mode, dataset path/hash, case count, categories, quality-gate reference, pre-registered success criteria, model/settings metadata, estimated pre-flight cost, skipped/no-live status, safety exclusions, and claim boundaries.

The artifact must not include API keys, auth headers, raw provider payloads, raw request/response bodies, raw prompts, generated answer text, environment dumps, broad telemetry dumps, exception dumps, raw secrets, credentials, or provider raw metadata.

## Validation expectations

Tests should prove:

- no-live eval can write a summary artifact when `--save-summary` is used;
- the artifact is written under the intended safe path or an injected test path;
- the artifact excludes obvious sensitive fields and unsafe dump markers;
- default no-live behavior does not write the committed summary artifact unless opted in;
- existing no-live eval behavior still makes no provider calls;
- live-gated behavior is not enabled or broadened;
- docs mention the artifact path and safety exclusions.

## Backlog impact

`EVAL-ARTIFACT-PRESERVE-001` should be marked Done only after the PR implementing this spec is merged. The PR should be added as implementation evidence for this lane. Backlog spreadsheets are not edited from this repo task.

## Non-goals

- No MVP validation claim.
- No Alpha Solver superiority claim.
- No answer-superiority claim.
- No production-readiness claim.
- No broad runtime-readiness claim.
- No answer-quality benchmark success claim.
- No provider reasoning orchestration claim.
- No UI preview.
- No behavioral demo checklist.
- No live provider tests.
- No broad eval platform.
- No provider expert-pass behavior changes.
- No clarify behavior changes.
- No backlog workbook edits.
