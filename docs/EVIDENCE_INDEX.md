# Evidence Index — PRs #497–#509

> Created by lane `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-13**. Merge status verified read-only via GitHub
> (API `merged:true` for #497, #503, #505, #507, #508, #509; `base.sha` chain on
> `origin/main` for #499, #500, #501, #502, #504, #506). All packets are
> docs-only evidence. **Evidence value** states what each packet does and does
> **not** prove. Packet paths are under `docs/evals/runs/`.

## How to read "evidence value"

Every packet below is **plumbing / process / governance / boundary evidence**.
None is provider validation, value/quality proof, benchmark evidence, or
readiness evidence. The local-execution chain proves only offline determinism;
the OpenAI chain proves only planning/governance and that no provider call was
made.

## PR table

| PR | Title | Merged | Packet path (`docs/evals/runs/…`) | Verdict | Selected next lane | Evidence value | Non-claims | Status |
|----|-------|--------|-----------------------------------|---------|--------------------|----------------|-----------|--------|
| #497 | self-operator: local execution evidence | ✅ | `alpha-solver-post-level-3-level-14-self-operator-execution-evidence-001` | `LOCAL_EXECUTION_EVIDENCE_CAPTURED` (DEF-001 partial) | EXECUTION-EVIDENCE-002 | Offline Self Operator suite + release-gate run | No provider/runtime/benchmark/readiness | historical |
| #499 | self-operator: execution evidence 002 | ✅ | `…execution-evidence-002` | `PARTIAL_LOCAL_FLOW_CAPTURED_OPERATOR_INPUT_REQUIRED` | EXECUTION-EVIDENCE-003 | Partial local flow; needs real operator approval | No provider/runtime; not full DEF-001 | historical |
| #500 | self-operator: approved local execution evidence | ✅ | `…execution-evidence-003` | `APPROVAL_CAPTURED_EXECUTION_BLOCKED_BY_LOCAL_SAFETY_GATE` | EXECUTION-EVIDENCE-004 | Approval captured; safety gate blocked exec | No provider/runtime; gate working as designed | historical |
| #501 | self-operator: gate-compatible local execution evidence | ✅ | `…execution-evidence-004` | `APPROVAL_ACCEPTED_LOCAL_FLOW_CAPTURED` | DEF-002-DEF-003-EVIDENCE-BOUNDARY-001 | Local approved flow captured; DEF-001 advanced | No provider/runtime; DEF-002/003 still open | completed |
| #502 | eval: OpenAI free-token smoke & eval harness plan | ✅ | `alpha-solver-openai-free-token-eval-smoke-harness-plan-001` | `OPENAI_FREE_TOKEN_EVAL_SMOKE_HARNESS_PLAN_CAPTURED` | OPENAI-DATA-SHARING-OPERATOR-VERIFICATION-001 | Plan only; no call, no eval | No OpenAI/provider/eval validation | completed |
| #503 | self-operator: DEF-002 DEF-003 evidence boundary | ✅ | `alpha-solver-post-level-3-level-14-self-operator-def-002-def-003-evidence-boundary-001` | `DEF_002_DEF_003_EVIDENCE_BOUNDARY_CAPTURED` | LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001 | Records what closes DEF-002/003 | DEF-002 not resolved; DEF-003 not resolved | completed |
| #504 | openai: data-sharing operator verification | ✅ | `openai-data-sharing-operator-verification-001` | `OPENAI_DATA_SHARING_OPERATOR_VERIFICATION_PACKET_CAPTURED` | OPENAI-DATA-SHARING-OPERATOR-ATTESTATION-001 | Verification checklist (all `pending_operator_verification`) | No OpenAI validation; settings unverified | completed |
| #505 | openai: local token smoke capture 001 | ✅ | `local-openai-token-smoke-capture-001` | `BLOCKED_OPERATOR_ATTESTATION_PACKET_MISSING` | LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-001 | Self-blocked preflight; no call | No provider call; attestation missing | superseded (by #509 chain) |
| #506 | openai: synthetic smoke prompt fixture | ✅ | `openai-synthetic-smoke-prompt-fixture-001` | `OPENAI_SYNTHETIC_SMOKE_PROMPT_FIXTURE_CAPTURED` | WAIT_FOR_OPENAI_OPERATOR_PRE_SMOKE_ATTESTATION | Synthetic SMOKE-001 fixture; not sent | No call; synthetic data only | completed |
| #507 | openai: operator pre-smoke attestation | ✅ | `openai-data-sharing-operator-attestation-001` | `OPENAI_OPERATOR_PRE_SMOKE_ATTESTATION_CAPTURED` | LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001 | Operator go/no-go attestation (redacted) | No call; attestation ≠ project/billing proof | completed |
| #508 | openai: extend static checks to OpenAI packets | ✅ | `openai-packet-checker-scope-001` | `OPENAI_PACKET_CHECKER_SCOPE_EXTENDED` | LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-001 | Checker scope hardening (docs-only packet; checker code changed in same PR) | No provider/runtime; tooling only | completed |
| #509 | openai: local token smoke retry capture | ✅ | `local-openai-token-smoke-capture-retry-001` | `BLOCKED_OPENAI_PROJECT_OR_BILLING_NOT_VERIFIED` | OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001 | Retry halted before provider call | No call; key-presence ≠ project/billing readiness | **current-control** |

## Notes

- **#508 caveat**: the merged PR #508 changed `scripts/check_local_llm_*.py` and
  their tests *and* added a docs packet. From this docs-only lane we treat the
  packet as evidence and do **not** modify the checker code or tests.
- **#505 → #509**: PR #505 was the first blocked smoke attempt (missing
  attestation); after attestation (#507) and checker scope (#508), PR #509 was
  the blocked project/billing retry. #505 is therefore superseded as the active
  smoke attempt by the #509 retry chain, but preserved as evidence.
- No PR in this range claims OpenAI/provider validation, runtime/production/MVP
  readiness, security/privacy completion, benchmark validation/superiority, or
  DEF-002/DEF-003 resolution.

## Later merged PRs

None after #509 at verification time. Append rows here as new evidence merges.
