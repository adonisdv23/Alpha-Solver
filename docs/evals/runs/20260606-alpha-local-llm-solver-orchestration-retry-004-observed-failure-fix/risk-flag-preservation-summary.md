# Risk flag preservation summary

The risk-flag change is limited to benign local optimization ambiguity and missing-context labels.

Preserved behavior:

- high-risk prompt text blocks;
- serious risk flags block;
- non-allowlisted unknown or ambiguous flags block by default;
- composite flags containing high-risk tokens block;
- high-risk blocked outputs suppress unsafe considerations and assumptions.

Narrowing note: the ambiguous exact label `information risk` is not allowlisted. Only explicitly low or benign variants such as `low information risk` may be treated as low risk, and focused tests keep that path on the Prompt 2 clarification outcome with no pass-two call.
