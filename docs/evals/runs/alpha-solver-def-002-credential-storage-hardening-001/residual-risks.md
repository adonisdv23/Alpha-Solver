# Residual risks

## DEF-002 remains open

This lane addresses RR-02 only. DEF-002 remains open pending the remaining
must-fix or accepted-residual decisions from the accepted closure sequence.

## Remaining RR-02 limitations

- This lane hardens file and directory permissions; it does not implement
  encryption-at-rest, OS-keyring storage, cloud secret-manager integration, or
  envelope encryption.
- POSIX permission evidence is not portable to every operating system.
- Existing deployments with copied backups or previously exposed plaintext files
  require operator handling outside this lane.
- The dashboard-managed credential file still contains plaintext from the
  perspective of the owning OS account; this lane reduces cross-user filesystem
  exposure but does not protect against compromise of that account.

## Other DEF-002 risks not addressed

RR-03, RR-01, RR-09, RR-05, RR-07, RR-08, RR-06, and accepted-residual candidate
items remain outside this lane.
