# Pi.dev Harness Feasibility

Lane: `18 - PI.DEV-HARNESS-FEASIBILITY`

Mode: research/design only

Verdict: `BORROW_PATTERNS_ONLY_NO_INTEGRATION`

## TLDR

Pi.dev is relevant to Alpha Solver as a reference design for a small,
extensible, terminal-first agent harness, not as a runtime dependency or direct
integration target. The safest near-term action is to borrow UX and harness
patterns in a design note: prompt templates, explicit skills, tree-shaped
session evidence, JSON/event-stream style transcript export, interrupt/follow-up
controls, and local-first package boundaries. Do not install Pi, run Pi, call
providers through Pi, expose Alpha Solver APIs to Pi, or claim Pi.dev
integration.

## Useful patterns

- **Minimal core plus explicit extension points.** Pi.dev presents itself as a
  minimal terminal coding harness extended through TypeScript extensions,
  skills, prompt templates, themes, and packages. Alpha Solver can borrow the
  pattern of keeping the core workflow small while moving operator-specific
  affordances into explicit, reviewable packets or optional local tooling.
- **Prompt-packet and skill progressive disclosure.** Pi.dev skills are
  self-contained workflow packages with instructions, helper scripts, references,
  and assets that load on demand. Alpha Solver can adapt this as a repo-native
  operator-packet convention without importing Pi package mechanics.
- **Prompt templates as named operator actions.** Reusable slash-command style
  prompts map well to Alpha Solver prompt packets, demo packets, evidence review
  checklists, and lane-selection prompts.
- **Session tree and export discipline.** Pi.dev documents tree-structured
  sessions with branch navigation, HTML export, and gist sharing. Alpha Solver
  can use the session-tree idea for local evidence review, while forbidding
  public upload or external session sharing for private Alpha Solver work.
- **Interactive steering semantics.** Pi.dev distinguishes steering messages sent
  while an agent is working from follow-up messages queued until completion. That
  maps to Alpha Solver operator workflow controls: interrupt, stop-condition,
  approval-gate, and evidence-review interventions.
- **Multiple execution surfaces.** Pi.dev describes interactive, print/JSON,
  RPC, and SDK modes. Alpha Solver can borrow the interface taxonomy for future
  local harness design, but any Alpha implementation should stay offline/local
  first until a separate spec approves automation.
- **Provider abstraction as a cautionary pattern.** Pi.dev supports OAuth and API
  key providers. Alpha Solver should treat that as a risk surface to design
  around, not a near-term integration goal.
- **Containerization/sandbox guidance as a boundary reminder.** Pi.dev's own
  repository states the tool does not include a built-in permission system for
  filesystem, process, network, or credential restrictions and recommends
  container/sandbox patterns when stronger boundaries are needed.

## What direct integration would require

Direct integration is not recommended. If a future operator explicitly requests
it, a separate spec and threat model would be required before any prototype. At
minimum, direct integration would require:

1. exact Pi.dev package, version, source, license, and maintainer provenance;
2. npm/package-lock review, reproducible install policy, and third-party package
   allowlist;
3. isolated workspace with no Alpha Solver secrets, private artifacts, provider
   tokens, or production configuration;
4. provider/key policy that blocks OAuth login, environment key discovery, auth
   file writes, and outbound model calls by default;
5. sandbox policy for filesystem, process, shell, and network access;
6. explicit session-export policy forbidding gist, Hugging Face, package
   telemetry, or other external transcript sharing unless a sanitized public
   dataset is deliberately approved;
7. proof that `/v1/solve`, dashboards, runtime entrypoints, and public API
   behavior remain unexposed and unchanged;
8. cost controls for any model-provider experiment, including a dry-run mode;
9. legal/security review for extension/package execution and data handling;
10. rollback plan and a narrow non-runtime prototype location outside Alpha
    Solver or in docs-only form.

## Integration risks

- **Supply chain.** Pi.dev is distributed through npm and supports packages from
  npm or git. Third-party packages can add extensions, skills, prompt templates,
  themes, tools, UI, and behavior, so package installation is an executable-code
  trust decision rather than a passive configuration step.
- **Extension behavior.** Extensions may alter tools, commands, events,
  keybindings, UI, dynamic context, compaction, RAG, or memory. That is powerful
  but conflicts with Alpha Solver's narrow-evidence and deterministic-review
  posture unless every extension is pinned and reviewed.
