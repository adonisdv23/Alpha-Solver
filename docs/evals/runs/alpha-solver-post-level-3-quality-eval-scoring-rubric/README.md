# Quality Evaluation Scoring Rubric Packet

Lane:
`ALPHA-SOLVER-POST-LEVEL-3-QUALITY-EVAL-SCORING-RUBRIC-PACKET-001`

## Purpose

This docs-only packet defines a supporting scoring-rubric reference for future Alpha Solver quality evaluation design. It records proposed scoring dimensions, scale definitions, reviewer rules, disagreement handling, invalid-result rules, and claim-boundary limits for later use by an explicitly approved quality evaluation lane.

This rubric is a supporting reference only. It does not start scoring, does not score real outputs, and does not run benchmarks. Level 5 controls whether and how this rubric is used.

## Included files

- `source-evidence-reviewed.md` records the bounded source evidence reviewed for this docs-only packet.
- `scoring-dimensions.md` defines scoring dimensions such as instruction preservation, evidence-boundary safety, source-grounding, claim discipline, lane-continuity correctness, artifact completeness, failure-mode recognition, actionable next step quality, and unsupported-claim avoidance.
- `scale-definitions.md` defines the common score scale for future reviewers.
- `reviewer-rules.md` defines reviewer conduct rules.
- `disagreement-handling.md` defines future disagreement handling.
- `invalid-result-rules.md` defines conditions that make a result invalid rather than merely low-scoring.
- `claim-boundary-limits.md` defines claim limits and forbidden interpretations.
- `non-actions.md` records actions intentionally not performed.
- `selected-next-action.md` records the required no-further-lanes decision.
- `blocker-fallback-lane.md` records the fallback lane if this packet is incomplete or unsafe.
- `checks-run.md` records static checks run for this packet.

## Decision boundary

This packet does not claim quality, score quality, establish a benchmark, promote evidence, or authorize product-surface work. It is a design reference that future Level 5 quality evaluation work may accept, revise, reject, or supersede.

## Selected next action

`NO_FURTHER_QUALITY_EVAL_SCORING_RUBRIC_LANES_SELECTED`

## Blocker fallback lane

`ALPHA-SOLVER-POST-LEVEL-3-QUALITY-EVAL-SCORING-RUBRIC-FIX-001`

## Evidence boundary

This docs-only scoring-rubric design does not score outputs, run benchmarks, run models, call providers, claim quality, claim superiority, expose `/v1/solve`, expose dashboards, add fallback, perform billing work, or promote evidence.
