# Redaction boundary

Before any future provider call in `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001`:

- The prompt set must pass a redaction check.
- Prompts must contain only synthetic or sanitized content.
- Prompts must exclude secrets, credentials, private evidence, customer data, private business data, raw logs, private operator notes, and hidden instructions.
- Outputs must be reviewed before being committed.
- Any output containing sensitive or unexpected provider-returned material must not be committed unredacted.

This packet does not perform the redaction check for a final prompt set because no final prompt set is executed or sent in this lane.
