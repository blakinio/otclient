# W7-ENTRY-CONTRACT Worker Prompt

```text
Work autonomously in repository blakinio/otclient as lane W7-ENTRY-CONTRACT for wave OTERYN-W7-TECHNICAL-LOGIN.

Do not start unless the W7 planning PR and its separate archive are merged and the coordinator confirms exact current main, no overlapping owner and the shared-path lease.

Read root/nested AGENTS.md, docs/agents/README.md, CONTEXT_HANDOFF.md, oteryn-client PROGRAM/WORKSTREAMS/MULTI_AGENT_EXECUTION/CURRENT_PARALLEL_WAVE, architecture/lifecycle/security/repository-layout docs, foundation audits, current tasks/PRs/reviews/CI and exact Platform/Gateway evidence.

Create one unique task, branch, worktree and early draft PR. Record exact base and lease state.

Contract role: sole producer.

Exclusive paths:
- oteryn-client/crates/account-session/**
- oteryn-client/crates/world-directory/**
- oteryn-client/crates/game-session/**
- oteryn-client/docs/research/technical-login/W7_ENTRY_CONTRACT_EVIDENCE.md

Only this lane may produce:
- AccountSessionId
- CharacterId
- WorldId
- GameplayChannelId
- DirectoryRevision
- GameEntryRequest
- GameEntryCredential
- EntryFailure
- SessionEntered
- public entry lifecycle states

Required dependency direction:
- account-session owns AccountSessionId;
- world-directory owns CharacterId, WorldId, GameplayChannelId and DirectoryRevision;
- game-session depends on account-session and world-directory and owns request/credential/failure/result/lifecycle;
- no dependency on identity, platform, transport or protocol crates.

Required semantics:
- AccountSessionId is client-local opaque generation/correlation, not an external identity/account/bearer value.
- CharacterId and WorldId preserve Gateway protocol-v1 signed 64-bit JSON identifiers and reject invalid narrowing.
- DirectoryRevision is a client-local validated-directory generation because Gateway v1 has no revision field.
- GameplayChannelId is opaque but unused/unserialized for W7's one-exact-issuer flow.
- GameEntryCredential owns secret material, is non-Clone, redacts Debug/Display, cannot be serialized/persisted and is consumed by move exactly once.
- EntryFailure is typed, bounded, stable and never contains raw backend/OS text or secret.
- SessionEntered contains only non-secret typed admission evidence needed by composition.
- lifecycle rejects stale generations, invalid world-character relationships, duplicate credential handoff, terminal reuse and replay; terminal paths clear credential material.

Do not define Platform DTOs, OAuth messages, HTTP clients, transport interfaces, protocol opcodes or speculative multi-world/channel APIs.

Shared-path lease, only when granted:
- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- oteryn-client/deny.toml
- docs/agents/MODULE_CATALOG.md
- docs/agents/BUILD_TEST_MATRIX.md
- docs/agents/CHANGELOG.md
- oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
- oteryn-client/docs/operations/RUST_WORKSPACE.md

Manual Cargo.lock conflict resolution is prohibited. If the lease is unavailable, finish exclusive work, mark integration_ready and wait.

Evidence:
- focused unit/property tests for generations, stale/replay/duplicate/invalid-selection transitions;
- compile-time/non-Clone and redacted-format tests for credentials;
- no secret in snapshots, panic text or errors;
- locked metadata, cargo fmt --check, strict Clippy, all workspace tests, architecture check, cargo-deny and repository CI on exact head;
- complete diff review and no unresolved threads.

Do not claim external compatibility. Merge through gates, then let the coordinator create a separate archive PR before downstream finalization.
```
