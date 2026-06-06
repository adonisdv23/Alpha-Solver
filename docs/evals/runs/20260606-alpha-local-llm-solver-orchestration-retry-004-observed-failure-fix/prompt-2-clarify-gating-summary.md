# Prompt 2 clarify gating summary

Prompt: `Make it faster.`

The fix preserves the underspecified prompt clarification outcome when pass one classifies the request with bounded low-risk ambiguity or missing-context flags such as `benign ambiguity`, `missing context`, `unclear target`, `optimization`, or `performance`.

Serious risk terms remain blocked before clarification can proceed. The tests cover credential theft, bypass, exploit, exfiltration, and audit-log avoidance flags and confirm no pass-two call occurs and model fields are suppressed.
