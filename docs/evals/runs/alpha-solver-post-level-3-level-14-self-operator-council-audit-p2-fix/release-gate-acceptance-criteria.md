# Release-gate acceptance criteria (P2-003)

These criteria define the future bounded release-gate review lane `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-COUNCIL-RELEASE-GATE-REVIEW-001`. They exist so the gate has stated checks instead of open-ended authorization. The gate lane is a read-and-review lane: it reviews evidence against these criteria and records a pass/fail/blocked outcome. It does not deploy, expose, execute, or claim readiness.

## What the gate lane checks

1. That every required input listed below exists and is current.
2. That each P2 item from the Council synthesis is resolved with evidence or carries an operator-accepted deferral.
3. That the D-1 through D-5 caveats, read in source form, remain non-blocking for the package scope below.
4. That no forbidden claim appears in any gate-lane input or output.
5. That repo state at gate time is re-verified read-only and matches the state the evidence describes.

## Self Operator package scope under review

The package under gate review is the narrow, local-only, operator-supervised Self Operator candidate as recorded in this repository: the `alpha/self_operator/` implementation, its tests, and the post-level-7 design and control packets (scope matrix, approval controls, lifecycle state machine, runbook draft, failure-mode risk register) under `docs/evals/runs/`. Anything beyond operator-supervised local use — hosted operation, provider integration at scale, broad users, autonomous operation — is outside the package scope and outside the gate.

## Required inputs

- This P2 hardening packet, accepted by manual operator review.
- The Council synthesis summary (`council-synthesis-summary.md`) and, on request, the operator-held raw capture file and `ALPHA-SOLVER-COUNCIL-SYNTHESIS-REPORT-001`.
- D-1 through D-5 source text (`p2-001-d1-d5-caveat-source-text.md` and its cited sources).
- #492 / F-1 correction primary evidence (`p2-002-f1-correction-primary-evidence.md`).
- The deferral register (`deferral-register.md`) with operator sign-off recorded for each open deferral.
- A fresh read-only repo-state verification performed at gate time (tip SHA, lineage from `448cf34`, open PR state, presence of this packet), recorded as a gate-lane artifact.

## Minimum evidence requirements

- Every load-bearing claim in gate inputs must carry a source-type label (source artifact, derivative packet, model/auditor judgment, operator assertion, missing evidence, inference, or platform-failure capture note).
- Operator assertions and model/auditor judgments are not proof; where the gate relies on them, the reliance must be stated.
- Council agreement over a single shared packet counts as one source, not as independent corroboration.

## Pass conditions

The gate records pass only if all of the following hold:

- All required inputs present and current; repo-state re-verification matches.
- No P0/P1 finding is open from any source.
- Every P2 item is resolved with evidence or carries a recorded, operator-accepted deferral whose unblock condition does not bind the gate's own scope.
- DEF-001 (execution evidence) and DEF-002 (security/privacy review) remain acceptable only for outcomes that keep the package within operator-supervised local use; any outcome expanding operation or exposure beyond that fails the gate until those deferrals are met with evidence.
- No forbidden claim appears in gate inputs or the gate record.

## Fail or blocked conditions

- Any required input missing or stale: blocked, route to `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-COUNCIL-AUDIT-P2-FIX-BLOCKER-001`.
- Repo-state re-verification contradicts the evidence: blocked, stop and report.
- A surfaced caveat or new finding presents a plausible P0/P1: fail, escalate to a blocker lane; do not absorb it into a deferral.
- Any forbidden claim in inputs or outputs: fail until corrected.

## Out-of-scope claims and standing forbidden claims

The gate outcome, including a pass, must never be stated as or compressed into: MVP readiness, release readiness, production readiness, runtime readiness, provider readiness, hosted readiness, benchmark validation, benchmark superiority, broad-user readiness, autonomous readiness, or final approval. A gate pass means exactly: the named inputs satisfied the named checks for the named narrow package scope on the named repo state.

## How the Council run must be cited

Always: "16 usable raw audit responses plus 1 documented failed platform slot." Never "17 Council responses" or "the full Council." The Venice - Auto slot is a documented platform failure with no inferred findings, and the Security / Privacy lens is correspondingly under-covered. The prior targeted Fable delta audit is cited only as "reported no P0/P1 blockers."

## What Council consensus does and does not prove

Council consensus proves that no seat found a blocker in the shared evidence packet and that the seats converged on the P2 item set. It does not prove repository state, runtime behavior, provider behavior, product value, security posture, or readiness of any kind, because all seats consumed one shared packet and their agreement on its assertions is replication of that packet, not independent corroboration.
