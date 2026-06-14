# Residual Risks

- Sidecar feasibility is captured, but the sidecar security/API-shape gate is not complete.
- The exact bridge endpoint or CLI seam and request mapping are not approved.
- Public exposure remains no-go.
- `/v1/solve` auth/tenancy is not proven for public or sidecar use.
- CORS/CSRF behavior for a browser-based sidecar remains a blocker.
- Dashboard session auth must not be assumed sufficient for API bridge auth.
- Provider lockdown verification for UI sidecars is not yet specified.
- Evidence capture format for UI sidecar interactions is not yet specified.
- Conversation retention, deletion, export, audit identity, and replay policy are not decided.
- Local model backend behavior remains smoke-only/non-evidence unless a later lane upgrades the evidence model.
- No approved RAG, upload, memory, workspace sync, embedding, or private-file ingestion boundary exists.
- Provider cost controls for arbitrary sidecar traffic are not proven.
