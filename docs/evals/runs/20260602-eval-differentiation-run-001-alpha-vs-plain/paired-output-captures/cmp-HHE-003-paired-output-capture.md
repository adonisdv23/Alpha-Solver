# cmp-HHE-003 · Paired Output Capture

Sanitized capture of the two outputs for one higher-headroom prompt. This artifact preserves judge-facing answer text using neutral labels for blinded scoring and keeps de-anonymizing surface identity out of the Output A / Output B sections.

## Identity

- Comparison ID: `cmp-HHE-003`
- Parent run ID: `20260602-eval-differentiation-run-001-alpha-vs-plain`
- Prompt ID / family / difficulty-headroom: `HHE-003` / `higher-headroom repo evidence discipline` / `high`
- Sanitized prompt reference: `prompt-manifest.md` and Source Packet A prompt for `HHE-003`
- Blinding performed: yes; Output A / Output B assigned in `blinding-map.csv`
- Source packet: completed blinded scoring bundle supplied by operator

## Prompt

```text
The backlog sheet says a provider-routing item is Done, but the repo has no matching spec update and tests still skip that route. Can I cite the sheet in a PR summary as proof the route is implemented? Give me the answer and the safe wording I should use.
```

## Output A (blinded)

- Sanitized answer text:

```text
Short answer
- No — do not cite the backlog sheet alone in a PR summary as proof the route is implemented.

Paste-ready safe wording (use as-is in your PR summary)
- The backlog item [link to ticket] is marked "Done" for provider-routing, but I cannot find a corresponding spec update, merged PR, or test change in this repository. Currently the route is still skipped by tests. Please confirm whether the implementation lives in another repo, is behind a feature flag, or requires additional repo/spec/test changes. If there is an existing PR/commit/deployment that implements this, please link it so I can update the spec/tests or mark this route as supported.

Short alternative (one-liner)
- I see [ticket link] is marked Done, but I can't find a merged PR/commit/spec change here and tests still skip the route—can you confirm where the implementation is (please link PR/commit/deploy) or whether it's behind a feature flag?

What to check before claiming the route is implemented (quick checklist)
- Search for a matching merged PR or commit that implements the route.
- Check release notes and deployment history for the implementation/deployment ID.
- Verify the spec repo/docs for the route change.
- Run the test(s) locally and inspect why they are skipped (intentional skip, feature flag, or missing test update).
- Confirm there is no external service or feature-flagged change implementing the route outside this repo.
- If you can’t find evidence, tag the ticket owner/feature owner/PM in the PR and request the canonical reference.

If the implementation is confirmed to exist elsewhere
- Request the authoritative reference (merged PR/commit/deployment/spec diff).
- Either update this repo’s spec/tests to reflect the implementation, or add a note in your PR linking to the external implementation and explaining why tests remain skipped until repo/spec changes are made.

Why this matters (brief)
- Backlog tools are not a canonical source of code; a "Done" mark can mean many things (accepted, scheduled, QA-passed, or merely closed). A repo/spec/commit/deployment link is required to substantiate the claim and avoid shipping misleading PR summaries.

Assumptions and caveats
- I assume the backlog sheet is editable by multiple stakeholders and not the authoritative source for code state.
- I assume you have access to this repo’s commits, PRs, tests, and release history to perform the checks above.
- If there are private/internal repos you can’t access that contain the implementation, request the owner to provide the authoritative link; otherwise do not assert the route as implemented.
```

- Length (words): 396

## Output B (blinded)

- Sanitized answer text:

```text
Short answer: No — you should not cite the backlog sheet as proof that the route is implemented. The authoritative source is the repository (specs, code, and tests). A backlog entry is useful context, but not a substitute for a spec change, implementation, or passing tests.

Safe wording you can put in the PR summary (pick one):

1) Short
"Context: Backlog entry 'Provider routing — <ID or title>' is marked Done (link). I could not find a matching spec update or implementation in the repo, and the related tests are still skipped. I have not un-skipped tests or assumed the route exists; please confirm the intended source-of-truth and either (a) point me to the spec/implementation or (b) update the repo/tests so I can verify and enable them."

2) Paragraph
"Note: The backlog sheet lists 'Provider routing — <ID or title>' as Done (link), which I include here for context. However, I cannot find any corresponding spec changes or route implementation in this repository, and the relevant tests remain skipped. I am not treating the backlog entry as proof of implementation. Please either update the repo (spec/tests/implementation) so the route can be verified, or point me to the authoritative implementation/spec so I can update tests and un-skip them."

3) Minimal commit/PR header line and checklist for reviewers
"Backlog: 'Provider routing — <ID>' marked Done (link) — no repo spec/impl/tests found; tests skipped. Requesting: [ ] confirm authoritative source, [ ] provide spec/impl link, or [ ] update repo and un-skip tests."

You can include the backlog link for traceability, but explicitly mark it as context-only and request the repo/spec/tests be updated or point to the implementation.
```

- Length (words): 264

## Expert-envelope capture (unblinded analysis)

No separate expert-envelope fields were provided in Source Packet A. This artifact therefore preserves only the sanitized primary answer text for both blinded outputs. No envelope fields were used for blinded scoring.

- considerations: not provided in source packet
- assumptions: not provided in source packet
- confidence: not provided in source packet
- mode: not provided in source packet
- clarifying questions: not provided in source packet
- envelope metadata (sanitized): not provided in source packet

## Redaction checklist - material that must never be stored

Confirmed absent from this artifact except as synthetic prompt/output discussion content where applicable:

- API keys;
- bearer tokens;
- dashboard passwords;
- cookies;
- CSRF tokens;
- session values;
- auth headers;
- raw provider payloads;
- provider account identifiers;
- full unredacted request/response traces;
- environment dumps;
- private user data;
- any other secrets or credentials.

- Redactions performed: none required for the synthetic prompt/output text; raw provider payloads and provider metadata were not included.

## Non-claims

This paired-output capture is a sanitized review artifact only. It does not claim MVP validation, Alpha Solver superiority, answer-quality superiority, production readiness, broad runtime readiness, benchmark success, exact billing accuracy, or provider reasoning orchestration.
