# Blinding method

The scorer-facing packet preserves each task ID and task-family summary while presenting two anonymized answers as Answer A and Answer B. It excludes route metadata, source paths beside individual answers, model/provider/runtime/tool/source identities, PR numbers, and source identity labels from the scorer-facing packet.

Deterministic assignment was used because no prior committed assignment rule was found for this packet: odd task IDs assign Answer A to the plain source and Answer B to the routed source; even task IDs assign Answer A to the routed source and Answer B to the plain source. This assignment rule is recorded only in `blind-assignment-map-private-placeholder.md`, which is not scorer-facing.
