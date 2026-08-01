---
task_id: OTC2-20260801-secret-owner-completion
status: active
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: secret-lifecycle
phase: implementation
branch: fix/OTC2-20260801-secret-owner-completion
base_branch: main
created: 2026-08-01T16:03:00+02:00
updated: 2026-08-01T16:03:00+02:00
last_verified_commit: "7596a792fbf747609a65e9fc35678b800b2d56e2"
required_base_commit: "7596a792fbf747609a65e9fc35678b800b2d56e2"
risk: medium
related_pr: null
depends_on:
  - OTC2-20260801-post-remediation-closure-audit
  - audit merge 958881038ca5a5bc2f25a878a898ab5446d5e5c4
  - audit archive merge 7596a792fbf747609a65e9fc35678b800b2d56e2
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-secret-owner-completion.md
  - oteryn-client/crates/identity/src/lib.rs
  - oteryn-client/crates/game-session/src/lib.rs
shared_path_lease: []
modules_touched:
  - OAuth loopback callback owner
  - one-shot game-entry credential owner
crates_touched:
  - oteryn-identity
  - oteryn-game-session
features_touched:
  - callback target encapsulation
  - rejected secret input cleanup
reuses:
  - existing standard-library overwrite helpers
  - existing non-cloneable credential types
contracts_produced:
  - externally immutable callback target ownership
  - explicit rejected-credential byte cleanup
contracts_consumed:
  - CallbackAttempt::new fake/receiver construction
  - GameEntryCredential public constructor
contracts_touched:
  - project-owned secret overwrite invariant
implementation_authorized: true
policy_version: 2
task_kind: implementation
execution_mode: chat-github-connector
execution_reason: two source-local standard-library edits and focused tests with no dependency or manifest change
context_pressure: low
context_growth: stable
context_score: 5
estimate_confidence: high
decomposition_decision: single
decomposition_reason: both residuals are the two remaining clauses of one audited LOW secret-owner finding and share one rollback boundary
validation_level: heavy
heavy_validation_runs: 0
session_rotation_count: 0
---

# Goal

Close audited LOW residual `OTC2-POST-001` without broadening any memory-erasure claim.

# Required invariant

- callers outside `oteryn-identity` cannot mutate, take or replace the callback target after `CallbackAttempt::new` accepts ownership;
- the callback target remains bounded, redacted, non-cloneable and explicitly overwritten on terminal drop;
- direct non-empty oversized `GameEntryCredential` input is explicitly overwritten before validation returns `TooLarge`;
- accepted credential ownership, expiry and one-shot admission behavior remain unchanged;
- only project-owned initialized bytes are claimed; allocator, library, browser, TLS and operating-system copies remain out of scope.

# Planned implementation

- make `CallbackAttempt` fields private;
- expose only a copy-valued peer accessor; retain the target accessor as crate-private implementation detail;
- add a compile-fail API example proving the callback target is not publicly mutable;
- make rejected credential validation operate on a mutable owned vector and fill oversized bytes before returning;
- retain the accepted vector as the private secret owner without an unnecessary representation conversion;
- add focused tests for oversized rejected-input cleanup, redaction and existing construction/flow behavior.

# Exclusions

No shutdown, asset-open, architecture-policy, workflow, manifest, lockfile, dependency, shared PR #23 documentation, endpoint or protocol change.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T16:03:00+02:00
head: 7596a792fbf747609a65e9fc35678b800b2d56e2
branch: fix/OTC2-20260801-secret-owner-completion
pr: null
status: active
phase: implementation
proven:
  - The independent closure audit found no defect above LOW severity.
  - CallbackAttempt.target is public and mutable after accepted ownership.
  - SecretBytes::new returns TooLarge without explicitly clearing direct oversized input.
  - Current internal Gateway producer enforces the same credential maximum before GameEntryCredential construction.
  - Open PRs 23, 48 and 97 do not touch identity or game-session source.
derived:
  - One standard-library-only source-local patch closes the residual without API changes to normal constructors or consumers.
unknown:
  - Exact rustfmt placement for the compile-fail example and focused cleanup helper.
conflicts: []
first_failure:
  marker: OTC2-POST-001
  evidence: post-remediation closure audit on main 67a6c9d726f7e70977803b028270475570210db0.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-secret-owner-completion.md
validation: []
blockers: []
next_action: Open the draft PR, patch the two private owners and run focused plus complete workspace validation.
```
