# Batch C and Runtime Firewall

Lane ID: `ALPHA-OPERATOR-TEST-BATCH-C-RUNTIME-FIREWALL-001`

Status: firewall established; no Batch C, runtime, provider, billing, or `/v1/solve` work authorized by this memo.

## Firewall statement

Limited operator-test preparation and any later limited operator-test feedback must remain separated from Batch C, runtime wiring, provider orchestration, `/v1/solve`, MVP validation, billing validation, and production-readiness decisions.

The limited operator-test lane prepares or collects operator usability feedback on the portable Alpha behavior contract. It is not a Batch C execution lane, not a runtime measurement lane, not a provider orchestration lane, not a billing lane, and not a production-readiness lane.

## Required separations

### Packet preparation is not user testing

The limited operator-test packet prepared materials only. Preparing prompts, templates, stop conditions, claim boundaries, result-log templates, defect logs, and preservation checklists does not mean any user has tested Alpha and does not produce validation evidence.

### Operator feedback is not Batch C readiness

Future limited operator feedback may reveal usability signals or defects. That feedback is not a readiness decision for Batch C and cannot be used to skip Batch C planning, prompt approval, artifact-preservation rules, measurement design, or readiness review.

### Results import is not validation

If a future repo task imports operator-test feedback or filled templates, that import only preserves records. Importing records does not validate the MVP, prove superiority, prove runtime behavior, prove provider behavior, prove billing, or authorize broader measurement.

### Interpretation is not production readiness

A future interpretation may summarize operator feedback or defects within the limited operator-test boundary. Interpretation does not prove production readiness, runtime readiness, MVP validation, public-launch readiness, or broad Alpha-vs-plain generalization.

### Batch C requires a separate readiness decision

Batch C remains blocked until a separate Batch C readiness decision explicitly approves its scope, prompt set, measurement plan, preservation method, scoring method, stop conditions, and non-claim boundaries.

### Runtime work requires a separate wiring/readiness review

Runtime wiring, runtime API work, model-routing work, provider-adapter work, and `/v1/solve` measurement remain blocked until a separate runtime wiring/readiness review authorizes exact surfaces, instrumentation, safety checks, expected evidence, and rollback boundaries.

## Runtime and provider non-claims

This firewall does not prove or authorize:

- `/v1/solve` behavior
- runtime API behavior
- provider behavior
- provider orchestration
- provider-adapter readiness
- model routing behavior
- exact billing accuracy
- billing instrumentation sufficiency
- production readiness
- MVP validation
- public launch readiness

`/v1/solve` remains unproven unless separately measured on the actual runtime surface. Provider orchestration remains blocked unless separately authorized, wired, measured, and reviewed. Exact billing remains blocked unless separately instrumented, measured, reconciled, and reviewed.

## Protected surfaces

This memo does not change and must not be used to change protected surfaces, including:

- runtime APIs
- `/v1/solve`
- provider adapters
- model routing
- billing or budget guard logic
- SAFE-OUT behavior
- SolverEnvelope behavior
- observability, replay, or determinism behavior
- scored artifacts or scorer-facing materials
- raw outputs or operator-only maps
