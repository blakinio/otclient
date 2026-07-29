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
updated: 2026-07-29T20:31:00+02:00
last_verified_commit: "845a56a7dd23dd5917a9d1147be2586f980b3fd5"
required_base_commit: "8094d9075fecd7b7c3de0d1b0eb400207a839776"
risk: medium
related_pr: "#92"
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

- [x] `main` was exactly `8094d9075fecd7b7c3de0d1b0eb400207a839776` at worker launch.
- [x] W6 plan PR #90 and archive PR #91 are merged.
- [x] W1-W5 are closed and not launchable.
- [x] PR #23 remains legacy OTUI/Lua only; PR #48 remains isolated operational non-merge work.
- [x] No active task or open PR owns the W6 package paths, schema/compiler contract or shared integration paths.
- [x] This task holds the unique W6 Cargo/lockfile/shared-document lease.
- [x] Architecture checker source/rules/fixtures, Rust toolchain and permanent CI remain read-only.

# Delivered implementation

- `oteryn-asset-types`, category `asset-types`;
- `oteryn-asset-compiler`, category `tool`, consuming asset-types;
- non-zero typed IDs, closed synthetic blob/RGBA8 kinds and bounded metadata;
- manifest schema v1 and original deterministic little-endian pack schema v1;
- SHA-256 payload digests and canonical sorting independent of manifest order;
- strict decoder/validator for malformed, truncated, trailing, non-canonical and digest-invalid data;
- explicit checked limits for records, strings, payloads, pack bytes and RGBA8 dimensions;
- constrained relative manifest-root sources with absolute, parent, prefix, separator escape, symlink, canonical-containment, directory and non-regular-file rejection;
- same-directory `create_new` temporary output, sync and final rename without replacing an existing final file;
- original synthetic manifest, blob and raw 2x2 RGBA8 fixtures with documented provenance.

# Explicit exclusions

No asset runtime, mounting, streaming, cache, activation, renderer/GPU integration, image decoder, archive/compression, real Tibia/Canary importer, proprietary input, download/updater, signing, authenticated manifest, protocol, identity, networking, UI, audio, localization, domain, feature or external-repository work.

# Acceptance criteria

- [x] Exactly two packages and original synthetic fixtures implemented.
- [x] Every schema/string/count/payload/pack/dimension/path limit is checked.
- [x] Deterministic, malformed-input, digest, RGBA8 and filesystem security tests pass on the validated implementation head.
- [x] Cargo/lockfile/docs are integrated under the unique lease without policy weakening.
- [x] Evidence document distinguishes automated proof from production/runtime/legal blockers.
- [x] Current changed-file inventory is exactly 18 authorized paths with no workflow, toolchain, architecture-checker, `deny.toml` or `REPOSITORY_LAYOUT.md` change.
- [ ] Complete final synchronized full-diff review passes.
- [ ] Exact-head Rust Client and repository required CI pass after this task synchronization.
- [ ] PR squash-merges and the task archives separately.

# Validation history

- Rust run `30478218458` proved the predecessor lock was stale.
- Temporary generator run `30478760455` generated and committed the exact lock on Rust 1.94/Windows; the temporary workflow was then deleted and is absent from the PR diff.
- Rust run `30478907534` passed locked metadata and Supply Chain but found only mechanical rustfmt differences.
- A temporary Rust 1.94 formatter applied exact `cargo fmt --all`; its workflow was then deleted and is absent from the PR diff.
- Rust run `30479263818` passed locked metadata, formatting, Clippy and Supply Chain; one test helper encoded a backslash path as invalid JSON before path validation.
- The helper now serializes source values through `serde_json`, so the portable path test reaches the intended validator.
- Rust run `30479573355` on implementation head `142a0b657d128d9e26b1a54c4f768a75aa722673` passed locked metadata, formatting, Clippy, all workspace tests, architecture policy and Supply Chain. Windows job `90669816067` and Supply Chain job `90669816059` succeeded.
- Required evidence and integration documentation were added after that run, so final exact-head validation is pending on the synchronized task head.

# Final scope before exact-head validation

Exactly 18 paths:

1. `docs/agents/BUILD_TEST_MATRIX.md`
2. `docs/agents/CHANGELOG.md`
3. `docs/agents/MODULE_CATALOG.md`
4. `docs/agents/tasks/active/OTC-20260729-synthetic-asset-schema-compiler.md`
5. `oteryn-client/Cargo.lock`
6. `oteryn-client/Cargo.toml`
7. `oteryn-client/assets/test-fixtures/synthetic-v1/blob.txt`
8. `oteryn-client/assets/test-fixtures/synthetic-v1/checker.rgba`
9. `oteryn-client/assets/test-fixtures/synthetic-v1/manifest.json`
10. `oteryn-client/crates/asset-types/Cargo.toml`
11. `oteryn-client/crates/asset-types/src/lib.rs`
12. `oteryn-client/crates/asset-types/tests/pack.rs`
13. `oteryn-client/docs/operations/RUST_WORKSPACE.md`
14. `oteryn-client/docs/research/assets/W6_FORMAT_AND_SECURITY_EVIDENCE.md`
15. `oteryn-client/tools/asset-compiler/Cargo.toml`
16. `oteryn-client/tools/asset-compiler/src/lib.rs`
17. `oteryn-client/tools/asset-compiler/src/main.rs`
18. `oteryn-client/tools/asset-compiler/tests/compiler.rs`

# Preserved blockers

Automated synthetic compiler evidence does not prove real Tibia/Canary format compatibility, redistribution rights, production import, runtime mounting/streaming, renderer/GPU behavior, authenticated manifests/signing, updater/download security, production limits, throughput, memory or hardware compatibility.

# Completion

- Final status: in progress
- PR: #92
- Merge commit: pending
- Shared-path lease: active
- Archived at: pending
