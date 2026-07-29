# Current Parallel Agent Wave

Status: accepted launch plan  
Wave ID: `OTERYN-W6-SYNTHETIC-ASSETS`  
Evidence cut: `main` `0aa75744a1cad0fad987f56545088f54b9adc098`

Live Git, active tasks and open PRs remain authoritative. W1-W5 are completed, archived and not launchable. This plan authorizes exactly one W6 implementation lane only after the W6 plan PR and its separate lifecycle archive merge.

## 1. Confirmed transition state

- W1 foundation primitives are merged/archived and must not be relaunched.
- Every W2 implementation/evidence lane is merged/archived and must not be relaunched.
- W3 deterministic test support is merged/archived and must not be relaunched.
- W4 Windows application shell is merged/archived and must not be relaunched.
- W5 renderer surface ownership is merged/archived and must not be relaunched.
- Every prior Cargo, lockfile, dependency-policy, integration and shared-document lease is released.
- Open PR #23 owns legacy OTUI/Lua presentation only; PR #48 is isolated operational non-merge work.
- No active Rust task or open PR owns `crates/asset-types`, `tools/asset-compiler`, the normalized asset schema/compiler contract or its shared integration paths.
- Architecture checker already recognizes categories `asset-types` and `tool`; no checker/rule/fixture change is needed.

## 2. Objective

Implement one bounded normalized synthetic asset schema and deterministic compiler slice that proves typed IDs, validated metadata, content hashing, deterministic pack encoding and safe relative-file ingestion without beginning runtime asset mounting, renderer integration or real game import.

The wave uses:

```text
1 coordinator
1 implementation worker
```

No secondary implementation or research lane is authorized.

## 3. Dependency graph

```text
foundation asset/licensing audit (#47)
merged workspace/architecture policy (#50/#53)
completed renderer boundary (#86/#87)
closed W5 (#88/#89)
          |
          v
W6-ASSET synthetic schema/compiler slice
```

## 4. Lane W6-C — Coordinator

Prompt: `prompts/COORDINATOR_AGENT.md`

Responsibilities:

- verify exact live ownership, base and merged plan lifecycle before worker launch;
- prevent every W1-W5 relaunch and prevent a second asset schema producer;
- grant one Cargo/lockfile/dependency-policy/shared-document lease only to W6-ASSET;
- require exact dependency, deterministic-format, filesystem-security, Windows workspace, architecture, supply-chain and repository CI evidence;
- require explicit synthetic-versus-production evidence classification;
- merge/archive the worker independently;
- close W6 and record exactly one next bounded recommendation.

The coordinator does not implement the asset worker while preparing or closing the wave.

## 5. Lane W6-ASSET — Synthetic asset schema/compiler

Prompt: `prompts/NEXT_SYNTHETIC_ASSET_AGENT.md`

Workstream: WS-R09 assets and tooling  
Contract role: producer

Required merged producers/evidence:

```text
foundation asset/licensing audit: PR #47
workspace/architecture policy: PR #50 / archive #53
renderer boundary: PR #86 / archive #87
W5 closure: PR #88 / archive #89
W6 plan/archive: current main at worker preflight
```

Purpose:

- add `oteryn-asset-types` under `oteryn-client/crates/asset-types/`, category `asset-types`;
- add `oteryn-asset-compiler` under `oteryn-client/tools/asset-compiler/`, category `tool`, depending on `oteryn-asset-types`;
- define non-zero typed `AssetId` and a closed first-slice `AssetKind` limited to synthetic binary blobs and validated RGBA8 images;
- define manifest schema version 1 and an original deterministic pack schema version 1;
- store bounded logical metadata, license/provenance text and SHA-256 payload digests;
- compile one constrained JSON manifest plus relative source files into one deterministic pack;
- expose a strict decoder/validator for tooling/tests only;
- use only original synthetic fixtures with documented provenance.

Required design boundaries:

- maximum 4096 records, 16 MiB payload per record and 64 MiB compiled pack;
- maximum 16,384 pixels per RGBA8 dimension with checked `width * height * 4`;
- checked count, length, offset and allocation arithmetic;
- deterministic sorting independent of manifest order;
- original little-endian length-delimited encoding;
- stable non-secret error kinds without absolute paths or arbitrary OS/backend text;
- relative normalized source paths only;
- absolute/root/prefix/parent/separator-escape and symlink rejection;
- canonical containment under the manifest root;
- directory and special-file rejection;
- same-directory temporary output plus final rename so failed compilation preserves an existing final output.

