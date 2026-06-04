# Operator Run Checklist

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-RUN-WORKSHEET-001`

This checklist is for manual execution only. It does not authorize capture, scoring, rescoring, unblinding, provider calls, `/v1/solve`, runtime testing, Batch C, Google Sheets updates, or readiness claims.

## Pre-run checklist

- [ ] Open the original operator test task set.
- [ ] Open the original feedback form, result log template, defect log, stop conditions, and claim boundaries.
- [ ] Confirm the first pass is the smoke subset: `LT-001` through `LT-006`.
- [ ] Confirm `LT-007` through `LT-010` are optional if time allows.
- [ ] Confirm no rows, ratings, snippets, defects, or conclusions are prefilled.
- [ ] Confirm the run is portable-surface operator feedback only, not validation or benchmark scoring.

## During-run checklist

- [ ] Paste one task prompt at a time from the task set.
- [ ] Record only observed response snippets.
- [ ] Fill ratings only after observing each response.
- [ ] Mark `keep`, `refine`, or `reject` only after reviewing the observed response.
- [ ] Log defects using the defect taxonomy when defect signals appear.
- [ ] Keep snippets short and sufficient; do not copy unnecessary raw output.
- [ ] Stop immediately if any stop condition is reached.

## Stop-condition reminders

Stop the test if Alpha:

- fabricates repo state, PR status, file paths, results, scores, or readiness claims;
- claims runtime, `/v1/solve`, provider behavior, production readiness, validation, superiority, or Batch C readiness;
- reconstructs missing results from memory;
- uses raw outputs or operator maps without authorization;
- repeatedly over-frames low-headroom tasks;
- gives multiple next lanes when exactly one was requested;
- starts Batch C or runtime work;
- produces output that cannot be safely interpreted.

If a stop condition occurs:

1. Stop immediately.
2. Record the task ID and stop condition.
3. Preserve the smallest safe evidence snippet needed to explain the stop.
4. Do not reconstruct results, score, rescore, unblind, run capture, call providers, update Google Sheets, start Batch C, or make readiness claims.

## Post-run checklist

- [ ] Confirm every entered snippet came from an observed response.
- [ ] Confirm every rating was filled after observation.
- [ ] Confirm defect entries cite observed behavior only.
- [ ] Confirm no result language exceeds limited operator feedback.
- [ ] Confirm no validation, superiority, production readiness, runtime, provider, `/v1/solve`, or Batch C claims were added.
- [ ] Preserve the completed worksheet/logs as operator feedback artifacts.

## What to send to Codex after completion

Send only the completed manual-run artifacts and a short note containing:

- tasks actually run;
- whether any stop condition occurred;
- where the completed result capture, feedback, and defect notes are stored;
- confirmation that ratings and snippets are observed manual-run data only;
- any explicit request for a separate follow-up lane, if needed.
