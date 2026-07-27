# Initial Parallel Agent Wave

Status: launch plan after this coordination package is merged  
Wave ID: `OTERYN-W1-FOUNDATION-EVIDENCE`

## 1. Objective

Start several agents immediately without allowing competing implementation of the young Rust workspace or unresolved shared contracts.

The wave uses:

```text
1 coordinator
1 implementation worker
3 isolated evidence workers
```

Maximum active sessions: five including the coordinator.

## 2. Dependency graph

```text
                    +--------------------------+
                    | W1-C coordinator         |
                    +-------------+------------+
                                  |
           +----------------------+-----------------------+
           |                      |                       |
           v                      v                       v
+--------------------+  +--------------------+  +--------------------+
| W1-F foundation    |  | W1-CP Canary       |  | W1-AR asset input  |
| implementation     |  | evidence           |  | evidence           |
+---------+----------+  +---------+----------+  +---------+----------+
          |                       |                       |
          |                       +-----------+-----------+
          |                                   |
          v                                   v
+--------------------+             +-----------------------+
| merged foundation |             | reviewed evidence     |
| public primitives |             | recommendations only  |
+---------+----------+             +-----------+-----------+
          |                                    |
          +-------------------+----------------+
                              |
                              v
                    +--------------------------+
                    | coordinator selects W2   |
                    +--------------------------+

Independent fourth worker:

+--------------------+
| W1-PR Windows      |
| platform evidence  |
+---------+----------+
          |
          +----------------------> Wave 2 platform decision
```

Research workers do not depend on W1-F and do not edit its paths. W1-F does not consume unmerged research output.

## 3. Lane W1-C — Coordinator/integrator

Prompt: `prompts/COORDINATOR_AGENT.md`

Responsibilities:

- verify each worker creates an authoritative task and draft PR;
- reject overlapping paths or duplicate public contracts;
- monitor the shared workspace lease held by W1-F;
- prevent research findings from being represented as accepted code contracts;
- verify W1-F rebases on current `main` and passes exact-head Rust/required CI;
- merge order: independent docs evidence PRs may merge whenever ready; W1-F merges only through its own gate;
- archive completed tasks;
- recommend Wave 2 from actual merged evidence.

Owned paths, when a coordinator task is required:

```text
oteryn-client/docs/agents/coordination/**
docs/agents/tasks/active/<coordinator-task>.md
```

The coordinator should avoid editing implementation worker paths or shared Rust workspace files.

## 4. Lane W1-F — Foundation implementation

Prompt: `prompts/NEXT_FOUNDATION_AGENT.md`

Purpose:

- implement exactly one `oteryn-foundation` crate;
- typed generations/technical identities;
- deterministic monotonic time;
- explicit cancellation ownership;
- narrow non-secret errors.

Expected exclusive implementation paths:

```text
oteryn-client/crates/foundation/**
```

