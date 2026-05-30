# Alpha Solver Operator & Technology Manual

## 1. Purpose

This manual is the operator-facing bridge across Alpha Solver setup, repository architecture, runtime truth, tool roles, pull request workflow, backlog workflow, and known gaps. It is written for a solo non-developer operator who uses ChatGPT for planning and review, Codex for repository edits and validation, GitHub for pull request review and merging, and Claude as optional drafting or review support.

This manual does not replace:

- `.specs/`, which contains implementation contracts.
- `docs/OPERATING_GUIDE.md`, which defines the lightweight operating workflow.
- `docs/RUNTIME_READINESS.md`, which records current runtime status and known gaps.
- Repo code, tests, and CI evidence, which remain the source of current behavior.

Use this document as a practical map. When it disagrees with repo evidence, inspect the repo and update the manual instead of relying on memory.

## 2. Current State Snapshot

Alpha Solver is currently local/offline by default. The default `.env.example` sets `MODEL_PROVIDER=local`, and local checks do not require OpenAI, Anthropic, or Google credentials.

Current repo-grounded state:

- Local/offline operation remains the verified default.
- Provider environment validation has been corrected so `scripts/check_env.py` validates provider configuration only.
- `.specs/PROVIDER-OPENAI-001.md` defines the OpenAI provider contract.
- The OpenAI provider client foundation exists in `alpha.providers.openai`.
- FastAPI `/v1/solve` can route through the OpenAI provider only when `MODEL_PROVIDER=openai` is explicitly enabled.
- Default CI remains credential-free and makes no live OpenAI calls.
- Prompt adapters remain prompt renderers, not provider clients.
- The portable solver remains local/offline.
- CLI remote provider execution has not been added.
- This manual does not claim production-hardened OpenAI use.

Treat OpenAI provider execution as an explicit opt-in service path. Minimal no-secret lifecycle telemetry now exists for FastAPI `/v1/solve`; follow-up hardening is still needed for budget accounting, SAFE-OUT and fallback orchestration, replay and determinism integration, expanded observability, and optional gated live smoke testing.

## 3. Source-of-Truth Hierarchy

Use this hierarchy when sources disagree:

1. Current user instruction or explicit operator decision.
2. GitHub repo `main` for code, docs, specs, tests, and history.
3. `.specs/` for implementation contracts and behavior intent.
4. `docs/RUNTIME_READINESS.md` for current runtime truth and known gaps.
5. `docs/OPERATING_GUIDE.md` for workflow.
6. External backlog workbook for planning and evidence ledger entries.
7. External model outputs from ChatGPT, Codex, Claude, or any other assistant as advisory only.

Warnings:

- Do not let Claude, Codex, or ChatGPT silently override repo truth.
- Do not treat stale backlog rows as implementation evidence without repo confirmation.
- Do not treat old summaries, copied spec bodies, or prior chat memory as proof that code exists.
- When in doubt, inspect files, tests, PRs, and CI results.

## 4. Technology Stack

The current technology stack visible in the repo includes:

| Layer | Current repo evidence | Operator meaning |
| --- | --- | --- |
| Language | Python 3.12+ | Use Python 3.12 or newer for normal local development and CI alignment. |
| Web service | FastAPI, Starlette, Pydantic | Service endpoints, request validation, and response models. |
| ASGI server | Uvicorn | Local service runner for FastAPI. |
| HTTP client | httpx | Used for HTTP client behavior, including the OpenAI provider path. |
| Metrics | prometheus-client | Prometheus-format metrics support exists, with deployment wiring still separate. |
| Config and validation | PyYAML, jsonschema | Registry/config/document validation support. |
| Testing | pytest | Default Python test framework. |
| CI | GitHub Actions | Pull request validation and merge gate. |
| Provider path | `alpha.providers.openai` | Minimal OpenAI provider client foundation. |
| Model sets | `service/models/`, `service/config/model_sets.yaml` | Model-set registry and resolver for service routing/config. |
| Local reasoning | `alpha/reasoning/`, Tree-of-Thought and ReAct-style paths | Offline reasoning paths remain baseline behavior. |
| Docs/spec workflow | `.specs/`, `docs/`, `AGENTS.md` | Specs define behavior contracts, docs explain operation and status. |

