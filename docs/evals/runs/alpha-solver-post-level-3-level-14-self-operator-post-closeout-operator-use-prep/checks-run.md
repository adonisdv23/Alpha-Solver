# Checks run

Exact checks run by this lane on 2026-06-11, from the repo root on branch
`claude/zealous-ramanujan-bfbuti` (created from `main` at
`12f7503afe3ab58bb027ef42d5a4e888d4896ffa`).

## Repository state checks

```bash
git status --short
git diff --name-only
git diff --check
```

Result: changed files are exactly the files of this packet directory; no
whitespace errors; no file outside the allowed file list
(`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-post-closeout-operator-use-prep/`).

## Packet consistency check

```bash
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-post-closeout-operator-use-prep
```

Result: passed.

## Read-only release-gate re-check (prerequisite verification)

```bash
python scripts/check_self_operator_release_gate.py --repo-root . --output /tmp/live-gate-check.json
```

Result: exit 0; all eleven gates `pass`;
`release_closeout_review_complete: pass`; final status
`eligible_for_release_closeout_review`. The JSON output stayed outside the
repository; no committed file was written by the checker.

## Deterministic forbidden-claim scan

```bash
rg -n "production ready|runtime ready|provider ready|hosted ready|benchmark superior|benchmark validated|autonomous ready|autonomous|MVP ready|release ready|broad user ready|/v1/solve|deployment|billing|credential|secret|provider call|hosted model" docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-post-closeout-operator-use-prep
```

Every hit was reviewed and classified into exactly one of
`allowed_boundary_reference`, `forbidden_claim`, or
`irrelevant_false_positive`.

### Classification

Final-state scan over this packet: 32 hit lines in 8 files; the other 12
packet files produced zero hits. Every hit line was read in place and
classified.

| File | Hit lines | Classification | Reason |
| --- | --- | --- | --- |
| `operator-use-contract.md` | 11 | `allowed_boundary_reference` | The explicit not-claims list; every phrase appears only as quoted forbidden vocabulary under a negation. |
| `redaction-and-secrets.md` | 5 | `allowed_boundary_reference` | Title, marker text, and pre-import review items stating what must be absent. |
| `forbidden-actions.md` | 4 | `allowed_boundary_reference` | Surfaces named only in order to forbid them. |
| `non-actions.md` | 4 | `allowed_boundary_reference` | Deliberate did-not statements. |
| `operator-confirmation-requirements.md` | 3 | `allowed_boundary_reference` | Quoted #461 confirmation text that de-authorizes the listed surfaces. |
| `first-use-checklist.md` | 2 | `allowed_boundary_reference` | Checklist items confirming required absences before a future run. |
| `checks-run.md` | 2 | `allowed_boundary_reference` | The quoted scan command itself and this table's file-name column. |
| `README.md` | 1 | `allowed_boundary_reference` | The packet-contents table cites the redaction file by name. |

Totals: `allowed_boundary_reference`: 32; `forbidden_claim`: 0;
`irrelevant_false_positive`: 0. No phrase appears as an affirmative project
status claim anywhere in this packet.

### Decision

`pass` — zero `forbidden_claim` classifications remain; this lane is not
blocked.
