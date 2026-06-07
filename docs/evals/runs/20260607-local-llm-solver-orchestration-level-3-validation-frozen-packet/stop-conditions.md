# Stop Conditions

Work must stop and use the blocker fallback lane if any of the following occur:

- local model execution before a separate execution lane is merged;
- hosted provider call;
- provider fallback;
- hosted fallback;
- non-loopback endpoint;
- hosted provider key use or exposure;
- `/v1/solve` exposure or call;
- dashboard exposure or call;
- billing work;
- benchmark run or benchmark claim;
- evidence-model promotion;
- production readiness claim;
- MVP readiness claim;
- local model quality claim;
- Alpha superiority claim;
- provider-orchestration evidence claim;
- missing provenance;
- malformed or unparseable artifact expectation without explicit classification;
- modification of preserved source artifacts;
- reopening Level 2 controlled usage;
- Google Sheets or backlog workbook action.

## Blocker fallback lane

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-LEVEL-3-VALIDATION-FROZEN-PACKET-FIX-001`
