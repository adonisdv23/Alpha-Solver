# Runtime Configuration Contract

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001`

## Configuration goals

The future implementation must add the smallest configuration surface needed to run an explicitly selected local LLM backend without disturbing existing hosted paths.

## Required local LLM configuration fields

A future implementation must define configuration for:

- provider mode, explicitly selecting `local_llm` or hosted mode;
- local endpoint URL, constrained by `local-endpoint-contract.md`;
- model identifier for the local service;
- finite timeout in seconds;
- enablement flag or equivalent explicit opt-in.

## Default-off requirement

Default configuration must not use local LLM mode. A missing, empty, malformed, or partial local LLM configuration must fail closed or leave local LLM disabled.

## No provider keys

Local LLM configuration must not require hosted provider API keys, hosted-provider credentials, billing credentials, or local-provider credentials.

## Blocked surfaces for this implementation phase

A future implementation under the selected next lane must keep local LLM mode blocked from:

- `/v1/solve` exposure;
- dashboard preview exposure.

Those surfaces require separate explicit authorization in a later lane.

## Evidence model preservation

Configuration must not cause local LLM output to become behavior evidence. `behavior_evidence=false` must remain preserved unless a later lane explicitly changes the evidence model.
