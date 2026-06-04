# Scorer-Facing Sanitization Checklist

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`

Status: checklist template only. No outputs exist in this packet PR, so no sanitization is performed here.

## Boundary

Raw outputs are preservation artifacts and must remain exact. The sanitized scorer-facing render is a separate blind-scoring artifact created only after a future authorized capture task has preserved raw outputs.

Sanitization must follow `docs/evals/BLIND_SCORING_PROCEDURE.md`. It may strip or neutralize direct brand, provider, route, condition, heading, footer, and obvious envelope tells. It must preserve substantive content as plain prose.

## Symmetric sanitization checklist

For each comparison in a future scoring-prep task, confirm:

- [ ] Raw Output A source is preserved exactly before sanitization.
- [ ] Raw Output B source is preserved exactly before sanitization.
- [ ] Sanitization is applied symmetrically to both outputs.
- [ ] Direct brand names are removed or neutralized.
- [ ] Provider/model names are removed or neutralized.
- [ ] Route or condition labels are removed or neutralized.
- [ ] Pipeline-confirmation branding is removed or neutralized.
- [ ] Condition-identifying headings or footers are removed or neutralized.
- [ ] Substantive content remains intact.
- [ ] Caveats, reasoning, risks, assumptions, recommendations, and answer-quality defects remain intact.
- [ ] No expected answers or scoring hints were added.
- [ ] Sanitization decisions are recorded in an operator-only log outside the scorer-facing packet.

## Stop condition

If direct tells cannot be removed without substantive rewriting, stop before scoring. Mark the scorer packet invalid and regenerate a sanitized scorer-facing packet from the preserved raw outputs under a separately authorized task.
