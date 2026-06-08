# Local-Only Smoke Test Plan

Local smoke tests are future checks that may run only offline, deterministic, local commands. This packet does not run them.

## LS-001: Offline command harness smoke

- Method: Run only a future offline harness that uses local fixtures and deterministic sample inputs.
- Pass: The harness completes without network access, provider calls, credentials, dashboard exposure, `/v1/solve` exposure, deployment, fallback, or evidence promotion.
- Fail: The harness attempts network access, provider access, credential access, route exposure, deployment, fallback, or promotion.

## LS-002: Local fixture availability smoke

- Method: Verify required local fixture files exist and can be read without service startup.
- Pass: Fixtures are present and readable locally.
- Fail: The smoke check downloads fixtures, calls providers, requests credentials, or starts services.

## LS-003: Fail-closed local prerequisite smoke

- Method: Simulate missing local-only prerequisites in a future isolated environment.
- Pass: The harness fails closed with a documented stop condition and no fallback.
- Fail: The harness falls back to provider-backed behavior, credentials, dashboard routes, `/v1/solve`, or deployment paths.

## LS-004: Local artifact write smoke

- Method: Write future smoke outputs only to a local packet-specific output directory.
- Pass: New artifacts are local, timestamped or uniquely named, and do not overwrite source evidence.
- Fail: Artifacts overwrite source evidence, promote results, write credentials, or require external storage.