Expected shared-path lease:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/tools/architecture-check/**
oteryn-client/tests/architecture-fixtures/**
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
```

Rules:

- W1-F is the only implementation lane allowed to modify the Rust workspace during Wave 1.
- It produces no game/domain/channel identifiers and no async runtime.
- Research agents may not edit its crate/category/workspace integration.
- W1-F does not absorb research scope into its PR.

## 5. Lane W1-CP — Canary Current-profile evidence

Prompt: `prompts/CANARY_EVIDENCE_AGENT.md`

Purpose:

- revalidate the exact current Canary profile/build/version evidence;
- prepare a provenance-first fixture acquisition manifest for the minimum playable families;
- identify build-string, capability and multi-channel mapping gaps;
- make no client or server implementation change.

Owned paths:

```text
oteryn-client/docs/research/canary-current/**
docs/agents/tasks/active/<canary-evidence-task>.md
```

Forbidden paths:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/crates/**
oteryn-client/contracts/**
oteryn-client/tools/architecture-check/**
.github/workflows/**
```

Output is evidence, not accepted packet constants. Any cross-repository contract recommendation remains blocked until separately coordinated.

## 6. Lane W1-AR — Asset input and provenance evidence

Prompt: `prompts/ASSET_RESEARCH_AGENT.md`

Purpose:

- refine the legally safe source/input matrix for synthetic and future compatibility assets;
- define non-content statistics needed before texture/pack decisions;
- design a provenance record and importer threat checklist;
- add no real/proprietary asset bytes and no pack implementation.

Owned paths:

```text
oteryn-client/docs/research/asset-inputs/**
docs/agents/tasks/active/<asset-research-task>.md
```

Forbidden paths:

```text
oteryn-client/assets/**
oteryn-client/crates/asset-*/**
oteryn-client/tools/asset-compiler/**
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
.github/workflows/**
```

Output may recommend a later WS-R09 synthetic package but does not freeze its binary schema.

## 7. Lane W1-PR — Windows platform dependency evidence

Prompt: `prompts/PLATFORM_RESEARCH_AGENT.md`

Purpose:

- evaluate current primary documentation for Windows event/window integration candidates;
- record DPI, IME, raw input, event-loop, shutdown and surface ownership requirements;
- produce a narrow spike recommendation for WS-R02;
- add no platform/application crate and no dependency.

Owned paths:

```text
oteryn-client/docs/research/windows-platform/**
docs/agents/tasks/active/<platform-research-task>.md
```

Forbidden paths:

```text
oteryn-client/apps/**
oteryn-client/crates/platform/**
oteryn-client/crates/app-runtime/**
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/deny.toml
.github/workflows/**
```

Output is dependency evidence only. A later implementation task revalidates versions and owns Cargo integration.

## 8. Shared-path leases for Wave 1

| Path group | Lease holder | Other lanes |
|---|---|---|
| Cargo workspace/lockfile | W1-F | read-only |
| architecture checker/fixtures | W1-F | read-only |
| Rust CI/toolchain/deny policy | none; already merged | read-only for all Wave 1 lanes |
| foundation crate/category | W1-F | no duplicate types |
| Canary research docs | W1-CP | other lanes read-only |
| asset research docs | W1-AR | other lanes read-only |
| platform research docs | W1-PR | other lanes read-only |
| coordination protocol | W1-C | implementation workers do not edit |

A new lease requires the coordinator to verify no live task/PR overlap. No worker edits a leased path because a merge conflict appears convenient.

## 9. Merge rules

- W1-CP, W1-AR and W1-PR are independent docs-only PRs and may merge in any order once exact-head checks pass.
- W1-F may merge independently of research lanes because it does not consume their findings.
- A research PR that changes accepted architecture or shared contracts must stop and split an ADR/contract task instead of merging as research.
- After any `main` change affecting shared agent docs, remaining lanes rebase/restack before final validation.
- Every lane archives its task in a separate lifecycle PR.

## 10. Wave 1 completion

Wave 1 closes when:

- W1-F is merged and archived, or explicitly blocked with preserved evidence;
- all three research lanes are merged/archived or explicitly deferred;
- no active task still claims an expired shared-path lease;
- the coordinator reviews actual merged outputs and publishes one Wave 2 recommendation.

## 11. Candidate Wave 2 DAG

This is a planning envelope, not authorization to start all tasks.

```text
foundation merged
    |
    +--> deterministic test support / diagnostics primitives
    |
    +--> minimal Windows platform/application shell
    |
    +--> synthetic asset-types/compiler slice
    |
    +--> domain technical storage primitives

platform shell + synthetic asset contract
    |
    +--> renderer synthetic instancing/window slice

foundation + domain contract + exact Canary evidence
    |
    +--> protocol-core then one Canary message family
```

Rules for Wave 2:

- at most three implementation lanes;
- one producer per shared contract;
- Cargo/lockfile integration remains serialized;
- renderer waits for the minimum asset/render-handle contract;
- Canary adapter waits for merged domain/protocol-core contracts and exact producer evidence;
- Identity/channel implementation remains blocked on its explicit cross-repository contract where required.

## 12. Launch checklist

Before opening agent sessions:

1. merge this coordination package;
2. copy the coordinator prompt into one session;
3. copy `NEXT_FOUNDATION_AGENT.md` into the implementation session;
4. copy the three research prompts into separate sessions;
5. require each session to perform its own fresh preflight;
6. do not assign branches or PR numbers in advance;
7. let live Git/task state determine whether a lane remains safe to claim.
