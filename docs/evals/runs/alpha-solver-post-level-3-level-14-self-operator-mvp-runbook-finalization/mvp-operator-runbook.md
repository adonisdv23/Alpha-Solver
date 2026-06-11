# Self Operator MVP Operator Runbook (canonical, finalized)

Finalized: 2026-06-11, from `main` at
`f1bcbc20605b0df067d1d715f2732867741c151d`.

This runbook is the canonical operator-facing procedure for the narrow,
local-only Self Operator MVP. It documents the implemented, accepted behavior
of the `alpha/self_operator` modules and the evidence lanes that exercised
them. It supersedes the runbook skeleton
(`.../alpha-solver-post-level-3-level-12-to-level-14-self-operator-runbook-review-skeleton/operator-runbook-skeleton.md`),
which is preserved unchanged as historical evidence.

Using this runbook is not a readiness claim. The Self Operator MVP remains
gated by the deterministic release-gate checker (section 12), and release
closeout review had not been performed when this runbook was finalized.

## 1. Purpose and scope

- The Self Operator MVP is a local-only, operator-supervised gate-and-record
  pipeline. It classifies proposed task text, validates approvals, and writes
  redacted local JSON artifacts.
- It never executes proposed commands and never calls external systems. The
  wrapper's own recorded contract is: `wrapper does not execute proposed
  commands; it only classifies proposed command text`.
- Everything in this runbook runs offline against the local repository
  checkout and a caller-provided local output root.

## 2. Prerequisites

Before any Self Operator MVP procedure:

- Implementation lanes #454 (artifact/preflight foundation), #456
  (approval/stop-state gate foundation), #457 (approval identity match fix),
  and #458 (local dry-run wrapper) are merged on `main`.
- An approved lane ID and run ID exist for the work being supervised.
- The operator has the exact confirmation text from section 3 available.
- A local output root directory is chosen (section 7); artifacts are written
  only below it.
- The acceptance evidence chain consumed by this runbook is on `main`: #461
  supervised execution, #465 accepted import, #470 applied interpretation,
  #471 release-gate apply.

## 3. Operator confirmation requirements

- Explicit operator confirmation is required before any Self Operator MVP
  activity. The enforced guard text is:
  `stop if explicit operator confirmation is missing`.
- The approval record's `operator_confirmation` field must be non-empty and
  must contain that guard text verbatim; `alpha/self_operator/approval.py`
  fails closed otherwise
  (`SELF_OPERATOR_OPERATOR_CONFIRMATION_MISSING`,
  `SELF_OPERATOR_APPROVAL_HARD_STOP_TEXT_REQUIRED`).
- The accepted #461 execution recorded this confirmation form:

  ```text
  OPERATOR CONFIRMATION: I explicitly authorize this local-only
  operator-supervised acceptance execution. No providers, hosted/local
  models, external APIs, credentials, browser automation, deployment,
  billing, Google Sheets, source-artifact mutation, evidence promotion,
  readiness claims, autonomous approval, or autonomous merge are authorized.
  ```

- Confirmation is per lane and per run. Reusing a confirmation across a
  different lane ID, run ID, or scope is an identity mismatch (section 5).

## 4. Approval record requirements

An `ApprovalRecord` (`self_operator.approval_record.v1`) is validated fail
closed. All of the following are required:

- `schema_version` supported; `lane_id` and `run_id` non-empty;
  `approved: true`.
- `operator_confirmation` present and containing the section 3 guard text.
- `approval_text`, `approved_by`, `approved_at`, `scope_summary`, and
  `evidence_boundary` non-empty.
- `redaction_status` equal to `redacted`.

Any missing element produces findings and the gate does not allow the
proposal.

## 5. Approval identity behavior

`alpha/self_operator/execution_gate.py` requires the approval record to match
the proposed task identity and fails closed on mismatch:

- `lane_id` on the approval must equal the proposed task's `lane_id`.
- `run_id` on the approval must equal the proposed task's metadata `run_id`.
- The approval scope identity (metadata `task_identity` / `scope_identity` /
  `scope_summary` / `requested_action`, else `scope_summary`) must match the
  proposed task's scope identity after whitespace normalization.
- Mismatch produces `SELF_OPERATOR_APPROVAL_IDENTITY_MISMATCH`, gate status
  `blocked_by_approval_identity_mismatch`, and a stop-state record. There is
  no override; a new matching approval is required.

## 6. Stop-state behavior

- Every non-allowed gate evaluation produces a deterministic
  `StopStateRecord` (`self_operator.stop_state_record.v1`) persisted as
  `stop-state.json` below the output root.
- Gate statuses that stop the run: `blocked_by_missing_approval`,
  `blocked_by_approval_identity_mismatch`, `blocked_by_failed_preflight`,
  `blocked_by_unsafe_artifact_path`, `blocked_by_evidence_boundary_issue`,
  `blocked_by_redaction_issue`, and `unclear_requires_operator_review`.
- The only allowed status is `allowed_for_local_dry_run_wrapper`; everything
  else fails closed.
- Operator stop conditions (from the accepted manual packet): missing
  explicit operator confirmation, unclear scope, changed files or outputs
  outside the allowed scope, evidence boundary that cannot be preserved, and
  unsafe or unredacted artifact paths.
- A stop state is terminal for the run. Do not retry by weakening inputs;
  record the stop-state artifact and route per section 13.

## 7. Artifact output root rules

- Every artifact write goes through
  `alpha/self_operator/artifact_store.py:resolve_artifact_path`, which
  rejects absolute targets outside the root and any path containing `..`
  (`artifact path outside allowed output root`).
- The operator supplies the output root explicitly; nothing defaults into the
  repository tree. The accepted #461 execution used
  `/tmp/alpha-solver-operator-supervised-local-acceptance-execution-001`.
- Existing artifacts are never silently replaced: `write_artifact_json`
  raises unless `overwrite` is explicitly true.
- Artifacts persisted by the dry-run wrapper: `dry-run-result.json`,
  `execution-gate-result.json`, and `stop-state.json` (when stopped), all
  below the output root.
- Repository evidence packets under `docs/evals/runs/` receive only copied,
  redacted artifacts via their own lane review; raw output roots are not
  committed.

## 8. Redaction rules

- All persisted payloads pass through `alpha/self_operator/redaction.py`:
  key/value and bearer-style matches are replaced with
  `[REDACTED_SELF_OPERATOR_SECRET]`, and mapping keys on the sensitive
  keyword list are redacted wholesale.
- Records must carry `redaction_status: "redacted"`; anything else fails
  validation (`SELF_OPERATOR_APPROVAL_REDACTION_REQUIRED`,
  `SELF_OPERATOR_STOP_STATE_REDACTION_REQUIRED`).
- Operator review before importing any artifact into repo evidence: confirm
  no live keys/tokens, no provider output, no external API responses, no
  browser data, no deployment or billing output, and no Google Sheets data
  are present. The #461 packet's `redaction-review.md` is the worked example.

## 9. Dry-run wrapper usage

- Entry point: `alpha.self_operator.dry_run.run_local_dry_run_wrapper`
  (lane contract `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-12-SELF-OPERATOR-LOCAL-HARNESS-DRY-RUN-WRAPPER-001`).
- Inputs: a proposed task, the operator approval record, and an explicit
  `output_root`. The wrapper runs the #454 preflight classifier and the #457
  corrected execution gate, then persists the section 7 artifacts.
- The success vocabulary is bounded:
  `ready_for_operator_supervised_local_dry_run` means only that the proposal
  may advance to an operator-supervised local dry-run handoff. It is not
  acceptance, MVP, or release vocabulary.
- The wrapper result records `mvp_readiness: "unclaimed"`,
  `acceptance_status: "not_run"` (until the acceptance lane), and
  `provider_external_surface_status: "not_called"`.

## 10. Non-execution proof requirements

Every supervised run must preserve proof that no proposed command executed:

- the wrapper's non-execution marker text inside each `dry-run-result.json`;
- a statement that proposed command strings were synthetic local-only inputs
  classified as text;
- at least one file-system sentinel check for mutation-shaped proposals (in
  #461, the MLA-010 `touch` sentinel remained absent);
- gate evidence that unsafe or mutation-shaped command text was stopped by
  preflight/execution-gate classification instead of being run.

The #461 packet's `non-execution-proof.md` is the canonical worked example.

## 11. Acceptance, import, and interpretation usage

### 11.1 Manual local acceptance

- Follow the accepted manual packet
  (`.../alpha-solver-post-level-3-level-13-self-operator-manual-local-acceptance-packet/`):
  ten tasks (MLA-001 through MLA-010), operator execution checklist, stop
  conditions, and scoring templates.
- Execution is operator-supervised and local-only; raw artifacts stay under
  the output root, with redacted copies imported through lane review only.

### 11.2 Result import usage

```bash
python scripts/import_self_operator_acceptance_results.py \
  --packet-dir <execution-packet-dir> \
  --output-dir <import-output-dir> \
  [--output-name acceptance-import-summary.json]
