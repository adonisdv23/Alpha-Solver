# Residual Risks

- Fake fixtures may pass schema checks while real local models echo prompts or ignore role boundaries.
- Local model family assignment may create apparent diversity without independent reasoning behavior.
- Finalizer prompts may accidentally smooth over disagreement unless the disagreement matrix is mandatory.
- Evidence auditor behavior is fragile if artifacts are missing, malformed, or uncited.
- Safety reviewer outputs may conflict with router outputs; this must escalate instead of being majority-voted away.
- Operator-supplied model catalogs may be stale, unavailable, or inconsistent across machines.
- Local model transcripts may contain private data if operators ignore the preflight checklist.
- A later implementation could accidentally add hosted fallback unless local-only flags and tests explicitly forbid it.
