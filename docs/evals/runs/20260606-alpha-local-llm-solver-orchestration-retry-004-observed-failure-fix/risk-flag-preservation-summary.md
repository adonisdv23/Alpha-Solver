# Risk flag preservation summary

The risk-flag change is limited to benign local optimization ambiguity and missing-context labels.

Preserved behavior:

- high-risk prompt text blocks;
- serious risk flags block;
- non-allowlisted unknown or ambiguous flags block by default;
- composite flags containing high-risk tokens block;
- high-risk blocked outputs suppress unsafe considerations and assumptions.
