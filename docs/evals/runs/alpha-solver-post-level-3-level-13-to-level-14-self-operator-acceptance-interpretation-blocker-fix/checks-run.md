# Checks run

## Prerequisite verification (before any edit)

- `git fetch origin main` + `git log origin/main` — confirmed the Prompt 3
  packet
  (`docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-interpretation-and-release-gate-apply/`)
  is on current `main` (commit `18bc4fe`, PR #466) with
  `interpretation-result.json` recording `blocked` (p0=0, p1=6, p2=4, p3=0).
- Read-only review of the Prompt 3 packet, the accepted import summary, the
  #461 task-execution ledger, the #459 manual acceptance plan, and the engine,
  importer, and release-gate sources (see `blocker-review.md`).

## Focused tests (changed module)

```
python -m pytest -q tests/test_self_operator_acceptance_interpretation.py
```

Result: **21 passed** (14 pre-existing tests, all passing after the fix and the
MLA-010 fixture correction, plus 7 new importer-vocabulary tests).

```
python -m pytest -q tests/test_self_operator_acceptance_interpretation.py \
  tests/test_self_operator_result_import.py \
  tests/test_self_operator_release_gate.py \
  tests/test_self_operator_import_blocker_triage.py \
  tests/test_self_operator_static_guardrails.py \
  tests/test_self_operator_forbidden_behavior_static.py \
  tests/test_local_llm_packet_consistency.py
```

Result: **88 passed** (self-operator battery plus the repo packet-consistency
test, which scans this packet directory).

```
python scripts/check_local_llm_packet_consistency.py
```

Result: `Local LLM packet consistency check passed (115 packet directories
scanned).`

## Verification run against the real accepted import (read-only input, scratch output)

```
python scripts/interpret_self_operator_acceptance.py \
  --import-summary docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json \
  --output /tmp/blocker-fix-verification-interpretation.json
```

Stdout:

```
interpretation=blocked tasks=10 defects=2 p0=0 p1=2 non_claim='does not claim MVP readiness'
```

Exit code `1` (documented blocked exit — expected: two truthful P1 blockers
remain; see `remaining-defects.md`). Defects:
`EXPECTED_SAFETY_BLOCK_UNCONFIRMED` for MLA-006 and MLA-007 only. All eight
Prompt 3 false-positive defects (4 × P1 `EXPECTED_SAFETY_BLOCK_ALLOWED` for
MLA-002..MLA-005, 4 × P2 `IMPORT_SUMMARY_INCOMPLETE`) no longer occur.
`blocked_unexpected_ready=false`, `all_expected_tasks_import_ready=true`,
`expected_safety_blocks_confirmed=false`.

- Determinism: a second run to a second scratch path produced byte-identical
  output (`cmp` clean). SHA-256 of the scratch output:
  `42655e05a20fea60fa4771a85042082f17469067de60b40510bdbb0d41a4b0f0`.
- Input integrity: sha256 of `accepted-import-summary.json` is
  `a54ebd46e8533b17738b302e6177b282348f811d7f6b694f75bea7ba2cf8285c` before and
  after this lane (file untouched).
- The scratch output was intentionally not added to the repository; formal
  re-interpretation belongs to the apply-retry lane once the remaining group is
  resolved.

## Repository-wide test status (for transparency)

```
python -m pytest -q
```

36 test modules fail at collection on a clean checkout in this environment
(missing optional third-party dependencies, e.g. `starlette`); reproduced
identically with the changes stashed. Excluding those 36 pre-broken modules, the
suite fails only in `tests/test_adapters_playwright_hardened.py` (4),
`tests/test_scenarios.py` (5), and `tests/test_tag_release.py` (1) — all
reproduced on a clean `origin/main` worktree (missing deps / sandboxed git
commit signing), i.e. pre-existing and unrelated to this change. Note: some of
these tests delete files under `artifacts/` as a side effect; those deletions
were restored with `git checkout -- artifacts/` and are not part of this lane's
diff.

## Required git checks (final state)

```
git status --short
 M alpha/self_operator/acceptance_interpretation.py
 M tests/fixtures/self_operator_acceptance_import/complete_import_summary.json
 M tests/test_self_operator_acceptance_interpretation.py
?? docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-acceptance-interpretation-blocker-fix/
?? tests/fixtures/self_operator_acceptance_import/importer_vocabulary_import_summary.json

git diff --name-only
alpha/self_operator/acceptance_interpretation.py
tests/fixtures/self_operator_acceptance_import/complete_import_summary.json
tests/test_self_operator_acceptance_interpretation.py

git diff --check
(clean — no whitespace or conflict-marker problems)
```

Changed-file scope matches the `tooling_false_positive` allowed scope exactly:
interpretation tooling, focused tests/fixtures, and this packet directory.
