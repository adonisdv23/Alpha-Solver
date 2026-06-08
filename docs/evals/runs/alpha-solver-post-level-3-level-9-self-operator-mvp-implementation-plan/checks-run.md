# Checks Run

## Required checks

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-mvp-implementation-plan`
- `rg "READY_FOR_FIRST_CODE_STATIC_TEST_SCAFFOLD_PLANNING_ONLY|ALPHA-SOLVER-POST-LEVEL-3-LEVEL-10-SELF-OPERATOR-STATIC-TEST-SCAFFOLD-IMPLEMENTATION-001|ALPHA-SOLVER-POST-LEVEL-3-LEVEL-9-SELF-OPERATOR-MVP-IMPLEMENTATION-PLAN-FIX-001|does not implement Self Operator|no provider calls|no external API calls|no credentials|no browser automation|no deployment|no billing|no evidence promotion" docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-mvp-implementation-plan`
- Confirm changed files are only under `docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-mvp-implementation-plan/`.

## Result log

| Check | Result | Notes |
|---|---|---|
| `git status --short` | PASS | Showed only the new packet directory as untracked before staging. |
| `git diff --name-only` | PASS | No tracked-file paths were listed because all changes are new untracked packet files. |
| `git diff --check` | PASS | No whitespace errors were reported. |
| `make check-local-llm-orchestration-guardrails` | PASS | Evidence-boundary (450 files), doc path/link (49 files), and packet consistency (81 packet directories) guardrails passed. |
| `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-mvp-implementation-plan` | PASS | Target packet consistency check passed for one packet directory. |
| `rg "<required phrases>"` | PASS | All required decision, lane, fallback, and boundary phrases were found in the packet. |
| Changed-file boundary confirmation | PASS | All changes are only under the new packet directory. |

## Evidence boundary

Checks for this packet are repository and documentation checks only. They do not implement Self Operator, modify runtime, create tests, run future Self Operator tests, call providers, expose `/v1/solve`, expose dashboards, configure credentials, run models, run benchmarks, deploy, perform billing work, autonomously merge, control browsers, or promote evidence.
