# Do Not Consolidate Yet

Do not consolidate these zones until value proof, security proof, and operator authorization exist:

1. `alpha_solver_portable.py` portable standalone contract.
2. `/v1/solve` runtime behavior and provider/local branching.
3. Provider client/request/accounting/SAFE-OUT machinery.
4. Dashboard auth/session/CSRF and expert preview guard.
5. Dashboard settings secret storage and audit file paths.
6. Auth/JWT/API-key middleware and tenant middleware.
7. Evidence API/store/collector semantics.
8. Budget guard, determinism, observability, replay, routing, SAFE-OUT, and SolverEnvelope behavior.
9. Legacy/reference entrypoints `alpha-solver-v91-python.py` and `alpha_solver_entry.py`.
10. CI/tests that encode current behavior.

Reason: these surfaces are security-sensitive, contract-sensitive, or evidence-sensitive, and the repository state explicitly does not yet support broad runtime/provider/public-readiness claims.
