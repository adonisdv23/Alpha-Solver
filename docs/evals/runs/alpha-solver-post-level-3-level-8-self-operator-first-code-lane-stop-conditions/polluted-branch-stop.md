# Polluted branch stop

A future first code lane must stop if the branch is polluted or not current-main-based.

## Polluted branch indicators

- The branch contains unrelated local modifications before the lane starts.
- The branch is behind or unrelated to current `main`.
- The branch contains files outside the selected lane's allowed scope.
- The branch contains generated, source artifact, credential, deployment, billing, browser automation, external API, `/v1/solve`, or dashboard changes that are not explicitly authorized by the selected lane.

## Required response

Do not edit, commit, or open a PR from a polluted branch. Report the branch state and restart from a clean current-main-based branch before any future implementation work proceeds.
