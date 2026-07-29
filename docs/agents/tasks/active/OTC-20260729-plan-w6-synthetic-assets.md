---
task_id: OTC-20260729-plan-w6-synthetic-assets
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W6-SYNTHETIC-ASSETS
parallel_lane: W6-C
parallel_lane_state: active
branch: docs/OTC-20260729-plan-w6-synthetic-assets
base_branch: main
created: 2026-07-29T19:43:00+02:00
updated: 2026-07-29T19:43:00+02:00
last_verified_commit: "0aa75744a1cad0fad987f56545088f54b9adc098"
required_base_commit: "0aa75744a1cad0fad987f56545088f54b9adc098"
risk: low
related_pr: pending
depends_on:
  - W5 renderer surface PR #86 and archive PR #87
  - W5 closure PR #88 and archive PR #89
owned_paths:
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/NEXT_SYNTHETIC_ASSET_AGENT.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260729-plan-w6-synthetic-assets.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - completed W5 renderer boundary
  - foundation asset/licensing audit
  - existing asset-types architecture category and WS-R09 ownership
crates_touched: []
features_touched: []
contracts_touched:
  - W6 launch authorization and worker routing only
modules_touched: []
reuses:
  - existing exact serde_json workspace dependency
  - existing architecture checker asset-types and tool categories
  - existing Rust workspace, lints and cargo-deny policy
public_interfaces:
  - coordination documentation only
cross_repo_tasks: []
performance_evidence:
  - no production asset-size, compiler-throughput or runtime-performance claim
security_evidence:
  - synthetic/original fixtures only; no proprietary bytes, secrets, network input or external-repository writes
---

# Goal

Accept one bounded W6 plan for a normalized synthetic asset schema and deterministic compiler slice after W5 closed, without starting implementation, claiming a lease or defining a production-compatible asset pack.

# Live preflight

- `main` is exactly `0aa75744a1cad0fad987f56545088f54b9adc098`.
- W1-W5 are merged, archived and not launchable.
- Open PR #23 owns legacy OTUI/Lua presentation only.
- Open PR #48 is isolated operational non-merge work.
- No active Rust task or open PR owns `crates/asset-types`, `tools/asset-compiler`, the normalized asset schema, Cargo/lockfile integration or the future W6 shared-document lease.
- Architecture checker already recognizes categories `asset-types` and `tool`; no checker/rule/fixture change is required by the planned slice.
- Workspace Rust is 1.94; `serde_json = "=1.0.145"` is already an exact workspace dependency and passed current cargo-deny.
- Primary crate evidence reviewed on 2026-07-29 supports candidate `sha2 0.11.0`, MIT OR Apache-2.0, Rust 1.85; the worker must revalidate exact source/features/advisories and cargo-deny before adoption.

# Proposed accepted wave

Exactly one implementation lane `W6-ASSET` after this plan and its separate archive merge.

The worker may add exactly two packages:

1. `oteryn-asset-types` under `oteryn-client/crates/asset-types/`, category `asset-types`;
2. `oteryn-asset-compiler` under `oteryn-client/tools/asset-compiler/`, category `tool`, consuming `oteryn-asset-types`.

The implementation must remain one independently mergeable work package. No secondary worker or research lane is authorized.

# Bounded contract

The slice may define:

- non-zero typed `AssetId` and a closed first-slice `AssetKind` limited to synthetic binary blobs and tightly validated RGBA8 images;
- manifest schema version 1 and original pack schema version 1;
- explicit license/provenance text, dimensions where applicable and SHA-256 content digests;
- deterministic record ordering and deterministic little-endian length-delimited pack encoding;
- a strict decoder/validator for round-trip and malformed-input tests, not runtime mounting;
- one CLI compiler accepting a constrained JSON manifest and relative source paths under the manifest root;
- stable non-secret error kinds without absolute paths or arbitrary operating-system error text.

Synthetic acceptance limits must be explicit and checked, including at least:

- maximum 4096 records;
- maximum 16 MiB source payload per record;
- maximum 64 MiB compiled pack;
- maximum 16,384 pixels per image dimension;
- checked `width * height * 4` for RGBA8;
- bounded logical names, license identifiers and provenance text;
- duplicate ID rejection and deterministic sorting independent of manifest order.

These are schema-v1 synthetic engineering limits, not production budgets or compatibility claims.

# Input and filesystem safety

The compiler must:

- accept relative normalized paths only;
- reject absolute, root, prefix and parent-directory components;
- reject symlinks in the source path chain;
- prove the final source remains within the manifest root;
- reject directories and special files;
- bound file reads before allocation and use checked arithmetic;
- write deterministic output without embedding source-machine absolute paths;
- use a same-directory temporary output and rename only for compiler-output integrity, not runtime activation.

Archives, decompression, scripts, network downloads and recursive directory discovery are excluded from W6.

# Dependency candidates

- reuse exact workspace `serde_json = "=1.0.145"` for constrained manifest parsing;
- candidate exact `sha2 = "=0.11.0"` with default features disabled for SHA-256 only;
- no CLI framework, async runtime, archive, image-decoding, compression, signing or filesystem-watcher dependency.

The generated lockfile and exact cargo-deny advisories/licenses/bans/sources are authoritative. The worker may reject `sha2` or amend the plan through a blocker record; it may not weaken policy.

# Required tests

- typed ID and metadata validation;
- known SHA-256 vector;
- deterministic byte-identical output across repeated builds and shuffled manifest order;
- encode/decode round trip;
- duplicate IDs and unknown kind/schema rejection;
- malformed, truncated, trailing, oversized and count/length/offset overflow cases;
- RGBA8 dimension/payload mismatch and arithmetic overflow;
- absolute, parent, prefix, backslash-escape and symlink path rejection on supported platforms;
- source outside root, directory and special-file rejection;
- bounded output failure before partial final-file replacement;
- output contains no absolute source path.

# Exclusive worker paths

- `oteryn-client/crates/asset-types/**`
- `oteryn-client/tools/asset-compiler/**`
- `oteryn-client/assets/test-fixtures/synthetic-v1/**`
- `oteryn-client/docs/research/assets/W6_FORMAT_AND_SECURITY_EVIDENCE.md`

# Future shared-path lease

Only W6-ASSET may claim, after the plan archive merges:

- `oteryn-client/Cargo.toml`
- `oteryn-client/Cargo.lock`
- `oteryn-client/deny.toml` only for a narrowly evidenced license clarification if required
- `oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md`
- `oteryn-client/docs/operations/RUST_WORKSPACE.md`
- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `docs/agents/CHANGELOG.md`

Architecture checker source/rules/fixtures, Rust toolchain and CI workflows remain read-only unless an independently recorded blocker proves a separate change is required.

# Explicit exclusions

No asset-runtime package, runtime mounting/streaming/cache, renderer or GPU integration, texture atlas/array decision, image decoder, real Tibia/Canary importer, proprietary fixture, updater/download, signing, authenticated manifest, protocol, identity, UI, audio, localization, game-domain or external-repository work.

No production pack, legal redistribution, compatibility, security-signature or performance claim is authorized.

# Acceptance criteria

- [x] Fresh live preflight and ownership check completed.
- [ ] Current wave, coordinator routing, worker prompt and README consistently authorize exactly one W6 worker only after plan archive.
- [ ] Plan changes exactly five documentation paths.
- [ ] No implementation, dependency, lease, source, Cargo, lockfile, CI or asset byte is added.
- [ ] Exact-head required CI passes; plan merges and archives independently.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Shared-path lease: none
- Worker launch: prohibited until plan archive merge and fresh overlap check
