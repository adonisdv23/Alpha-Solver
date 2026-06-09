# Artifact validation contract

The importer validates each expected local artifact against these constraints:

1. The artifact path must resolve inside the execution packet.
2. Expected artifacts from `raw-artifacts-index.md` must be present unless the task explicitly expected no copied artifact.
3. JSON artifacts must parse to JSON objects.
4. SHA-256 checksums are generated for every present artifact.
5. Ledger checksums are compared when present.
6. Schema version, lane ID, and run ID are required when present in the artifact contract.
7. Ledger schema version, lane ID, and run ID must match parsed JSON values when both are present.
8. Dry-run artifacts must include a non-execution confirmation.
9. Evidence-boundary text must preserve local-only/no-execution markers.
10. Redaction status must remain `redacted` when present.
11. Source-artifact mutation markers block import for operator review.

This contract imports evidence only. It does not decide acceptance meaning or readiness.
