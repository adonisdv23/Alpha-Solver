# Evaluation Methodology Design

## Methodology goal

A future quality evaluation lane should measure whether Alpha Solver produces useful, bounded, reproducible solver outputs for defined task families under controlled conditions. The methodology must separate design, execution, review, and interpretation so that no single packet both invents criteria and overclaims results.

## Required future evaluation phases

1. **Authorization phase**: confirm an approved execution lane, source task set, model/provider boundary, evaluator roster, artifact storage path, and claim boundary before any output generation.
2. **Task finalization phase**: freeze prompts, task metadata, category labels, expected evaluation dimensions, and contamination controls before model outputs are generated.
3. **Execution phase**: run only the authorized systems under the authorized environment and record exact commands, versions, inputs, outputs, timestamps, and failures.
4. **Review phase**: score outputs against the frozen rubric with reviewer independence, disagreement handling, defect logging, and no retroactive rubric edits.
5. **Interpretation phase**: summarize results only within the accepted claim boundary, including limitations, invalidated tasks, missing evidence, and stop-condition outcomes.
6. **Closeout phase**: select the next lane or blocker fallback and preserve all artifacts required for reproducibility.

## Design constraints

A future methodology must be:

- **bounded**: each result maps to an explicit task family, environment, model/provider, prompt set, and scoring rubric;
- **reproducible**: a later reviewer can identify exactly what was run and what was scored;
- **auditable**: raw outputs, score sheets, reviewer notes, and defect logs are preserved;
- **non-promotional**: results do not imply Alpha superiority, MVP readiness, production readiness, or product readiness unless a later lane is explicitly designed and accepted for that claim;
- **stop-aware**: missing, stale, contradictory, overbroad, or non-reproducible evidence stops interpretation rather than being smoothed over.

## Why this packet does not run benchmarks or outputs

This packet is the design prerequisite for evaluation execution. Running benchmarks, generating model outputs, or scoring answers here would mix methodology design with execution, bypass task-set freezing, and risk creating unsupported quality evidence before the review workflow and claim boundaries are accepted.
