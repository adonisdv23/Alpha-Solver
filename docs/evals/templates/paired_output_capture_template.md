# <Comparison ID> · Paired Output Capture

Sanitized capture of the two outputs for one higher-headroom prompt, plus the
Alpha expert envelope, for blinded scoring and unblinded lift analysis. Follow
`docs/evals/ARTIFACT_PRESERVATION.md` and `docs/evals/BLIND_SCORING_PROCEDURE.md`.

Store **sanitized answer text**, not raw provider output. For the synthetic
higher-headroom prompt set the answer text is secret-free by construction and may
be preserved in full sanitized form to keep scoring re-scorable.

## Identity

- Comparison ID:
- Parent run ID:
- Prompt ID / family / difficulty-headroom:
- Sanitized prompt reference:
- Blinding performed: yes/no (Output A / Output B assigned in `blinding_map_template.csv`)
- Form capture level: full-sanitized / summary-only / not-captured
- Capture commit SHA: git-sha / not-captured
- Capture started at: ISO-8601 / not-captured
- Capture completed at: ISO-8601 / not-captured
- Capture model set: model-set-label / not-captured
- Capture surface count: count
- Capture provider execution count: count / not-captured (summary-level only)

## Output A (blinded)

- Sanitized answer text:
- Length (words):
- Tokens: token count / not-captured

## Output B (blinded)

- Sanitized answer text:
- Length (words):
- Tokens: token count / not-captured

## Alpha expert-envelope capture (unblinded analysis)

Captured for the Alpha output only; used to verify material lift, not shown during
blinded scoring (the envelope is a structural tell).

- considerations:
- assumptions (each tagged material? yes/no, correct? yes/no):
- confidence:
- mode:
- clarifying questions:
- envelope metadata (sanitized):

## Redaction checklist — material that must never be stored

Confirm none of the following appear in this artifact:

- API keys;
- bearer tokens;
- dashboard passwords;
- cookies;
- CSRF tokens;
- session values;
- auth headers (for example `Authorization` values);
- raw provider payloads;
- provider account identifiers;
- full unredacted request/response traces;
- environment dumps;
- private user data;
- any other secrets or credentials.

- Redactions performed:

## Non-claims

This paired-output capture is a sanitized review artifact only. It:

- does not validate the MVP;
- does not prove Alpha Solver superiority;
- does not prove answer-quality superiority;
- does not prove production readiness;
- does not prove broad runtime readiness;
- does not prove benchmark success;
- does not prove exact billing accuracy;
- does not prove provider reasoning orchestration.
