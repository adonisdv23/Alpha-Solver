# Operator Authorization Template

Use the following exact language only in a future separately authorized pass. Do not treat this template as authorization by itself.

```text
I authorize ALPHA-SOLVER-VALUE-READ-UNBLINDING-FINAL-INTERPRETATION-PASS-001 to perform a bounded Value Read source-identity review and final interpretation pass using the locked blind score output at docs/evals/runs/alpha-solver-value-read-blind-scoring-pass-post-581-001/score-output.md.

The pass must preserve the committed locked scores exactly, must not change scoring fields, and must record any source-identity mapping as operator-provided or operator-reviewed material according to the approved custody rules for that future pass.

The pass may reveal source identities only inside the future pass artifacts and only after confirming the locked score-output checksum or equivalent source-of-truth identity of the score file.

The pass may create a bounded final interpretation only after the source-identity review is complete and only with explicit non-claims for value, readiness, benchmark proof, provider/local-model behavior, production/public status, security/privacy completion, partnership/Pi.dev integration, and Alpha superiority.

The pass must stop rather than infer identities, change scores, inspect raw outputs unnecessarily, call providers, run local models, expose runtime endpoints, expose dashboard/public API behavior, expose /v1/solve, mutate Google Sheets, add dependencies, or start a release lane.
```

## Authorization checklist for the future pass

Before a future operator uses the template, they must confirm:

- The current selected next state still permits a future unblinding/source-identity review and final interpretation authorization.
- The locked score-output file exists at `docs/evals/runs/alpha-solver-value-read-blind-scoring-pass-post-581-001/score-output.md`.
- The future pass has an explicit lane id distinct from this authorization packet.
- The identity map or source-identity information is supplied under an approved custody process outside this packet.
- The future pass will not call providers, run local models, expose endpoints, mutate Google Sheets, add dependencies, or implement a release lane.
