# Observability and Provenance Contract

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001`

## Required distinction

A future implementation must make local LLM output distinguishable from hosted provider output in logs, returned metadata, smoke artifacts, or equivalent provenance records.

## Required local LLM metadata

Local LLM records must include, at minimum:

- provider mode identifying `local_llm`;
- local backend class or equivalent adapter identifier;
- configured local model identifier;
- sanitized local endpoint category or localhost/loopback confirmation;
- timeout value used;
- status and reason label;
- `behavior_evidence=false`.

## Hosted output separation

Hosted output must not be labeled as local LLM output. Local LLM failure must not be converted into hosted success unless a later lane separately authorizes and labels explicit fallback.

## Raw and sanitized smoke artifacts

Before any future runtime-readiness claim, a runtime smoke lane must preserve artifacts sufficient to confirm:

- explicit local provider selection;
- localhost/loopback endpoint use;
- finite timeout;
- absence of hosted-provider fallback;
- status, reason, and `behavior_evidence=false` preservation;
- raw local response shape, with secrets absent or redacted.
