# Shared stop conditions

Future lanes must stop under these conditions:

- stop if explicit operator confirmation is missing;
- stop if Level 10 static-test scaffold is not merged and GS done before runtime-adjacent scaffolds;
- stop if scope is unclear;
- stop if changed files exceed allowed scope;
- stop if forbidden surface is detected;
- stop if provider/network/browser/deployment/billing/credential access is required;
- stop if source artifacts would be mutated;
- stop if evidence would be promoted.

Stopping means fail closed, preserve a reviewable blocker note or authorized stop-state artifact, and do not continue into adjacent implementation.
