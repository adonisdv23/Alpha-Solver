# Checks run

## Prerequisite verification

```
git fetch origin main
git log origin/main --oneline -8
git ls-tree origin/main --name-only docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/
```

Outcome: `origin/main` HEAD is `752f271` (#465);
`accepted-import-summary.json` is present on current main. Prerequisite satisfied
— this lane proceeds against main and is not stacked on an unmerged branch.

## Input integrity

```
sha256sum docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json
```

Outcome: `a54ebd46e8533b17738b302e6177b282348f811d7f6b694f75bea7ba2cf8285c`. The
file was read-only input and is unmodified (absent from `git status`/`git diff`).

## Interpretation (always-run check)

```
python scripts/interpret_self_operator_acceptance.py \
  --import-summary docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json \
  --output docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-interpretation-and-release-gate-apply/interpretation-result.json
```

Outcome: exit `1` (documented blocked exit code); stdout
`interpretation=blocked tasks=10 defects=10 p0=0 p1=6 non_claim='does not claim MVP readiness'`.

Determinism check: a second run with the same input to a scratch path produced
byte-identical JSON (`diff -q` identical; SHA-256
`23b5cfd50a7590fcf1bcfbf99f79d025f355b94ffe500fddf1d9dd6b4d8e707e` for both). The
scratch copy was deleted.

## Release gate (conditional check)

Not run. The lane contract permits running
`python scripts/check_self_operator_release_gate.py --repo-root . --output .../release-gate-report.json`
only if interpretation does not return a blocker. Interpretation returned
`blocked` with 6 unresolved P1 and 4 unresolved P2 defects, so the gate was
skipped and no gate report exists for this lane.

## Scope checks (always-run)

```
git status --short
git diff --name-only
git diff --check
```

Outcomes: only the new packet directory is present (untracked); no tracked file
changed; `git diff --check` clean (exit 0). See
`changed-file-scope-proof.md` for the captured outputs.

No pytest run was required: this lane changed no code and added docs only, per the
AGENTS.md validation guidance for docs-only changes the relevant check commands
above were run instead.
