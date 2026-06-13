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
