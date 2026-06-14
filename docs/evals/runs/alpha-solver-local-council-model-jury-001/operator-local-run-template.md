# Operator Local Run Template

Use this template only in a future authorized execution lane. Do not use it to call hosted providers or expose `/v1/solve`.

## Preflight

- [ ] Confirm execution mode is `fake_model` or `local_model` only.
- [ ] Confirm no provider API keys or tokens are loaded into prompts.
- [ ] Confirm no private data is included.
- [ ] Confirm no dashboard, API route, or `/v1/solve` surface is invoked.
- [ ] Confirm local model names are operator supplied.
- [ ] Confirm capture directory is under `docs/evals/runs/`.

## Run metadata

```yaml
run_id:
date_utc:
operator:
execution_mode: fake_model | local_model
local_endpoint: loopback only | none for fake
model_catalog_source:
models:
  router:
  solver:
  critic:
  safety_boundary_reviewer:
  evidence_auditor:
  finalizer:
forbidden_surfaces_confirmed:
  hosted_providers: not_called
  tokens: not_used
  v1_solve: not_called
  dashboard: not_called
  google_sheets: not_updated
```

## Role capture

Paste sanitized role outputs in this order:

1. Router
2. Solver
3. Critic
4. Safety / Boundary Reviewer
5. Evidence Auditor
6. Finalizer

## Disagreement matrix

| Claim or decision | Agreeing roles | Disagreeing roles | Category | Evidence state | Escalation? | Finalizer permission |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  | ambiguity / missing evidence / route mismatch / safety concern / weak prompt design | supported / unsupported / missing | yes / no | synthesize / constrain / stop |

## Verdict

Choose one:

- `LOCAL_COUNCIL_MODEL_JURY_DESIGNED_NOT_EXECUTED`
- `LOCAL_COUNCIL_FAKE_MODEL_HARNESS_CAPTURED`
- `LOCAL_COUNCIL_BLOCKED_LOCAL_MODEL_EVIDENCE_MISSING`
- `STOP_INCONCLUSIVE`

## Required non-claims

The run record must state that it does not prove council quality, model superiority, benchmark value, Alpha superiority, production readiness, broad local model readiness, provider orchestration, or `/v1/solve` readiness.
