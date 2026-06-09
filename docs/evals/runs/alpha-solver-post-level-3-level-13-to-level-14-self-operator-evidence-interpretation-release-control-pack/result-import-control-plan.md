# Result Import Control Plan

This file prepares future import control only. It does not import evidence and does not interpret real results.

## Import owner

- Import is performed by a later explicitly authorized result-import lane.
- The operator provides the output root and confirms that the artifacts are from operator-supervised local acceptance.

## Files allowed to be imported

- Raw JSON artifacts from the operator-provided local output root.
- Checksum or integrity notes created for those raw artifacts.
- Operator notes that identify task ID, run ID, lane ID, commit SHA, and redaction status.

## Files not allowed to be imported

- Source code, tests, fixtures, scripts, CI, Makefile, credentials, deployment files, billing files, provider outputs, hosted-model outputs, browser automation output, Google Sheets files, source artifacts, or promoted evidence.

## Where summaries may be written

- A later import lane may write concise summaries only in its own new packet directory.
- It must not modify existing packets or the raw artifacts.

## Required source evidence

- Level 12 dry-run wrapper evidence, including `run_local_dry_run_wrapper`, `DryRunResult`, `write_dry_run_result_json`, and `ready_for_operator_supervised_local_dry_run`.
- Manual local acceptance packet and operator execution evidence, once available.

## Required artifact integrity checks

- Complete `artifact-integrity-checklist.md` for each imported artifact.
- Record checksum or integrity notes before any interpretation.

## Stop conditions

- Missing raw artifact, malformed JSON, path outside output root, missing lane/run/task identity, unresolved redaction issue, source mutation concern, evidence promotion concern, or any request to claim readiness during import.

No Google Sheets update is allowed unless the operator explicitly asks in a later lane. No evidence interpretation is allowed during import unless a separate interpretation lane is active.
