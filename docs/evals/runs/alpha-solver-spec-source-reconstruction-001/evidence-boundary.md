# Evidence Boundary

Included evidence:

- Committed implementation files listed in each contaminated spec's `## Code Targets`.
- Committed test files listed in each contaminated spec's `## Code Targets`.
- Existing audit and reconciliation documents.

Excluded evidence:

- Memory or inferred original intent.
- Provider calls, live tokens, external services, or runtime executions beyond local checks.
- The contaminated MCP-005 copied body, except as contamination history.

Allowed verdict emitted by this packet: `SPEC_SOURCE_RECONSTRUCTION_CAPTURED`.
