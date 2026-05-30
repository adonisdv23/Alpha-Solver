# Alpha Solver Operator & Technology Manual

## 1. Purpose of This Manual

This manual is the operator-facing control document for Alpha Solver development.
It ties together current runtime state, source-of-truth rules, tool roles,
pull-request review, backlog discipline, and the remaining roadmap.

It explains:

- what Alpha Solver currently does;
- what is verified, partial, mocked, specified, or not implemented;
- which files are source of truth;
- which tools to use for each kind of task;
- how to review PRs safely;
- how to avoid overclaiming runtime readiness;
- what remains on the roadmap.

This manual is not a replacement for code, tests, specs, or CI evidence. It is
the human operating guide that helps the operator use those sources in the right
order.

## 2. Current State Snapshot

### 2.1 Verified default behavior

Current default behavior is local/offline and credential-free:

- Local/offline remains the default operating mode.
- `.env.example` defaults to `MODEL_PROVIDER=local`.
- Default CI remains credential-free and network-free for provider behavior.
- `scripts/check_env.py` validates configuration and environment-variable
  presence only. It does not prove live provider usability, billing, quota,
  model access, or network connectivity.
- Prompt adapters remain prompt renderers, not provider clients.
- The portable solver remains local/offline.

### 2.2 FastAPI `/v1/solve` current state

FastAPI `/v1/solve` has a local default path and an explicit OpenAI provider
path:

- `/v1/solve` supports local/offline behavior by default.
- `/v1/solve` can enter the OpenAI provider path only when
  `MODEL_PROVIDER=openai`.
- The OpenAI provider path requires `OPENAI_API_KEY` at runtime for live use.
- OpenAI provider use remains explicit opt-in.
- Default CI uses fake/mocked provider tests, not live OpenAI calls.

### 2.3 Implemented OpenAI provider capabilities

Implemented:

- OpenAI provider client foundation.
- Explicit `/v1/solve` OpenAI provider integration.
- Provider lifecycle telemetry:
  - `provider.request.started`
  - `provider.request.completed`
  - `provider.request.failed`
  - `provider.request.timeout`
- Success-only post-call provider cost accounting:
  - `provider.cost.recorded`
- Structured provider SAFE-OUT response normalization for OpenAI provider
  failures.
- No-secret, allowlist-based telemetry/accounting/SAFE-OUT response
  construction.

### 2.4 Not implemented

Not implemented:

- Optional gated live OpenAI smoke test.
- Hard or soft budget enforcement.
- Pre-call budget blocking.
- Persistent tenant budgets.
- Real billing integration.
- Local fallback after provider failure.
- `provider.fallback.local` emission.
- CLI remote provider execution.
- Portable solver remote provider execution.
- Production SLO enforcement.
- Full replay/determinism integration for provider paths.
- Expanded Prometheus/Grafana/OpenTelemetry provider observability.
- Production hardening.

## 3. Source-of-Truth Hierarchy

Use this hierarchy when documents, agents, backlog rows, or memory disagree:

1. **Repo code and tests** — current executable truth.
2. **`.specs/*.md`** — implementation contracts and boundaries.
3. **`docs/RUNTIME_READINESS.md`** — current runtime status: verified, partial,
   mocked, placeholder, future.
4. **`docs/OPERATING_GUIDE.md`** — workflow rules for planning, specs, PRs,
   merges, and source discipline.
5. **`docs/OPERATOR_TECHNOLOGY_MANUAL.md`** — human-readable operating
   synthesis.
6. **`README.md`** — entry navigation and onboarding pointer.
7. **Backlog spreadsheet / changelog / operating log** — planning and evidence
   ledger, not runtime truth.
8. **ChatGPT, Codex, Claude, or other assistant output** — advisory unless tied
   to inspected files, commits, PRs, tests, or CI evidence.

Key distinction:

- `.specs/` says what should be built.
- Runtime Readiness says what currently works or is still partial/future.
- Operating Guide says how work should happen.
- Operator Manual explains how the operator should run the project.
- Backlog spreadsheets track history, pending tasks, and decisions.

## 4. Technology Stack and Runtime Surfaces

### 4.1 Core repo surfaces

