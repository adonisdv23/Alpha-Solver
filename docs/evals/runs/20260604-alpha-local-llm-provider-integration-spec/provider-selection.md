# Provider Selection

## Selected option

Exactly one future provider option is selected: an Ollama-style local HTTP
backend.

## Rationale

This shape is the narrowest common local endpoint option from the prior plan. It
can be constrained to localhost, bounded by mandatory timeouts, guarded by
explicit opt-in, skipped by default in tests, and covered first by offline
fixtures.

## Non-selected options

The OpenAI-compatible local endpoint option is not selected for this lane. The
direct subprocess wrapper option is not selected for this lane.

A later spec may revisit alternatives only by replacing this selection and
restating authorization, file-boundary, test, rollback, and evidence rules.
