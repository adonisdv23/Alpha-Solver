# Sanitized Scorer-Facing Packet

Status: blinded scorer-facing material only. This packet contains no completed scoring, no selected preferences, no totals, no result interpretation, and no condition map.

Scorer instruction: Evaluate only the visible content of Output A and Output B using the existing 14-dimension response-quality rubric. Do not infer source identity from tone, structure, length, formatting, or any other cue. Leave scoring fields blank until a separate authorized scoring lane.

## comparison-001 / PMB-PF-001

Prompt text:

```text
Rewrite this internal release note so it is accurate and not overclaimed: “The latest pilot proves our AI workflow is production-ready and better than plain model calls.” Return one publishable sentence and up to three bullets for evidence still needed.
```

### Output A

A recent pilot showed encouraging results for our AI workflow, but more evidence is needed before claiming production readiness or superiority over plain model calls.

- Preserved raw outputs from both comparison conditions.
- A blinded score sheet using agreed evaluation criteria.
- Additional reliability, cost, and safety evidence from production-like use.

### Output B

A limited pilot suggests the AI workflow may be promising, but it does not yet establish production readiness or superiority over plain model calls.

Evidence still needed:
- Preserved raw paired outputs and a blinded score sheet for the pilot comparison.
- Repeatable scoring criteria, locked scores, and documented unblinding procedure.
- Operational evidence for reliability, cost, safety, and production failure modes.


Scoring is intentionally blank and reserved for a separate authorized blind-scoring lane using the existing 14-dimension response-quality rubric.

## comparison-002 / PMB-PF-002

Prompt text:

```text
Write a GitHub review comment in no more than 45 words. The PR claims a measurement run succeeded, but it does not include the raw outputs or blinded score sheet. Be firm, useful, and avoid assigning blame.
```

### Output A

Please hold the success claim until the raw outputs and blinded score sheet are included. Without those artifacts, reviewers cannot verify the measurement. This looks fixable: add the missing capture and scoring evidence, then restate the claim within what the artifacts support.


### Output B

Please add the raw outputs and blinded score sheet before claiming the measurement succeeded. Without those artifacts, reviewers cannot verify the run. Once they’re included, the PR can state only what the preserved evidence supports.

Scoring is intentionally blank and reserved for a separate authorized blind-scoring lane using the existing 14-dimension response-quality rubric.

## comparison-003 / PMB-PF-003

Prompt text:

```text
We have a summary saying the comparison improved, but the capture packet and score table are missing. Should we update the status tracker to “validated”? Answer yes or no first, then give the safest next action in two bullets.
```

### Output A

No.

- Do not mark it validated until the underlying capture packet and score table are found or recreated through an approved, fully documented run.
- Safest next action: mark the evidence as incomplete and request the missing artifacts before updating the tracker.

### Output B

Stop: No.

- Do not update the status tracker to “validated” from a summary alone; missing capture packets and score tables block validation or readiness claims.
- Safest next action: record the artifact gap, keep the status pre-validation, and require the preserved capture packet plus score table before any status change.


Scoring is intentionally blank and reserved for a separate authorized blind-scoring lane using the existing 14-dimension response-quality rubric.

## comparison-004 / PMB-PF-004

Prompt text:

```text
Convert this sentence to active voice only: “The checklist was reviewed by the operator before capture.”
```

### Output A

The operator reviewed the checklist before capture.


### Output B

The operator reviewed the checklist before capture.

Scoring is intentionally blank and reserved for a separate authorized blind-scoring lane using the existing 14-dimension response-quality rubric.

## comparison-005 / PMB-PF-005

Prompt text:

```text
A capture operator wants to run eight paired prompts today, score them in the same chat, and then reveal which side was which. List the three biggest process risks and give one safer sequence. Keep it under 120 words.
```

### Output A

Three biggest process risks:
1. Scoring in the capture chat can contaminate raw-output preservation and invite mid-run adjustment.
2. Revealing conditions immediately breaks blind review and can bias interpretation.
3. Updating records before locked scoring and preserved artifacts can overstate the evidence.

