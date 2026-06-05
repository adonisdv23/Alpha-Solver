# Decision Options

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-FINAL-DECISION-001`

## Option review

| Option | Selection status | Reason |
| --- | --- | --- |
| `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-RETRY-001` | selected | A required raw provenance field is incomplete or non-reproducible: the preserved command summary is not exact executable provenance for the imported JSON stdout. |
| `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-FAILURE-INTERPRETATION-001` | not selected | The issue is command provenance, not a preserved failed-closed smoke outcome. |
| `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-RESULTS-IMPORT-REPAIR-001` | not selected | The source artifact is imported and the defect is preserved; the needed next step is retry execution with complete provenance. |
| `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-REPAIR-001` | not selected | The preserved import does not establish an implementation defect; it establishes a command-provenance defect in the artifact. |
| `STOP-HERE-LOCAL-LLM-RUNTIME-TRACK-CLOSED` | not selected | Closeout is blocked because the preserved command summary does not call `run_configured_local_llm_runtime`, pass a prompt, serialize a result, or itself produce the imported JSON stdout. |

## Exactly one selected lane

Only one next lane is selected: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-RETRY-001`.
