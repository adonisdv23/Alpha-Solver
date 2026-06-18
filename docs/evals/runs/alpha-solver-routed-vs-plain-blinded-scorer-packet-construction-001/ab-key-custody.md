# A/B key custody

The A/B identity key is operator-held and is not committed to the repository.

Scorers must not request, reconstruct, or use the key during blind scoring. Repository materials must not include the source identity assignment, deterministic assignment rules, source folder identity, source paths for scorer-facing cases, or any source-arm mapping.

Any future unblinding requires a separate authorized lane after scoring is complete and locked.
