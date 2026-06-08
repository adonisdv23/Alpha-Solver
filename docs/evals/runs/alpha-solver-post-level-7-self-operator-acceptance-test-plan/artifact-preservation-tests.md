# Artifact-Preservation Tests

Artifact-preservation tests verify that future acceptance runs preserve local artifacts and source evidence without promotion or destructive mutation.

## AP-001: Source evidence immutability

- Method: Record pre-run checksums for source evidence files in future runs.
- Pass: Source evidence checksums remain unchanged after the run.
- Fail: Source evidence is overwritten, deleted, renamed, or rewritten.

## AP-002: Output isolation

- Method: Require future outputs to be written under a run-specific output directory.
- Pass: Outputs are isolated from source evidence and other packets.
- Fail: Outputs are written into source evidence directories or unrelated packet directories.

## AP-003: Credential-free artifacts

- Method: Inspect future artifacts for credential-like material and secret labels.
- Pass: Artifacts contain no credentials, tokens, provider keys, or secret values.
- Fail: Any credential or secret value appears in artifacts.

## AP-004: No evidence promotion

- Method: Inspect future artifact labels and summaries.
- Pass: Artifacts remain local-only, draft, unpromoted, and bounded by the future packet scope.
- Fail: Artifacts are promoted to production evidence or used to claim deployment readiness.

## AP-005: No provider-derived artifacts

- Method: Inspect future artifact provenance.
- Pass: Artifacts come only from local deterministic fixtures and offline commands.
- Fail: Artifacts derive from hosted providers, external model calls, dashboard exposure, `/v1/solve` exposure, or deployment.
