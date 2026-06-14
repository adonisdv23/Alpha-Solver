# Selected next lane

## Selected lane

**ALPHA-SOLVER-OPERATOR-UI-SIDECAR-SECURITY-GATES-001**

## Purpose

Decide the security and exposure gates required before any UI sidecar can be connected to an Alpha Solver controlled endpoint.

## Required decisions

- Endpoint exposure model: local-only, loopback, LAN, or authenticated shared deployment.
- Authn/authz model and per-user audit identity.
- CORS/CSRF/session constraints for browser-based sidecars.
- Provider lockdown requirements and verification method.
- Upload/RAG/memory/tooling disablement requirements.
- Conversation retention, deletion, export, and replay policy.
- Evidence-envelope rendering contract.
- Configuration test plan proving the UI cannot bypass Alpha Solver routing.

## Initial implementation lane after security gates

If gates pass, implement a **minimal local operator console prototype** rather than integrating a full third-party UI first.
