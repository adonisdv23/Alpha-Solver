# Evidence Import Prerequisites

Before any future result import can happen:

1. Manual local acceptance packet merged and GS done.
2. Operator-supervised local acceptance actually executed.
3. Raw artifacts exist.
4. Artifact paths are local and inside the operator-provided output root.
5. Artifact checksums or integrity notes are recorded.
6. Redaction status is verified.
7. Lane ID and run ID match expected acceptance task IDs.
8. No source artifacts were mutated.
9. No evidence promotion occurred.
10. No readiness conclusion has been made before interpretation.

If any prerequisite is missing, stop import and record the blocker without interpreting results.
