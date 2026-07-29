# W6 Synthetic Asset Schema and Compiler Agent Prompt

Use this prompt only after the W6 plan PR and its separate lifecycle archive have merged. Live Git, active tasks, open PRs and exact checks remain authoritative.

```text
Work autonomously in repository:

blakinio/otclient

Role: implement the single authorized `W6-ASSET` lane for `OTERYN-W6-SYNTHETIC-ASSETS`.

Do not rely on chat history. Before writing, read current main, root and nested AGENTS.md, docs/agents/README.md, architecture/security/asset audit documents, PROGRAM.md, WORKSTREAMS.md, MULTI_AGENT_EXECUTION.md, CURRENT_PARALLEL_WAVE.md, RUST_WORKSPACE.md, every active Rust task and all open PRs/checks/review threads.

Repository safety:

- write only to blakinio/otclient;
- never mutate Canary, Oteryn Platform, upstream or another repository;
- never push directly to main;
- create one task, branch/worktree and early draft PR;
- claim the exact W6 shared-path lease in task front matter before shared integration edits;
- no branch-protection, review, CI, supply-chain or architecture bypass;
- no proprietary/unlicensed game bytes, credentials, private paths or external downloads.

Fresh launch gate:

- W1-W5 are merged, archived and not launchable;
- W6 plan and separate plan archive are merged;
- no active task or PR owns `crates/asset-types`, `tools/asset-compiler`, the W6 schema/compiler contract or its shared-path lease;
- open PR #23 remains legacy OTUI/Lua only and PR #48 remains isolated operational non-merge work;
- architecture checker still recognizes `asset-types` and `tool` without a source/rule/fixture change;
- exact dependency evidence and cargo-deny still support the planned candidates or a blocker is recorded before implementation.

Implement exactly one bounded work package with exactly two packages:

1. `oteryn-asset-types` at `oteryn-client/crates/asset-types/`, metadata category `asset-types`;
2. `oteryn-asset-compiler` at `oteryn-client/tools/asset-compiler/`, metadata category `tool`, consuming `oteryn-asset-types`.

Exclusive paths:

- oteryn-client/crates/asset-types/**
- oteryn-client/tools/asset-compiler/**
- oteryn-client/assets/test-fixtures/synthetic-v1/**
- oteryn-client/docs/research/assets/W6_FORMAT_AND_SECURITY_EVIDENCE.md

Unique shared-path lease:

- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- oteryn-client/deny.toml only if exact cargo-deny requires one narrowly evidenced license clarification
- oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
- oteryn-client/docs/operations/RUST_WORKSPACE.md
- docs/agents/MODULE_CATALOG.md
- docs/agents/BUILD_TEST_MATRIX.md
- docs/agents/CHANGELOG.md

Architecture checker source/rules/fixtures, Rust toolchain and CI workflows are read-only unless a separate blocker proves an independently scoped change is required.

Required schema/compiler contract:

- non-zero typed `AssetId`;
- closed first-slice `AssetKind` limited to synthetic binary blobs and validated RGBA8 images;
- manifest schema version 1 and original pack schema version 1;
- explicit bounded logical name, license identifier and provenance text;
- SHA-256 content digest for each payload;
- deterministic sorting independent of manifest order;
- original deterministic little-endian, length-delimited pack encoding;
- strict decoder/validator for tests and tooling only, not runtime mounting;
- one CLI compiler from constrained JSON manifest plus relative source files to one pack output;
- stable non-secret errors with no absolute source paths or arbitrary OS/backend text.

Required synthetic limits:

- at most 4096 records;
- at most 16 MiB payload per record;
- at most 64 MiB compiled pack;
- image dimensions at most 16,384 each;
- checked `width * height * 4` for RGBA8;
- explicit bounded string lengths;
- duplicate IDs rejected;
- all count, length, offset and allocation arithmetic checked.

These are synthetic schema-v1 engineering limits, not production budgets.

Filesystem rules:

- source paths are relative normalized manifest-root paths only;
- reject absolute/root/prefix/parent components and separator escapes;
- reject symlinks in every source path component;
- prove canonical source containment under the manifest root;
- reject directories and special files;
- bound reads before allocation;
- never embed source-machine absolute paths in the output or errors;
- write via a same-directory temporary file and final rename so failure does not replace a valid final output;
- no recursive discovery, archives, decompression, scripts, network access or watchers.

Dependency envelope:

- reuse exact workspace `serde_json = "=1.0.145"` for constrained manifest parsing;
- candidate exact `sha2 = "=0.11.0"`, default features disabled, for SHA-256 only;
- no CLI framework, async runtime, image decoder, archive/compression, signing, network or filesystem-watcher dependency;
- regenerate Cargo.lock after current-main integration; never merge it manually;
- exact cargo-deny advisories/licenses/bans/sources may reject a candidate and must not be weakened.

Minimum tests:

- ID, kind, metadata and string-bound validation;
- known SHA-256 vector;
- byte-identical repeated output and shuffled-manifest invariance;
- encode/decode round trip;
- duplicate IDs, unknown schema/kind, malformed/truncated/trailing input;
- oversized count/string/payload/pack and checked-overflow cases;
- RGBA8 dimension/payload mismatch and multiplication overflow;
- absolute, parent, prefix, separator-escape and symlink rejection;
- source outside root, directory and special-file rejection;
- failed compilation preserves an existing final output;
- output contains no absolute source path;
- only original synthetic fixtures with documented provenance.

Required evidence document:

`W6_FORMAT_AND_SECURITY_EVIDENCE.md` must record the exact manifest/pack layouts, limits, dependency source/version/license/MSRV/advisory evidence, fixture provenance, tests run, Windows runner identity and explicit automated-versus-unproven boundaries.

Explicitly excluded:

- asset-runtime, mounting, streaming, cache, activation or rollback;
- renderer/GPU integration, upload, atlas/texture-array strategy or visual output;
- real Tibia/Canary importer, official/proprietary inputs or production pack;
- download/updater, signatures or authenticated manifests;
- protocol, identity, network, UI, text, audio, localization, domain or feature work;
- production compatibility, legal redistribution, security-signature or performance claims.

Merge readiness:

- full changed-file list and complete diff reviewed against exact ownership;
- exact-head `cargo metadata --locked`, formatting, Clippy with warnings denied, all workspace tests, architecture policy and cargo-deny pass;
- repository required CI passes on the same final head;
- deterministic and negative security tests pass on Windows;
- no unresolved comments, reviews, threads, overlap or cross-repository blocker;
- base is current main and PR is mergeable;
- squash merge followed by a separate lifecycle archive PR.

After archive, the coordinator closes W6 and recommends exactly one next bounded package. Do not expand the worker into runtime assets or renderer integration.
```
