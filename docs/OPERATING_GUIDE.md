# Operating Guide

A practical workflow for a solo, non-developer operator running an AI-assisted
project. The goal is high-quality, narrowly-scoped, reviewed PRs with low
overhead. This is not a governance manual. If a rule here adds ceremony without
reducing risk, the rule is wrong.

## 1. Purpose

Lock a simple, repeatable loop: plan → scope → implement → review → merge →
record. Keep it light enough for one person to run without drift.

## 2. Source of Truth

- **GitHub repo** — code, docs, tests, commits, PRs, history.
- **`.specs/`** — implementation contracts. The authority for *what behavior is
  intended*.
- **`AGENTS.md`** — the single canonical instruction file for AI agents. Any
  future tool-specific file (e.g. `CLAUDE.md`, `.cursorrules`) must be a thin
  pointer back to `AGENTS.md`, never a separate policy.
- **External backlog workbook** — planning, status, evidence, next action. A
  ledger, not the codebase.
- **`data/alpha_solver_master_table_v0_7_0.*`** — registry export, *not* a
  backlog. See `data/README.md`.

When two sources disagree, the repo wins for code/behavior; `.specs/` wins for
intent; the workbook never overrides repo evidence.

Runtime status and known gaps are tracked in `docs/RUNTIME_READINESS.md`; this
guide covers the operating workflow, not feature readiness.

## 3. Who Does What

- **ChatGPT** — planning, triage, scope clarification, writing Codex prompts,
  PR review support, explaining what happened.
- **Codex** — repo inspection, narrowly-scoped implementation, tests, branch
  and PR creation. Follows `AGENTS.md`.
- **GitHub Web UI** — final PR review, CI visibility, squash merge.
- **You** — approve scope, approve merges, hold final judgment.

## 4. When a Spec Is Required

A spec in `.specs/` is required **before changing behavior** — for example (not
exhaustive): features, behavior-changing bugfixes, API/solver/routing/SAFE-OUT/
budget-guard/determinism/observability/replay behavior, and auth/policy/
rate-limit behavior.

A spec is **not** required for docs-only or process-only changes — for example:
README cleanup, `AGENTS.md` edits, this guide, registry/backlog clarification,
typo fixes, link updates.

If a "docs-only" change actually changes expected behavior, it is not docs-only
— write or update the spec first.

## 5. Tests & CI

CI runs the test suite on every PR. Trust a green CI as the signal.

- **Code or test changes** — CI must pass; add or update focused tests for the
  change.
- **Docs-only / process-only PRs** — no manual full test run is needed. `git
  diff --check`, and a quick smoke/help command only if the docs reference an
  executable command.

Do not run the full suite by hand as ceremony when CI already covers it.

## 6. Inspect-Only vs Implement

Use **Codex inspect-only** (no file changes) when something is genuinely
unclear: repo evidence is uncertain, a row may already be implemented, a spec
may be drifted or copied, a placeholder may be mistaken for finished work,
deletion/rename/archiving is being considered, or sources of truth conflict.

Use **Codex implementation** when the change is confirmed, the scope is narrow,
the target files are known, acceptance criteria are clear, and unrelated cleanup
is excluded.

Inspect-only is for ambiguity, not for every task.

## 7. Backlog & Live Queue

- A row is **not "implemented"** without PR + merge commit + spec/test evidence.
- Record an update **immediately** after: implementation PRs, spec changes,
  source-of-truth/process docs, and PRs that close or change a backlog item.
- Trivial docs-only updates may be **batched**.
- Use **one PR changelog table**. Do not create a new sheet per PR.
- The workbook is the planning/evidence ledger. Keep the actionable live items
  short and clean; park research and long-horizon items separately so the live
  list stays readable.

Automation candidates (validators, link checkers, drift checks) belong in the
backlog as rows, not in this guide.

## 8. Tool Stack

- **Primary now:** ChatGPT, Codex, GitHub Web UI, `.specs/`, the backlog
  workbook, `AGENTS.md`.
- **Later (after local Mac setup):** VS Code, GitHub Desktop.
- **Not now:** Cursor, Claude Code, GitHub Copilot as primary agents; Devin,
  Replit, Windsurf, Notion, Linear, Jira; full backlog migration to GitHub
  Issues. A small Issues pilot for a live queue may be considered later.

Codex remains the primary implementation agent. Adding a second agent is a
later experiment, only if a clear need appears.

## 9. Security

- Never commit `.env`. `.env.example` may be tracked.
- API/provider keys live only in: local environment, local `.env`, or GitHub
  Actions secrets.
- Agents must never paste real keys into docs, tests, logs, PR bodies, or
  sample output.
