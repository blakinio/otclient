---
task_id: OTC-20260729-synthetic-asset-schema-compiler
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R09
parallel_wave: OTERYN-W6-SYNTHETIC-ASSETS
parallel_lane: W6-ASSET
parallel_lane_state: active
branch: feat/OTC-20260729-synthetic-asset-schema-compiler
base_branch: main
created: 2026-07-29T20:05:00+02:00
updated: 2026-07-29T20:05:00+02:00
last_verified_commit: "8094d9075fecd7b7c3de0d1b0eb400207a839776"
required_base_commit: "8094d9075fecd7b7c3de0d1b0eb400207a839776"
risk: medium
related_pr: pending
depends_on:
  - W6 plan PR #90 and archive PR #91
  - foundation asset/licensing audit PR #47
owned_paths:
  - oteryn-client/crates/asset-types/**
  - oteryn-client/tools/asset-compiler/**
  - oteryn-client/assets/test-fixtures/synthetic-v1/**
  - oteryn-client/docs/research/assets/W6_FORMAT_AND_SECURITY_EVIDENCE.md
  - docs/agents/tasks/active/OTC-20260729-synthetic-asset-schema-compiler.md
shared_path_lease:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/deny.toml
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
  - oteryn-client/docs/operations/RUST_WORKSPACE.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
contract_role: producer
contracts_produced:
  - normalized synthetic asset schema v1
  - deterministic synthetic asset pack v1
  - bounded offline synthetic asset compiler
contracts_consumed:
  - accepted W6 plan
  - workspace architecture and supply-chain policy
crates_touched:
  - oteryn-asset-types
  - oteryn-asset-compiler
features_touched:
  - typed synthetic asset IDs and metadata
  - deterministic pack encode/decode
  - safe manifest-root file ingestion
contracts_touched:
  - new asset-types public API
  - new asset-compiler CLI and library API
modules_touched: []
reuses:
  - exact workspace serde_json 1.0.145
  - architecture categories asset-types and tool
  - existing Rust lints, exact-head Windows CI and cargo-deny
public_interfaces:
  - AssetId
  - AssetKind
  - AssetMetadata
  - AssetRecord
  - AssetPack
  - AssetError
  - compile_manifest
  - CompilerError
cross_repo_tasks: []
performance_evidence:
  - synthetic limits only; no production size, throughput or runtime claim
security_evidence:
  - original synthetic fixtures only; strict path, symlink, containment, size and arithmetic validation
---

# Goal

Implement the single authorized W6 synthetic asset schema/compiler slice as exactly two Rust packages, with deterministic bounded pack encoding and strict offline filesystem safety.

# Launch preflight

- [x] `main` is exactly `8094d9075fecd7b7c3de0d1b0eb400207a839776`.
- [x] W6 plan PR #90 and archive PR #91 are merged.
- [x] W1-W5 are closed and not launchable.
- [x] PR #23 remains legacy OTUI/Lua only; PR #48 remains isolated operational non-merge work.
- [x] No active task or open PR owns the W6 package paths, schema/compiler contract or shared integration paths.
- [x] This task holds the unique W6 Cargo/lockfile/shared-document lease.
- [x] Architecture checker source/rules/fixtures, Rust toolchain and CI remain read-only.

# Authorized implementation

- `oteryn-asset-types`, category `asset-types`;
- `oteryn-asset-compiler`, category `tool`, consuming asset-types;
- synthetic blobs and validated RGBA8 only;
- manifest and pack schema v1;
- SHA-256 payload digests;
- deterministic ordering and little-endian bounded encoding;
- strict decode/validation and negative tests;
- constrained relative manifest-root sources with absolute, parent, separator escape, symlink, containment, directory and special-file rejection;
- same-directory temporary output and final rename without partial final replacement.

# Explicit exclusions

No asset runtime, mounting, streaming, cache, activation, renderer/GPU integration, image decoder, archive/compression, real Tibia/Canary importer, proprietary input, download/updater, signing, authenticated manifest, protocol, identity, networking, UI, audio, localization, domain, feature or external-repository work.

# Acceptance criteria

- [ ] Exactly two packages and original synthetic fixtures implemented.
- [ ] Every schema/string/count/payload/pack/dimension/path limit is checked.
- [ ] Deterministic, malformed-input, digest, RGBA8 and filesystem security tests pass.
- [ ] Cargo/lockfile/docs are integrated under the unique lease without policy weakening.
- [ ] Evidence document distinguishes automated proof from production/runtime/legal blockers.
- [ ] Complete changed-file and full-diff review passes.
- [ ] Exact-head Rust Client and repository required CI pass.
- [ ] PR squash-merges and the task archives separately.

# Current state

- Worker branch and lease created from exact authorized base.
- Implementation and draft PR pending.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Shared-path lease: active
- Archived at: pending
