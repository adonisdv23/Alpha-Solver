# Repo-state verification

Read-only verification performed 2026-06-13 (no writes, no provider calls).
Repo: `adonisdv23/Alpha-Solver`. Branch for this lane:
`claude/stoic-archimedes-6q8rd0` (cut from `main`).

## PR merge status

Verified `merged:true` directly via the GitHub API for **#497, #503, #505,
#507, #508, #509**. The remaining PRs (**#499, #500, #501, #502, #504, #506**)
are confirmed merged via the `base.sha` chain on `origin/main` — each PR's base
commit is the prior PR's merge commit — matching the local `git log` on
`origin/main`.

| PR | merged | merge/verification anchor |
|----|--------|---------------------------|
| #497 | ✅ API `merged:true` | `merged_at 2026-06-13T05:17:35Z` |
| #499 | ✅ chain | commit `070007c` on main |
| #500 | ✅ chain | commit `85168b8` on main |
| #501 | ✅ chain | commit `00cc968` on main |
| #502 | ✅ chain | commit `0ce8cdb` on main (base of #503) |
| #503 | ✅ API `merged:true` | `merged_at 2026-06-13T07:23:42Z` |
| #504 | ✅ chain | commit `f8efc99` on main (base of #505) |
| #505 | ✅ API `merged:true` | `merged_at 2026-06-13T07:41:03Z` |
| #506 | ✅ chain | commit `f5bc500` on main (base of #508) |
| #507 | ✅ API `merged:true` | `merged_at 2026-06-13T07:46:56Z` |
| #508 | ✅ API `merged:true` | `merged_at 2026-06-13T08:07:02Z` |
| #509 | ✅ API `merged:true` | `merged_at 2026-06-13T13:52:58Z` |

**PR #509 is merged → not `BLOCKED_PR_509_NOT_MERGED`.**

## Open PRs

`list_pull_requests(state=open)` → **`[]`**. No open PRs conflict with this docs
lane.

## Required directories present on `main`

- OpenAI checker-scope hardening packet (PR #508):
  `docs/evals/runs/openai-packet-checker-scope-001/` ✅
- Local OpenAI token smoke retry packet (PR #509):
  `docs/evals/runs/local-openai-token-smoke-capture-retry-001/` ✅
- DEF-002 / DEF-003 boundary packet (PR #503):
  `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-def-002-def-003-evidence-boundary-001/` ✅
- OpenAI packet directories: `openai-*`, `local-openai-*`,
  `alpha-solver-openai-*` ✅
- Local execution evidence directories:
  `alpha-solver-post-level-3-level-14-self-operator-execution-evidence-001..004` ✅

## Environment note

`OPENAI_API_KEY` presence was **not** checked or used in this lane; this is a
docs-only lane and performs no provider preconditions. No secrets were read or
printed.
