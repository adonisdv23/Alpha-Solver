# Recommended next prompts

## AUDIT-001

- Priority: A
- Classification: `active_now`
- Recommended prompt: In the limited repeatability packet, add explicit first-use review step labels and require each evidence reference to cite the exact reviewed step number.

## AUDIT-002

- Priority: A
- Classification: `active_now`
- Recommended prompt: Update future prompt-bank packets to require concise reasoning plus evidence references for every material review conclusion.

## AUDIT-003

- Priority: A
- Classification: `active_now`
- Recommended prompt: For each generated script or test help check, add a file-exists precondition and record skipped_missing_file when the target is absent.

## AUDIT-004

- Priority: B
- Classification: `active_next`
- Recommended prompt: Replace broad importer/exporter wording with exact file, packet, checker, or documentation surface names in future prompts.

## AUDIT-005

- Priority: A
- Classification: `decision_recorded`
- Decision record: `../alpha-solver-post-level-3-level-14-self-operator-pre-council-audit-005-decision-and-bundle-routing-fix/audit-005-decision-record.md`
- Status update: the prior backlog triage status required an operator decision; the pre-Council decision lane now records that decision.
- Recommended prompt: Future combined tooling/docs or multi-blocker lanes, including `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-CHECKER-SCOPE-EXTENSION-001`, must quote and satisfy the recorded AUDIT-005 decision before proceeding.

## AUDIT-006

- Priority: A
- Classification: `active_now`
- Recommended prompt: Add a preflight checklist requiring all canonical runbook paths to be populated before a runbook prompt is executed.

## AUDIT-007

- Priority: A
- Classification: `active_now`
- Recommended prompt: Require guardrail test commands to include file-exists checks unless the same lane adds the target test file.

## AUDIT-008

- Priority: C
- Classification: `deferred`
- Recommended prompt: Record the final local status CLI as deferred until a separate implementation spec and approval exist.

## AUDIT-009

- Priority: C
- Classification: `deferred`
- Recommended prompt: When a final local status CLI is authorized, add tests proving absent prerequisites return missing_prerequisite and do not infer eligibility from incomplete evidence.

## AUDIT-010

- Priority: B
- Classification: `active_next`
- Recommended prompt: Add explicit non-integration guarantees to future repeatability and status prompts and require evidence-boundary files to restate them.

## AUDIT-011

- Priority: B
- Classification: `active_next`
- Recommended prompt: Require each future packet to include a no-readiness and no-evidence-promotion boundary section.

## AUDIT-012

- Priority: A
- Classification: `active_now`
- Recommended prompt: Add a live-state-first preflight to future review and prompt-generation lanes before drafting commands or findings.

## AUDIT-013

- Priority: A
- Classification: `active_now`
- Recommended prompt: For every reviewed command, record the generated step number, executed command evidence reference, and reviewer conclusion in the same row.

## AUDIT-014

- Priority: A
- Classification: `active_now`
- Recommended prompt: Before an execution lane starts, add a plan-verification checkpoint comparing the generated command plan against intended targets and allowed files.

## AUDIT-015

- Priority: A
- Classification: `active_now`
- Recommended prompt: Before every supervised execution lane, require target-match proof covering branch, commit, packet directory, allowed files, and lane ID.
