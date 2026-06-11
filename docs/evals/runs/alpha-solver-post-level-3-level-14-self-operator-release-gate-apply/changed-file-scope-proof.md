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

- `alpha/self_operator/release_gate.py`: the defect scan distinguishes
  severity-vocabulary references from actual defect markers per line. Bare
  (non-backticked) P0/P1 markers keep the original scan behavior. A
  backtick-quoted severity token (`P0`/`P1`) is treated as a vocabulary
  reference unless the line is an actual defect-register entry: a markdown
  table row pairing the severity with a defect word, or a line with an
  explicit unresolved/open marker near the severity token. Inline code spans
  are not stripped globally, so real backticked defect markers (for example
  "- `P1`: unresolved approval failure" or "| `P0` | source mutation
  violation |") still block, while taxonomy-only definition lines do not.
  Resolved references (e.g. "No `P0` or `P1` defects remain open") stay
  allowed only when clearly marked resolved.
- `tests/test_self_operator_release_gate.py`: added focused regression tests:
  `test_backticked_severity_vocabulary_does_not_block`,
  `test_backticked_unresolved_p0_marker_blocks`,
  `test_backticked_unresolved_p1_marker_blocks`,
  `test_table_form_backticked_defect_rows_block`, and
  `test_resolved_backticked_references_allowed_only_when_marked_resolved`.
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
