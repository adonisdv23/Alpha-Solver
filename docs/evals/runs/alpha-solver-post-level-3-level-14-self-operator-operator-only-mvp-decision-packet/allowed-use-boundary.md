# Allowed-use boundary

This file defines the boundary of the accepted `OPERATOR_ONLY_LOCAL_MVP_CANDIDATE_ACCEPTED`
status. The boundary is intentionally narrow and must not be widened by compression or
restatement.

## What the accepted status allows

The accepted status allows no more than:

- Adonis-controlled evaluation and continued development of an operator-supervised local
  Self Operator candidate.

That is the entire allowed scope. Evaluation and development are performed by the
operator (Adonis), under the operator's supervision, on local artifacts, for the purpose
of continuing to build and assess the narrow Self Operator candidate.

## What the accepted status does not authorize

The accepted status does not authorize any of the following:

- public release
- production use
- hosted use
- provider claims
- runtime validation claims
- security/privacy completion claims
- benchmark validation claims
- benchmark superiority claims
- broad-user use
- autonomous operation
- `/v1/solve` exposure
- dashboard exposure

## Why the boundary stays narrow

The boundary stays narrow because the load-bearing evidence is still open:

- Self Operator execution evidence is missing (DEF-001). Until it exists, no claim about
  how the candidate behaves at runtime may be made, and the candidate may not be expanded
  beyond operator-supervised local use.
- Product-level security/privacy review is missing (DEF-002). Until it completes, there
  may be no exposure beyond the operator-supervised self-operator context.
- The prior targeted Fable delta audit full text is operator-held or missing from
  repository evidence (DEF-003). It may be cited only as a summarized model/auditor
  judgment that reported no P0/P1 blockers, not as independent proof.

"MVP candidate" is a development label for operator-controlled work. It is not MVP
readiness, release readiness, production readiness, runtime readiness, provider
readiness, hosted readiness, benchmark validation, benchmark superiority, broad-user
readiness, autonomous readiness, or final approval, and it must never be compressed into
any of those.
