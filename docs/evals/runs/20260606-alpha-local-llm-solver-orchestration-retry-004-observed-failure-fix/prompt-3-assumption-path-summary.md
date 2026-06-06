# Prompt 3 assumption path summary

Prompt shape: draft a concise execution plan to improve a small Python CLI's startup time when only profiling later is available, and state assumptions.

The fix lets a pass-one `mode=clarify` result proceed to pass two as `answer_with_assumptions` only when the existing deterministic assumption gate passes:

- confidence is parsed and at or above threshold;
- considerations and assumptions are non-empty and bounded;
- missing information is bounded;
- risk flags are safe and allowlisted;
- no high-risk text is present;
- no forbidden boundary claim is present.

Low or unparseable confidence remains a clarify path with no pass-two call.
