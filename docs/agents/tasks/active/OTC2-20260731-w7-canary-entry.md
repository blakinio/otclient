---
task_id: OTC2-20260731-w7-canary-entry
project_lane: otclient-v2
status: in_progress
agent: "W7-CANARY-ENTRY worker"
track: greenfield-rust
workstream: transport-protocol-canary
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-CANARY-ENTRY
parallel_lane_state: active
phase: investigate
session_id: chat-github-20260731-w7-canary-entry-1
execution_mode: chat-github
execution_reason: GitHub DNS is unavailable in the sandbox; repository inspection and bounded writes use the connected GitHub API
lease_expires_at: 2026-07-31T09:57:00+02:00
branch: feat/OTC2-20260731-w7-canary-entry
base_branch: main
created: 2026-07-31T09:12:00+02:00
updated: 2026-07-31T09:12:00+02:00
last_verified_commit: "3c33f97fe2dca533d14a4284c3b13a7b6220a85d"
required_base_commit: "9ecc43a4465f6565bc1c12ea61f170a96edcbe35"
risk: high
related_pr: pending
depends_on:
  - W7 plan PR #101 merged as f7ddc2849838df05a95e4d7260bfe7c3359b4c8d
  - W7 plan archive PR #102 merged as 11a14721e1f3ef81e6bbab54cdfbb631d7ec81e0
  - W7 entry producer PR #104 merged as 9ecc43a4465f6565bc1c12ea61f170a96edcbe35
  - W7 entry lifecycle archive PR #105 merged as 8dcd353d5a9f19fabccf49508c27074f7749e3cf
  - current main 3c33f97fe2dca533d14a4284c3b13a7b6220a85d
integration_after:
  - W7-ENTRY-CONTRACT
owned_paths:
  - oteryn-client/crates/transport/**
  - oteryn-client/crates/protocol-core/**
  - oteryn-client/crates/protocol-canary/**
  - oteryn-client/contracts/canary/current-entry/**
  - oteryn-client/docs/research/technical-login/W7_CANARY_ENTRY_EVIDENCE.md
  - docs/agents/tasks/active/OTC2-20260731-w7-canary-entry.md
shared_path_lease:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/deny.toml
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
  - oteryn-client/docs/operations/RUST_WORKSPACE.md
contract_role: consumer-and-sole-w7-transport-admission-producer
contracts_consumed:
  - GameEntryRequest and AdmissionCredential from producer merge 9ecc43a4465f6565bc1c12ea61f170a96edcbe35
  - EntryLifecycle, EntryFailure and SessionEntered from producer merge 9ecc43a4465f6565bc1c12ea61f170a96edcbe35
  - Canary Current source at 95b276db311cf6e9acd58b847f1fb0ca6697b137, protocol paths unchanged since planning cut 4b2d6f432d92628c42bde1d95daed6ae0d0eb88f
contracts_produced:
  - bounded W7 transport interface
  - bounded protocol-core reader/writer and error categories
  - exact-evidence-gated Canary Current admission adapter
crates_touched:
  - transport
  - protocol-core
  - protocol-canary
cross_repo_tasks: []
---

# Goal

Implement the smallest bounded Rust TCP transport and Canary Current-profile admission boundary that consumes one moved W7 credential and can return only shared entry lifecycle outcomes. No gameplay is implemented.

# Preflight

- Current OTClient main is `3c33f97fe2dca533d14a4284c3b13a7b6220a85d`.
- W7-ENTRY-CONTRACT is merged and archived; exact producer merge is `9ecc43a4465f6565bc1c12ea61f170a96edcbe35`.
- Open PRs #23, #48 and #97 do not own Rust transport, protocol or W7 shared integration paths.
- W7-IDENTITY is merged and archived; its shared Cargo/document lease is released.
- Canary current main is `95b276db311cf6e9acd58b847f1fb0ca6697b137`.
- Comparing Canary planning cut `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f` to current main shows only documentation, agent tooling, catalog and OTBM changes; no network/protocol source path changed.
- Canary and Platform remain read-only.

# Boundaries

- Do not create substitute ENTRY identifiers, credential, lifecycle, failure or result types.
- Do not expose raw sockets or credentials to application code.
- Do not decode map, creature, item, chat, combat or general gameplay packets.
- Do not claim real Canary compatibility without exact named controlled admission evidence.
- If exact packet/fixture provenance is insufficient, keep the real adapter disabled and merge only bounded generic transport plus original synthetic protocol fixtures.
- No private captures, server secrets, credentials or proprietary assets may enter Git.

# Current evidence state

## PASS

- Producer contract and ownership are exact and merged.
- Current Canary protocol source is unchanged from the accepted planning cut.
- Exclusive paths and serialized shared-path lease are free.

## OBSERVED

- Canary Current is selected on the modern game port.
- Server source parses the Current login through the profile-owned login layout and uses sequence checksum for official/OTClient operating systems.

## UNKNOWN

- Complete source-path and function inventory for every Current framing, RSA, XTEA, compression and admission-denial branch.
- Public fixture provenance sufficient for committing exact real transcript bytes.
- Availability of a fresh configured credential and named deployed issuer for real Rust admission.

## BLOCKED

- `W7-BLOCK-REAL-RUST-E2E` until one exact configured Rust admission through `0x0F` is observed.
- `W7-BLOCK-DEPLOYMENT-EVIDENCE` for TLS, DNS, firewall, secret manager and deployed revision claims.

# Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-31T09:12:00+02:00
head: pending-task-record-commit
branch: feat/OTC2-20260731-w7-canary-entry
pr: pending
status: in_progress
phase: investigate
execution_mode: chat-github
last_completed_step: verified current main, producer merge, open-PR overlap, lease state and unchanged Canary protocol source cut
proven:
  - W7-CANARY-ENTRY is launchable and owns the exact planned paths.
  - Producer merge 9ecc43a4465f6565bc1c12ea61f170a96edcbe35 is present on current main.
  - Canary protocol source paths did not change between accepted cut and current main.
unknown:
  - exact complete Current wire evidence and permissible fixture provenance
blockers:
  - W7-BLOCK-REAL-RUST-E2E
  - W7-BLOCK-DEPLOYMENT-EVIDENCE
next_action: Complete exact Canary source inventory, then implement bounded transport and protocol-core with synthetic fixtures before enabling any real admission bytes.
```
