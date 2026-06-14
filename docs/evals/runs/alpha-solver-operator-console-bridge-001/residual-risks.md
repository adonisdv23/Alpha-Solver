# Residual Risks

- Sidecar architecture is undecided in this checkout.
- Public exposure remains no-go.
- `/v1/solve` auth/tenancy is not proven for public or sidecar use.
- CORS remains a public-readiness blocker.
- Dashboard session auth must not be assumed sufficient for API bridge auth.
- Evidence capture format for UI sidecar interactions is not yet specified.
- Local model backend behavior remains smoke-only/non-evidence unless a later lane upgrades the evidence model.
- No approved RAG or private-file ingestion boundary exists.
- Provider cost controls for arbitrary sidecar traffic are not proven.