Do not invent extra infrastructure when planning work. If a technology is not in the repo or not proven by CI/runtime evidence, label it as future work or external dependency.

## 5. Repository Architecture Map

| Area | Files / folders | Purpose | Current readiness |
| --- | --- | --- | --- |
| Specs | `.specs/` | Implementation contracts, templates, provider contract, spec index. | Active source for behavior intent. Do not move or rename specs casually. |
| Docs | `docs/` | Operator guides, runtime readiness, entrypoint docs, CLI docs, architecture and operational references. | Active documentation. Some docs intentionally mark placeholders and known gaps. |
| Service | `service/` | FastAPI app, health, metrics, auth, policy, model sets, replay, budget, MCP, adapters. | Mixed readiness. Core local service paths and selected tests exist; some production-style targets are partial or future. |
| Providers | `alpha/providers/` | Provider abstractions, fake provider test support, OpenAI provider client. | OpenAI client foundation exists with fake/mocked testing; live hardening remains follow-up. |
| Prompt adapters | `alpha/adapters/` | Prompt rendering for provider families and instruction formatting. | Local prompt rendering only. Do not treat adapters as provider clients. |
| Core | `alpha/core/` | Routing, budgets, gates, determinism, observability, loaders, policy, replay, prompt writer. | Local/offline core functionality exists; broad behavior changes require specs. |
| Reasoning | `alpha/reasoning/` | Tree-of-Thought, Chain-of-Thought, ReAct-lite, scoring, cache/logging helpers. | Local/offline reasoning baseline. |
| Python client | `clients/python/` | Client SDK packaging and helper code. | Existing client surface. Auth hardening remains a known future area. |
| CLI | `cli/`, `alpha_solver_cli.py`, `alpha.cli` | Local command workflows, run/replay/gates/finops/traces-style commands, root CLI wrapper. | Local/offline. Remote provider CLI execution is not implemented. |
| Scripts | `scripts/` | Environment checks, benchmarks, release helpers, registry validation, replay and audit utilities. | Useful local tooling. `scripts/check_env.py` validates configuration only. |
| Tests | `tests/` | Unit, integration, CLI, service, provider, docs, and validation tests. | CI-backed test suite. Full local pytest may depend on Python version and environment. |
| Registries | `registries/` | Routing, regions, tools, risks, policy, MCP registry, priors, budget and SLA config. | Repo config/provenance data. Validate before changing behavior. |
| Data | `data/` | Registry export/provenance artifacts and datasets. | `alpha_solver_master_table_v0_7_0.*` is not a backlog workbook. Do not modify as backlog. |

## 6. Entrypoints

Alpha Solver intentionally keeps several entrypoint files because they serve different roles. Do not rename, delete, merge, or consolidate them casually.

| Entrypoint | Role | Runtime posture | Operator guidance |
| --- | --- | --- | --- |
| `alpha_solver_portable.py` | Portable standalone behavior contract and monolith. | Local/offline. | Sensitive behavior contract. Avoid editing unless explicitly scoped and spec-backed. |
| `alpha-solver-v91-python.py` | Modular/reference compatibility entrypoint. | Local/modular reference path. | Use for architecture grounding and compatibility, not as disposable legacy code. |
| `alpha_solver_entry.py` | Import bridge that loads the hyphenated reference file and re-exports `AlphaSolver`. | Local compatibility bridge. | Keep because Python imports cannot directly import the hyphenated filename. |
| `alpha_solver_cli.py` | Root CLI wrapper over the compatibility entry path. | Local/offline Tree-of-Thought CLI. | Useful smoke path. Not a remote provider CLI. |
| `cli/alpha_solver_cli.py` | Command-oriented CLI for repo workflows such as run, replay, gates, finops, and traces. | Local/offline command workflows. | Use for local validation and operator commands. |
| `python -m alpha.cli` | Package CLI entrypoint. | Local/offline package CLI. | Useful when validating installed/package-style command access. |
| FastAPI `/v1/solve` | Service/API solve endpoint. | Local by default; OpenAI only with explicit `MODEL_PROVIDER=openai`. | This is the current explicit opt-in OpenAI provider integration surface. |

