# Opportunity Register

> Created by lane `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-13**. Each opportunity is classified by readiness:
> `DO_NOW` · `AFTER_SMOKE` · `AFTER_VALUE_PROTOCOL` · `LATER_HARDENING` ·
> `DO_NOT_DO_YET`. Classification reflects the current phase (pre-first-smoke,
> blocked on project/billing). Docs-only; nothing here authorizes a provider
> call or exposure.

| opportunity | class | rationale / status |
|-------------|-------|--------------------|
| Evidence ledger | **DO_NOW** | Delivered this lane: [`EVIDENCE_INDEX.md`](EVIDENCE_INDEX.md). |
| Lane registry | **DO_NOW** | Delivered this lane: [`LANE_REGISTRY.md`](LANE_REGISTRY.md). |
| Deferral register | **DO_NOW** | Delivered this lane: [`DEFERRAL_REGISTER.md`](DEFERRAL_REGISTER.md). |
| Archive index | **DO_NOW** | Delivered this lane: [`ARCHIVE_INDEX.md`](ARCHIVE_INDEX.md). |
| Current lane resolver | **DO_NOW** | Delivered this lane: [`CURRENT_STATE.md`](CURRENT_STATE.md) names the single controlling lane + next lane. |
| Claim-to-source matrix | **DO_NOW** (lightweight) | Partially delivered via packet `claim-boundary.md`; a full matrix mapping each public claim → committed evidence is a small follow-up. |
| Value experiment protocol | **AFTER_SMOKE** | `ALPHA-SOLVER-VALUE-EXPERIMENT-PROTOCOL-001` — highest strategic value; design after a real tiny smoke proves plumbing. See [`VALUE_EXPERIMENT_DIRECTION.md`](VALUE_EXPERIMENT_DIRECTION.md). |
| Synthetic eval corpus | **AFTER_SMOKE** | Needed to feed the value protocol with enough tasks to reduce noise; build alongside the protocol design. |
| Smoke-to-eval progression policy | **AFTER_SMOKE** | Define explicit gates from "tiny smoke (plumbing)" → "scored eval (value)" so smoke is never mistaken for value. |
| Security/privacy threat model | **AFTER_SMOKE** | Inputs captured now in [`DEF_002_SECURITY_PRIVACY_INPUTS.md`](DEF_002_SECURITY_PRIVACY_INPUTS.md); the full review is DEF-002 and must precede public exposure. |
| Evidence graph / lane DAG | **AFTER_SMOKE** | Lightweight DAG already in `LANE_REGISTRY.md`; a generated graph over all packets is a follow-up. |
| Prompt registry | **AFTER_VALUE_PROTOCOL** | Versioned prompt store becomes valuable once experiments scale and prompts need provenance. |
| Redaction gates | **LATER_HARDENING** | Harden `alpha/self_operator/redaction.py` (ISS-009 Unicode normalization) before public exposure; not needed for synthetic smoke. |
| Reproducible artifact manifests | **LATER_HARDENING** | Add hashes/manifests to packets for stronger provenance; valuable but not blocking. |
| Operator cockpit / dashboard | **DO_NOT_DO_YET** | Dashboard exposure is explicitly out of scope; building a cockpit now is premature and risks implying readiness. |

## Reading

- **DO_NOW** items are largely delivered by this lane.
- The single most valuable *strategic* opportunity is the **value experiment
  protocol** (`AFTER_SMOKE`), because the core value question is still unresolved
  (see [`VALUE_EXPERIMENT_DIRECTION.md`](VALUE_EXPERIMENT_DIRECTION.md)).
- `DO_NOT_DO_YET` items are deferred specifically to avoid implying readiness
  the evidence does not support.

## Deferred Addendum — 2026-06-14

These ideas were independently reviewed but are **not** folded into active lanes now.
Preserve them as later candidates, not current execution. No executable prompts are
provided for these items by design.

### Later Candidates

Add later only if the value-read signal supports them:

| candidate | deferred activation condition |
|-----------|-------------------------------|
| Decision Provenance Ledger | Convert evidence packets into a buyer-facing decision trail only after value-read signal supports buyer-facing governance demand. |
| Stop Engine | Add a pre-generation answerability verdict before any model answer only after value-read or near-term failure evidence supports it. |
| Discrimination Task Bank Asset | Build a reusable false-premise, hidden-constraint, should-stop task bank only after it materially improves value reads or operator decisions. |
| Prompt-Contract Simulation Methodology | Package as a reusable kit only if the current value-read method proves useful. |
| Overclaim Auditor | Use Alpha to audit external AI claims and readiness language only after value-read supports the lane. |
| Second-Opinion Widget | Critique AI answers for missing assumptions and unsupported claims only after value-read supports the lane. |
| OpenAI-Compatible Discrimination Pipe | Consider endpoint contract only after security and value proof. |
| Air-Gapped Local-First Governance | Treat as a business-strategy lane only after local smoke proves viability. |
| Local Model Refusal/Instruction Registry | Consider after local multi-model smoke. |
| Evidence-Bound Investor Proof Harness | Consider after value-read and MVP Scorecard. |
| Compliance-Pack Generator | Consider after Decision Provenance Ledger validates governance demand. |

### Reject for Now

- generic chat UI
- direct Pi integration
- broad RAG
- consensus-only model jury
- broad observability dashboard
- commercial launch material

### Activation Rule

Do not add a candidate as an execution lane unless it either follows a positive
value-read signal, prevents a concrete near-term failure, or materially improves
operator decision quality without weakening evidence boundaries.

### Explicitly Deferred or Forbidden Exposure/Claim Lanes

These remain deferred even after the expanded prompt set. Do not run them until
the required evidence gates pass.

| item | executor | status | reason |
|------|----------|--------|--------|
| Actual external exposure | none | deferred | Requires public exposure readiness gate to pass, DEF-002 closure, smoke evidence, operator approval, auth/rate-limit/tenant/CORS closure, cost controls, and incident-response minimums. |
| Production readiness claims | none | forbidden | No evidence supports production readiness. Do not create a prompt for this until value, runtime, security, provider, and exposure gates all pass. |
| Benchmark superiority claims | none | forbidden | Requires an executed value experiment or stronger benchmark protocol that passes predefined criteria. Protocol-only evidence is not enough. |
| Deleting evidence packets | none | forbidden | Evidence packets should be archived, indexed, or superseded, not deleted. Deletion would damage traceability. |
| Broad runtime architecture rewrite | none | deferred | Runtime entrypoint map may recommend future consolidation, but no broad rewrite should start before value proof and specific low-risk consolidation lanes exist. |
| Large broad eval run | none | deferred | Use smoke, no-echo gate, preregistration, and value pilot first. Do not run large evals until protocol preconditions are satisfied. |
| Commercial launch | none | deferred | Needs value proof, security closure, product UX, support plan, legal/privacy review, and pricing/billing model. |
