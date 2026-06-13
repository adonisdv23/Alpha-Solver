# Capture-integrity process for future Council runs (DOC-003)

The completed Council run experienced one mid-run capture failure that required a rerun (a pre-Council phase plan was captured instead of a Council response) and one platform failure (Venice - Auto). For a solo operator capturing many seats manually, these are expected failure modes. The following lightweight checks apply to future Council or multi-seat capture runs.

## Per-slot capture checklist (apply at capture time, not only at synthesis)

- Correct seat header present (slot number, model/platform, assigned lens).
- Model declaration section present and the declared model noted, including any mismatch with the slot label.
- All required response sections present through the final recommendation paragraph (no truncation).
- Exactly one recommendation token present and legible.
- No prompt text captured in place of the response.
- No operator commentary inside the response body; operator notes go outside the markers.
- Record raw character count and a SHA-256 (or prefix) per slot at capture time, before any cleanup.

## Platform-failure handling

If a platform produces no usable output, record a formal capture note in the slot containing: slot number, platform, assigned lens, status `PLATFORM_FAILED_NO_USABLE_OUTPUT`, and explicit statements that no response was reconstructed or fabricated, no partial output is treated as valid evidence, and the slot must not be counted as substantive Council evidence.

## Completeness table

Before synthesis, produce a completeness table with one row per expected slot: slot number, model/platform, lens, capture status, rerun status, declared-model mismatch notes, and validity notes. Synthesis does not start until every row is either valid or a documented platform failure within the allowed exclusion budget.

## Cleanup disclosure

If captures are cleaned (prompt blocks removed, markers rebuilt), the cleaned file must disclose every cleanup step and carry per-slot hashes, and downstream documents must describe it as cleaned raw capture, not raw capture.
