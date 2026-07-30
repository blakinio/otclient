---
task_id: OTC-20260730-w7-identity
status: ready_for_review
agent: "W7-IDENTITY worker"
track: greenfield-rust
workstream: native-oauth-gateway
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-IDENTITY
parallel_lane_state: ready_for_review
branch: feat/OTC-20260730-w7-identity
base_branch: main
created: 2026-07-30T21:45:00+02:00
updated: 2026-07-30T23:00:00+02:00
validated_implementation_head: "99b28f3cfccb03f798f08c3b186737f0d274c575"
required_base_commit: "626c7954e6e6999bb4b8c8d051500b543e3c09e0"
required_producer_commit: "9ecc43a4465f6565bc1c12ea61f170a96edcbe35"
required_producer_archive_commit: "8dcd353d5a9f19fabccf49508c27074f7749e3cf"
workspace_repair_commit: "9e580a0fa615cc0e42f70c9d76395cf5a9fd0238"
workspace_repair_archive_commit: "626c7954e6e6999bb4b8c8d051500b543e3c09e0"
platform_revision: "55ba8840a7de6556b6b173f587179f986a5a68e1"
risk: high
related_pr: "#110"
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
  - exact deployed OAuth client ID, Identity/Gateway URLs, TLS/DNS/firewall state and secret injection remain external
  - real Windows browser launch/return against a configured producer remains interactive
  - exact deployed cross-repository Identity -> Gateway -> Canary E2E remains unproven
  - current token-family revocation bounds W7 to one bootstrap attempt
  - Gateway v1 does not expose general multi-world issuer or gameplay-channel routing
---

# Goal

Implement the bounded Rust native Identity -> Game Login Ticket -> Gateway protocol-v1 consumer for W7 without redefining producer-owned contracts.

# Launch proof

- W7 plan and archive are merged.
- W7-ENTRY-CONTRACT merged as `9ecc43a4465f6565bc1c12ea61f170a96edcbe35` and archived as `8dcd353d5a9f19fabccf49508c27074f7749e3cf`.
- The post-merge workspace regression was repaired by PR #108 and archived by PR #109; the Cargo/shared-document lease was free at launch.
- No active PR or branch owned `crates/platform`, `crates/identity` or `tests/security/auth`.
- PR #23 is legacy OTUI/Lua presentation only, #48 is isolated operational non-merge work, and #97 is a legacy asset rehearsal.
- Platform head `55ba8840a7de6556b6b173f587179f986a5a68e1` advanced from the planning cut only in UX/portal/testing paths; no inspected OAuth, ticket or Gateway contract path changed.

# Implemented result

## Platform boundary

- explicit Identity/Gateway base URLs with HTTPS required outside loopback;
- synchronous Ureq adapter using `NativeTls` and `PlatformVerifier` for normal system certificate/hostname validation;
- redirects, environment proxy discovery and automatic retries disabled;
- bounded timeout, response headers and response body;
- exact OAuth token, Game Login Ticket and Gateway protocol-v1 requests;
- strict content type, no-store/no-cache, unknown-field and trailing-data validation;
- signed-64 IDs, positive port, duplicate identifier and character/world relation validation;
- raw DTO conversion only into merged ENTRY `AccountDirectorySnapshot` and `GameEntryCredential`.

## Identity transaction

- CSPRNG state/verifier and RFC PKCE `S256`;
- IPv4 `127.0.0.1:0` bind before browser launch;
- exact assigned port in authorization and token exchange;
- direct system-browser process argument without shell interpolation;
- bounded callback parser with exact path, IPv4 loopback peer, state, active generation, stale and duplicate checks;
- callback request target has no ordinary `Clone` or revealing `Debug` surface;
- cancellation/generation checks before and between one-shot stages;
- one non-retried ticket issuance and one Gateway login;
- refresh-token discard and terminal secret cleanup;
- no password collection/fallback, embedded browser, async runtime, persistence, UI or Canary packet implementation.

# Automated evidence

Synthetic tests cover:

- RFC PKCE vector and independent state/verifier material;
- bind-before-launch and dynamic callback port propagation;
- complete fake browser/listener/HTTP success with exactly three requests;
- callback state, peer, path, generation, duplicate, malformed, timeout and cancellation negatives;
- callback code/state debug redaction;
- unknown/trailing JSON, redirect, missing cache policy and oversized body rejection;
- unsupported Gateway protocol version;
- duplicate world ID, invalid port and unknown character/world relation;
- stale generation without network work;
- access/code/ticket/session credential redaction;
- conversion only into merged ENTRY types.

All fixtures are synthetic. No production credential, account, private capture or proprietary material is present.

# Dependency review

- exact versions and features are committed in `Cargo.lock` generated by Cargo `1.94.0`;
- `base64`, `getrandom`, `serde`, `time`, `url` and Ureq native TLS are the bounded new graph;
- no wildcard, Git or unknown-registry dependency was introduced;
- cargo-deny permits no new license class;
- one exact documented `windows-sys 0.61.2` duplicate branch is allowed for native-tls/SChannel beside the existing winit `windows-sys 0.52` branch;
- no manual `Cargo.lock` conflict resolution occurred.

# Validation evidence

Exact implementation/documentation head `99b28f3cfccb03f798f08c3b186737f0d274c575` passed:

- Rust Client run `30581250441`;
- Windows job `91001745775`: locked metadata, formatting, strict Clippy, all workspace tests/doctests and architecture policy succeeded;
- supply-chain job `91001745838`: advisories, licenses, bans and sources succeeded;
- repository CI run `30581251450`;
- `CI / Required` job `91002362697`: succeeded;
- complete 17-path diff review;
- no requested reviews, review submissions or unresolved review threads;
- no temporary workflow, substitute ENTRY contract, credential, private capture or proprietary artifact in the final diff.

This checkpoint commit changes only the task record. Its exact-head draft-state and ready-state checks remain required before merge.

# Acceptance criteria

- [x] one active task, branch and draft PR only;
- [x] no substitute ENTRY public types;
- [x] focused fake browser/listener/HTTP tests cover success and required rejection/cleanup paths;
- [x] dependency versions/features/licenses/advisories are pinned and reviewed for Rust 1.94;
- [x] implementation/documentation head passed locked metadata, fmt, strict Clippy, all tests/doctests, architecture policy and cargo-deny;
- [x] full diff and review-thread checks passed;
- [ ] checkpoint exact-head CI, ready-state CI, merge and separate archive remain.
