# Safe closure sequence

This DEF-002-local remediation sequence is ordered by risk, blast radius, and
dependency. Each lane remains narrow and must produce evidence before the next
risk category is considered. This sequence does not change the repo-global
selected next lane; repo-global lane selection remains controlled by
`docs/CURRENT_STATE.md` and `docs/LANE_REGISTRY.md`.

1. `ALPHA-SOLVER-DEF-002-CREDENTIAL-STORAGE-HARDENING-001`
   - Close or materially reduce RR-02.
   - No provider calls; use synthetic placeholder values only.
2. `ALPHA-SOLVER-DEF-002-DEFAULT-CREDENTIALS-HARDENING-001`
   - Close RR-03 after storage behavior is safe.
   - Prove known defaults are not usable by default.
3. `ALPHA-SOLVER-DEF-002-CORS-DEFAULT-HARDENING-001`
   - Close RR-01 by tightening default CORS behavior.
4. `ALPHA-SOLVER-DEF-002-SOLVE-AUTH-TENANCY-DECISION-001`
   - Close RR-09 by either documenting the intended API-key-only model with
     explicit exposure blockers or wiring the selected JWT/tenant model.
5. `ALPHA-SOLVER-DEF-002-DATA-CLASSIFICATION-RECONCILIATION-001`
   - Close RR-05 by establishing one authoritative classification policy or
     documented precedence.
6. `ALPHA-SOLVER-DEF-002-DEPENDENCY-LOCK-HASHING-001`
   - Close RR-07 and coordinate with RR-06.
7. `ALPHA-SOLVER-DEF-002-VENDORED-DEPENDENCY-PROVENANCE-001`
   - Close RR-08 with inventory/provenance or replacement.
8. `ALPHA-SOLVER-DEF-002-DEPENDENCY-SOURCE-OF-TRUTH-001`
   - Close remaining RR-06 drift if not fully closed by the lock/hash lane.
9. `ALPHA-SOLVER-DEF-002-OPERATOR-RISK-ACCEPTANCE-001`
   - Only after must-fix closure evidence exists or operator deferrals are
     explicitly recorded, review RR-04, RR-A1, JWT keystore management, and
     evidence payload hygiene for acceptance.
10. `ALPHA-SOLVER-DEF-002-CLOSEOUT-001`
    - Only after closure evidence and accepted residuals exist. This plan does
      not authorize closeout.

## Sequence safeguards

- Do not combine public exposure, provider validation, or readiness claims with
  these remediation lanes.
- Do not run these DEF-002 remediation lanes in parallel with the repo-global
  selected next lane unless the operator explicitly chooses the DEF-002 track.
- Do not use real credentials in tests; use synthetic placeholders.
- Do not print environment variables or secret values.
- Do not mount or expose dashboard or `/v1/solve` outside isolated tests.
