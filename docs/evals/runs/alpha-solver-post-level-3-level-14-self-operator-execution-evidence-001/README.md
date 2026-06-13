# Self Operator — Local Execution Evidence Packet

Lane ID: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-EXECUTION-EVIDENCE-001`

Verdict: **`LOCAL_EXECUTION_EVIDENCE_CAPTURED`**

DEF-001 status after this lane: **`DEF-001_PARTIALLY_RETIRED`**

## What this packet is

This packet records a single, bounded, operator-supervised **local/offline execution run** of the
existing Self Operator code, executed to *begin* retiring `DEF-001` ("Self Operator execution evidence
remains missing"). It runs only deterministic, in-repository, provider-free entry points: the Self
Operator pytest suite and the Self Operator release-gate checker CLI. It also records the authoritative
full-suite validation result.

This packet is the first execution-evidence lane selected by the PR #496 operator-only MVP decision
packet (`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-operator-only-mvp-decision-packet/`).
It does **not** re-enable any provider, does **not** use any token, and makes **no** readiness claim of
any kind (see `forbidden-claims.md`, `evidence-boundary.md`).

## Required questions answered

| # | Question | Answer |
| --- | --- | --- |
| 1 | Was PR #496 merged into `main`? | Yes. `merged: true`, `merged_at 2026-06-13T03:20:38Z`, base `main`; current `main` tip `f91ced31f808b5689f0ac31c8ecdc031de83368f` is the #496 squash commit. See `repo-state-verification.md`. |
| 2 | What exact local execution target was selected? | (a) `python -m pytest tests/test_self_operator_*.py` (17 files, 213 tests); (b) `python scripts/check_self_operator_release_gate.py --repo-root .`. See `execution-plan.md`. |
| 3 | Why was that target safe under the local/offline boundary? | `alpha/self_operator/` has zero `openai`/`anthropic`/`requests`/`httpx` imports, no credential/env reads, no command execution; tests carry no `live`/`openai` markers; the CLI inspects only local files. See `execution-plan.md`. |
| 4 | What commands were run? | See `commands-run.md` (verbatim, with exit codes). |
| 5 | What inputs/fixtures were used? | In-repo deterministic test fixtures; the release-gate CLI inspects live in-repo evidence directories. See `execution-results.md`. |
| 6 | What outputs/logs/artifacts were produced? | pytest counts (via JUnit XML), release-gate JSON report (embedded in `artifacts-index.md`), exit codes. |
| 7 | Did execution succeed, fail, or stop? | The selected Self Operator targets **succeeded** (213/213 passed; release-gate exit 0, 11/11 gates pass). Consistent with the PR #496 recorded full-suite behavior, the separate provider-env-unset full suite still reports the same two unrelated failures. See `execution-results.md`. |
| 8 | If it failed, what failed and why? | Consistent with the PR #496 recorded full-suite behavior, the provider-env-unset full suite still reports the same two unrelated failures (`test_release_script`, `test_tag_release`); in this run each is caused by the container's commit-signing server returning HTTP 400 in throwaway `git init` repos. Not Self Operator code. See `failure-analysis.md`. |
| 9 | Did any command require provider/model/token/API access? | No. `OPENAI_API_KEY` is present in the environment but was not used; the authoritative full-suite run unsets provider env vars. No provider/model/hosted/API call was made. |
| 10 | Does this evidence partially retire DEF-001, fully retire it, or leave it open? | **Partially** (`DEF-001_PARTIALLY_RETIRED`). See `evidence-boundary.md`. |
| 11 | What remains blocked? | Full operator-supervised end-to-end DEF-001 run; DEF-002 (security/privacy); DEF-003 (Fable audit text); all provider/token/hosted/runtime/benchmark work. See `evidence-boundary.md`. |
| 12 | What next lane is selected? | `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-EXECUTION-EVIDENCE-002` (continue local, no tokens). See `selected-next-lane.md`. |

## Files in this packet

| File | Purpose |
| --- | --- |
| `README.md` | This overview and the required-questions table. |
| `repo-state-verification.md` | Read-only repo-state verification (branch, SHAs, PR #496 merge, open PRs). |
| `execution-plan.md` | The selected execution target and why it is safe under the offline boundary. |
| `commands-run.md` | Exact commands run, with exit codes. |
| `execution-results.md` | Captured results: pytest counts and release-gate output. |
| `artifacts-index.md` | Index of produced artifacts, including the embedded release-gate JSON report. |
| `failure-analysis.md` | Analysis of the 2 unrelated full-suite failures (isolated from this lane). |
| `evidence-boundary.md` | What this packet proves and explicitly does not prove. |
| `forbidden-claims.md` | Claims this packet explicitly does not make. |
| `selected-next-lane.md` | Exactly one selected next lane. |
| `non-actions.md` | Actions this packet did not perform. |

## Boundary

This packet may prove only what was actually run locally. It is documentation/evidence material. It does
not authorize provider re-enable, hosted use, deployment, `/v1/solve` exposure, dashboard exposure,
autonomous operation, or any public/production use, and it makes no MVP, release, runtime, provider,
hosted, benchmark, benchmark-superiority, broad-user, or autonomous readiness claim.