## 7. Runtime Modes

| Mode | How enabled | What works | What does not work | Use when |
| --- | --- | --- | --- | --- |
| Local/offline default | Use repo defaults and keep `.env.example` style `MODEL_PROVIDER=local`. | Local solver, local CLI, local service behavior, fake/mocked tests, no provider keys. | No live remote LLM execution. | Normal development, docs-only PRs, most tests, safe operator checks. |
| `MODEL_PROVIDER=local` | Set `MODEL_PROVIDER=local`. | Environment check passes without provider keys; local/offline paths remain baseline. | Does not call OpenAI, Anthropic, or Google. | Default local configuration. |
| `MODEL_PROVIDER=none` | Set `MODEL_PROVIDER=none`. | Environment check accepts no-key validation. | Does not represent a live provider. | No-key config validation and local-only scenarios. |
| `MODEL_PROVIDER=openai` | Set `MODEL_PROVIDER=openai` and provide `OPENAI_API_KEY`. | FastAPI `/v1/solve` can opt into the OpenAI provider path. | CLI remote execution is not implemented; live usability is not proven by env validation alone; production hardening remains future work. | Explicit OpenAI service testing with private credentials and scoped expectations. |
| Fake/mocked provider tests | Use tests/fakes/mocked transports. | Provider contracts and service integration can be tested without live credentials. | Does not prove account access, model availability, quota, or live network behavior. | Default CI and safe provider development. |
| Optional future live OpenAI smoke test | Not currently implemented. Future gated mode should require explicit flags and `OPENAI_API_KEY`. | Would prove minimal live connectivity only when deliberately enabled. | Must not run in default CI; not a substitute for production hardening. | Future provider readiness checks after a spec defines scope. |

## 8. OpenAI Provider Status

`.specs/PROVIDER-OPENAI-001.md` defines the OpenAI provider contract. The repo now includes the `alpha.providers.openai` client foundation, and FastAPI `/v1/solve` can use it only when `MODEL_PROVIDER=openai` is explicitly set.

Default CI makes no live OpenAI calls. Real live use requires a private `OPENAI_API_KEY`, compatible OpenAI account access, a supported model, network access, and operator acceptance that this path is not yet production-hardened.

Minimal no-secret provider lifecycle telemetry exists for the explicit FastAPI `/v1/solve` OpenAI path. Follow-up work remains for provider budget and cost accounting, deeper SAFE-OUT and fallback orchestration, replay/determinism integration, expanded metrics/tracing hardening, and optional gated live smoke tests.

| Layer | Status | Notes |
| --- | --- | --- |
| Env validation | implemented | checks key presence only |
| Provider client | implemented | fake/mocked tested |
| `/v1/solve` integration | implemented opt-in | `MODEL_PROVIDER=openai` |
| CLI remote execution | not implemented | local/offline only |
| Portable solver remote execution | not implemented / intentionally avoided | local behavior contract |
| Live OpenAI CI test | not implemented | must be gated |

## 9. Setup and Install Workflow

Recommended local setup:

1. Clone the repository.
2. Use Python 3.12 or newer.
3. Create and activate a virtual environment.
4. Install dependencies through the current supported path.
5. Copy `.env.example` to `.env`.
6. Keep `MODEL_PROVIDER=local` unless intentionally testing OpenAI.
7. Run the environment checker.

Example:

