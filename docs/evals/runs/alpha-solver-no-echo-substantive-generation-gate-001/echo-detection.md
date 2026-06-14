# Echo Detection

STATUS: FAILED NO-ECHO GATE.

Lane ID: `ALPHA-SOLVER-NO-ECHO-SUBSTANTIVE-GENERATION-GATE-001`

## Detection rule

For each fixture, compare the user-visible final answer fields against the prompt:

- Exact prompt echo if normalized `solution` equals normalized prompt.
- Exact prompt echo if normalized `final_answer` equals normalized prompt.
- Static stub if materially identical output appears across unrelated fixture shapes.
- Missing final-answer generation if the route returns routing/scaffold text rather than a task-shaped answer.

Normalization used for this packet was direct string equality after reading the `repr(...)` values printed by the local gate command; no semantic scoring or provider judge was used.

## Findings

| Fixture ID | `solution` equals prompt | `final_answer` equals prompt | Finding |
| --- | --- | --- | --- |
| `FACT_EXPLAIN` | YES | YES | Echo; no two-sentence explanation generated. |
| `LIST_PLAN` | YES | YES | Echo; no checklist generated. |
| `AMBIGUOUS` | YES | YES | Echo; no clarifying questions or recommendation generated. |
| `FALSE_PREMISE` | YES | YES | Echo; no calibrated uncertainty/refusal generated. |

## Verdict

`BLOCKED_ALPHA_PATH_ECHOES_PROMPT`
