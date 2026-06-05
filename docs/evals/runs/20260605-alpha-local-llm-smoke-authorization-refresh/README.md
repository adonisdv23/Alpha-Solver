# Local LLM Smoke Authorization Refresh

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-AUTHORIZATION-REFRESH-001`

Status: docs-only authorization refresh after endpoint-locality hardening.

## Decision

Endpoint-locality hardening allows the local LLM track to proceed to a separately authorized smoke execution lane.

## Selected next lane

`ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001`

## Execution boundary

This PR does not execute smoke. The future smoke lane still requires explicit operator approval, localhost / loopback endpoint, exact operator-supplied model name, finite timeout, raw artifact preservation, and sanitized result import afterward.
