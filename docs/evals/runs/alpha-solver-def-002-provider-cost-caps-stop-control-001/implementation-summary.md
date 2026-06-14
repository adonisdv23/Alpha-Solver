# Implementation Summary

- `/v1/solve` OpenAI-provider execution now requires explicit operator caps before a provider client can execute.
- Required caps are `ALPHA_PROVIDER_MAX_COST_USD`, `ALPHA_PROVIDER_MAX_INPUT_TOKENS`, `ALPHA_PROVIDER_MAX_OUTPUT_TOKENS`, and `ALPHA_PROVIDER_MAX_REQUESTS`.
- `ALPHA_PROVIDER_EMERGENCY_STOP=1` blocks provider execution before the fake or real provider client is invoked.
- Postflight checks block missing/unknown cost estimates and input/output/cost values that exceed the configured caps.
