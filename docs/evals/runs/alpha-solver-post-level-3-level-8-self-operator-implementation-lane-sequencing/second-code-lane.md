# Second code lane

## Recommended second future code lane

The second future code lane should be a **local artifact schema code scaffold** lane, after the static test scaffold exists and passes.

## Allowed future intent

A later authorized local artifact schema lane may add minimal local-only structures for:

- run metadata;
- prompts and prompt redaction markers;
- local output capture references;
- operator confirmation records;
- stop reasons;
- blocked-state reasons;
- review notes.

## Why this comes second

Artifact schemas should precede runnable preflight and harness work because later execution must have a deterministic place to write local evidence, stop reasons, and operator confirmations. Without this scaffold, later runner work could create ad hoc artifacts that are harder to audit.

## Not started here

This packet does not create schema code, artifact files, migrations, runtime output directories, or generated evidence.
