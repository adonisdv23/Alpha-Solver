# Bridge Design

## Decision

Design only. The bridge is not implemented because the required sidecar architecture decision from lane 33 is not present in this repository checkout.

## Minimal safe shape after dependency is satisfied

A future bridge may be considered only as a loopback-only operator interface that forwards requests into Alpha Solver instead of calling any model directly.

Required properties:

1. **Local-only bind**: loopback address only, no public hostname, no external tunnel, no deploy target.
2. **Strict auth boundary**: explicit operator auth separate from dashboard session state; no default credentials; no token capture in evidence.
3. **No direct model bypass**: the sidecar can request Alpha Solver work only through the selected Alpha Solver bridge seam. It must not call hosted providers, local Ollama, or any model backend directly and then label that result Alpha Solver evidence.
4. **Envelope preservation**: responses must preserve Alpha Solver response shape, SAFE-OUT behavior, request IDs, mode/route metadata, cost/accounting metadata when present, and evidence labels.
5. **Default-off local model backend**: any local model backend must remain controlled by Alpha Solver's local adapter and loopback validation, not by the UI sidecar.
6. **Evidence capture hooks**: capture sanitized request ID, route, verdict, SAFE-OUT status, local-only flags, model/provider disabled state, and non-claim labels.
7. **No RAG/private ingestion**: no repository files, private documents, secrets, or user file ingestion without a separate approved lane.

## Explicitly rejected shapes

- Public FastAPI route mounted on `service.app`.
- CORS expansion for sidecar access from arbitrary origins.
- Dashboard-session reuse as API authorization.
- Direct browser-to-model or sidecar-to-model calls.
- Hosted-provider smoke or token-based preview.
- Retrieval or private-file ingestion.