| Surface | Role | Operator rule |
| --- | --- | --- |
| `alpha_solver_portable.py` | Portable standalone behavior contract. | Keep local/offline unless explicitly approved and spec-backed. Do not casually edit. |
| `alpha-solver-v91-python.py` | Modular/reference entrypoint path. | Treat as a sensitive entrypoint; consult `docs/ENTRYPOINTS.md` before changes. |
| `alpha_solver_entry.py` | Bridge/root entrypoint path. | Treat as part of entrypoint compatibility. |
| `alpha_solver_cli.py` | Root CLI wrapper/entrypoint. | CLI remote provider execution is not implemented. |
| `cli/alpha_solver_cli.py` | CLI implementation surface. | Preserve local/offline behavior unless a spec approves remote provider execution. |
| `service/app.py` | FastAPI app and `/v1/solve` integration point. | Local by default; OpenAI provider path only by explicit `MODEL_PROVIDER=openai`. |
| `alpha/providers/base.py` | Provider request/result/error data contracts. | Do not broaden provider behavior without a provider spec. |
| `alpha/providers/openai.py` | OpenAI provider client foundation. | Live use requires private credentials and is not production-hardened. |
| `alpha/providers/telemetry.py` | No-secret provider lifecycle telemetry helpers. | Emit only allowlisted safe fields. |
| `alpha/providers/accounting.py` | No-secret success-path provider cost accounting helpers. | Accounting records are not budget enforcement. |
| `alpha/providers/safeout.py` | Structured provider SAFE-OUT response helpers. | Normalize failures safely; do not imply local fallback. |
| `alpha/providers/*` | Provider abstractions, fake provider support, OpenAI provider path. | Default CI should stay fake/mocked for live-provider behavior. |
| Prompt adapters | Prompt rendering for provider families. | Prompt rendering is not provider execution. |
| `.specs/` | Implementation contracts and boundaries. | Add/update specs before behavior-changing work. |
| `docs/` | Operator docs, runtime readiness, entrypoint docs, architecture and references. | Update when runtime claims or workflows change. |
| `tests/` | Executable verification and fake/mocked provider coverage. | Add/update focused tests for behavior changes. |
| `.env.example` | Safe default environment template. | Keep local/offline as the default. |
| `scripts/check_env.py` | Environment/configuration checker. | Validates shape and required env vars only; no live provider calls. |

### 4.2 Provider path

Current OpenAI provider lifecycle for FastAPI `/v1/solve`:

1. Operator explicitly sets `MODEL_PROVIDER=openai`.
2. `/v1/solve` builds a `ProviderRequest` from request/query/model-set data.
3. Service emits `provider.request.started`.
4. OpenAI provider client executes.
5. On success:
   - emits `provider.request.completed`;
   - emits `provider.cost.recorded`;
   - returns the provider success response.
6. On failure:
   - emits `provider.request.failed` or `provider.request.timeout`;
   - records the SAFE-OUT metric;
   - returns a structured provider SAFE-OUT response;
   - emits no cost accounting;
   - executes no local fallback.

### 4.3 Local/offline path

Default local/offline behavior is preserved:

- Default local path is safe to run without provider API keys.
- `.env.example` keeps `MODEL_PROVIDER=local`.
- No provider telemetry or provider cost accounting is emitted in local/offline
  mode.
- Local/offline behavior is the baseline for normal development, docs-only PRs,
  and default CI.

## 5. Tool Roles

### 5.1 ChatGPT

Use ChatGPT for:

- project strategy;
- architecture sequencing;
- prompt creation for Codex or Claude;
- PR review assistance;
- comparing Codex and Claude outputs;
- detecting scope creep;
- deciding what should be merged, refined, or deferred;
- converting findings into next prompts.

Do not rely on ChatGPT alone to claim repo state unless it has inspected the
relevant PR, files, terminal output, or CI evidence.

### 5.2 Codex

Use Codex for:

- implementation PRs;
- focused repo edits;
- tests;
- specs;
- runtime docs;
- CI-safe changes;
- one task per PR.

Best Codex pattern:

1. New task thread per PR.
2. Precise objective.
3. Explicit files to inspect.
4. Explicit forbidden changes.
5. Acceptance criteria.
6. Validation commands.
7. Expected PR body.
8. Suggested squash title and extended description.

Avoid:

- vague prompts;
- multi-lane PRs;
- “fix everything” tasks;
- changing tests, docs, runtime, and CI all at once unless explicitly required.

