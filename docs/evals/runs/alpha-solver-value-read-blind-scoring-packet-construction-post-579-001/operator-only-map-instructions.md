# Operator-Only Map Instructions

The unblinding map must not be committed to the repository. It must not be placed in a PR body, issue comment, committed artifact, tracked file, or generated score file.

The operator should store the map outside the repository in an operator-controlled private location such as an encrypted password-manager note, encrypted local file, or private operations vault. The storage location should be access-limited to the operator and any separately authorized reviewer who is allowed to unblind after score lock.

Unblinding may happen only in a separately authorized future lane after scores are locked. That future lane must cite the locked score-output path and must preserve the no-final-interpretation boundary unless final interpretation is separately authorized.
