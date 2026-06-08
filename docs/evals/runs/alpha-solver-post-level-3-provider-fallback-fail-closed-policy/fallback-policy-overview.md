# Fallback policy overview

Fallback means any automatic, semi-automatic, or operator-assisted movement from one provider path, model path, hosted path, local path, credential context, or routing decision to another after an attempted solve path is unavailable, blocked, timed out, rejected, budget-limited, circuit-open, unsafe, or otherwise not selected.

## Default stance

Provider fallback is default-forbidden unless a future authorized lane explicitly permits it. Absence of a prohibition is not permission. Ambiguous authorization is a blocked fallback state.

## Boundary principles

- Fallback must not be inferred from provider availability.
- Fallback must not be inferred from timeout, retry, or circuit-breaker design.
- Fallback must not be inferred from registry presence or capability metadata.
- Fallback must not be inferred from credentials being configured.
- Fallback must not be inferred from cost-control design.
- Fallback must not be inferred from provenance or observability design.
- Fallback must not be inferred from safety or claim-gate design.
- Fallback must not cross local-hosted boundaries unless a future authorized lane explicitly permits the exact transition and records explicit operator opt-in.

## Level 7 control

Level 7 controls whether and how this packet is used, revised, rejected, or superseded. This packet is a supporting reference only. It does not start Level 8.
