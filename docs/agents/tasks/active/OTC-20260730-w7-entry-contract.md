---
task_id: OTC-20260730-w7-entry-contract
status: in_progress
agent: "W7-ENTRY-CONTRACT worker"
track: greenfield-rust
workstream: account-session-world-directory-game-session
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-ENTRY-CONTRACT
parallel_lane_state: validation
coordinator_task: none
branch: feat/OTC-20260730-w7-entry-contract
base_branch: main
created: 2026-07-30T12:25:00+02:00
updated: 2026-07-30T13:00:00+02:00
last_verified_commit: "4ef46befd5d6a45b6f75137a1f3976c6134f0309"
required_base_commit: "11a14721e1f3ef81e6bbab54cdfbb631d7ec81e0"
risk: high
related_pr: "#104"
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
  - oteryn-foundation monotonic time contracts
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
  - existing foundation ManualClock, Moment, Deadline and MonotonicClock
  - existing architecture categories and workspace policy
  - exact accepted W7 type ownership
public_interfaces:
  - typed W7 entry/session/directory primitives and lifecycle
cross_repo_tasks: []
performance_evidence:
  - deterministic bounded state-transition tests only; no latency or compatibility claim
security_evidence:
  - credential non-Clone/redacted/move-once/terminal-drop overwrite properties
  - no credential persistence, logging, raw backend text, capture or external-repository write
---

# Goal

Implement the sole shared contract producer for W7 account-session, directory and one-shot game-entry lifecycle types. This lane does not implement OAuth/HTTP, transport, Canary protocol, application composition or real compatibility.

# Current implementation

- `oteryn-account-session` owns non-zero client-local `AccountSessionId`.
- `oteryn-world-directory` owns positive signed-64 identifiers, bounded authoritative summaries, deterministic ordering, duplicate/relation validation and explicit selection tied to one local directory revision.
- `oteryn-game-session` owns the attempt/request, opaque bounded credential, explicit one-shot admission move, typed lifecycle/failures/actions and non-secret `SessionEntered`.
- `W7_ENTRY_CONTRACT_EVIDENCE.md` documents every invariant and the exact first API calls expected from W7-IDENTITY, W7-CANARY-ENTRY and W7-LOGIN-E2E.
- No third-party dependency or `deny.toml` exception was added.

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
- `game-session` depends only on `account-session`, `world-directory` and merged lower `foundation` time contracts and owns `GameEntryRequest`, `GameEntryCredential`, `EntryFailure`, `SessionEntered` and lifecycle states.
- `GameEntryCredential` owns secret bytes, is non-`Clone`, redacts `Debug`/`Display`, is never serializable/persisted and moves exactly once into admission.
- Secret-buffer overwrite on Drop is a best-effort safe-Rust cleanup barrier, not a claim that compiler/runtime copies can never exist.
- `EntryFailure` is bounded, typed and stable; it contains no secret or raw backend/OS error text.
- No Platform DTO, OAuth message, HTTP client, transport interface, protocol opcode, packet enum or speculative multi-world/channel API may be added.

# Acceptance criteria

- [x] Create the three crates only in exclusive paths with architecture-valid dependency direction.
- [x] Produce every named public type exactly once; no substitute public contract exists.
- [x] Deterministically reject stale account/directory/entry generations.
- [x] Reject invalid selected world/character relationships.
- [x] Reject duplicate/late credential handoff, terminal reuse and replay.
- [x] Clear credential material on terminal lifecycle replacement/drop.
- [x] Add compile-fail non-`Clone` and runtime redacted-format/no-secret regressions.
- [x] Add focused unit tests for legal and illegal transitions and no mutation after rejection.
- [x] Update only lease-authorized Cargo and shared documentation paths.
- [x] Keep architecture-check policy, lint/unsafe policy and dependency-deny policy unchanged.
- [ ] Commit the generated pinned-toolchain `Cargo.lock` update.
- [ ] Exact-head locked metadata, `cargo fmt --check`, strict Clippy, all workspace tests, architecture check, cargo-deny and repository required CI pass.
- [ ] Complete changed-file/diff review and resolve every review thread.
- [ ] Revalidate/restack on current `main` if it advances before final validation.
- [ ] Merge through branch protection, then archive this task separately and release the full shared-path lease before downstream producer integration.

# Validation environment

The worker sandbox cannot resolve GitHub DNS and has no Rust toolchain, so it cannot attach a functional local checkout or run Cargo. Repository writes use the authenticated GitHub API and exact-head GitHub Actions are authoritative. This environment limitation does not waive any required check.

# Parallel-task answers

- Safe concurrency: no W7 sibling is launched; legacy/operational PRs own disjoint paths.
- Exclusive paths/contracts: exactly those declared in front matter and the accepted W7 plan.
- Shared paths: held exclusively by this task; all other tasks keep them read-only.
- Contract role: sole producer.
- Validation invalidation: any newer `main` changing foundation/test-support/workspace policy or the accepted W7 architecture invalidates prior full validation and requires restack/re-run.
- `integration_ready`: exclusive crates/tests complete while generated lockfile/CI integration is being finalized under this lane's lease.
- `blocked`: overlapping owner, changed external identifier width, architecture contradiction, dependency-policy failure or inability to prove redaction/one-shot semantics.
- Independent merge: yes, after its own exact-head gates; it must merge before every W7 consumer finalizes.
- Lease release: separate archive PR after the feature PR merges.

# Implementation checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-30T13:00:00+02:00
head: 4ef46befd5d6a45b6f75137a1f3976c6134f0309
branch: feat/OTC-20260730-w7-entry-contract
pr: 104
status: validation
required_main: 11a14721e1f3ef81e6bbab54cdfbb631d7ec81e0
proven:
  - W7 plan PR #101 and archive PR #102 are merged.
  - This lane remains the sole public W7 entry-contract producer and owns the full shared lease.
  - Three bounded crates and their focused tests are implemented without a new third-party dependency.
  - Credential and admission formatting is always redacted and ordinary cloning/serialization is absent.
  - Consumer API and migration notes are documented in the isolated evidence record.
derived:
  - W7-IDENTITY, W7-CANARY-ENTRY and W7-LOGIN-E2E can consume these APIs only after the exact producer feature merge and separate archive release.
unknown:
  - exact compiler/Clippy/test outcome until GitHub Actions completes on the final generated-lockfile head.
conflicts: []
first_failure:
  marker: local-toolchain-unavailable
  evidence: sandbox has no Rust toolchain and cannot resolve GitHub DNS; local Cargo validation is unavailable.
changed_paths:
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/tasks/active/OTC-20260730-w7-entry-contract.md
  - oteryn-client/Cargo.toml
  - oteryn-client/crates/account-session/**
  - oteryn-client/crates/world-directory/**
  - oteryn-client/crates/game-session/**
  - oteryn-client/docs/research/technical-login/W7_ENTRY_CONTRACT_EVIDENCE.md
validation:
  - GitHub Actions Rust Client run 30536380039 started on head 4ef46befd5d6a45b6f75137a1f3976c6134f0309.
  - GitHub Actions repository CI run 30536380283 started on the same head.
blockers:
  - generated Cargo.lock update and exact-head CI remain pending.
next_action: Finalize the generated lockfile, inspect exact CI failures, repair the implementation, then complete exact-head review and merge gates.
```