```bash
git clone https://github.com/adonisdv23/Alpha-Solver.git
cd Alpha-Solver
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
set -a && source .env && set +a
python scripts/check_env.py
```

Notes:

- `pyproject.toml` lists runtime dependencies for package metadata.
- `requirements.txt` remains supported by the README setup path.
- Do not commit `.env`.
- Do not paste real secrets into prompts, screenshots, logs, PR bodies, or docs.

## 10. Environment Variables and Secrets

Common environment variables currently visible in repo setup and docs:

| Variable | Purpose | Secret? | Notes |
| --- | --- | --- | --- |
| `MODEL_PROVIDER` | Selects provider mode for environment validation and service provider opt-in. | No | Accepted by env checker: `local`, `none`, `openai`, `anthropic`, `gemini`, `google`. |
| `OPENAI_API_KEY` | Required for OpenAI provider key presence validation and real OpenAI service use. | Yes | Needed only when intentionally using `MODEL_PROVIDER=openai`. |
| `ANTHROPIC_API_KEY` | Required for Anthropic key presence validation. | Yes | Env validation only; no live Anthropic provider execution is implemented. |
| `GOOGLE_API_KEY` | Required for Gemini/Google key presence validation. | Yes | Env validation only; no live Google/Gemini provider execution is implemented. |
| `API_KEY` | Service/auth style key referenced in service/auth docs and configuration surfaces. | Yes | Treat as a secret when used in any local or deployed environment. |
| `DEBUG` | Debug mode flag. | No | `.env.example` sets `DEBUG=false`. |
| `PROD` | Production mode flag. | No | `.env.example` sets `PROD=false`. `scripts/check_env.py` rejects `PROD=true` with `DEBUG=true`. |

Secret rules:

- No real secrets in repo files.
- No real secrets in prompts to ChatGPT, Codex, Claude, or other assistants.
- No real secrets in logs, screenshots, test output, PR bodies, docs, trace files, snapshots, or telemetry examples.
- Missing-key errors may name the variable, but must never include the value.
- `scripts/check_env.py` checks configuration only. It does not prove live provider usability, valid billing, quota, model access, or network connectivity.

## 11. How to Run and Validate Locally

Common local validation commands:

```bash
python scripts/check_env.py
python alpha_solver_cli.py --help
python cli/alpha_solver_cli.py --help
python -m alpha.cli --help
python alpha_solver_portable.py "Summarize Alpha Solver restart state" --json --deterministic
python -m pytest tests/api/test_solve.py -q
python -m pytest tests/providers -q
python -m pytest tests/cli/test_alpha_solver_cli.py -q
```

Use focused commands for the PR scope first. For docs-only changes, `git diff --check` plus existence or heading checks is usually enough unless the docs add or change runnable commands.

Full `python -m pytest -q` is useful when practical, but do not overstate it. If a full run fails because of a known unrelated issue, report the exact command, environment, and failure summary instead of hiding it.

## 12. Testing and Validation Workflow

Use this pattern for most PRs:

1. Run the most focused tests or checks for the changed files.
2. Run `git diff --check` before committing.
3. Run full pytest when practical for behavior-changing work.
4. Use GitHub Actions as the merge gate.
5. If a failure appears unrelated, identify it clearly and avoid folding unrelated fixes into the PR unless the operator approves a scope change.
6. Do not add default live provider tests. Live provider tests must be explicitly gated in a future spec.

For docs-only PRs:

- Confirm changed files are docs-only.
- Run `git diff --check`.
- Verify new docs exist and key headings are present.
- Do not run full pytest as ceremony unless the doc changes require it.

## 13. Codex Workflow

Codex is the repository execution tool. Use a new Codex thread for each PR so context and scope stay clean.

Codex should:

- Inspect the repo and relevant specs before implementation.
- Keep one task per thread.
- Create or update a spec before behavior-changing code unless the operator explicitly scopes exploratory or docs-only work.
- Make narrow file changes.
- Run focused validation.
- Commit changes and open a PR.
- Return files changed, validation run, PR URL, suggested squash title, and extended description.

