# Stop Conditions

Stop before output generation or interpretation if any of the following is true:

- Output-generation mechanism is ambiguous.
- Any provider token, credential, billing access, or hosted service is required but not explicitly authorized.
- Local model execution is required but not explicitly authorized.
- Prompt set is incomplete.
- Raw-output preservation path is missing.
- Scoring packet is missing.
- Blinding map storage is missing.
- Claim boundaries are missing.
- Any runtime endpoint, public endpoint, `/v1/solve`, dashboard, public API, or Google Sheets mutation is involved.
- Scorer-facing material exposes identity before score lock.
- Raw output is missing, edited before preservation, or contaminated with private data, secrets, or unauthorized execution metadata.
