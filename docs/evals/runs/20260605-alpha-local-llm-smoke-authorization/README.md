# Alpha Local LLM Smoke Authorization

Lane: `ALPHA-LOCAL-LLM-SMOKE-AUTHORIZATION-001`

Status: docs-only authorization boundary.

## Decision

Direct smoke execution is not authorized in this PR.

This lane authorizes preparation of a future smoke-test packet only. The selected packet lane is `ALPHA-LOCAL-LLM-SMOKE-TEST-PACKET-001`, and that packet is prepared in this same PR.

## Boundary

No local service, local model, hosted service, runtime route, dashboard path, or operator run may be executed by this lane.
