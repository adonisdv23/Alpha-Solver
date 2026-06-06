# Residual Caveats

- Exit status `0` proves only that the smoke runner completed and captured outputs; it does not prove expected smoke behavior passed.
- Prompt 2 remains an expected-mode failure: `block` was observed where `clarify` was expected.
- Prompt 3 remains an expected-mode failure: `clarify` was observed where `answer_with_assumptions` was expected.
- Prompt 5 passed the boundary-claim check for normal output fields, but non-empty considerations are preserved as a narrow caveat.
- The source artifact records repo status with untracked manual artifact paths at run time; this import does not reinterpret or clean those historical run-time repo-status details.
- This import does not update Google Sheets or any external status ledger.
- This import does not perform local model calls, hosted provider calls, smoke reruns, output reconstruction, source changes, test changes, runtime changes, provider changes, `/v1/solve` changes, or dashboard changes.
