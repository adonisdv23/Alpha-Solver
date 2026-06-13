# Selected next lane

Recommended DEF-002-local next remediation lane:
`ALPHA-SOLVER-DEF-002-DEFAULT-CREDENTIALS-HARDENING-001`

## Rationale

The public exposure gate remains captured as no-go. PR #521 merged the accepted
credential-storage hardening evidence packet,
`ALPHA-SOLVER-DEF-002-CREDENTIAL-STORAGE-HARDENING-001`, which records
`DEF_002_RR_02_CREDENTIAL_STORAGE_HARDENED` for the narrow RR-02 file-backed
dashboard credential-storage boundary. DEF-002 as a whole remains open.

The next public-exposure-readiness/security remediation step should therefore
follow the DEF-002-local sequence to RR-03 default credential hardening:
`ALPHA-SOLVER-DEF-002-DEFAULT-CREDENTIALS-HARDENING-001`.

## Boundary

This is a DEF-002-local recommendation only. It does not replace the repo-global
selected next lane, which remains controlled by `docs/CURRENT_STATE.md` and
`docs/LANE_REGISTRY.md`.

This selection is not an exposure lane. It does not authorize public API,
`/v1/solve`, dashboard, provider calls, token use, deployment, production
readiness, security/privacy completion, public readiness, or DEF-002 closeout.
