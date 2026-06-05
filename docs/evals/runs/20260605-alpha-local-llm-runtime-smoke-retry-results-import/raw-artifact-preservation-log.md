# Raw Artifact Preservation Log

## Source artifact

`docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-execution-retry/source-evidence/ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-RETRY-002.md`

## Preserved raw sections

- Execution metadata, including `attempt_id: 002` and retry reason.
- Precheck command, stdout, stderr, and `exit_code: 0`.
- Runtime smoke execution fields, including `smoke_ran: yes` and `smoke_exit_code: 0`.
- Exact executable shell command.
- Exact Python script executed.
- Runtime smoke stdout JSON.
- Runtime smoke stderr.
- Artifact preservation notes.
- Evidence boundary and non-claims.
- Repo status caveats before and after retry artifacts.

## Exact preserved command

```bash
PYTHONPATH="<repo-root>" python3 "docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-execution-retry/manual-artifacts-attempt-002/runtime_smoke_retry_executable.py"
```

## Preservation decision

The source artifact was imported from the repo only. Terminal wrapper material outside the source artifact was not imported as smoke evidence.
