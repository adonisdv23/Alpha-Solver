# Test-Set Design

## Future test-set requirement

A future frozen validation packet must define a stable prompt/test-case set before any execution lane is selected.

## Required future test-case fields

Each future test case must include:

- stable prompt/test-case ID;
- prompt text or prompt-file path;
- intended orchestration mode stressor, such as direct answer, clarification, answer with assumptions, or blocked response;
- allowed status expectations without requiring a specific model-quality outcome;
- safety review notes;
- artifact capture path;
- redaction notes;
- evidence boundary statement.

## Candidate categories for freezing later

The future packet may include categories such as:

- straightforward solver orchestration prompt;
- underspecified prompt expected to test clarification handling;
- prompt requiring bounded assumptions;
- high-risk or unsafe prompt expected to test blocking/safety flag handling;
- malformed or edge-case prompt expected to test artifact robustness.

## Prohibited test-set behavior now

This packet does not create live validation results, execute prompts, score outputs, benchmark models, compare models, or infer local model quality.