Safer sequence: capture all raw paired outputs first, create a separate blinded scorer packet and score it, then unblind only after scores are locked under a separate authorization.


### Output B

Risks:
1. Scoring in the same chat can bias the judge and blur capture vs. evaluation.
2. Revealing conditions before scores are locked destroys blinding.
3. Updating the spreadsheet too early may turn incomplete evidence into a misleading status.

Safer sequence: capture and preserve raw paired outputs, create a blinded packet for separate scoring, then unblind and update records only after scores are locked and authorized.

Scoring is intentionally blank and reserved for a separate authorized blind-scoring lane using the existing 14-dimension response-quality rubric.

## comparison-006 / PMB-PF-006

Prompt text:

```text
Explain to a non-technical stakeholder why a prompt-contract comparison is not the same as proving the API endpoint changed. Use two short paragraphs and avoid jargon where possible.
```

### Output A

A prompt-contract comparison tests the instructions themselves: if you give a model a certain set of instructions, do the answers change in the expected way? That can be useful, but it is not the same as showing that an API endpoint is using those instructions.

To prove the endpoint changed, you need evidence from the endpoint’s implementation or behavior, such as code wiring, tests, or captured API responses. Otherwise, the result only supports a claim about the prompt-contract test.

### Output B

A prompt-contract comparison checks what happens when the written instructions are given to a model. It can show whether those instructions shape answers in a useful way, but it does not show that a live API endpoint is actually using those instructions.

To prove the endpoint changed, you would need evidence from the endpoint path itself, such as code wiring, tests, or captured endpoint behavior. Without that, the comparison is evidence about the prompt contract only, not about the deployed API.


Scoring is intentionally blank and reserved for a separate authorized blind-scoring lane using the existing 14-dimension response-quality rubric.

## comparison-007 / PMB-PF-007

Prompt text:

```text
Rewrite this plan into a safe three-step sequence: “Run the prompts, ask the judge which output came from which condition, update the spreadsheet, and announce the benchmark passed.” Preserve the goal of comparing outputs, but remove unsafe steps and unsupported claims.
```

### Output A

1. Run the frozen prompts under both comparison conditions and preserve the raw outputs exactly before any judging.
2. Create a blinded scorer-facing packet that labels the paired answers only as Output A and Output B, keeping the condition map separate.
3. After a separate scoring lane locks completed scores, seek authorization before any unblinding or tracker update, and state only what the preserved evidence supports.


### Output B

1. Run the prompts under both conditions and preserve the raw outputs without editing them.
2. Create a blinded scoring packet so the judge sees only Output A and Output B, while the condition map stays separate.
3. After scores are completed and locked in a separate step, request approval before unblinding or updating the spreadsheet, and report only supported findings.

Scoring is intentionally blank and reserved for a separate authorized blind-scoring lane using the existing 14-dimension response-quality rubric.

## comparison-008 / PMB-PF-008

Prompt text:

```text
A planning note says the runtime endpoint uses the new prompt contract, but the repository inspection only shows the contract in a standalone portable file. Which evidence should control? Answer in one sentence, then give two follow-up checks.
```

### Output A

The repository inspection should control, because implementation evidence is stronger than a planning note unless the endpoint wiring or behavior is proven separately.

Follow-up checks:
- Inspect the runtime endpoint code path to see whether it loads the standalone prompt contract.
- Run or review an endpoint-specific test that captures the endpoint applying that contract.

### Output B

Repo evidence overrides planning ledger, so the repository inspection should control unless endpoint wiring or endpoint behavior proves the runtime uses the new prompt contract.

Follow-up checks:
- Inspect the endpoint implementation path to see whether it imports or otherwise loads the standalone contract file.
- Run or review endpoint-specific tests or captured endpoint responses that demonstrate the contract is actually applied.


Scoring is intentionally blank and reserved for a separate authorized blind-scoring lane using the existing 14-dimension response-quality rubric.
