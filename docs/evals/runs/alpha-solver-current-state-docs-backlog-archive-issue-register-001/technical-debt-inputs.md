# Technical debt inputs

Full notes: [`docs/TECHNICAL_DEBT_AND_RUNTIME_NOTES.md`](../../../TECHNICAL_DEBT_AND_RUNTIME_NOTES.md).

| item | status | classification |
|------|--------|----------------|
| alpha/service overlap (ISS-012) | CONFIRMED | LATER_HARDENING |
| Multiple entrypoints (intentional) | CONFIRMED | LATER_HARDENING |
| Duplicate provider/adapter surfaces (ISS-008) | CONFIRMED | BLOCKS_PUBLIC_RUNTIME |
| Hardcoded pricing (ISS-007) | PARTIALLY_CONFIRMED | AFTER_SMOKE |
| Sanitizer Unicode normalization (ISS-009) | CONFIRMED | BLOCKS_PUBLIC_RUNTIME |
| Commit-signing test hermeticity (ISS-006) | CONFIRMED | LATER_HARDENING |
| Orphan/duplicate MVP docs (ISS-010) | PARTIALLY_CONFIRMED | LATER_HARDENING |
| Stale branches/refs (ISS-011) | CONFIRMED | LATER_HARDENING |

Nothing here `BLOCKS_SMOKE`. Remediation happens in dedicated future lanes; this
lane records inputs only and changes no runtime/test/CI code.
