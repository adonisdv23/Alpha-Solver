# Changed-file scope proof

## Allowed scope for this lane

- Packet directory:
  `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-gate-apply/`
- Code files, only because a release-gate tooling bug was proven:
  - `alpha/self_operator/release_gate.py`
  - `scripts/check_self_operator_release_gate.py`
  - `tests/test_self_operator_release_gate.py`

## Proven tooling bug

The `p0_p1_defects_absent` defect scan matched backtick-quoted
severity-vocabulary references (taxonomy and contract definition lines such as
"- `P0`: evidence boundary or source mutation violation") as if they were
unresolved defect markers. The authoritative defect registers record zero
defects, so the gate's first-run block contradicted the evidence it scans.
This masked the true earliest missing gate and prevented this lane from
producing a correct result.

## Fix applied

- `alpha/self_operator/release_gate.py`: the defect scan now strips markdown
  inline-code spans from each line before matching, so backtick-quoted
  severity vocabulary is treated as a reference, not a defect marker. Bare
  defect markers (e.g. "P0 defect: open source mutation violation") still
  block, as the existing tests assert.
- `tests/test_self_operator_release_gate.py`: added
  `test_backticked_severity_vocabulary_does_not_block` reproducing the exact
  false-positive lines and asserting the gate passes.
- `scripts/check_self_operator_release_gate.py`: unchanged.

## Changed files in this PR (complete list)

```
alpha/self_operator/release_gate.py
tests/test_self_operator_release_gate.py
docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-gate-apply/ (new packet, 12 files)
```

`git status --short`, `git diff --name-only`, and `git diff --check` outputs
are recorded in `checks-run.md`. Every changed file is inside the allowed
scope; no existing evidence packet, source artifact, or out-of-scope file was
modified.
