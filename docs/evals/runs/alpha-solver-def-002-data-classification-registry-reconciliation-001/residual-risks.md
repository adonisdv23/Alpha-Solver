# Residual risks

| ID | Risk | Status | Required follow-up |
| --- | --- | --- | --- |
| DCR-01 | Runtime still has two classification inputs with different actions. | Reconciled for precedence, not migrated. | Implement a dedicated migration lane to make runtime use the canonical registry or generate compatibility config from it. |
| DCR-02 | Replay and generic JSONL logging can persist caller-supplied event content without automatic classification or redaction. | Open. | Add capture-time classification/redaction or document approved event schemas. |
| DCR-03 | Registry shortlist snapshots include raw `query` text. | Open. | Decide whether shortlist snapshots require redaction, hashing, opt-in, or retention limits. |
| DCR-04 | Tool registry governance fields are mostly null and not enforcement-backed. | Open. | Populate audited values and wire enforcement only after policy approval. |
| DCR-05 | Public-exposure data-sharing/telemetry gate remains not ready. | Open. | Continue exposure-readiness gap closure; do not expose dashboard/API based on this packet. |
| DCR-06 | Pattern-based redaction can miss novel secrets. | Open residual candidate. | Expand tests/formats or require operator acceptance with compensating controls. |
| DCR-07 | Broad test execution can exercise provider paths when ambient provider environment variables or credentials are present. | Open validation risk; occurred once during this lane and is not provider-readiness evidence. | Add/require no-provider validation profiles for DEF/security lanes before running broad suites. |
