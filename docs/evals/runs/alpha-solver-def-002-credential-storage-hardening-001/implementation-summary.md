# Implementation summary

## Lane

`ALPHA-SOLVER-DEF-002-CREDENTIAL-STORAGE-HARDENING-001`

## Risk addressed

RR-02 recorded High-severity plaintext provider secrets at rest in dashboard
file-backed provider key storage. This lane materially reduces that risk by
hardening the existing file-backed storage permissions without changing provider,
model, dashboard exposure, auth, tenancy, CORS, or `/v1/solve` behavior.

## Changes made

- Added private storage mode constants for dashboard private artifacts:
  directory mode `0700` and file mode `0600`.
- Added parent-directory handling that creates app-owned storage directories with
  `0700` on POSIX platforms.
- Changed existing caller-supplied parent directory handling so existing parents
  are not silently chmodded.
- Added fail-closed POSIX validation for existing storage parents with any group
  or world permission bits before writing credential or audit artifacts.
- Updated `FileSecretsBackend` writes to create credential files with `0600` and
  tighten the file itself to `0600` after writes.
- Updated the dashboard settings audit log writer to create audit files with
  `0600` and tighten the file itself to `0600`; audit records remain masked.
- Preserved existing masked display behavior for provider API keys.
- Added focused tests using synthetic placeholder secrets only.

## Design choice

This lane selected the smallest correct implementation direction: protected
file-backed storage with fail-closed parent-directory validation. It did not add
encryption, OS keyring integration, migration machinery, or a new key-management
system because no suitable existing mechanism was required for this narrow RR-02
file-permission closure lane.

## Platform note

POSIX mode assertions are covered by tests and skipped on non-POSIX platforms
because Unix permission bits are not portable across all operating systems.
