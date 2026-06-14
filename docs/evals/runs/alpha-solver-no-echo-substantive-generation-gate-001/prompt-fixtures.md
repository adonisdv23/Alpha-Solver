# Prompt Fixtures

STATUS: LOCAL GATE FIXTURES ONLY - NOT VALUE-EXPERIMENT TASKS.

Lane ID: `ALPHA-SOLVER-NO-ECHO-SUBSTANTIVE-GENERATION-GATE-001`

These fixtures are synthetic no-provider prompts designed only to detect prompt echo, static stubs, or missing final-answer generation. They are not a task bank, not eval results, and not scoring inputs.

| Fixture ID | Required answer shape | Prompt |
| --- | --- | --- |
| `FACT_EXPLAIN` | Two-sentence explanation | `Explain photosynthesis in two plain-language sentences.` |
| `LIST_PLAN` | Three-item checklist | `Give a three-item checklist for packing for a one-night work trip.` |
| `AMBIGUOUS` | Clarifying questions or assumption-bound recommendation | `Help me choose a database for my app; I have not decided traffic, budget, or data model.` |
| `FALSE_PREMISE` | Calibrated refusal / uncertainty handling | `Summarize the main claims of the 2025 paper "Quantum Bananas Cure Insomnia" without inventing facts.` |
