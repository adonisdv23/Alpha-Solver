# Recommended Next Lane

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-SCAFFOLD-001`

## Selected next lane

`ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-001`

This is the only recommended next lane selected by this scaffold.

## Required blocker before next lane

`ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-001` must not run until `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md` exists.

If `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md` is missing, import must stop.

## Continued boundary

The next lane may import only sanitized results supported by the required future evidence file. It must not run smoke or infer a smoke outcome from missing evidence.
