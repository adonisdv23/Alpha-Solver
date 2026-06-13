# Risk-to-lane matrix

| Finding | Lane assignment | Lane type | Priority | Rationale |
| --- | --- | --- | --- | --- |
| RR-02 | `ALPHA-SOLVER-DEF-002-CREDENTIAL-STORAGE-HARDENING-001` | Implementation | P0 | High-severity plaintext provider API keys at rest. |
| RR-03 | `ALPHA-SOLVER-DEF-002-DEFAULT-CREDENTIALS-HARDENING-001` | Implementation | P0 | High-severity known API/dashboard defaults. |
| RR-01 | `ALPHA-SOLVER-DEF-002-CORS-DEFAULT-HARDENING-001` | Implementation | P1 | Browser/API exposure default must be safe before public use. |
| RR-09 | `ALPHA-SOLVER-DEF-002-SOLVE-AUTH-TENANCY-DECISION-001` | Decision + possible implementation | P1 | `/v1/solve` auth/tenancy model must be confirmed or wired before exposure. |
| RR-05 | `ALPHA-SOLVER-DEF-002-DATA-CLASSIFICATION-RECONCILIATION-001` | Implementation/docs | P2 | Conflicting classification registries weaken policy evidence. |
| RR-07 | `ALPHA-SOLVER-DEF-002-DEPENDENCY-LOCK-HASHING-001` | Supply-chain implementation | P2 | Lock/hash posture is required for reproducible reviewed installs. |
| RR-08 | `ALPHA-SOLVER-DEF-002-VENDORED-DEPENDENCY-PROVENANCE-001` | Supply-chain inventory/hardening | P2 | Vendored/shimmed libraries need provenance and patch tracking. |
| RR-06 | `ALPHA-SOLVER-DEF-002-DEPENDENCY-SOURCE-OF-TRUTH-001` | Supply-chain cleanup | P3 | Dependency drift is lower severity but should be closed with RR-07. |
| RR-04 | `ALPHA-SOLVER-DEF-002-OPERATOR-RISK-ACCEPTANCE-001` | Operator acceptance | After must-fix lanes | Inherent provider data sharing can be accepted only after disclosure is committed. |
| RR-A1 | `ALPHA-SOLVER-DEF-002-OPERATOR-RISK-ACCEPTANCE-001` | Operator acceptance | After must-fix lanes | Pattern redaction limits require operator acknowledgement or a separate hardening lane. |
| JWT keystore management | `ALPHA-SOLVER-DEF-002-OPERATOR-RISK-ACCEPTANCE-001` | Operator acceptance | After must-fix lanes | Deployment custody/rotation responsibility, not repo secrets. |
| Evidence payload hygiene | `ALPHA-SOLVER-DEF-002-OPERATOR-RISK-ACCEPTANCE-001` | Operator acceptance | After must-fix lanes | Caller policy or later guardrails required; not a runtime fix in this plan. |

## Must-fix set

- RR-02, RR-03, RR-01, RR-09, RR-05, RR-07, RR-08, RR-06.

## Accepted residual candidate set

- RR-04, RR-A1, JWT keystore management, evidence payload hygiene.

## Not-now set

- Provider smoke/eval lanes, public exposure lanes, production/runtime readiness
  lanes, dashboard expansion lanes, benchmark/value experiment lanes, broad auth
  redesign outside the RR-09 decision boundary.
