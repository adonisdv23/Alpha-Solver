# Failure Classification

Lane ID: `ALPHA-LOCAL-LLM-POST-SMOKE-DECISION-FRAMEWORK-001`

Status: classification framework only; no failure is claimed here.

## Classification rules for future imported evidence

The future smoke-results decision lane must classify failures without expanding the evidence boundary.

### Endpoint locality failure

Use when imported evidence shows a non-local endpoint, private hosted endpoint, hosted provider endpoint, or failed endpoint-locality validation. The required next lane is `ALPHA-LOCAL-LLM-ENDPOINT-LOCALITY-REPAIR-001`.

### Environment setup failure

Use when imported evidence shows local smoke prerequisites were missing or inconsistent before endpoint/model behavior could be meaningfully evaluated. The required next lane is `ALPHA-LOCAL-LLM-SMOKE-ENVIRONMENT-RETRY-001`.

### Model unavailable

Use when imported evidence shows the local endpoint was contacted but the exact operator-supplied model was absent, unavailable, unloaded, or rejected as unknown. The required next lane is `ALPHA-LOCAL-LLM-MODEL-AVAILABILITY-RETRY-001`.

### Timeout

Use when imported evidence shows a finite timeout expired before valid adapter output or an expected fail-closed label was reached. The required next lane is `ALPHA-LOCAL-LLM-SMOKE-TIMEOUT-REVIEW-001`.

### Connection failure

Use when imported evidence shows the local loopback endpoint could not be reached because of refusal, reset, DNS misuse, socket failure, service absence, or similar connection setup failure. The required next lane is `ALPHA-LOCAL-LLM-SMOKE-CONNECTION-REVIEW-001`.

### Malformed response

Use when imported evidence shows the response body, status, JSON structure, role/content fields, or parser input shape was invalid for the adapter/parser contract. The required next lane is `ALPHA-LOCAL-LLM-RESPONSE-PARSER-REPAIR-001`.

### Empty output

Use when imported evidence shows the returned or parsed assistant content was empty or whitespace-only. The required next lane is `ALPHA-LOCAL-LLM-EMPTY-OUTPUT-REVIEW-001`.

### Prompt or system echo

Use when imported evidence shows the output materially echoed the user prompt, system prompt, or portable contract text rather than producing a distinct assistant response. The required next lane is `ALPHA-LOCAL-LLM-PROMPT-ECHO-REPAIR-001`.

### Skipped or blocked

Use when imported evidence shows smoke did not run, was skipped, lacked authorization, lacked raw artifacts, lacked a sanitized import, or cannot support classification. The required next lane is `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-RETRY-001`.
