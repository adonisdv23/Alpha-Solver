# Source Evidence Reviewed

## Scope

This file records the source material reviewed for this docs-only future runbook draft. It is not evidence that Self Operator exists, has been implemented, has been run, or is safe to run.

## Reviewed repo evidence

- Repo-level agent instructions in `AGENTS.md`, including source-of-truth, safety, validation, and narrow-scope workflow guidance.
- Existing packet patterns under `docs/evals/runs/`, especially docs-only operator packet structures that separate runbooks, evidence boundaries, selected-next decisions, fallback lanes, and checks.
- Local packet consistency checker behavior in `scripts/check_local_llm_packet_consistency.py`, used only as a static documentation consistency check for this packet path.

## Evidence not reviewed or not available

No Self Operator implementation source, runtime entrypoint, CLI, route, provider adapter, scheduler, permissions model, artifact schema, or deployment evidence was reviewed because this packet is explicitly a future-use draft.

## Drafting implication

Every operational instruction in this packet is conditional. A future operator may use it only after a separate implementation, authorization, evidence review, and safety gate prove that a Self Operator run path exists and is approved for the specific task.
