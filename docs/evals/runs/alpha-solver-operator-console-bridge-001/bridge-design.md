# Bridge Design

## Decision

Design only. The bridge is not implemented. This packet binds to the sidecar feasibility packet's selected pattern: the UI sidecar may interact only with an Alpha Solver controlled endpoint, and Alpha Solver remains responsible for routing, policy, SAFE-OUT, evidence, cost, telemetry, and model backend control.

## Current blocker

Bridge implementation remains blocked pending the sidecar security/API-shape decision gate, including the API-shape compatibility gate merged by PR #549. That gate must define the approved endpoint or CLI seam, request mapping, response-envelope mapping, authn/authz, tenant identity, CORS/CSRF constraints for browser-based sidecars, provider lockdown verification, cost controls, telemetry/audit identity, retention, replay, and evidence-capture rules.

## Minimal safe shape after the gate passes

A future bridge may be considered only as a loopback-only operator interface that forwards requests into Alpha Solver instead of calling any model directly.

Required properties:

1. **Alpha Solver controlled endpoint or CLI seam**: the sidecar may call only an approved Alpha Solver endpoint or CLI bridge seam.
2. **Local-only bind**: loopback address only, no public hostname, no external tunnel, no deploy target.
3. **Strict auth boundary**: explicit operator auth separate from dashboard session state; no default credentials; no token capture in evidence.
4. **No direct model bypass**: the sidecar can request Alpha Solver work only through the selected Alpha Solver bridge seam. It must not call hosted providers, local Ollama, or any model backend directly and then label that result Alpha Solver evidence.
5. **Envelope preservation**: responses must preserve Alpha Solver response shape, SAFE-OUT behavior, request IDs, mode/route metadata, cost/accounting metadata when present, telemetry hooks, audit identity, replay hooks, and evidence labels.
6. **Default-off local model backend**: any local model backend must remain controlled by Alpha Solver's local adapter and loopback validation, not by the UI sidecar.
7. **Evidence capture hooks**: capture sanitized request ID, route, verdict, SAFE-OUT status, local-only flags, model/provider disabled state, and non-claim labels.
8. **No RAG/private ingestion**: no repository files, private documents, secrets, credentials, uploads, embeddings, memory, workspace sync, or user file ingestion without a separate approved lane.

## Explicitly rejected shapes

- Public FastAPI route mounted on `service.app`.
- Direct exposure of `/v1/solve` as a sidecar target before API-shape/request mapping is approved.
- CORS expansion for sidecar access from arbitrary origins.
- Dashboard-session reuse as API authorization.
- Direct browser-to-model or sidecar-to-model calls.
- Hosted-provider smoke or token-based preview.
- Credential access or provider-key management from the sidecar.
- Retrieval, RAG, memory, uploads, or private-file ingestion.
