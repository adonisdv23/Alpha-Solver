# Boundary Guard Preservation

Boundary handling remains fail-closed for untrusted model fields.

Preserved checks:

- pass-one forbidden boundary terms fail closed before normal answer exposure;
- pass-two forbidden positive boundary claims fail closed before normal answer exposure;
- prompt echo and system echo remain unsafe output;
- blocked high-risk paths suppress model-produced answer, final answer, considerations, and assumptions;
- safe negative boundary disclaimers in pass two remain allowed by the existing sentence-scoped check.

The tests cover forbidden pass-one terms across considerations, assumptions, missing information, and risk flags, and cover pass-two forbidden claim suppression.
