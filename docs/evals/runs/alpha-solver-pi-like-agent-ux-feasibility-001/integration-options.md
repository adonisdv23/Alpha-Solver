# Integration Options

## Option A: No integration; capture UX principles only

Status: recommended.

Alpha Solver can adopt selected UX principles: warmer guidance, artifact-grounded memory summaries, stop-condition reminders, next-action coaching, and local-first operator assistance. This option does not require external product dependencies.

## Option B: Alpha-native local operator assistant

Status: plausible future lane, not implemented here.

A future spec could define a local assistant surface backed by Alpha Solver artifacts. It would need strict memory provenance, privacy policy, operator controls, and evidence-boundary rendering.

## Option C: Voice/conversational mode

Status: defer.

Voice may be useful later for low-risk status review. It should wait until transcript handling, consent, redaction, storage, and citation behavior are specified.

## Option D: Direct Pi or third-party assistant integration

Status: blocked unless operator provides an exact source link and explicit approval.

This lane does not assume an API, license, embedding right, or technical feasibility. Direct integration would require a separate source-linked technical and legal review.

## Decision

Choose Option A now and select Option B as the future design direction. Do not choose Option D in this lane.
