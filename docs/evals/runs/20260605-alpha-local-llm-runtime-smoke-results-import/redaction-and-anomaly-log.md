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

- Required raw fields for the decision rule are present.
- Precheck exit code is present and is `0`.
- Runtime smoke execution is present with `smoke_ran: yes` and `smoke_exit_code: 0`.
- Result fields are present: `status: non_evidence`, `reason: local_llm_provider_adapter_wiring_only`, `output_text: OK`, and `behavior_evidence: false`.
- Local runtime provenance fields are present, including `no_hosted_fallback: true` and `no_provider_keys_required: true`.
- No artifact-integrity blocker remains for bounded interpretation and final decision.