Codex should not:

- Change broad areas without explicit scope.
- Modify source, tests, specs, CI, env files, package metadata, or backlog workbooks in a docs-only PR.
- Treat placeholder docs as implemented behavior.
- Rename or delete sensitive entrypoints casually.
- Paste secrets into output.

Codex task checklist:

- [ ] State the approved scope and files allowed to change.
- [ ] Inspect `AGENTS.md`, relevant specs, and relevant docs.
- [ ] Confirm whether the change is docs-only or behavior-changing.
- [ ] If behavior-changing, link or create the spec first.
- [ ] Implement only the approved scope.
- [ ] Run focused validation and `git diff --check`.
- [ ] Commit on the current branch.
- [ ] Open the PR with title, motivation, files changed, summary, validation, docs-only/source-change confirmation, and suggested squash text.
- [ ] Return PR URL and exact commands run.

## 14. Claude Workflow and Limitations

Claude can be useful for drafting, critique, and architecture review, but do not assume it has repository write access.

Important limitations:

- Claude Project/chat may be read-only or drafting-only unless it has explicit GitHub write tools.
- Switching from Haiku to Opus can improve reasoning quality, but it does not grant GitHub write access.
- Claude output is advisory unless backed by repo inspection, a branch, commits, PRs, and CI evidence.
- Do not rely on Claude to push code unless it proves it can create branches, commit changes, open PRs, and inspect CI.

Good Claude uses:

- Drafting manuals or spec language.
- Reviewing architecture explanations.
- Critiquing prompts before sending to Codex.
- Comparing docs for consistency when given exact file excerpts.

Claude capability-check checklist:

- [ ] Can it inspect current repo files, not just uploaded snippets?
- [ ] Can it create a branch?
- [ ] Can it commit changes?
- [ ] Can it open a GitHub PR?
- [ ] Can it report a PR URL?
- [ ] Can it inspect GitHub Actions results?
- [ ] Can it prove the exact files changed?

If any answer is no, treat Claude as drafting/review support only.

## 15. ChatGPT Review Role

ChatGPT is best used as the operator's planning and review assistant.

Use ChatGPT to:

- Design Codex prompts.
- Clarify PR scope and acceptance criteria.
- Review Codex summaries and changed-file lists.
- Review PR diffs when file excerpts or links are provided.
- Provide merge recommendations based on evidence.
- Track roadmap order and backlog cleanup strategy.
- Draft and refine manuals, operating notes, and workbook update language.

ChatGPT should not claim tests passed unless that is verified by Codex output, terminal output, GitHub Actions, or another concrete tool result. Treat ChatGPT memory as advisory, not as repo truth.

## 16. PR Review and Squash Merge Workflow

Before merging a PR:

1. Verify changed files match scope.
2. Verify GitHub Actions are green or that any failure is understood and accepted by the operator.
3. Inspect diffs for scope creep.
4. Check docs, tests, specs, and source consistency.
5. Confirm no secrets or local files were committed.
6. Use the suggested squash merge title if accurate.
7. Use an extended description that records what changed and what did not change.
8. Record the PR number, merge commit, validation, status, and next action in the backlog workbook when applicable.

Extended description template:

```text
Summary:
- <main change 1>
- <main change 2>

Validation:
- <command or CI result>

Scope confirmations:
- <docs-only or behavior-changing confirmation>
- <source/test/spec/CI/env/package metadata confirmation>

Follow-up:
- <known gap or next action, if any>
```

For squash merges, prefer a concise title such as `Add operator and technology manual` and a body that explains motivation, files changed, validation, and explicit scope exclusions.

## 17. Backlog and Workbook Workflow

The backlog workbook is a planning and evidence ledger. It is not the source of code truth.

Rules:

