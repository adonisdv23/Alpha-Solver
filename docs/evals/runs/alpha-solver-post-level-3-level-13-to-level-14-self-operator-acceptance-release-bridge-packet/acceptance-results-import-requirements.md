# Acceptance results import requirements

A future results import lane must:

- preserve raw artifacts;
- preserve redacted artifacts;
- identify artifact hashes if available;
- record command/session metadata if available;
- distinguish raw execution evidence from interpreted evidence;
- do not alter source artifacts;
- do not promote evidence beyond the local-only acceptance boundary.

Imported evidence must remain clearly labeled as local-only acceptance evidence and must not be treated as production, hosted, provider, benchmark, or autonomous-operation evidence.
