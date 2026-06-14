# Model Assignment Policy

## Policy summary

The lane starts with fake-model roles before any local model execution. Future local execution may assign local model families from the operator catalog, but the harness must stay local-only, default-off, and without hosted fallback.

## Assignment phases

### Phase 0: fake-model templates

Use deterministic fixtures or hand-authored role stubs to exercise the capture schema. This phase is suitable for checking disagreement formatting, stop-state handling, and finalizer boundaries without model inference.

### Phase 1: single local family, multiple roles

If a later execution lane is authorized, one local model family may be reused across roles to test orchestration plumbing. This may expose prompt-role fragility but must not be treated as model-family diversity evidence.

### Phase 2: local family diversity

If multiple local model families are available in the operator catalog, assign roles across families to surface route mismatch and role sensitivity. Example family categories for catalog mapping:

- small instruction-tuned model family for router and boundary checks;
- code/reasoning-oriented family for solver on technical prompts;
- general instruction family for critic;
- safety- or policy-prompted local role for boundary review;
- compact deterministic fake/auditor role for evidence checking.

These are assignment categories, not quality rankings.

## Assignment constraints

- No hosted provider may be called.
- No provider token, API key, dashboard credential, or private user data may be sent to a model.
- Local model names must be operator-supplied or read from a local catalog; the harness must not download or install models automatically.
- Missing local model evidence must produce `LOCAL_COUNCIL_BLOCKED_LOCAL_MODEL_EVIDENCE_MISSING` or `STOP_INCONCLUSIVE` rather than a quality claim.
- Role diversity may be described only as a test-design choice, not as proof of better answers.

## Assignment record template

```yaml
run_id: LOCAL-COUNCIL-YYYYMMDD-NN
execution_mode: fake_model | local_model
models:
  router: fake-router-v0
  solver: fake-solver-v0
  critic: fake-critic-v0
  safety_boundary_reviewer: fake-safety-v0
  evidence_auditor: fake-auditor-v0
  finalizer: fake-finalizer-v0
assignment_rationale:
  - local-only
  - no hosted fallback
  - role-diverse prompts
catalog_source: operator supplied | local config path | fake fixture
missing_models: []
```
