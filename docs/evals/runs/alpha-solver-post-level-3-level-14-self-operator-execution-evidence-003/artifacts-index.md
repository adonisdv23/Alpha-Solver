# Artifacts index

Generated artifacts under this packet:

| Artifact | SHA-256 | Purpose |
| --- | --- | --- |
| `artifacts/execution-gate-result.json` | `a2d8d06f9ad67962cd017af4385b64dc4c34a685d2370a596138dd00c72687fa` | Local execution gate result. |
| `artifacts/dry-run-result.json` | `ba4456623e7458be2e94b82a8c63d39cf933ca0026806c5e6128accee173d068` | Local dry-run wrapper result. |
| `artifacts/stop-state.json` | `89fa6f8fe388a4912f74c9c58174c99fe12a1b80d1819e2ceb20518859f86e59` | Fail-closed stop-state record. |
| `artifacts/result-import-summary.json` | `e62d043b1ef7af8ac81882d33a13bd02893cf6a5d60ecf385cdad8412ce8d9e2` | Deterministic local result import summary. |
| `artifacts/acceptance-interpretation.json` | `f007f0416e0b156d0921ccc5229fe6c37408104a7f0374ffea4dee285bf70160` | Deterministic local acceptance interpretation output. |
| `candidate-task.json` | `023489af725f1596d342c26071b2eef79aee4cae06bee1797c41a3070233c2da` | Representative candidate task fixture. |
| `operator-approval-artifact.json` | `1494204811c6748f32f19e6b1cefe4a43ecc2efe71446072f169f7dd5b2da82c` | Real operator approval artifact preserved from the prompt. |

The generated artifacts are local JSON/Markdown evidence only. They do not contain provider, token, hosted model, local model, credential, browser, deployment, dashboard, `/v1/solve`, Google Sheets, runtime/provider, or prior-evidence mutation outputs.

## Path portability correction

`artifacts/result-import-summary.json` was normalized to repo-relative path strings instead of machine-specific `/workspace/Alpha-Solver/...` paths. The `relative_path` fields remain the portable artifact identifiers.

## Selected-next-lane disambiguation

`artifacts/dry-run-result.json` preserves the dry-run wrapper metadata value `selected_next_lane=ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-MANUAL-LOCAL-ACCEPTANCE-PACKET-001`, which is the wrapper's internal handoff/fallback lane from the reusable dry-run harness. The controlling packet-level next lane for this PR remains `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-EXECUTION-EVIDENCE-004` as recorded in `selected-next-lane.md`.
