# Input artifacts

A future repeatability execution lane must create these input artifacts under the
fresh output root before any wrapper invocation:

| Artifact | Required contents |
| --- | --- |
| `inputs/approval-record.json` | Operator confirmation labels and text from `operator-confirmation-required.md`, operator identifier, UTC approval timestamp, approved target, and fresh run ID. |
| `inputs/proposed-task.json` | Lane ID, fresh run ID, proposed command text, target packet path, expected outputs, forbidden surfaces, stop-state rules, and output root. |
| `inputs/source-evidence-index.json` | Paths and commit SHA for first-use review input, first-use execution input, current packet, and checker scripts. |
| `inputs/repeatability-plan-verification.json` | Machine-readable result of the mandatory pre-execution checkpoint. |

The proposed task must include only the literal supervised command text:

```text
python scripts/check_local_llm_packet_consistency.py
```

The proposed task must not include network commands, provider commands, model
commands, browser commands, deployment commands, billing commands, credential or
secret access commands, source-artifact mutation commands, or final status CLI
implementation commands.