- **Sandbox and permissions.** The Pi repository says Pi has no built-in
  permission system restricting filesystem, process, network, or credential
  access. Running it in Alpha Solver's workspace would therefore inherit the
  launching user's access unless separately sandboxed.
- **Provider/key exposure.** Pi.dev provider docs describe subscription OAuth,
  API keys via environment variables, and auth-file storage. That creates risk of
  accidental use of personal subscriptions, leaked environment variables, or
  persisted auth files.
- **Cost and quota.** Multi-provider support increases risk of unintended token
  spend, subscription overage, or model switching outside the operator's intended
  budget guardrails.
- **Data sharing.** Pi.dev session export/share patterns and repository guidance
  encouraging public OSS session sharing are useful for open work, but unsafe for
  private Alpha Solver artifacts unless a sanitized dataset process exists.
- **Public-surface confusion.** A Pi harness could be mistaken for Alpha Solver
  runtime support. Any prototype must not expose dashboards, `/v1/solve`, public
  API behavior, production readiness, or provider validation claims.
- **License/provenance drift.** Pi core may be open source, but package catalog
  entries can have different licenses, maintainers, release cadences, and
  security postures. Each package would need separate review.

## Security/data boundaries

- Do not install Pi.dev in this repository for this lane.
- Do not run Pi.dev against Alpha Solver source, artifacts, credentials, or
  private operator sessions.
- Do not call model providers, OAuth flows, API-key providers, package install
  endpoints, or external session-sharing tools through Pi.dev.
- Do not copy Alpha Solver private prompts, traces, eval artifacts, dashboard
  outputs, env files, or solver traffic into Pi.dev or Pi packages.
- Do not expose dashboards, `/v1/solve`, bridge entrypoints, runtime settings,
  public API behavior, or production endpoints to a Pi harness.
- If future experimentation is approved, use a disposable non-secret fixture repo
  and network/provider-disabled sandbox first.

## Recommended status

`BORROW_PATTERNS_ONLY_NO_INTEGRATION`

Create or extend an Alpha-native design note for operator harness UX. The note
should capture useful patterns while preserving Alpha Solver's repo-native
specs, evidence boundaries, budget guardrails, and no-runtime-change posture.
Direct Pi.dev integration should be deferred.

## Proposed future lane

`ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001`

Scope:

- define local operator-harness concepts inspired by Pi.dev without importing Pi;
- map prompt packets to named local templates;
- define local session evidence format, branch labels, export redaction, and
  no-upload defaults;
- define interrupt/follow-up/stop-condition UX semantics;
- define package/skill review rules for any future local-only tooling;
- produce docs-only artifacts first.

## Minimum safe future PR

A minimum safe future PR is docs-only and should:

1. add an Alpha-native operator-harness design note;
2. add a threat-model checklist for external agent harness experiments;
3. add a session-evidence/export redaction checklist;
4. explicitly state that Pi.dev is not installed, integrated, or runtime-linked;
5. avoid dependency, runtime, API, dashboard, provider, and credential changes.

## Non-claims

This research does not claim:

- Pi.dev is integrated with Alpha Solver;
- Pi.dev is approved for Alpha Solver runtime use;
- Pi.dev provider behavior was validated;
- Pi.dev packages are safe for Alpha Solver;
- Alpha Solver public APIs, dashboards, `/v1/solve`, or runtime behavior support
  Pi.dev;
- Alpha Solver is production-ready because of Pi.dev patterns;
- Pi.dev creates Alpha Solver value, superiority, or partnership;
- Odysseus, AGPL code, or unrelated operator-workbench components were folded
  into Alpha Solver.

## Sources reviewed

- Pi.dev homepage/docs (`https://pi.dev/`, `https://pi.dev/docs/latest`):
  minimal harness, customization, modes, providers, session tree/export, context
  engineering, and extension/package model.
- Pi.dev provider docs (`https://pi.dev/docs/latest/providers`): OAuth
  subscription providers, API keys, auth-file storage, and provider model
  resolution.
- Pi.dev skills docs (`https://pi.dev/docs/latest/skills`): skill package
  structure, loading rules, and executable-code security warning.
- Pi GitHub repository README (`https://github.com/earendil-works/pi`): package
  layout, session-sharing guidance, permissions/containerization statement, and
  development notes.
- Pi.dev package catalog (`https://pi.dev/packages`): third-party package
  breadth and package install model.
