# Allowed files

The future first-code lane may add or change only the file categories listed here. The default scope is static test scaffold only unless the controlling Level 9 packet explicitly widens it.

## Allowed file categories

- New or updated **static test files** under the repository test tree (for example `tests/`) whose sole purpose is to detect prohibited Self Operator behavior.
- New or updated **inert fixtures** consumed only by those static tests: static data files, expected-output snapshots, and fixture inputs that contain no runtime behavior.
- The first-code lane's own **docs packet** files describing what it did, plus its checks-run record.

## Conditions on allowed files

- Allowed test files must be deterministic and offline.
- Allowed test files must assert the absence or refusal of prohibited Self Operator behavior; they must not call it into existence.
- Allowed fixtures must be inert. A fixture must not embed credentials, live endpoints, provider keys, or executable runtime logic.
- The set of changed files must stay inside the changed-file scope proof recorded before commit and before PR creation.

Any file not in these categories is out of scope and is governed by `forbidden-files.md`.