### 5.3 Claude Code

Use Claude Code for:

- read-only audits;
- long-form document review;
- contradiction detection;
- second-opinion architecture review;
- docs/spec work when Codex is unavailable;
- small controlled edits with explicit approval.

Claude Code session hygiene:

- New lane = new Claude Code session.
- Same lane follow-up = same Claude session.
- After merge = new Claude session.
- Ask Claude to use targeted inspection first.
- Avoid broad repo exploration unless required.
- Do not rely on long-running Claude sessions as repo truth.

Mode guidance:

- Plan mode = audit/planning artifact.
- Accept edits = controlled implementation.
- Auto mode = avoid for this project for now.

### 5.4 GitHub web UI

Use GitHub web UI for:

- reviewing changed files;
- checking CI;
- editing tiny docs/spec changes if agents are unavailable;
- squash merging;
- confirming merge state.

### 5.5 Manual editing

Manual editing is acceptable for:

- tiny docs/spec changes;
- typo fixes;
- small table updates;
- obvious one-line navigation links.

Avoid manual editing for:

- provider code;
- tests;
- CI workflows;
- runtime behavior;
- security-sensitive logic;
- any change requiring multi-file consistency.

## 6. PR Workflow

Standard PR workflow:

1. Identify the lane.
2. Decide whether a planning audit is required.
3. If architecture-sensitive, ask Codex and/or Claude for read-only audit.
4. Convert the audit into a narrow implementation prompt.
5. Use one Codex thread per PR.
6. Review PR:
   - changed files;
   - diff;
   - tests;
   - CI;
   - forbidden changes;
   - docs/spec alignment.
7. Squash merge with clean title and extended description.
8. Update runtime/docs/backlog if needed.
9. Move to the next lane.

Merge checklist:

- Does the PR match the requested lane?
- Did it change forbidden files?
- Did it add live calls to default CI?
- Did it change local/offline default?
- Did it expose secrets, prompts, raw payloads, or raw exceptions?
- Did it overclaim readiness?
- Did tests run?
- Is CI green?
- Does the squash title match the lane?
- Does the extended description preserve scope boundaries?

Suggested squash description shape:

```text
Summary:
- <main change>
- <main change>

Validation:
- <command or CI result>

Scope confirmations:
- <docs-only or behavior-changing confirmation>
- <source/test/spec/CI/env/package metadata confirmation>

Follow-up:
- <known gap or next action, if any>
```

## 7. Current Provider/OpenAI Truth

### 7.1 What exists

- OpenAI provider client.
- Explicit `/v1/solve` OpenAI provider path.
- Provider lifecycle telemetry.
- Success-only cost accounting.
- Structured provider SAFE-OUT responses.
- Provider failure normalization.
- Fake/mocked CI coverage.

### 7.2 What does not exist

- Live OpenAI smoke test.
- Production-readiness guarantee.
- Live provider reliability guarantee.
- Budget enforcement.
- Local fallback after provider failure.
- `provider.fallback.local`.
- CLI remote execution.
- Portable solver remote execution.

### 7.3 Current operator rule

Passing `scripts/check_env.py` means configuration shape is valid. It does not
mean OpenAI works live.

OpenAI live readiness requires:

- valid `OPENAI_API_KEY`;
- account access;
- model access;
- billing/quota;
- network availability;
- successful gated live test, once implemented.

## 8. Runtime Readiness Summary

The Operator Manual summarizes Runtime Readiness; it should not duplicate every
readiness row. `docs/RUNTIME_READINESS.md` remains the detailed source for:

- verified local/offline behavior;
- env-validation-only behavior;
- mocked/simulated behavior;
- partial runtime features;
- placeholder/future features;
- external-service requirements;
- non-implemented surfaces.

When runtime status changes, update Runtime Readiness first or in the same PR as
this manual. Do not use this manual to create behavior that code does not
implement.

## 9. Backlog and Operating Ledger Sync

### 9.1 Purpose

The backlog spreadsheet is the planning and tracking ledger.

It should track:

- completed PRs;
- specs added;
- implemented capabilities;
- deferred tasks;
- known gaps;
- next actions;
- ownership/tool recommendation;
- current status;
- evidence links.

### 9.2 What the backlog is not

