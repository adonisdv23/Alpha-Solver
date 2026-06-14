# Selected Next Lane

Selected next lane: `ALPHA-SOLVER-LOCAL-COUNCIL-MODEL-JURY-001`

## Rationale

The council/model-jury lane is selected only as a likely next documentation-and-harness lane after this routing matrix because the prior local model catalog and fake-transport multi-model smoke harness exist, and this packet defines candidate roles, evidence fields, and stop conditions.

## Gate before execution

Do not run real local council or model-jury calls until:

1. operator authorizes local model runs;
2. local smoke passes for the exact candidate models;
3. synthetic non-private task bank is frozen;
4. pass/fail/unknown criteria are preregistered;
5. no hosted-provider keys are present;
6. endpoint validation confirms loopback-only use.

If these gates are not met, use verdict `LOCAL_ROUTING_MATRIX_BLOCKED_MODEL_SMOKE_MISSING` or `STOP_INCONCLUSIVE` rather than executing.
