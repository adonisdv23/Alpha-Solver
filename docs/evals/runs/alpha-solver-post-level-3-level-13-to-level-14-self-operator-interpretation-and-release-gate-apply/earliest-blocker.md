# Earliest blocker

## Earliest blocker in this lane's pipeline

Interpretation of the accepted real import summary returned `blocked` before the
release-gate stage was reached. The earliest blocking defect in the engine's
ordered output is:

```
P1 EXPECTED_SAFETY_BLOCK_ALLOWED (MLA-002, blocked_unexpected_ready)
```

together with the rest of its defect group (MLA-003 through MLA-007) and four
unresolved P2 `IMPORT_SUMMARY_INCOMPLETE` defects.

## Root-cause framing

The earliest blocker sits at the importer-to-engine interface: the acceptance
interpretation engine (#464) does not parse the vocabulary actually emitted by the
acceptance result importer (#463/#465), although both label the interface
`self_operator.acceptance_import_summary.v1`. See `defect-register.md` for the
exact field-level mismatches. Whether the P1 defects reflect a real safety
regression or an interpretation-layer false positive is the blocker-fix lane's
determination to make.

## Release gate consequence

The release-gate checker (`scripts/check_self_operator_release_gate.py`) was not
run, because this lane's contract only permits running it when interpretation does
not return a blocker (no `blocked` implication and no P0/P1/unresolved P2
defects). Interpretation returned `blocked` with 6 unresolved P1 and 4 unresolved
P2 defects, so the gate's success path is unreachable in this lane and
`release-gate-report.md` / `release-gate-report.json` are intentionally not
produced. No earliest-missing-gate value exists for this lane because the gate did
not run; the runbook-finalization branch of the next-lane logic therefore does not
apply.
