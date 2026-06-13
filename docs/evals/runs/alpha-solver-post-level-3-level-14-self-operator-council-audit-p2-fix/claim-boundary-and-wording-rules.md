# Claim-boundary and wording rules (DOC-001, DOC-002)

These rules apply to every document, PR description, ledger entry, and conversation artifact that describes the Council run, its synthesis, or any lane that follows. They exist to prevent status drift of the kind PR #492 had to correct.

## Required wording

- The Council run is always described as: **16 usable raw audit responses plus 1 documented failed platform slot.** Never "17 Council responses," never "the full Council."
- The prior targeted Fable delta audit is always cited as: **"reported no P0/P1 blockers."** Never "cleared" or "validated."
- The Venice - Auto slot is described as a documented platform failure with no inferred findings. It is never counted toward consensus or coverage.

## Compression bans (DOC-001)

- "Cleared the Council bundle **for manual Council review**" must never be shortened to "cleared." The qualifying phrase is load-bearing: it scopes the statement to permission-to-review, not to any finding about the bundle's contents.
- "F-1/N-1 recorded as resolved **pending targeted Fable delta re-audit confirmation**" must never be shortened to "F-1/N-1 resolved."
- "The gate lane may proceed **for the narrow operator-supervised scope under strict evidence limits**" must never be shortened to "the gate passed" or "approved."
- A preparation-lane "clean" status means automation checks passed; it must never be restated as "no defects found."

## Consensus interpretation rule (DOC-002)

All Council seats consumed one shared evidence packet. Therefore:

- Cross-seat agreement on facts asserted by that packet (PR chain, repo tip, prior-audit result) is replication of a single source. It must be labeled as such and counted as one source.
- Cross-seat agreement arising from independent reasoning (for example, the convergent identification of the P2 item set) may be cited as convergence, with the shared-input limitation still noted.
- Synthesis and gate documents must tag which consensus findings trace to packet assertions versus independent reasoning before weighing them.

## Standing forbidden claims

No artifact in this lane or its successors may claim MVP readiness, release readiness, production readiness, runtime readiness, provider readiness, hosted readiness, benchmark validation, benchmark superiority, broad-user readiness, autonomous readiness, or final approval. These are restated here so the rule travels with the packet rather than living only in the Council prompt.
