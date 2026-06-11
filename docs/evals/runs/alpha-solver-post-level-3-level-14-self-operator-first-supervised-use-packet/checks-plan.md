# Checks plan

## Required checks for the execution lane

Before that lane's PR is opened, the execution lane must run, from the repo
root:

```bash
git status --short
git diff --name-only
git diff --check
python scripts/check_local_llm_packet_consistency.py <its own packet directory>
```

plus the deterministic forbidden-claim scan over its own packet directory
(same pattern as below), with every hit reviewed and classified into
exactly one of `allowed_boundary_reference`, `forbidden_claim`, or
`irrelevant_false_positive`. Any remaining `forbidden_claim` blocks that
lane. The execution lane must also verify: changed files are exactly its
own packet directory, the success criteria in `expected-artifacts.md` were
met (or a stop was recorded instead), and the redaction review in
`redaction-rules.md` passed for every imported artifact.

## Checks run by this packet lane

Run on 2026-06-11 from the repo root on branch
`claude/first-supervised-use-packet-eopfop` (created from `main` at
`d12c56e8364854ff823e1edfa7ec08ab54a5032a`):

```bash
git status --short
git diff --name-only
git diff --check
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet
```

Result: changed files are exactly the files of this packet directory; no
whitespace errors; no file outside the allowed file list; consistency check
passed.

### Amendment re-run (2026-06-11)

The same four checks plus the forbidden-claim scan were re-run on branch
`claude/self-operator-first-use-packet-46veay` (created from `main` at
`f1197e4`, #478 merged) after amending `operator-confirmation-required.md`
to carry the mandatory `OPERATOR_APPROVED_FIRST_USE_TARGET:` and
`OPERATOR_CONFIRMATION:` labeled fields, the local-models clause, and the
explicit no-final-status-CLI-implementation statement. Changed files were
exactly `operator-confirmation-required.md` and this file; all checks
passed. The classification table and totals below reflect the post-
amendment final state.

## Deterministic forbidden-claim scan (this lane)

```bash
rg -n "production ready|runtime ready|provider ready|hosted ready|benchmark superior|benchmark validated|autonomous ready|autonomous|MVP ready|release ready|broad user ready|/v1/solve|deployment|billing|credential|secret|provider call|hosted model" docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet
```

Every hit was reviewed in place and classified.

### Classification

Final-state scan over this packet: 32 hit lines in 10 files; the other 7
packet files produced zero hits. Every hit line was read in place and
classified.

| File | Hit lines | Classification | Reason |
| --- | --- | --- | --- |
| `use-scope.md` | 9 | `allowed_boundary_reference` | The forbidden-surfaces list; every phrase appears only in order to forbid it. |
| `redaction-rules.md` | 4 | `allowed_boundary_reference` | A cited prep-packet file name, pre-import review items stating what must be absent, and the conformance statement that none of these values appear. |
| `operator-confirmation-required.md` | 5 | `allowed_boundary_reference` | Quoted confirmation text that de-authorizes the listed surfaces. |
| `input-artifacts.md` | 3 | `allowed_boundary_reference` | Explicit input exclusions naming values that must be absent. |
| `evidence-boundary.md` | 3 | `allowed_boundary_reference` | Boundary statements of what this packet does not claim or touch. |
| `use-target.md` | 2 | `allowed_boundary_reference` | Avoided-surfaces statement. |
| `non-actions.md` | 2 | `allowed_boundary_reference` | Deliberate did-not statements. |
| `abort-conditions.md` | 2 | `allowed_boundary_reference` | Abort triggers naming values that must be absent from inputs. |
| `source-evidence-reviewed.md` | 1 | `allowed_boundary_reference` | A cited prep-packet file name in the sources table. |
| `checks-plan.md` | 1 | `allowed_boundary_reference` | The quoted scan command itself. |

Totals: `allowed_boundary_reference`: 32; `forbidden_claim`: 0;
`irrelevant_false_positive`: 0. No phrase appears as an affirmative project
status claim anywhere in this packet.

### Decision

`pass` — zero `forbidden_claim` classifications remain; this lane is not
blocked.

### Command-plan repair re-run (2026-06-11)

Lane
`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-REPAIR-AND-EXECUTION-001`
repaired `execution-command-plan.md` (local-only preconditions replacing the
remote-fetch step; environment-variable handoff of the output root into the
step 2 heredoc) and added pre-run abort condition 8 to
`abort-conditions.md`, on branch `claude/eloquent-tesla-pmct3n` created from
`main` at `e04d4cc` (#479 merged). Before any execution, the same four
checks above were re-run, the packet-scoped consistency check passed, and a
focused unsafe-pattern scan plus the forbidden-claim scan were run over this
packet with every hit reviewed and classified; zero `forbidden_claim` and
zero `unsafe_executable_plan_pattern` classifications remain. The repaired
step 2 heredoc is classified `safe_quoted_heredoc_environment_root`. The
full classification, the before/after plans, and the pre-execution repair
verification are recorded in
`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet-repair/`.
The repair edits introduce no new hits for the scan pattern quoted above,
so the classification table and totals above remain the final state for
this packet.