The numeric limits are synthetic schema-v1 engineering limits, not production budgets.

Explicit exclusions:

- no `asset-runtime` package, runtime mounting, streaming, cache, activation or rollback;
- no renderer/GPU integration, upload, atlas/texture-array choice or visual output;
- no image decoder, archive, compression/decompression, recursive discovery or watcher;
- no real Tibia/Canary importer, official/proprietary fixture or production pack;
- no download/updater, signature or authenticated-manifest design;
- no protocol, identity, networking, UI, text, audio, localization, domain or feature work;
- no production compatibility, redistribution-rights, security-signature or performance claim.

Expected exclusive paths:

```text
oteryn-client/crates/asset-types/**
oteryn-client/tools/asset-compiler/**
oteryn-client/assets/test-fixtures/synthetic-v1/**
oteryn-client/docs/research/assets/W6_FORMAT_AND_SECURITY_EVIDENCE.md
```

Expected shared-path lease:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/deny.toml
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
```

`deny.toml` is leased only for a narrowly evidenced license clarification if exact cargo-deny proves the current policy insufficient. Architecture checker source/rules/fixtures, Rust toolchain and CI workflows remain read-only unless a separate blocker is recorded.

## 6. Dependency evidence cut

Primary/current evidence reviewed on 2026-07-29:

- workspace Rust is 1.94;
- exact workspace `serde_json 1.0.145` already exists and passed current supply-chain checks;
- candidate `sha2 0.11.0` reports Rust 1.85 and license `MIT OR Apache-2.0`;
- W6 may use exact `sha2 = "=0.11.0"` with default features disabled for SHA-256 only;
- no CLI framework, async runtime, archive, image, compression, signing, network or watcher dependency is authorized;
- generated Cargo resolution and exact cargo-deny advisories/licenses/bans/sources remain authoritative and may reject the candidate without policy weakening.

No dependency is added by this planning task.

## 7. Deterministic acceptance envelope

The worker must test at least:

- typed ID, kind, metadata and bounded-string validation;
- a known SHA-256 vector;
- byte-identical repeated builds;
- shuffled-manifest-order invariance;
- encode/decode round trip;
- duplicate ID and unknown schema/kind rejection;
- malformed, truncated, trailing and oversized input;
- count, length, offset and allocation overflow rejection;
- RGBA8 dimension/payload mismatch and multiplication overflow;
- absolute, parent, prefix, separator-escape and symlink path rejection;
- source outside root, directory and special-file rejection;
- failed compilation preserving an existing final output;
- no source-machine absolute path in pack bytes or stable errors.

Tests and fixtures must run without a GPU, window, network, proprietary input or interactive desktop.

## 8. Evidence policy

The worker evidence document must classify:

- `PASS`: exact schema, deterministic encoding, hashing, malformed-input, path-safety, workspace, architecture and supply-chain tests actually executed;
- `OBSERVED`: only behavior genuinely exercised on a named filesystem/Windows runner;
- `BLOCKED`: production asset rights, real Canary-compatible input formats, runtime mounting, GPU integration, signing/authenticated manifests, production limits and performance.

Synthetic compiler success is not production asset compatibility or redistribution approval.

## 9. Shared-path lease

| Path group | Lease holder after worker launch | Other work |
|---|---|---|
| Cargo workspace/lockfile and dependency policy | W6-ASSET | read-only |
| asset-types public schema/pack contract | W6-ASSET | no duplicate producer |
| asset-compiler tool and synthetic fixtures | W6-ASSET | no parallel compiler |
| shared catalogue/matrix/changelog/layout/workspace docs | W6-ASSET | read-only |
| architecture checker/rules/fixtures | none | read-only |
| Rust CI/toolchain | none | read-only |
| renderer/application shell | none | read-only; no W6 integration |

The worker claims the lease only through its active task and live draft PR after a fresh overlap check.

## 10. Merge and completion rules

- W6-ASSET starts only after this plan and its separate archive merge.
- Any material dependency evidence, schema producer or `main` change requires restack and exact-head revalidation.
- The worker merges only through the root autonomous gate and receives a separate lifecycle archive PR.
- W6 closes only after the worker is merged/archived, no lease remains and exactly one evidence-based next package is recorded.

Candidate next package after successful closure: a read-only verified synthetic pack mounting/lookup slice under `asset-runtime`, only if W6 proves a stable bounded pack contract. It is not authorized by this plan.
