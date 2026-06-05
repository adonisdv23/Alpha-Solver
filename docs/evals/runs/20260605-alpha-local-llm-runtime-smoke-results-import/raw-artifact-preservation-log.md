# Raw Artifact Preservation Log

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-RESULTS-IMPORT-001`

## Preservation source

- Source artifact path: `docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-execution/source-evidence/ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-001.md`
- Preserved copy: `source-evidence/sanitized-runtime-smoke-execution-artifact.md`
- Preservation method: copied from the repo-source artifact without adding terminal wrapper noise.

## Preserved artifact notes

- Raw stdout and stderr were captured before the source Markdown artifact was written.
- Endpoint is recorded only as localhost / loopback.
- Provider keys were unset before execution.
- No hosted provider endpoint or provider key is used by this smoke command.
- If precheck failed, smoke was not executed and the artifact records the stop condition.

## Preserved stdout and stderr sections

- Precheck stdout: preserved.
- Precheck stderr: preserved as an empty fenced text block.
- Runtime smoke stdout: preserved as JSON.
- Runtime smoke stderr: preserved as an empty fenced text block.

## Preservation boundary

No missing field was reconstructed. No uploaded file, terminal transcript outside the repo-source artifact, prior prompt, PR summary, retry execution, smoke re-execution, hosted provider call, local model call by Codex, or private URL was used for this import.
