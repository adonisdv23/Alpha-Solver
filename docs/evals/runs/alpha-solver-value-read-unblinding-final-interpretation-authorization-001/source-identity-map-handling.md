# Source-Identity Map Handling

This packet does not access, reveal, infer, create, or commit a source-identity map.

## Future custody requirements

A future pass may use a source-identity map only if an operator supplies or approves a custody method for that pass. The future pass must record:

- Who or what supplied the identity map.
- Where the identity map was reviewed, without committing private or disallowed material if custody rules prohibit it.
- Whether all case identities were complete and unambiguous.
- Whether any identity-map defect triggered a stop condition.

## Handling boundaries

The future pass must not infer identities from writing style, answer content, formatting, score patterns, file ordering, or raw outputs. If the approved identity map is missing, incomplete, ambiguous, or inconsistent with the locked score rows, the future pass must stop.

## Repository boundary

No identity map is committed by this lane. No source identities are revealed by this lane.
