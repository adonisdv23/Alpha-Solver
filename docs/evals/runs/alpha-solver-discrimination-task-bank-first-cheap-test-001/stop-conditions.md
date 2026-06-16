# Stop conditions

Stop and return to operator review if any of the following occurs:

- Source-of-truth mismatch across `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, and `docs/EVIDENCE_INDEX.md`.
- Missing derivation-check packet at `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/`.
- Missing discrimination task-bank asset at `docs/evals/runs/alpha-solver-discrimination-task-bank-asset-001/`.
- Copying-label inconsistency, including failure to use `unsupported_copying` as the canonical copying failure label.
- Raw Alpha output inspection or raw baseline output inspection.
- Score change or scoring attempt.
- Provider, local-model, runtime, API, dashboard, `/v1/solve`, Google Sheets, or external-service dependency.
- Unblinding or source-map request.
- Broad value, readiness, benchmark, provider, local-model, runtime, production, public, security/privacy, partnership, Pi.dev integration, external-use approval, buyer-validation, traction, or Alpha-superiority claim.
- Any attempt to execute the task bank in this lane.
