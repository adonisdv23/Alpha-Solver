# First supervised-use target

## Selected target

**Existing evidence packet consistency review**, operator-supervised and
local-only: a single supervised run in which the Self Operator
gate-and-record pipeline (preflight classification, approval validation,
execution gate, local dry-run wrapper) processes one docs-only proposed
task whose proposed command text is the deterministic read-only packet
consistency check over the existing Self Operator evidence chain, followed
by the operator personally running that same deterministic read-only check
and preserving the outputs below the output root.

Target type (from the allowed list): existing evidence packet consistency
review, with the gate-and-record portion doubling as a local-only dry-run
wrapper rehearsal that executes nothing.

## What the first use consists of

1. The operator drafts one `ProposedTask` whose `proposed_commands` contain
   only the read-only checker command text recorded in
   `execution-command-plan.md`. The wrapper classifies this text; it does
   not execute it (`alpha.self_operator.dry_run.run_local_dry_run_wrapper`).
2. The pipeline validates the approval record, evaluates preflight and the
   execution gate, and persists `dry-run-result.json`,
   `execution-gate-result.json`, and `stop-state.json` (if stopped) below
   the output root.
3. Separately and under direct supervision, the operator runs the
   deterministic read-only consistency checker
   (`scripts/check_local_llm_packet_consistency.py`) over the existing
   Self Operator packet directories, capturing stdout below the output
   root. This command reads repository docs and writes nothing inside the
   repository.

## Why this target

- It is docs-only / evidence-packet maintenance: the subject matter is the
  existing documentation evidence chain, and the only tool that runs is a
  deterministic, offline documentation checker that already runs in CI-style
  use today.
- It is local-only and low risk: no network access, no runtime behavior, no
  repository mutation, and the wrapper portion executes no proposed
  commands by construction.
- It exercises exactly the pipeline the prep packet's
  `allowed-use-scope.md` item 3 already scoped for a chartered first use,
  on the narrowest possible subject.
- Its success criteria are deterministic: gate status
  `allowed_for_local_dry_run_wrapper`, checker exit code 0, and artifacts
  present below the output root.

## Explicitly avoided surfaces

This target touches no provider, no hosted or local model, no external API,
no browser automation, no deployment surface, no billing surface, no
credential or secret, no `/v1/solve` route, and no dashboard. Those surfaces
are forbidden for the first use regardless of approval text (see
`use-scope.md`).

## Non-execution statement

This packet defines the target only. Nothing in this section was executed
by this lane; execution may occur only in the selected execution lane after
`operator-confirmation-required.md` is satisfied in full.
