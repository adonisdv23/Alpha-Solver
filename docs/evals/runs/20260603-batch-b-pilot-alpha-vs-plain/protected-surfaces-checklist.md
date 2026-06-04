# Protected Surfaces Checklist

Status: implementation-surface planning aid only
Lane: `ALPHA-IMPLEMENTATION-SURFACE-MAP-001`

Use this checklist before any future Alpha implementation PR. This checklist does not authorize runtime behavior changes, routing changes, provider/model changes, capture, rescoring, Sheet updates, or Batch C.

## Provider files to avoid

Do not touch without explicit authorization:

- `alpha/providers/openai.py`
- `alpha/providers/base.py`
- `alpha/providers/safeout.py`
- `alpha/providers/accounting.py`
- `alpha/providers/telemetry.py`
- `alpha/adapters/openai.py`
- `alpha/adapters/base.py`
- provider execution and provider error helpers in `service/app.py`
- provider-focused tests except as regression checks with fake clients

## Model config files to avoid

Do not touch for Alpha behavior shaping:

- `service/config/model_sets.yaml`
- `service/models/modelset_registry.py`
- `service/models/modelset_resolver.py`
- model-set switcher tests except as regression checks

## Routing files to avoid until authorized

Do not touch until the operator explicitly approves routing or gate implementation:

- `alpha/core/router.py`
- `alpha/router/progressive.py`
- `alpha/router/agents_v12.py`
- `alpha/routing/router_v12.py`
- `alpha_solver_entry.py` gate behavior
- route/mode selection helpers in `service/app.py`

## Eval artifacts to avoid

Treat these as preserved evidence:

- `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/score-table.csv`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blinded-score-sheet.csv`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blinding-map.csv`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/blind-scorer-result.md`
- `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/source-packet.md`
- existing defects, summaries, evidence packets, and capture packets in official run folders

New tests should use new fixtures outside official scored artifact paths.

## Score/rubric files to avoid

Do not change:

- `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- `docs/evals/LIFT_DECISION_RULE.md`
- `docs/evals/BLIND_SCORING_PROCEDURE.md`
- `docs/evals/ARTIFACT_PRESERVATION.md`
- `docs/evals/templates/comparison_score_table_template.csv`

## Secrets/configs to avoid

Do not touch unless the task is explicitly about environment/config expectations:

- `.env.example`
- `scripts/check_env.py`
- `service/auth/*`
- `service/middleware/secret_middleware.py`
- `service/auth/secret_store.py`
- deployment or secret-management files

Do not introduce secret-like strings, live credentials, unredacted provider payloads, or external Sheet updates.

## Checklist before implementation PR

Before any future behavior implementation PR, confirm:

- [ ] The implementation spec is merged and explicitly authorizes runtime work.
- [ ] The scope identifies one primary seam and lists protected surfaces.
- [ ] Official A3-1 and Batch B artifacts remain unchanged.
- [ ] Scoring rubric and eval controls remain unchanged.
- [ ] Provider adapters remain unchanged unless explicitly authorized.
- [ ] Model config remains unchanged unless explicitly authorized.
- [ ] Routing remains unchanged unless explicitly authorized.
- [ ] `/v1/solve` behavior remains unchanged unless explicitly authorized and tested.
- [ ] Tests are offline and deterministic.
- [ ] No live-provider tests are required for the PR.
- [ ] No new capture, rescoring, unblinding, Sheet update, or Batch C work is included.
- [ ] Non-claims are repeated: no MVP validation, no broad superiority, no production readiness, no benchmark success, no exact billing accuracy, and no provider reasoning orchestration.
