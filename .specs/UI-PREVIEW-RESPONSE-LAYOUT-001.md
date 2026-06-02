# UI-PREVIEW-RESPONSE-LAYOUT-001 · Expert Preview Long Response Layout

## Purpose

Improve `/dashboard/expert-preview` readability when the plain same-provider pane or Alpha Solver expert-preview pane renders long primary answer text.

This defect was discovered during the first controlled operator demo run. It does not validate the MVP, prove Alpha Solver superiority, or prove production readiness.

## Scope

In scope:

- keep the existing authenticated expert-preview route and form behavior;
- keep prompt preservation unchanged;
- keep loading-state and duplicate-submit behavior unchanged;
- keep dashboard auth/session/CSRF behavior unchanged;
- keep live spend guard behavior unchanged;
- keep provider/runtime behavior unchanged;
- make both primary answer boxes wrap long text and expand vertically without clipping;
- keep details sections accessible below the primary answer content.

Out of scope:

- enabling OpenAI;
- Cloud Run deployment;
- Google Sheet or backlog workbook updates;
- provider behavior changes;
- dashboard auth/session/CSRF changes;
- live spend guard semantic changes;
- MVP validation claims;
- Alpha Solver superiority claims;
- production-readiness claims;
- answer-quality benchmark claims;
- provider reasoning orchestration claims.

## Acceptance criteria

No-network UI tests should prove:

- long plain provider output renders inside the primary answer element;
- long Alpha Solver expert-preview output renders inside the primary answer element;
- both answer elements use layout CSS that wraps long text, allows panes to shrink inside the grid, and avoids fixed-height clipping;
- existing loading-state script behavior remains present;
- existing CSRF behavior remains covered by existing tests.

## Backlog impact

`UI-PREVIEW-RESPONSE-LAYOUT-001` should be marked Done only after the PR implementing this spec is merged.

This defect was discovered during the first controlled operator demo run. This does not validate the MVP, prove Alpha Solver superiority, or prove production readiness. Backlog spreadsheets and Google Sheets are not edited from this repo task.
