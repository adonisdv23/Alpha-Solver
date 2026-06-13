# Failure Analysis

## Scope

The two selected Self Operator execution targets did **not** fail: the Self Operator suite passed
213/213, and the release-gate CLI exited `0` with 11/11 gates passing.

The only failures observed were in the **separate full-suite validation run**, and they are pre-existing
and unrelated to this lane.

## The 2 full-suite failures

| Test | Cause |
| --- | --- |
| `tests/test_smoke_quickstart.py::test_release_script` | `subprocess.CalledProcessError: Command '['git', 'commit', '-m', 'chore: initial']' returned non-zero exit status 128` |
| `tests/test_tag_release.py::test_tag_release` | `subprocess.CalledProcessError: Command '['git', 'commit', '-m', 'init']' returned non-zero exit status 128` |

Both tests create a throwaway repository with `git init` under a pytest `tmp_path` and then run
`git commit`. In this container, commit signing is enforced and the signing server rejects commits in
throwaway repositories:

```
Error: signing failed: Signing failed: signing operation failed: signing server returned status 400 (140-byte body)
fatal: failed to write commit object
```

## Why these are not evidence against this lane

- **Environmental, not product logic.** The failure originates in the container's commit-signing
  infrastructure returning HTTP 400 for throwaway `git init` repos, not in any Self Operator or product
  code path.
- **Pre-existing and unchanged.** PR #496 recorded the identical result ("2 failed, 1211 passed, 3
  skipped") on `main` before this lane. This packet adds documentation only; it changes no test, product,
  or CI code, so the counts are unchanged.
- **Disjoint from the execution target.** Neither failing test is part of `alpha/self_operator/` or the
  Self Operator suite. The Self Operator targets are fully green.

## Skipped tests (not failures)

- `tests/providers/test_openai_live_smoke.py` — skipped: requires `ALPHA_LIVE_OPENAI=1` and a non-empty
  `OPENAI_API_KEY`. Correctly skipped; this lane does not enable live provider tests.
- `tests/test_decks_smoke.py` — skipped: web adapter disabled in the test environment.
- `tests/test_packaging_build.py` — skipped: build module missing / build skipped.

## Disposition

No action taken. Per the code-change policy for this lane, tests and CI were **not** modified to make
checks pass. The pre-existing signing-related failures are recorded honestly and isolated from the Self
Operator execution evidence.
