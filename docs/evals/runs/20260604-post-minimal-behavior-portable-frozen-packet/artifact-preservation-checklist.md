# Artifact Preservation Checklist

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`

Status: preservation plan only, pre-capture.

## Preservation checklist

- [ ] Preserve the source packet for any future capture task, including authorization, branch or commit, condition rules, and operator constraints.
- [ ] Preserve the frozen prompt packet exactly as merged, including prompt IDs, prompt order, and exact prompt text.
- [ ] Preserve raw outputs exactly in a future capture task without editing, polishing, scoring, or identity labels in scorer-facing material.
- [ ] Preserve the sanitized scorer-facing render separately from exact raw outputs.
- [ ] Preserve the sanitization log or checklist outside the scorer-facing packet.
- [ ] Preserve the blinded scorer packet separately from raw outputs and operator-only metadata.
- [ ] Preserve the operator-only unblinding map separately from the scorer-facing packet.
- [ ] Preserve the score sheet after blind scoring, including all 14 dimension scores, totals, preferences, rationales, and defects.
- [ ] Preserve defects and caveats from capture, scorer validation, scoring, and unblinding review.
- [ ] Preserve the final run summary only after capture, blind scoring, authorized unblinding, and score-table population are complete.

## Boundary between tasks

### Packet PR

This packet PR freezes prompts, condition rules, capture rules, blinding rules, scorer-facing structure, and preservation requirements. It does not run capture, call providers, score, unblind, update Sheets, or change runtime behavior.

### Future capture PR or task

A future authorized capture task may generate condition outputs using the frozen prompts and approved provider/model/tool settings. It must preserve raw outputs and operator logs. It may prepare a separate sanitized scorer-facing render only if authorized by the future task. It must not score, unblind, update Sheets, or start Batch C.

### Future scoring task

A separate scoring task may build the blinded packet from sanitized scorer-facing renders and run blind scoring with the existing 14-dimension rubric. It must not include condition identities, runtime metadata, operator-only maps, raw output paths, or new scoring semantics.

### Future scored artifact PR

A later artifact PR may preserve the official blind scorer result, score sheet, authorized unblinding map, score table, defects, caveats, and run summary. It must keep portable-surface evidence separate from `/v1/solve` claims unless a separate approved task proves that endpoint wiring.
