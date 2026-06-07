# Blocker Fallback Lane

If this packet is incomplete, inconsistent, unsafe, stale, overbroad, contradictory, or unable to preserve the accepted evidence boundary, use this blocker fallback lane:

`ALPHA-SOLVER-POST-LEVEL-3-QUALITY-EVAL-TASK-TAXONOMY-FIX-001`

## Fallback triggers

Use the fallback lane if:

- the taxonomy appears to start quality evaluation execution;
- a frozen task set is created;
- output scoring, benchmark execution, provider calls, local model inference, Ollama runs, dashboard exposure, `/v1/solve` exposure, fallback work, or billing work is required;
- Level 5 control over taxonomy use is missing;
- selected-next state is contradictory;
- required candidate families, inclusion criteria, exclusion criteria, risk labels, artifact expectations, non-actions, or checks are missing;
- preserved source artifacts, closed Level 2 packets, closed Level 3 packets, release-readiness ladder files, runtime files, provider files, CLI files, checker scripts, tests, Makefile targets, or CI files would need modification.
