# Artifact schema summary

Implemented `SelfOperatorArtifact`, `OperatorConfirmation`, `ArtifactFinding`, and `ValidationResult` as deterministic dataclass models.

Validation covers:

- unsupported schema version;
- missing lane ID;
- missing run ID;
- missing explicit operator confirmation;
- missing stop state when required;
- missing evidence boundary;
- malformed findings;
- artifact paths outside the caller-provided output root;
- unredacted secret markers when the artifact is not marked redacted.

Serialization uses stable key ordering and supports redacted output.
