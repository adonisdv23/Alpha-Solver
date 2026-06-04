# Operator Test Packet

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-001`

Status: packet prepared, test not yet executed.

## Objective

Give Adonis a controlled manual packet for testing whether the portable Alpha behavior contract remains answer-first, concise where appropriate, evidence-bounded, claim-bounded, and disciplined about stop conditions after the brevity/control refinement.

## Test surface

The test surface is the portable Alpha behavior contract only. It is not `/v1/solve`, runtime API testing, provider orchestration testing, Batch C, benchmark validation, production testing, or public user testing.

## Operator role

Adonis is the first operator unless a later approved packet names another operator. The operator should paste the provided prompts manually into the portable Alpha behavior-contract surface, capture the resulting answer, and record feedback without altering source evidence.

## Allowed tasks

- PR review gate
- Codex prompt generation
- lane-state recap
- claim-boundary review
- evidence-boundary review
- stop-condition detection
- concise reviewer comment
- low-headroom direct answer
- artifact-preservation checklist
- next-lane recommendation

## Forbidden tasks

- medical, legal, or financial advice as a formal expert
- live provider/API calls
- runtime `/v1/solve`
- Batch C
- production readiness
- public launch copy
- external user testing
- scoring or rescoring artifacts
- unblinding or map use
- raw-output interpretation

## Entry criteria

- PR #272 has been squashed, merged, and closed on `main`.
- This packet has merged.
- The operator has the packet files and understands that the test is manual, internal, and portable-surface only.
- The operator will not inspect raw outputs or operator-only maps.
- The operator will not use Google Sheets as proof.

## Exit criteria

- Each selected task has an operator feedback entry.
- Any observed defects are logged in the defect log format.
- The result-log table remains evidence-limited and is filled only after the operator actually runs the test.
- The operator records whether any stop condition was reached.
- The operator does not claim validation, readiness, benchmark success, runtime behavior, provider behavior, or superiority.

## Stop conditions summary

Stop the test if Alpha fabricates repo state, PR status, or file paths; claims runtime, `/v1/solve`, provider behavior, production readiness, or validation; reconstructs missing artifacts; uses raw outputs or operator maps when not authorized; repeatedly over-frames low-headroom tasks; gives multiple next lanes when exactly one was requested; starts Batch C or runtime work; produces output that cannot be safely interpreted; or leaves the operator unable to tell whether an answer is based on repo evidence or assumption.

## How to run the test manually

1. Confirm the entry criteria.
2. Open `operator-test-task-set.md`.
3. For each task, paste only the task's prompt into the portable Alpha behavior-contract surface.
4. Do not add hidden scores, Alpha/plain comparisons, raw outputs, operator maps, or Google Sheets content.
5. Save the response in the operator's local working notes or approved destination for the manual run.
6. Complete one feedback entry per task using `operator-feedback-form.md`.
7. Log defects using `operator-defect-log.md` when observed.
8. Stop immediately if any stop condition is triggered.

## How to record outputs

- Record the task ID, task family, date, operator name, and portable-surface context.
- Preserve enough response text to support feedback and defect review.
- Keep response evidence separate from source artifacts.
- Do not commit raw provider payloads, secrets, private data, or full unredacted traces.
- Do not fill the result-log template before the test is actually run.

## How to record defects

For each defect, record defect ID, task ID, severity, description, evidence snippet, likely cause, suggested refinement, and whether it should block future testing. Use the taxonomy in `operator-defect-log.md` and prefer concise snippets over full transcripts.

## How to avoid overclaiming

- Treat all findings as operator feedback only.
- State that the test is limited, manual, internal, and portable-surface only.
- Do not describe feedback as benchmark scores or validation.
- Do not infer `/v1/solve`, runtime API, provider, model routing, production, billing, self-healing, adaptive-learning, self-optimization, autonomous-optimization, or provider-orchestration behavior.
- Use `operator-test-claim-boundaries.md` for safe and forbidden language.
