# Parallel Wave Coordinator Agent Prompt

W1-W5 are completed and closed. W6 is the current accepted plan only after its planning lifecycle merges. Copy the block below into a fresh coordinator session; do not implement the worker package while coordinating.

```text
Work autonomously in repository:

blakinio/otclient

Role: coordinate `OTERYN-W6-SYNTHETIC-ASSETS`. Do not implement W6-ASSET while coordinating.

Current Git/main, root and nested AGENTS.md, live open PRs, active tasks, accepted architecture, merged contracts/evidence and exact CI are authoritative. Do not rely on chat history.

Repository safety:

- routine writes only to blakinio/otclient;
- never mutate Canary, Oteryn Platform, upstream or another repository;
- never push directly to main;
- one task/branch/worktree per change;
- no branch-protection, review or CI bypass;
- no success, legal, security or compatibility claim without exact evidence.

Mandatory reads:

1. AGENTS.md
2. docs/agents/README.md
3. oteryn-client/AGENTS.md
4. oteryn-client/docs/architecture/ARCHITECTURE.md
5. oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
6. oteryn-client/docs/agents/PROGRAM.md
7. oteryn-client/docs/agents/WORKSTREAMS.md
8. oteryn-client/docs/agents/MULTI_AGENT_EXECUTION.md
9. oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
10. oteryn-client/docs/operations/RUST_WORKSPACE.md
11. every active Rust task, open PR, review thread and required check
12. foundation asset/licensing audit and current security architecture
13. exact current primary evidence for serde_json/sha2 source, version, license, MSRV and advisories
14. merged foundation, diagnostics, test-support, application-shell and renderer contracts

Revalidate before launch:

- W1-W5 are completed/archived and not launchable;
- W6 plan PR and its separate archive PR are merged;
- no active task or PR owns `crates/asset-types`, `tools/asset-compiler`, the asset schema/compiler contract or shared integration paths;
- open PR #23 remains legacy OTUI/Lua only and PR #48 remains isolated operational non-merge work;
- architecture checker still recognizes `asset-types` and `tool` without needing source/rule/fixture edits;
- current evidence still supports exact workspace serde_json and candidate sha2 0.11.0, or a plan amendment/blocker is recorded before worker launch.

Current wave:

- one coordinator;
- one implementation lane `W6-ASSET` using `NEXT_SYNTHETIC_ASSET_AGENT.md`;
- no secondary implementation or research lane.

W6-ASSET packages:

- `oteryn-asset-types` under `crates/asset-types`, category `asset-types`;
- `oteryn-asset-compiler` under `tools/asset-compiler`, category `tool`, consuming asset-types;
- one independently mergeable work package only.

Required contract:

- non-zero typed AssetId;
- closed synthetic kinds: binary blob and validated RGBA8 only;
- manifest schema v1 and original deterministic pack schema v1;
- bounded logical metadata, license/provenance and SHA-256 payload digests;
- deterministic little-endian length-delimited encoding sorted independently of manifest order;
- strict decoder/validator for tooling/tests only;
- constrained JSON-manifest CLI with relative safe source paths;
- stable non-secret errors without absolute paths or arbitrary OS text.

Required limits and safety:

- maximum 4096 records, 16 MiB payload per record and 64 MiB pack;
- maximum 16,384 pixels per image dimension and checked width*height*4;
- checked count/length/offset/allocation arithmetic and bounded strings;
- reject duplicate IDs, unknown schema/kind and malformed/truncated/trailing input;
- reject absolute/root/prefix/parent/separator-escape paths and every symlink component;
- prove canonical containment under manifest root and reject directories/special files;
- same-directory temporary output plus final rename;
- no source-machine absolute path in output or errors.

Unique W6-ASSET shared-path lease:

- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- oteryn-client/deny.toml only for a narrowly evidenced license clarification
- oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
- oteryn-client/docs/operations/RUST_WORKSPACE.md
- docs/agents/MODULE_CATALOG.md
- docs/agents/BUILD_TEST_MATRIX.md
- docs/agents/CHANGELOG.md

Architecture checker/rules/fixtures, Rust toolchain and CI remain read-only unless a separate blocker is recorded.

Dependency envelope:

- reuse exact workspace serde_json 1.0.145;
- candidate exact sha2 0.11.0 with defaults disabled for SHA-256 only;
- no CLI framework, async runtime, image/archive/compression, signing, network or watcher dependency;
- generated lockfile and exact cargo-deny are authoritative and may reject candidates without policy weakening.

Explicit exclusions:

- no asset-runtime, mounting, streaming, cache, activation or rollback;
- no renderer/GPU integration, upload, atlas/texture strategy or visual output;
- no image decoder, archive, decompression or recursive discovery;
- no real Tibia/Canary importer, official/proprietary fixture or production pack;
- no download/updater, signature or authenticated manifest;
- no protocol, identity, networking, UI, text, audio, localization, domain or feature work;
- no production compatibility, redistribution-rights, security-signature or performance claim.

For the worker verify:

- unique task, branch/worktree and early draft PR;
- exact exclusive paths and unique shared-path lease in task front matter;
- exact dependency source/version/license/MSRV/advisory evidence;
- deterministic and malformed/path-security tests on the final head;
- original synthetic fixture provenance;
- task/PR remain current after failures, fixes and validation;
- synthetic success is never described as production asset compatibility.

Merge readiness:

- full changed-file list and complete diff reviewed;
- exact-head locked metadata, formatting, Clippy, all tests, architecture and cargo-deny pass;
- repository required CI passes on the same head;
- no unresolved comments, reviews, threads, overlap or cross-repository blocker;
- base is current main and PR is mergeable;
- squash merge followed by a separate lifecycle archive PR.

After the worker archive merges, close W6 durably, release every lease and recommend exactly one next bounded package. Do not implement that next package in the closure task.
```
