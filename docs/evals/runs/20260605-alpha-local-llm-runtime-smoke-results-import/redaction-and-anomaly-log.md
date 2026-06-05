# Redaction and Anomaly Log

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-RESULTS-IMPORT-001`

## Redaction checks

- Provider keys: confirmed absent from imported stdout/stderr; the source records provider keys were unset before execution.
- Secrets: confirmed absent.
- Credentials: confirmed absent.
- Private URLs: confirmed absent.
- Hosted provider endpoints: confirmed absent.
- Endpoint exposure: limited to localhost / loopback pattern `http://127.0.0.1:11434/api/chat`.
- Model name: preserved only because the repo-source artifact records `gemma3:4b` and the lane requires exact preservation.

## Terminal wrapper noise check

Terminal wrapper output from `git pull`, branch listings, shell prompts, and command echo material outside the artifact preview is not imported as smoke evidence. The copied source-evidence artifact includes the source cleanup note that excludes wrapper noise.

## Worktree caveat

The source artifact preserves this Git status caveat:

```text
?? ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md
```

The caveat is interpreted narrowly as an unrelated untracked prior smoke artifact at repo root unless repo evidence proves otherwise. No repo evidence in the imported source artifact proves that the caveat invalidates the runtime smoke result.

## Artifact integrity review

- Precheck exit code is present and is `0`.
- Runtime smoke execution fields are present with `smoke_ran: yes` and `smoke_exit_code: 0`.
- Result fields are present: `status: non_evidence`, `reason: local_llm_provider_adapter_wiring_only`, `output_text: OK`, and `behavior_evidence: false`.
- Local runtime provenance fields are present, including `no_hosted_fallback: true` and `no_provider_keys_required: true`.
- Artifact-integrity blocker recorded: the preserved command summary is not exact executable provenance for the imported JSON stdout.

## Command-provenance defect

The recorded command block is preserved exactly as source evidence, but it is incomplete or non-reproducible as executable provenance for the imported JSON stdout:

- preserved command does not call `run_configured_local_llm_runtime`;
- preserved command does not pass a user prompt;
- preserved command does not serialize the result;
- preserved command cannot itself produce the imported JSON stdout.

Because this required raw provenance field is incomplete, the imported smoke result cannot support local LLM runtime track closeout. The final decision must select `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-RETRY-001`.
