# Repo-state verification

Live GitHub verification was performed on 2026-06-13 using the GitHub Pulls API for `adonisdv23/Alpha-Solver`. Local repository verification was performed in `/workspace/Alpha-Solver`.

| Requirement | Status | Evidence |
|---|---:|---|
| PR #502 merged into `main` | verified | GitHub API: `state=closed`, `merged_at=2026-06-13T07:17:37Z`, title `docs(eval): add OpenAI free-token smoke and eval harness plan`. |
| PR #503 merged into `main` | verified | GitHub API: `state=closed`, `merged_at=2026-06-13T07:23:42Z`, title `docs(self-operator): add DEF-002 DEF-003 evidence boundary packet`. |
| PR #504 merged into `main` | verified | GitHub API: `state=closed`, `merged_at=2026-06-13T07:29:17Z`, title `docs(openai): add data-sharing operator verification packet`. |
| PR #505 merged into `main` | verified | GitHub API: `state=closed`, `merged_at=2026-06-13T07:41:03Z`, title `docs(openai): add local token smoke capture packet`. |
| PR #505 recorded blocked missing attestation | verified | `docs/evals/runs/local-openai-token-smoke-capture-001/blocked-before-provider-call.md` records `Required merged OpenAI operator pre-smoke attestation packet ... was missing`. |
| PR #506 merged into `main` | verified | GitHub API: `state=closed`, `merged_at=2026-06-13T07:47:03Z`, title `docs(openai): add synthetic smoke prompt fixture packet`. |
| PR #506 contains synthetic smoke prompt fixture | verified | `docs/evals/runs/openai-synthetic-smoke-prompt-fixture-001/synthetic-prompt-set.md` contains `SMOKE-001`. |
| PR #507 merged into `main` | verified | GitHub API: `state=closed`, `merged_at=2026-06-13T07:46:56Z`, title `docs(openai): add operator pre-smoke attestation packet`. |
| PR #507 contains operator pre-smoke attestation | verified | `docs/evals/runs/openai-data-sharing-operator-attestation-001/operator-attestation-artifact.json` exists and records the pre-smoke attestation fields. |
| PR #508 merged into `main` | verified | GitHub API: `state=closed`, `merged_at=2026-06-13T08:07:02Z`, title `docs(openai): extend static checks to OpenAI evidence packets`. |
| PR #508 extends static checker scope to OpenAI packet families | verified | `docs/evals/runs/openai-packet-checker-scope-001/README.md` records `OPENAI_PACKET_CHECKER_SCOPE_EXTENDED`. |

Required packet directories were present locally:

- `docs/evals/runs/alpha-solver-openai-free-token-eval-smoke-harness-plan-001/`
- `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-def-002-def-003-evidence-boundary-001/`
- `docs/evals/runs/openai-data-sharing-operator-verification-001/`
- `docs/evals/runs/local-openai-token-smoke-capture-001/`
- `docs/evals/runs/openai-synthetic-smoke-prompt-fixture-001/`
- `docs/evals/runs/openai-data-sharing-operator-attestation-001/`
- `docs/evals/runs/openai-packet-checker-scope-001/`
