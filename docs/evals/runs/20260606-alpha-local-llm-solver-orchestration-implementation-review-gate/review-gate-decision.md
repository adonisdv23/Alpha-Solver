# Review Gate Decision

## Decision

`AUTHORIZE_MANUAL_LOCAL_ORCHESTRATION_SMOKE`

## Rationale

The reviewed implementation satisfies the docs-only review requirements for authorizing a separate manual local orchestration smoke packet:

- non-production runner boundary is explicit;
- runner uses only the approved local runtime path;
- local LLM remains default-off and explicit opt-in;
- localhost or loopback endpoint restriction remains in force;
- provider keys are not required for local mode and are rejected if present;
- no hosted fallback is added;
- `behavior_evidence=false` is preserved;
- Pass 1 requests structured gate inputs and uses deterministic parse behavior;
- unsafe Pass 1 output fails closed or avoids unsupported successful answering;
- unsafe confidence cannot select answer modes;
- `answer_with_assumptions` requires safely parsed confidence and bounded assumptions;
- Pass 2 only runs after allowed answer modes;
- Pass 2 fails closed on required unsafe conditions;
- normalized Alpha-style fields are present;
- `/v1/solve` and dashboard preview are not exposed;
- no smoke execution, local model call, or result import occurred in this lane.

## Exactly one decision check

This file records one review-gate decision and does not select a fix lane.
