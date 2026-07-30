---
task_id: OTC-20260730-w7-entry-contract
status: in_progress
agent: "W7-ENTRY-CONTRACT worker"
track: greenfield-rust
workstream: account-session-world-directory-game-session
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-ENTRY-CONTRACT
parallel_lane_state: claimed
coordinator_task: none
branch: feat/OTC-20260730-w7-entry-contract
base_branch: main
created: 2026-07-30T12:25:00+02:00
updated: 2026-07-30T12:25:00+02:00
last_verified_commit: ""
required_base_commit: "11a14721e1f3ef81e6bbab54cdfbb631d7ec81e0"
risk: high
related_pr: pending
depends_on:
  - W7 plan PR #101 merged as f7ddc2849838df05a95e4d7260bfe7c3359b4c8d
  - W7 plan archive PR #102 merged as 11a14721e1f3ef81e6bbab54cdfbb631d7ec81e0
integration_after: []
owned_paths:
  - oteryn-client/crates/account-session/**
  - oteryn-client/crates/world-directory/**
  - oteryn-client/crates/game-session/**
  - oteryn-client/docs/research/technical-login/W7_ENTRY_CONTRACT_EVIDENCE.md
  - docs/agents/tasks/active/OTC-20260730-w7-entry-contract.md
shared_path_lease:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/deny.toml
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
  - oteryn-client/docs/operations/RUST_WORKSPACE.md
contract_role: producer
contracts_produced:
  - AccountSessionId
  - CharacterId
  - WorldId
  - GameplayChannelId
  - DirectoryRevision
  - GameEntryRequest
  - GameEntryCredential
  - EntryFailure
  - SessionEntered
  - public deterministic entry lifecycle states
contracts_consumed:
  - merged W7 technical-login architecture and accepted wave plan
  - Gateway protocol-v1 signed 64-bit identifier widths as read-only evidence
crates_touched:
  - account-session
  - world-directory
  - game-session
features_touched:
  - typed account-session generation
  - typed world/character directory identity
  - deterministic one-shot game-entry lifecycle
contracts_touched:
  - first shared W7 entry contract producer only
modules_touched: []
reuses:
  - existing foundation, diagnostics and test-support crates
  - existing architecture categories and workspace policy
  - exact accepted W7 type ownership
public_interfaces:
  - typed W7 entry/session/directory primitives and lifecycle
cross_repo_tasks: []
performance_evidence:
  - deterministic bounded state-transition tests only; no latency or compatibility claim
security_evidence:
  - credential non-Clone/redacted/move-once/terminal-clear properties
  - no credential persistence, logging, raw backend text, capture or external-repository write
---

# Goal

Implement the sole shared contract producer for W7 account-session, directory and one-shot game-entry lifecycle types. This lane does not implement OAuth/HTTP, transport, Canary protocol, application composition or real compatibility.

The coordinator launch commit creates only this task record. The assigned worker must attach a unique local worktree to branch `feat/OTC-20260730-w7-entry-contract` before implementation and keep the early draft PR current.

# Why this lane is safe to run

- The W7 plan and separate plan archive are merged.
- No other active Rust task or open PR owns the exclusive crate paths or named contracts.
- PR #23 is legacy OTUI/Lua only; PR #48 is isolated operational non-merge work; PR #97 is legacy asset rehearsal only.
- This is the first dependency root; it consumes no unmerged W7 producer.
- The coordinator grants this lane the single shared Cargo/document lease because workspace membership and generated lockfile integration cannot complete otherwise.
- All other W7 lanes remain unlaunched and may not touch the lease or define substitute types.

# Exclusive contract rules

- `account-session` owns `AccountSessionId` as client-local opaque generation/correlation identity, never an external identity/account ID or bearer value.
- `world-directory` owns `CharacterId`, `WorldId`, `GameplayChannelId` and client-local `DirectoryRevision`.
- `CharacterId` and `WorldId` preserve Gateway signed 64-bit JSON width and reject narrowing.
- `GameplayChannelId` remains opaque, unpopulated and unserialized in the one-exact-issuer milestone.
- `game-session` depends only on `account-session` and `world-directory` and owns `GameEntryRequest`, `GameEntryCredential`, `EntryFailure`, `SessionEntered` and lifecycle states.
- `GameEntryCredential` owns secret bytes, is non-`Clone`, redacts `Debug`/`Display`, is never serializable/persisted and moves exactly once into admission.
- `EntryFailure` is bounded, typed and stable; it contains no secret or raw backend/OS error text.
- No Platform DTO, OAuth message, HTTP client, transport interface, protocol opcode, packet enum or speculative multi-world/channel API may be added.

# Acceptance criteria

- [ ] Create the three crates only in exclusive paths with architecture-valid dependency direction.
- [ ] Produce every named public type exactly once; no substitute public contract exists.
- [ ] Deterministically reject stale account/directory/entry generations.
- [ ] Reject invalid selected world/character relationships.
- [ ] Reject duplicate/late credential handoff, terminal reuse and replay.
- [ ] Clear credential material on every terminal lifecycle path.
- [ ] Prove non-`Clone`, redacted formatting and no secret in snapshots/errors/panic text.
- [ ] Add focused unit/property tests for legal and illegal transitions.
- [ ] Update only lease-authorized Cargo/generated lockfile and shared documentation paths.
- [ ] Do not change architecture-check policy, lint/unsafe policy or dependency-deny policy to make implementation pass.
- [ ] Exact-head locked metadata, `cargo fmt --check`, strict Clippy, all workspace tests, architecture check, cargo-deny and repository required CI pass.
- [ ] Complete changed-file/diff review and resolve every review thread.
- [ ] Merge through branch protection, then archive this task separately and release the full shared-path lease before downstream producer integration.

# Parallel-task answers

- Safe concurrency: no W7 sibling is launched; legacy/operational PRs own disjoint paths.
- Exclusive paths/contracts: exactly those declared in front matter and the accepted W7 plan.
- Shared paths: held exclusively by this task; all other tasks keep them read-only.
- Contract role: sole producer.
- Validation invalidation: any newer `main` changing foundation/test-support/workspace policy or the accepted W7 architecture invalidates prior full validation and requires restack/re-run.
- `integration_ready`: exclusive crates/tests complete while a shared path cannot be updated; not expected while this task holds the lease.
- `blocked`: overlapping owner, changed external identifier width, architecture contradiction, dependency-policy failure or inability to prove credential erasure/redaction.
- Independent merge: yes, after its own exact-head gates; it must merge before every W7 consumer finalizes.
- Lease release: separate archive PR after the feature PR merges.

# Launch checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-30T12:25:00+02:00
head: pending-task-commit
branch: feat/OTC-20260730-w7-entry-contract
pr: pending
status: claimed
required_main: 11a14721e1f3ef81e6bbab54cdfbb631d7ec81e0
proven:
  - W7 plan PR #101 and archive PR #102 are merged.
  - The planning task is absent from tasks/active and present in tasks/archive.
  - Open PRs #23, #48 and #97 own no W7 Rust contract, crate or shared integration path.
  - No active/open W7 worker exists at launch preflight.
  - Current Platform head is eda893990dccca6ffe65549e224f908299d90750.
  - Current Canary head is 292681e424b21bcf938ba204c86f17c864d95393.
  - The relevant selected Platform/Gateway and Canary contract paths have not changed since the accepted cuts.
  - The full W7 shared Cargo/document lease is granted to this lane.
derived:
  - W7-IDENTITY, W7-CANARY-ENTRY and W7-LOGIN-E2E remain blocked from public contract/final integration work until this producer merges and archives.
unknown:
  - implementation details and whether any new dependency is necessary; dependencies require exact primary evidence and current cargo-deny review.
conflicts: []
first_failure:
  marker: worker-implementation-not-started
  evidence: coordinator launch contains only the task record and branch; no worker package has been implemented.
changed_paths:
  - docs/agents/tasks/active/OTC-20260730-w7-entry-contract.md
validation: []
blockers: []
next_action: Worker attaches a unique local worktree, opens/updates the early draft PR, reads the exact merged W7_ENTRY_CONTRACT_AGENT prompt and implements only the owned producer package under the granted lease.
```
