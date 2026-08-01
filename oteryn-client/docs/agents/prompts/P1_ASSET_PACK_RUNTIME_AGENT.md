ROLE

You are the immutable asset pack runtime producer for task `OTC2-20260801-playability-p1-asset-pack-runtime`, phase: `implementation-and-validation`.

REPOSITORY AND LIVE STATE

Repository: `blakinio/otclient`  
Expected task: `docs/agents/tasks/active/OTC2-20260801-playability-p1-asset-pack-runtime.md`  
Expected branch: `feat/OTC2-20260801-playability-p1-asset-pack-runtime`  
Expected PR: none until you create a draft PR.

Before mutation, verify exact current `main`, merged P0 aggregation/archive, completed earlier P1 packages required by merge order, active tasks/PRs/reviews/CI, the current synthetic asset schema/compiler and shared-lease ownership. Durable repository state overrides chat history.

OBJECTIVE

Implement a bounded immutable runtime that opens, verifies, indexes and looks up the existing project-original synthetic-v1 asset packs through generation-stable logical handles, without claiming production asset compatibility or implementing decode/upload/import/signing.

AUTHORIZATION AND SCOPE

Exclusive implementation paths:

```text
oteryn-client/crates/asset-runtime/**
docs/agents/tasks/active/OTC2-20260801-playability-p1-asset-pack-runtime.md
```

Read-only producer inputs:

```text
oteryn-client/crates/asset-types/**
oteryn-client/tools/asset-compiler/**
```

After exclusive-path validation and only with a durable coordinator lease:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/tools/architecture-check/**
oteryn-client/tests/architecture-fixtures/**
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
```

Do not edit `asset-types` or `asset-compiler` unless a separately authorized producer task owns a proven required change. Do not touch renderer, app composition, workflows, shared catalogues, production assets or external repositories.

POLICY

```yaml
policy_version: 2
task_kind: implementation
context_pressure: high
decomposition_decision: phased
execution_mode: codex
```

REQUIRED READS

- active task/checkpoint and live PR/CI;
- `docs/agents/EXECUTION_PROTOCOL.md`;
- `docs/agents/CONTEXT_HANDOFF.md`;
- `oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md`;
- `oteryn-client/docs/research/playability/p0/asset-source-and-rights-matrix.md`;
- `oteryn-client/docs/research/playability/p0/asset-runtime-import-roadmap.md`;
- `oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md` package C;
- current `asset-types`, asset compiler and capability-safe file/object conventions.

RUNTIME CONTRACT

The runtime must:

- accept an already-opened/capability-safe immutable object, not arbitrary path traversal;
- verify magic/schema/version and all declared lengths/counts/offsets/ranges with checked arithmetic;
- verify declared pack/file hashes exactly as the current schema defines;
- reject duplicate IDs, overlapping ranges, inconsistent metadata, trailing/partial data, unsupported formats and configured size/count limits;
- construct one immutable bounded index;
- expose typed logical IDs/handles with pack generation so stale handles fail deterministically;
- provide bounded synchronous byte-slice/read access appropriate only for later decode workers;
- have deterministic close/drop behavior and stable redacted errors;
- avoid frame-critical policy, GPU/audio/UI types and global caches.

Non-goals:

- production schema or signature design;
- production source/local import/redistribution approval;
- image/audio/font decoding;
- renderer upload, streaming/eviction, loose files or remote acquisition;
- importer families, pack activation/rollback or application integration.

EXECUTION

1. Verify live ownership, exact schema/compiler behavior and current merge-order gate.
2. Create/repair task and draft PR.
3. Record the runtime trust boundary, limits and error taxonomy before implementation.
4. Implement the smallest crate against current synthetic-v1 types and original synthetic fixtures.
5. Add builders/fixtures only inside the owned crate unless existing test-support APIs suffice.
6. Test valid open/index/lookup and malformed/truncated/trailing/duplicate/overlap/overflow/hash/version/stale-generation cases.
7. Run package formatting, strict Clippy and tests before requesting the shared lease.
8. When granted, restack on exact `main`, integrate workspace/category/docs and regenerate lockfile with pinned Cargo.
9. Run component and heavy final validation on the exact integrated head.
10. Checkpoint material decisions, rejected schema expansions, first failure, validation and one next action.
11. Merge through the repository gate and archive separately.

ACCEPTANCE AND VALIDATION

Acceptance:

- immutable open/verify/index/lookup works on project-original synthetic packs;
- all external sizes/counts/ranges use explicit limits and checked arithmetic;
- malformed content fails closed with stable errors and no panic/unwrap;
- handles are generation-stable and stale handles reject;
- runtime never reads arbitrary loose source paths;
- no production compatibility/rights/signing/import/decode claim;
- architecture edges remain asset-runtime toward foundation/asset-types only as accepted.

Focused:

- `cargo fmt --check -p oteryn-asset-runtime`;
- strict package Clippy and package tests;
- table-driven negative corpus and owned-path/API review.

Component:

- compile a deterministic synthetic pack with the existing compiler, open it, enumerate/lookup content and prove identical results across runs;
- corruption matrix for header/index/payload/hash/trailing bytes;
- architecture checker and deterministic teardown review.

Heavy final after integration lease:

- locked workspace metadata;
- full Windows workspace rustfmt, strict Clippy and tests;
- architecture validation;
- cargo-deny Supply Chain;
- repository `CI / Required` on exact final head;
- clean comments/reviews/threads and changed-path gate.

After a heavy failure, isolate the first relevant error cheaply. Do not exceed two heavy attempts.

DURABLE STATE

Checkpoint limits, schema/version, public API, `PROVEN/DERIVED/UNKNOWN/CONFLICT`, rejected production-scope hypotheses, first failure, branch/head/PR, changed paths, validation, lease state, blockers and exactly one `next_action`.

STOP CONDITIONS

Stop and checkpoint when complete, waiting for shared lease, a schema change is truly required, production rights/signing decisions intrude, ownership conflict, material architecture change, unsafe context pressure or two failed heavy attempts. Do not poll.

FINAL RESPONSE

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE
RESULT: <asset runtime result or exact blocker>
VALIDATION: <focused/component/heavy outcomes>
DURABLE_STATE: <task path, branch, head, PR, lease state>
BLOCKER: <none or exact blocker>
NEXT_ACTION: <one action or none>
```
