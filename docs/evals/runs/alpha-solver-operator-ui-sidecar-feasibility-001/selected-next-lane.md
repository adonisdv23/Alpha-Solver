# Selected next lane

## Selected lane

**ALPHA-SOLVER-OPERATOR-UI-SIDECAR-API-SHAPE-SECURITY-GATE-001**

## Purpose

Decide the security and API-shape gates required before any UI sidecar can be connected to an Alpha Solver controlled endpoint. This is not direct sidecar deployment.

## Required decisions

- Confirm that Alpha Solver's current route contract is not assumed OpenAI-compatible.
- Account for the current `/v1/solve` request shape, including the required `query` field.
- Decide whether the next implementation should be a minimal Alpha-native local console, an OpenAI-compatible shim, a sidecar native request mapper, or no sidecar integration yet.
- If considering Open WebUI, LibreChat, or a custom endpoint, prove that the trial is blocked until an approved compatibility path exists.
- Endpoint exposure model: local-only, loopback, LAN, or authenticated shared deployment.
- Authn/authz model and per-user audit identity.
- CORS/CSRF/session constraints for browser-based sidecars.
- Provider lockdown requirements and verification method.
- Upload/RAG/memory/tooling disablement requirements.
- Conversation retention, deletion, export, and replay policy.
- Evidence-envelope rendering contract.
- Configuration test plan proving the UI cannot bypass Alpha Solver routing.

## Initial implementation lane after this gate

If gates pass, implement only the selected approved lane. The default preference remains a **minimal local operator console prototype** rather than integrating a full third-party UI first. Open WebUI, LibreChat, or custom endpoint integration remains blocked unless an OpenAI-compatible shim/adapter, confirmed native request mapping, or separate approved bridge lane preserves Alpha Solver router, policy, SAFE-OUT, evidence, auth, tenancy, CORS, cost, and observability boundaries.