- Always use the latest uploaded workbook as the base when generating a new version.
- Record PR number, merge commit, validation, status, next action, and any known follow-up.
- Do not hallucinate workbook state from memory.
- Do not mark a row implemented without repo evidence.
- Keep the live queue small and actionable.
- Park research and long-horizon items separately so the live queue remains useful.
- Do not modify backlog workbooks from repo tasks unless the operator explicitly asks for a workbook artifact.

Evidence should point back to repo artifacts: merged PRs, commit hashes, specs, tests, CI results, and docs.

## 18. Runtime Readiness and Known Gaps

`docs/RUNTIME_READINESS.md` is the current runtime truth document. This manual summarizes major known gaps, but Runtime Readiness should be updated when runtime status changes.

Known gaps and future work include:

- Provider budget/cost accounting.
- Expanded provider observability beyond minimal `/v1/solve` OpenAI lifecycle events.
- Provider SAFE-OUT and fallback hardening.
- Optional gated live OpenAI smoke test.
- Model-set live usability and account access validation.
- Rate-limit Redis/SlowAPI mismatch.
- Placeholder health/rate-limit targets.
- Metrics/Grafana/Docker hardening.
- Simulated Google Sheets / Playwright live readiness decisions.
- SDK auth hardening.
- Production SLO enforcement.

Do not claim live production readiness from placeholders, docs, fake tests, env validation, or planned roadmap rows.

## 19. Live Queue and Remaining Roadmap

Ranked remaining roadmap:

1. Provider budget/cost accounting.
2. Provider SAFE-OUT/fallback orchestration.
3. Optional gated live OpenAI smoke test.
4. Rate-limit/health placeholder cleanup.
5. Metrics/Grafana/runtime hardening and expanded provider observability.
6. Simulated adapter live-readiness decisions.
7. SDK/auth hardening.

Decision rule:

- Do not start provider budget/cost accounting, expanded provider observability, or SAFE-OUT/fallback orchestration without clear scope and a spec if the change is broad.
- Prefer narrow PRs that retire one known gap at a time.
- Keep default CI credential-free unless a future spec adds explicitly gated live tests.

## 20. When Codex Credits Run Out

If Codex credits run out:

- Pause code PRs unless the change is very small and clearly understood.
- Use Claude for review, drafting, and manual/spec critique if helpful.
- Use ChatGPT for prompts, PR review support, merge decision support, and backlog wording.
- Use GitHub Actions and repo evidence as truth.
- Avoid manual code changes unless they are very small, low risk, and easy to review.
- Resume Codex for implementation when credits return.

Do not let credit pressure create broad manual edits, untested code changes, or source-of-truth drift.

## 21. Common Failure Modes

| Failure mode | Why it is risky | Safer response |
| --- | --- | --- |
| Stale docs overclaim runtime. | Operators may believe a future target already works. | Check `docs/RUNTIME_READINESS.md`, tests, and code before claiming readiness. |
| Provider env validation mistaken for live provider usability. | Key presence does not prove model access, quota, billing, or network behavior. | Say env-validation only unless a live gated test proves more. |
| Broad PRs mix docs, code, specs, tests, and CI. | Review becomes hard and regressions hide. | Split into narrow PRs. |
| Workbook treated as repo truth. | Planning rows may be stale. | Confirm with repo files, PRs, commits, tests, and CI. |
| Claude read-only mistaken for repo write access. | Drafts may be mistaken for committed changes. | Require branch, commit, PR URL, and CI evidence. |
| Secrets pasted into prompts/logs. | Credentials can leak outside the repo. | Use placeholders and rotate any exposed secret. |
| Portable solver edited as if disposable. | It is a behavior contract. | Touch only with explicit scope and review SAFE-OUT/routing/envelope effects. |
| Prompt adapters mistaken for provider clients. | Prompt rendering can be confused with live provider execution. | Keep provider execution in provider client paths. |

## 22. Operator Checklists

### Starting a new Codex task

