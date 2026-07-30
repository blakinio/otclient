---
task_id: OTC-20260730-w7-identity
status: in_progress
agent: "W7-IDENTITY worker"
track: greenfield-rust
workstream: native-oauth-gateway
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-IDENTITY
parallel_lane_state: active
branch: feat/OTC-20260730-w7-identity
base_branch: main
created: 2026-07-30T21:45:00+02:00
updated: 2026-07-30T21:45:00+02:00
required_base_commit: "626c7954e6e6999bb4b8c8d051500b543e3c09e0"
required_producer_commit: "9ecc43a4465f6565bc1c12ea61f170a96edcbe35"
required_producer_archive_commit: "8dcd353d5a9f19fabccf49508c27074f7749e3cf"
workspace_repair_commit: "9e580a0fa615cc0e42f70c9d76395cf5a9fd0238"
workspace_repair_archive_commit: "626c7954e6e6999bb4b8c8d051500b543e3c09e0"
platform_revision: "55ba8840a7de6556b6b173f587179f986a5a68e1"
risk: high
related_pr: pending
owned_paths:
  - oteryn-client/crates/platform/**
  - oteryn-client/crates/identity/**
  - oteryn-client/tests/security/auth/**
  - oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md
  - docs/agents/tasks/active/OTC-20260730-w7-identity.md
shared_path_lease:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/deny.toml
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
  - oteryn-client/docs/operations/RUST_WORKSPACE.md
contract_role: consumer
contracts_produced:
  - bounded Platform OAuth/ticket/Gateway protocol-v1 adapter surface
  - bounded Identity PKCE/loopback transaction service
contracts_consumed:
  - AccountSessionId
  - CharacterId
  - WorldId
  - DirectoryRevision
  - GameEntryCredential
  - merged W7 directory and entry lifecycle contracts
  - Platform native OAuth merge 27fa277c5def0e151d7ee013acef188dbfd6f463
  - Platform ticket merge cab00c140ce200e3cd51b7eafe2c1659842c2b90
  - Platform Gateway merge 8006534108d835474dadd208b0ec934e4a12528b
  - Platform hardening merge 53158217a6c6017230301cf4daa783b04fcc13d5
blockers:
  - exact deployed OAuth client ID, URLs, TLS/network reachability and secret injection remain external
  - real Windows browser-return evidence remains interactive
---

# Goal

Implement the bounded Rust native Identity -> Game Login Ticket -> Gateway protocol-v1 consumer for W7 without redefining producer-owned contracts.

# Launch proof

- W7 plan and archive are merged.
- W7-ENTRY-CONTRACT merged as `9ecc43a4465f6565bc1c12ea61f170a96edcbe35` and archived as `8dcd353d5a9f19fabccf49508c27074f7749e3cf`.
- The post-merge workspace regression was repaired by PR #108 and archived by PR #109; the Cargo/shared-document lease is free.
- No active PR or branch owns `crates/platform`, `crates/identity` or `tests/security/auth`.
- PR #23 is legacy OTUI/Lua presentation only, #48 is isolated operational non-merge work, and #97 is a legacy asset rehearsal.
- Platform current head `55ba8840a7de6556b6b173f587179f986a5a68e1` is six commits ahead of the planning cut only in UX/portal/testing paths; no OAuth, ticket or Gateway contract path changed.

# Required scope

- PKCE `S256` with CSPRNG state and verifier;
- bind IPv4 `127.0.0.1:0` before browser launch and use the actual assigned port;
- injected hardened system-browser adapter;
- exact callback path, loopback peer, state, generation, stale and duplicate validation;
- bounded authorization-code token exchange;
- one Game Login Ticket issuance with no duplicate retry;
- strict Gateway protocol-v1 request/response parsing;
- reject unknown/trailing/oversized JSON, redirects, invalid protocol version, IDs, ports, duplicates and world/character relations;
- convert raw DTOs only into merged ENTRY types;
- clear verifier, code, access/refresh token and ticket at terminal boundaries;
- no password collection, password fallback, async runtime, persistence or production compatibility claim.

# Exact external surface

- authorization: `/oauth/authorize`;
- token: `/oauth/token`;
- scope: `game:ticket`;
- callback base: `http://127.0.0.1/callback`, dynamic port accepted;
- ticket: `POST /api/v1/game-auth/tickets`, body `{"protocol_version":1}`;
- Gateway: `POST /v1/login`, body `{"protocol_version":1,"game_login_ticket":"..."}`;
- Gateway success: `protocol_version`, `session { credential, expires_at }`, `worlds[] { id, slug, name, region, host, port }`, `characters[] { id, name, level, vocation, world_id }`.

# Acceptance criteria

- [ ] one active task, branch and draft PR only;
- [ ] no substitute ENTRY public types;
- [ ] focused fake browser/listener/HTTP tests cover success and all required rejection/cleanup paths;
- [ ] dependency versions/features/licenses/advisories are pinned and reviewed for Rust 1.94;
- [ ] exact-head locked metadata, fmt, strict Clippy, all tests/doctests, architecture policy and cargo-deny pass;
- [ ] full diff and review-thread checks pass;
- [ ] merge through gates and archive separately.
