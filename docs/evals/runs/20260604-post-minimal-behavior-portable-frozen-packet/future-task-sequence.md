# Future Task Sequence

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`

Status: sequencing note only, pre-capture.

After this PR merges:

1. Review and merge the frozen packet PR.
2. Update Google Sheets only after merge, if separately authorized.
3. Run capture in a separate authorized task.
4. Build the blinded scorer packet.
5. Run blind scoring in a separate authorized task.
6. Populate scored post-improvement artifacts.
7. Interpret the result against A3-1 and Batch B.
8. Keep portable-surface evidence separate from runtime `/v1/solve` claims.
