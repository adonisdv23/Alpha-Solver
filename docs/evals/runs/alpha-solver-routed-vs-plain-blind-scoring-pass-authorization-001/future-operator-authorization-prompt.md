# Future Operator Authorization Prompt

Copy only after this prep lane is merged:

> I authorize a new lane to perform blind scoring of the routed-vs-plain scorer-facing packet constructed by PR #619. Use only the approved scorer-facing packet and the scoring protocol. Preserve task IDs `RVP-001` through `RVP-012`. Score Response A and Response B independently on the frozen rubric dimensions. Record scores, preference, rationale, caveat, contested-score flag, scorer identifier or scorer method, and scoring timestamp only in that scoring lane. Do not unblind. Do not inspect or commit an A/B key or source identity map. Do not inspect source artifacts, source folders, route metadata, closed duplicate PR #618, or unblinding material. Do not interpret results or compute final aggregate interpretation. Lock scores before any later source identity review.

This prompt contains no live scoring results and does not authorize unblinding or interpretation.
