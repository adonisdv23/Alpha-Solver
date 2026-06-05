# Alpha Local LLM Smoke-Test Packet

Lane: `ALPHA-LOCAL-LLM-SMOKE-TEST-PACKET-001`

Status: draft/prepared reference only, blocked pending endpoint-locality hardening.

## Purpose

This directory prepares a future local smoke-test packet for the offline adapter/parser implementation. The packet contains templates and operator instructions only. It does not include an actual model name, access material, private endpoint, raw result, or executed command output.

## Blocking condition

This packet must not proceed directly to execution. A later smoke lane must not run until the backend fails closed on non-loopback / non-local endpoint URLs before invoking any transport.

The future hardening lane must add tests proving hosted URLs such as `https://example.com/api/chat` fail closed without transport invocation. Localhost or loopback endpoint validation must be implemented before smoke can be authorized.

## Contents

- `smoke-test-task-set.md`
- `smoke-command-template.md`
- `operator-instructions.md`
- `raw-artifact-log-template.md`
- `smoke-feedback-template.md`
- `result-import-requirements.md`
- `evidence-boundary.md`
- `recommended-next-lane.md`
- `smoke-packet-preservation-checklist.md`

## Future execution requirement

A later explicitly approved operator lane is required before any command in this packet may be run, and that lane remains blocked until endpoint-locality hardening is merged and reviewed.