The backlog is not runtime truth. If the backlog disagrees with code, tests,
specs, or Runtime Readiness, update the backlog rather than overriding the repo.

Do not modify backlog workbooks from repo tasks unless the operator explicitly
asks for a workbook artifact.

### 9.3 Required backlog sync after provider stabilization

Add or update rows for:

- provider env validation/local default;
- OpenAI provider spec;
- OpenAI provider client;
- `/v1/solve` OpenAI integration;
- package dependency reconciliation;
- Runtime Readiness matrix;
- Operator & Technology Manual;
- Python 3.14 math compatibility;
- provider telemetry;
- provider budget/cost accounting;
- provider SAFE-OUT response normalization;
- optional gated live OpenAI smoke;
- future budget enforcement;
- future fallback orchestration;
- future CLI remote execution;
- future portable provider integration.

### 9.4 Backlog fields to use

Recommended columns:

- ID
- Task name
- Lane
- Status
- Priority
- Source of truth
- PR number
- Spec file
- Runtime/docs impacted
- Owner/tool
- Validation evidence
- Deferred dependencies
- Next action
- Notes

## 10. Common Failure Modes

### 10.1 Spec mistaken for runtime truth

Risk: a spec says something should exist, but code does not implement it.

Correction: check code, tests, and Runtime Readiness.

### 10.2 Env validation mistaken for live provider readiness

Risk: `scripts/check_env.py` passes and the operator assumes OpenAI is
live-verified.

Correction: remember it checks env/config only.

### 10.3 Claude stale session

Risk: Claude inspects an old branch after a merge.

Correction: start a new Claude session after merges.

### 10.4 Codex scope expansion

Risk: Codex implements related future work not requested.

Correction: use forbidden-changes lists and review diffs carefully.

### 10.5 Fallback event without actual fallback

Risk: `provider.fallback.local` is emitted for SAFE-OUT-only behavior.

Correction: reject the change. `provider.fallback.local` can only emit when
actual local fallback executes.

### 10.6 Overclaiming production readiness

Risk: docs imply the provider path is production-ready.

Correction: say explicit opt-in service path exists, but production hardening
remains future work.

## 11. Remaining Roadmap

### 11.1 Near-term

1. Optional gated OpenAI live smoke, Codex later.
2. Backlog spreadsheet sync.
3. Final Operator & Technology Manual refresh.
4. Rate-limit/health placeholder cleanup.
5. Expanded provider observability or metrics hardening.

### 11.2 Later

1. Budget enforcement and persistence.
2. Local fallback orchestration, opt-in only.
3. `provider.fallback.local`, only if actual fallback executes.
4. Replay/determinism integration.
5. CLI remote provider execution.
6. Portable solver provider integration, only if explicitly approved.
7. Production SLO/hardening.

Roadmap items are not blockers for current local/offline operation. They are
known future lanes that should be scoped into narrow specs and PRs before
implementation.

## 12. Operator Quick-Use Playbook

### If you want to implement code

Use Codex.

### If you want to inspect or critique architecture

Use Claude Code Plan mode or ChatGPT.

### If you want to review a PR

Bring the PR link and Codex/Claude notes to ChatGPT.

### If you want a tiny docs/spec update and agents are unavailable

Use GitHub web UI manually.

### If live provider behavior is involved

Do not add it to default CI. Gate it. Spec it first.

### If secrets are involved

Never paste secrets into prompts, PR bodies, docs, tests, logs, screenshots, or
telemetry examples.

## 13. Final Manual Acceptance Criteria

This manual is ready when:

- It matches current repo state after the provider telemetry, accounting, and
  SAFE-OUT stabilization work reflected in Runtime Readiness.
- It does not claim a live OpenAI smoke test exists unless implemented.
- It says optional live smoke is planned/deferred.
- It distinguishes specs from runtime truth.
- It explains Codex, Claude, ChatGPT, GitHub, and manual editing roles.
- It includes Claude session hygiene.
- It includes backlog spreadsheet sync rules.
- It lists remaining roadmap items without turning them into blockers.
- It avoids production-readiness overclaims.
- It gives the operator a clear next action: keep default work local/offline,
  use Codex for narrow PRs, update the backlog from repo evidence, and defer
  live-provider proof until an explicitly gated smoke-test lane is implemented.
