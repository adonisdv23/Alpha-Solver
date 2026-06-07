# Task Category Design

## Candidate categories

Future quality evaluation lanes may consider these candidate task categories, provided a later lane freezes the actual task set before execution:

1. **Structured problem solving**: tasks requiring decomposition, constraints tracking, and final answer synthesis.
2. **Tool-use planning without tool calls**: tasks requiring the model to propose safe local steps without actually invoking external tools.
3. **Evidence-bound reasoning**: tasks requiring answers to distinguish known evidence from unsupported claims.
4. **Error detection and correction**: tasks requiring identification of contradictions, missing prerequisites, or invalid assumptions.
5. **Operator workflow assistance**: tasks requiring clear procedural guidance under local-only constraints.
6. **Boundary-sensitive refusal or deferral**: tasks where the correct behavior is to defer, stop, or avoid a prohibited claim/action.
7. **Artifact interpretation**: tasks requiring summarization of provided artifacts without inventing evidence or promoting results.

## Non-frozen status

These categories are design candidates only. This packet does not freeze prompts, create a benchmark, select final tasks, determine sample size, run models, or score outputs.

## Future category requirements

A future execution packet must define for each category:

- category purpose;
- inclusion and exclusion criteria;
- minimum and maximum task counts;
- task source and authorship record;
- allowed context materials;
- expected difficulty range;
- contamination controls;
- known invalidation risks;
- scoring dimensions that apply to the category;
- category-specific pass/fail criteria.

## Category stop conditions

A candidate category must be deferred or removed if its tasks depend on unavailable evidence, require product surface behavior not yet designed, require live provider calls not authorized by the lane, require local model inference outside the lane boundary, or cannot be scored reproducibly.