- [ ] Define the desired PR title and scope.
- [ ] List allowed files or file categories.
- [ ] State forbidden changes, such as source/test/spec/CI/env/package metadata changes for docs-only work.
- [ ] Include relevant current runtime truth.
- [ ] Ask Codex to inspect repo files before editing.
- [ ] Ask for files changed, summary, validation, PR URL, squash title, and extended description.

### Reviewing a PR

- [ ] Changed files match the requested scope.
- [ ] Diff does not include unrelated cleanup.
- [ ] Docs do not overclaim runtime readiness.
- [ ] Specs are updated when behavior changes.
- [ ] Tests are added or updated for behavior changes.
- [ ] Validation output is concrete.
- [ ] No secrets, local env files, generated noise, or backlog workbooks were committed.

### Squash merging

- [ ] CI is green or accepted with a documented reason.
- [ ] Squash title is accurate.
- [ ] Extended description lists motivation, summary, validation, and scope confirmations.
- [ ] Follow-ups are recorded.
- [ ] PR number and merge commit are captured for the backlog workbook when applicable.

### Updating backlog

- [ ] Start from the latest uploaded workbook.
- [ ] Record PR number.
- [ ] Record merge commit.
- [ ] Record validation evidence.
- [ ] Update status and next action.
- [ ] Keep live queue small.
- [ ] Do not mark implementation complete from memory.

### Deciding whether a task needs a spec

- [ ] Does it change runtime behavior?
- [ ] Does it change API, solver, routing, SAFE-OUT, budget, determinism, observability, replay, MCP, auth, policy, rate-limit, or provider behavior?
- [ ] Does it change expected outputs or envelopes?
- [ ] Does it retire or redefine a placeholder target?
- [ ] If yes to any of these, create or update a spec before code changes.
- [ ] If it is docs-only or process-only and does not change expected behavior, a spec is usually not required.

### Deciding whether Claude can be used

- [ ] Is the task drafting, review, or critique? Claude can help.
- [ ] Does the task require repo writes? Confirm Claude has GitHub write tools first.
- [ ] Can Claude create a branch, commit, open a PR, and inspect CI?
- [ ] If not, use Claude output only as advisory text.
- [ ] Verify any Claude claims against repo files and CI.

### Checking runtime readiness

- [ ] Read `docs/RUNTIME_READINESS.md`.
- [ ] Check relevant specs.
- [ ] Inspect implementation files.
- [ ] Check tests and CI.
- [ ] Separate local/offline, fake/mocked, env-validation only, service-dependent, and live-provider behavior.
- [ ] Record known gaps instead of smoothing them over.

## 23. Glossary

| Term | Meaning |
| --- | --- |
| local/offline mode | Alpha Solver behavior that runs without live remote LLM credentials or remote provider calls. This is the default baseline. |
| provider client | Code that executes or prepares execution against a model provider API, such as `alpha.providers.openai`. |
| prompt adapter | Code that renders prompts for a provider family. It is not proof of live provider execution. |
| SAFE-OUT | Safety fallback behavior that returns safe, bounded responses when normal solving or provider execution cannot proceed safely. |
| SolverEnvelope | The structured solver response shape/contract referenced by portable and service behavior. |
| Runtime Readiness | The repo document that records what is verified, partial, env-validation only, mocked, service-dependent, or future work. |
| Operating Guide | The repo document that explains the solo operator workflow, roles, specs, PR review, and backlog update loop. |
| `.specs` | The implementation contract directory. Behavior-changing work should start from or update specs. |
| Live Queue | The small set of actionable next backlog items the operator intends to work on soon. |
| provider smoke test | A small test intended to prove a provider path can connect and return a minimal response. Live provider smoke tests must be gated and are not default CI today. |
| fake/mocked test | A test using fake clients, mocked transports, or fixtures instead of real external provider calls. Safe for default CI. |
| env-validation only | A check that required environment variables are present and basic config is valid. It does not prove live provider usability. |
