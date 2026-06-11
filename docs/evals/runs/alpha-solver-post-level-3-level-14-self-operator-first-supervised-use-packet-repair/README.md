# Self Operator first supervised-use packet repair

- Lane ID:
  `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-REPAIR-AND-EXECUTION-001`
  (repair record portion of the combined repair-and-execution lane).
- Objective: repair two defects in the already-merged first supervised-use
  packet command plan
  (`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet/execution-command-plan.md`),
  prove the repair is safe, and only then allow the execution portion of the
  combined lane to proceed.
- Base evidence: current `main` at
  `e04d4cc59f6f2079dc1b9fdbaefd973a5ca83329` (#478 and #479 merged: the
  first supervised-use packet and its confirmation-fields amendment).
- This is a combined lane because the first-use packet is already merged,
  but its command plan contained defects that had to be repaired before
  execution.

**No execution occurred until after the command-plan repair and the
pre-execution verification in `repair-verification-before-execution.md`
passed.** The lane began with a read-only inspection of the repo, the
merged packet, the relevant `alpha/self_operator/` modules, and the checker
scripts before any edit.

## Defects repaired

1. The executable plan used a remote-fetch precondition that could contact
   the network, violating the plan's own local-only boundary.
2. The executable plan used a quoted heredoc while relying on
   `Path("$ROOT")`, so `$ROOT` would never expand and Python would treat it
   as a literal path (resolving to a `$ROOT` directory under the current
   working directory — an in-repo write).

See `defects-repaired.md`, `command-plan-before.md`, and
`command-plan-after.md`.

## Packet contents

| File | Purpose |
| --- | --- |
| `defects-repaired.md` | The two defects, their risk class, and the repairs. |
| `command-plan-before.md` | The merged, defective command plan, verbatim. |
| `command-plan-after.md` | The repaired command plan, verbatim. |
| `repair-verification-before-execution.md` | The required pre-execution repair checkpoint. |
| `checks-run.md` | Exact checks run by the repair portion of this lane. |
| `evidence-boundary.md` | What this repair record is and is not evidence of. |
| `non-actions.md` | Deliberate non-actions of the repair portion. |
| `selected-next-lane.md` | Selected next lane. |
| `blocker-fallback-lane.md` | Blocker-fix and fallback lanes. |

Files repaired in the merged first-use packet (the only files outside this
directory touched by the repair portion): `execution-command-plan.md`,
`abort-conditions.md` (new pre-run hard-stop condition 8), and
`checks-plan.md` (repair re-run record).
