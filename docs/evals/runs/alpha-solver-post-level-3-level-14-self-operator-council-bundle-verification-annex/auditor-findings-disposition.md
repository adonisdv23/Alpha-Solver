# Auditor findings disposition

| Finding | Source | Status after #490 | Council impact | Notes |
|---|---|---|---|---|
| F-1 | same_thread_fable_chat_report; #489/#490 repo_artifact_found | resolved after #489 + #490, pending targeted Fable delta re-audit confirmation | Council should see the checker scope and directory reference fixes, but should not treat this as Council acceptance. | #489 widened scanning; #490 closed the suffix-less directory reference gap. |
| F-2 | same_thread_fable_chat_report; #488 repo_artifact_found | resolved by #488 | Council should see the AUDIT-005 decision/routing fix before any manual run. | #488 recorded the decision and clarified routing/wording. |
| F-6 | same_thread_fable_chat_report; #488 repo_artifact_found | resolved by #488 | Council should see corrected Council routing context. | #488 addressed the Council bundle wording/routing issue. |
| N-1 | same_thread_fable_chat_report; #490 repo_artifact_found | resolved by #490, pending targeted Fable delta re-audit confirmation | Council should know the directory reference gap has a recorded fix but has not received a targeted Fable delta re-audit in this lane. | #490 fixed suffix-less packet directory reference detection for post-Level and legacy local-LLM references. |
| N-2 | same_thread_fable_chat_report; this annex repo_artifact_found | resolved by this annex if completed | Council receives a refreshed post-#490 annex rather than a stale post-#487 bundle view. | This annex adds PR-chain, checker coverage, caveats, CI, and self-attestation notes. |
| N-3 | same_thread_fable_chat_report | recorded as a prior benign scope-deviation note, not retroactively fixed | Council should know this is historical context, not a new blocker asserted by this annex. | No prior evidence is mutated. |
| N-4 | same_thread_fable_chat_report | recorded as caveat | Council should weigh the caveat independently. | Tracked here for visibility. |
| D-1 | same_thread_fable_chat_report; #490 repo_artifact_found | non-blocking caveat/deferred polish | Council should see the future false-negative caveat. | Intentional missing-reference exemption terms such as deferred and does not exist remain the loosest future false-negative channel. |
| D-2 | same_thread_fable_chat_report | non-blocking caveat/deferred polish | Council should see that simplification remains optional. | Redundant checked-reference call can be simplified later. |
| D-3 | same_thread_fable_chat_report | non-blocking caveat/deferred polish | Council should see the style caveat. | Minor style issue in tests; non-blocking. |
| D-4 | same_thread_fable_chat_report | non-blocking caveat/deferred polish | Council should see self-attestation limits. | Lane checks-run.md remains self-attested prose; CI mitigates for #490. |
| D-5 | same_thread_fable_chat_report; #490 repo_artifact_found | non-blocking caveat/deferred polish | Council should see the AUDIT-005 wording caveat. | AUDIT-005 authorization restated conditions instead of quoting verbatim; substantively compliant. |

This annex does not claim Council has accepted any finding disposition.