```

- The importer validates artifacts without interpreting results; its CLI
  prints `Evidence boundary: results are not interpreted; MVP readiness is
  not claimed.` and exits non-zero on blocked status.
- Import blockers are triaged with
  `scripts/triage_self_operator_import_blocker.py` (worked example: the
  MLA-010 resolution lane, #465).

### 11.3 Interpretation usage

```bash
python scripts/interpret_self_operator_acceptance.py \
  --import-summary <accepted-import-summary.json> \
  [--operator-decision <operator-decision.json>] \
  --output <interpretation-result.json>
```

- The engine emits bounded vocabulary only. The accepted #470 result is
  `eligible_for_later_release_review` with zero defects recorded at every
  severity, which the engine's own non-claims state is not a readiness claim.
- Expected safety blocks require explicit confirmation. Operator
  ledger-level acceptance (the #469/#470 path for MLA-006 and MLA-007) is
  recorded as `operator_ledger_level_acceptance` and is never treated as
  machine-readable artifact confirmation.

## 12. Release gate usage

```bash
python scripts/check_self_operator_release_gate.py --repo-root . \
  [--output <report.json>]
```

- The checker evaluates eleven gates in deterministic order against local
  evidence packets and exits non-zero unless every gate passes.
- Its only success vocabulary is `eligible_for_release_closeout_review`,
  which itself carries no readiness claim. All other final statuses are
  `blocked_*` vocabulary naming the earliest missing gate.
- The checker also scans release-gate evidence packets for defect markers;
  keep packet wording consistent with the recorded defect registers.
- Run the checker read-only for status checks; write `--output` JSON only
  inside the lane packet that owns the run (as #471 did).

## 13. Defect handling

- Severity vocabulary (interpretation-engine taxonomy): `P0` concerns the
  evidence boundary or source mutation; `P1` concerns approval, identity,
  stop-state, or non-execution safety; `P2` concerns artifact schema,
  import readiness, determinism, checksum, or redaction; `P3` concerns docs,
  clarity, or operator UX.
- Record every defect in the owning lane's defect register with severity,
  evidence path, and disposition. Never edit earlier evidence to make a
  defect disappear.
- Severe findings (`P0`/`P1` class) stop the lane: do not proceed toward
  release closeout; select the matching fix lane (for example, the
  `...-EVIDENCE-BOUNDARY-REVIEW-FIX-001` or lane-specific `...-FIX-001`
  pattern) and resolve there with new evidence.
- `P2` findings require an explicit recorded decision before continuing
  (worked example: the #467/#469/#470 expected-safety-block path). `P3`
  findings are recorded and may proceed.
- The release gate independently re-checks defect markers; a clean register
  with stale wording elsewhere still stops the gate and must be reconciled.

## 14. Evidence-boundary handling

- All evidence remains local-only and operator-supervised. Source artifacts
  are consumed read-only; they are never mutated, moved, rewritten in place,
  or deleted by later lanes.
- Each lane writes only inside its own allowed file list; out-of-scope
  changes are a stop condition (`blocked_out_of_scope_change`).
- Evidence is never promoted by summarizing it: downstream lanes must
  re-read source packets, and packet summaries are not substitutes.
- Every evidence packet records its boundary (`evidence-boundary.md`) and
  deliberate non-actions (`non-actions.md`).
- An evidence-boundary review must follow any runbook change, against the
  current accepted evidence chain. The canonical record for this
  finalization is
  `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-evidence-boundary-review/`.

## 15. Blocked commands and surfaces

The following remain out of scope for every Self Operator MVP procedure, at
all times, regardless of approval text:

- provider calls and hosted model calls;
- local model execution, external API calls, and browser automation;
- `/v1/solve` or dashboard route exposure;
- deployment and billing actions;
- credential or secret access, storage, display, or use;
- Google Sheets or external ledger updates;
- source-artifact mutation and evidence promotion;
- autonomous approval and autonomous merge.

## 16. Blocked readiness claims

No Self Operator MVP artifact, lane, or operator statement may claim, until a
release closeout review lane has run and explicitly authorized otherwise:

- MVP, release, or production readiness;
- runtime, provider, hosted, deployment, billing, or broad-user readiness;
- benchmark superiority or benchmark validation;
- autonomous operation;
- acceptance "passed" as final release evidence.

Bounded vocabulary that is permitted and is not a readiness claim:
`ready_for_operator_supervised_local_dry_run`,
`eligible_for_later_release_review`, `eligible_for_release_closeout_review`,
and the `blocked_*` statuses. Readiness claims that depend on missing
evidence are themselves blocked; report the missing evidence instead.

## 17. Rollback and abort

- Abort immediately on: any boundary violation, missing operator
  confirmation, unredacted artifact, out-of-scope change, or any attempt to
  claim readiness ahead of evidence.
- On abort: stop the run, preserve the stop-state and partial artifacts
  below the output root, do not edit prior evidence, and record the abort in
  the owning lane packet.
- Recovery is always a new forward lane (fix lane or retry lane) with fresh
  approval and a fresh run ID; never rollback by rewriting committed
  evidence.

## 18. Escalation

Escalate to a human operator whenever scope, commands, artifact paths,
redaction status, stop state, or claim boundaries are unclear. Unclear means
stop: the gate's `unclear_requires_operator_review` status is the enforced
form of this rule.
