# Likely docs, specs, scripts, artifacts, and CI files

## May inspect

### Specs and repo operating contracts

- `AGENTS.md` — repo operating instructions and sensitive file rules.
- `.specs/INDEX.md` — spec index to keep synchronized when future specs are added.
- `.specs/LOCAL-LLM-SOLVER-ORCHESTRATION-001.md` — local solver orchestration contract.
- `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md` — local runtime integration contract.
- `.specs/PROVIDER-*.md`, `.specs/MCP-*.md`, `.specs/FINOPS-BUDGET-001.md`, and `.specs/PROVIDER-BUDGET-001.md` — adjacent provider, MCP, and budget contracts for boundary checks.

### Operator and entrypoint docs

- `docs/ENTRYPOINTS.md` — entrypoint roles and caution rules.
- `docs/local_llm_solver_orchestration_operator_guide/*.md` — operator guide, command reference, evidence boundary, safe-use, local environment, examples, and selected-next state.
- `docs/OPERATING_GUIDE.md` — operator workflow background, subordinate to `AGENTS.md`.
- `docs/API_REFERENCE.md`, `docs/api.md`, `docs/CLI.md`, `docs/RUN_GUIDE.md`, `docs/RUNTIME_READINESS.md`, and `docs/MVP_READINESS_CHECKPOINT.md` — user-facing operational docs that may need future alignment.
- `docs/BUDGETING.md`, `docs/FINOPS.md`, `docs/DETERMINISM.md`, `docs/REPLAY_GUIDE.md`, `docs/OBSERVABILITY.md`, `docs/TELEMETRY_SCHEMA.md`, `docs/POLICY.md`, and `docs/SECRETS_REDACTION.md` — adjacent safety and operations docs.

### Evidence packets and artifact folders

- `docs/evals/runs/local-llm-solver-orchestration-index/*` — local orchestration evidence index and decision ledger.
- `docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/*` — Level 3 validation packet and closeout state.
- `docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/*` — controlled usage operator run packet and closeout state.
- `docs/evals/runs/20260604-*local-llm*`, `docs/evals/runs/20260605-*local-llm*`, and `docs/evals/runs/20260606-*local-llm*` — earlier local LLM evidence packets.
- `artifacts/`, `telemetry/`, `logs/`, and any packet-local source artifact folders — output/artifact locations to understand, not to rewrite in this packet.

### Guardrail scripts and CI

- `Makefile` — local guardrail target definitions.
- `scripts/check_local_llm_evidence_boundaries.py` — static evidence-boundary guardrail.
- `scripts/check_local_llm_doc_paths.py` — static doc path/link guardrail.
- `scripts/check_local_llm_packet_consistency.py` — packet consistency guardrail.
- `scripts/check_env.py`, `scripts/preflight.py`, `scripts/replay.py`, `scripts/env_snapshot.py`, and `scripts/bundle_artifacts.py` — adjacent operator/runtime utility scripts.
- `.github/workflows/ci.yml`, `.github/workflows/tests.yml`, `.github/workflows/gates.yml`, `.github/workflows/nightly.yml`, and `.github/pull_request_template.md` — CI and PR validation surfaces.

## May modify later only with a separate approved implementation scope

- A future lane may add a Self Operator spec under `.specs/` and synchronize `.specs/INDEX.md` if behavior work is authorized.
- A future lane may update operator guide docs only if it preserves evidence boundaries and selected-next consistency.
- A future lane may update guardrail scripts or CI only if the spec explicitly requires new static checks and includes focused tests for the script changes.
- A future lane must not rewrite historical evidence packets, source artifacts, exported registries, backlog workbooks, or generated runtime artifacts unless explicitly authorized.
