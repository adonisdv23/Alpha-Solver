# Consolidation Candidates

These are staged strategy candidates only. They are not implementation tasks in this PR.

## Stage 0 — Keep mapping authoritative

- Keep this packet as the runtime entrypoint inventory for future architecture decisions.
- Require future runtime exposure PRs to cite which entrypoint(s) they touch.

## Stage 1 — Documentation-only alignment

- Add a concise public/non-public entrypoint table to `docs/ENTRYPOINTS.md` or a successor architecture doc.
- Cross-link the DEF-002 security/privacy packet and this runtime map.
- Document that bundled `/v1/solve` currently uses API-key/rate-limit controls, not the separate JWT/tenant middleware stack.

## Stage 2 — Low-risk config clarification

- Confirm intended auth/tenancy model for `/v1/solve` without changing code.
- Confirm whether standalone dashboard settings/request/run/jobs routes are legacy/demo-only or future product surfaces.

## Stage 3 — Only after value/security proof

- Consider unifying rate-limit semantics and telemetry labels.
- Consider explicit mount manifests for dashboard/evidence/service routers.
- Consider portable-vs-modular behavior drift tests before any contract consolidation.

## Not authorized here

No rewrite, runtime consolidation, route exposure, provider validation, credential migration, auth refactor, or dashboard enablement is authorized by this packet.
