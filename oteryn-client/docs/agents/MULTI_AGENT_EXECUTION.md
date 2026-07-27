# Multi-Agent Execution Protocol

Status: normative for parallel work under `oteryn-client/`  
Root `AGENTS.md`, nested `AGENTS.md`, live task records and open PRs remain authoritative.

## 1. Purpose

Several autonomous agents may work at the same time, but they do not share memory, a branch, a worktree or mutable runtime state. Coordination happens only through Git, task records, draft PRs, reviewed contracts and CI.

The objective is independent implementation with controlled integration, not unrestricted simultaneous editing.

## 2. Roles

### Coordinator/integrator

One coordinator may be active for a parallel wave. The coordinator:

- inspects current `main`, all open PRs, active tasks and review state;
- assigns or confirms non-overlapping lanes;
- verifies dependency order and shared-contract ownership;
- grants at most one shared-path integration lease at a time;
- decides merge order from declared dependencies and current evidence;
- detects stale branches, conflicting public APIs and duplicated abstractions;
- keeps coordination documentation and PR comments current when needed;
- does not implement a large product subsystem while coordinating;
- never bypasses CI, branch protection, review or cross-repository gates.

The coordinator is not a privileged source of product truth. Architecture, contracts, source, tests and accepted ADRs remain authoritative.

### Worker agent

Each worker:

- owns exactly one bounded task, branch and worktree;
- creates an active task record and draft PR before broad implementation;
- claims exact paths, contracts and dependencies;
- edits only owned paths and explicitly leased shared paths;
- consumes merged public contracts instead of creating local duplicates;
- rebases or restacks on the required producer commit before final validation;
- finishes its PR end to end or records a real blocker;
- archives its completed task in a separate lifecycle PR.

### Contract producer

A worker becomes the contract producer when its task owns a public shared interface, such as:

- foundation primitives;
- domain identifiers, `GameEvent` or `GameCommand`;
- render snapshot types;
- asset schema and pack envelope;
- UI registry/view-model contracts;
- protocol adapter traits;
- Identity/directory/channel identifiers.

Only one active task may own the same shared contract. Consumers must declare `depends_on` and wait for the producer to merge before claiming implementation compatibility.

### Research/evidence agent

A research agent may run before an implementation gate when it:

- writes only isolated evidence documents under an explicitly owned path;
- treats external repositories as read-only;
- labels unknown or blocked facts rather than freezing speculative code contracts;
- does not modify Cargo manifests, CI, product crates, shared architecture contracts or external repositories;
- leaves one implementation recommendation without implementing it.

Research PRs still follow the full task, draft PR, review and CI lifecycle.

## 3. Concurrency limit

Initial limit:

```text
1 coordinator + at most 4 worker agents
```

At most three workers should be implementation lanes until the workspace has stable foundation, test and integration contracts. Additional agents should remain isolated research/evidence lanes.

The coordinator lowers concurrency when:

- two tasks require the same public contract;
- multiple branches need the same shared workspace files;
- CI capacity becomes a bottleneck;
- cross-repository ordering is unresolved;
- a producer API is still changing materially.

Increasing the limit requires measured evidence that reviews, CI and merge conflicts remain manageable.

## 4. Lane states

Every parallel task records one state:

| State | Meaning |
|---|---|
| `proposed` | candidate lane; no paths claimed |
| `claimed` | task, branch and draft PR exist; ownership checked |
| `active` | implementation or evidence collection is in progress |
| `blocked` | cannot proceed without a named decision, producer or environment |
| `integration_ready` | owned implementation is complete; waiting for shared-path lease/rebase/merge order |
| `validating` | final exact-head local/CI validation is running |
| `ready` | merge gate is satisfied |
| `merged` | product/evidence PR merged; task awaits archive lifecycle PR |
| `archived` | completed task record moved to archive |

Task front matter `status` remains the repository-wide status. `parallel_lane_state` adds the wave-specific state.

## 5. Ownership model

### Exclusive implementation paths

`owned_paths` are advisory locks. Before editing, a worker must verify that no active task or open PR owns the same path, crate, feature, contract, protocol family or asset schema.

Directory ownership includes descendants unless the task explicitly narrows it.

Examples of safe independent ownership:

```text
crates/foundation/**
docs/research/canary-current/**
docs/research/asset-inputs/**
docs/research/windows-platform/**
```

Examples of unsafe overlap:

```text
crates/game-domain/** owned by two tasks
one task owns GameEvent while another adds adjacent variants
renderer and asset agents both define texture-handle types
identity and protocol agents both define WorldChannelId
```

### Shared integration paths

The following paths are high-contention integration surfaces:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/tools/architecture-check/**
oteryn-client/tests/architecture-fixtures/**
oteryn-client/rust-toolchain.toml
oteryn-client/deny.toml
.github/workflows/rust-client.yml
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
```

Only one active task may hold a shared-path integration lease for a given path set.

A worker may prepare its isolated crate/evidence without the lease. Before editing a shared integration path, it must:

1. declare `shared_path_lease` in the task;
2. verify no other active task/PR claims the path;
3. record the exact producer/base commit;
4. keep the shared edit minimal and limited to integrating its own package;
5. release the lease when the PR merges, is abandoned or is split.

The lease is represented by the task and live PR, not a manually edited global lock table.

### Cargo and lockfile rule

Parallel crate implementation is permitted, but workspace integration is serialized.

- Workers do not independently invent workspace dependency versions.
- The task holding the current `Cargo.toml`/`Cargo.lock` lease integrates one package at a time.
- Another worker may continue in isolated owned paths but marks itself `integration_ready` until the lease is available.
- Before final validation, the worker rebases/restacks on current `main`, regenerates the lockfile through Cargo and reruns the complete workspace checks.
- Manual lockfile conflict editing is prohibited.

## 6. Contract dependency protocol

A consumer task declares:

```yaml
depends_on:
  - OTC-... producer task
contracts_consumed:
  - exact contract name and producer PR
required_base_commit: <producer merge commit or pending>
```

Rules:

- A consumer may research or prototype privately, but it may not claim compatibility before the producer merges.
- Consumer code must not include a temporary duplicate public type intended to be replaced later.
- If a producer contract changes materially, consumers return to `blocked` or rebase and revalidate.
- Shared contract amendments belong to the producer/owner workstream or a dedicated contract PR, not an opportunistic consumer edit.
- A producer leaves migration notes and one exact first consumer action.

## 7. Dependency and merge order

The coordinator maintains order through task dependencies and PR bodies, not a permanent mutable queue file.

Default order:

1. architecture/contract producer;
2. foundation or shared implementation;
3. isolated consumers;
4. composition/application integration;
5. archive lifecycle PRs.

A PR can merge before another active lane only when:

- it does not invalidate the other lane's owned public contract;
- the other lane can rebase without speculative migration;
- all shared-path leases are respected;
- exact-head CI passes after the final base state.

When two independent PRs are both ready, merge the one with more downstream dependents first. The second PR rebases/restacks and revalidates.

## 8. Initial execution strategy

The first safe wave is defined in `INITIAL_PARALLEL_WAVE.md`.

It intentionally contains:

- one implementation lane for the Gate 1 foundation crate;
- three isolated docs-only evidence lanes for Canary, asset inputs and Windows platform dependencies;
- one coordinator/integrator.

This structure creates useful parallel progress without allowing several workers to mutate the young Rust workspace or define competing shared types.

## 9. Required task metadata

Parallel tasks extend the normal Rust task record with:

```yaml
parallel_wave:
parallel_lane:
parallel_lane_state:
coordinator_task:
shared_path_lease: []
contract_role: none | producer | consumer
contracts_produced: []
contracts_consumed: []
required_base_commit:
integration_after: []
```

Use `templates/PARALLEL_TASK.md` for guidance. These fields do not replace root task metadata.

## 10. Worker startup protocol

Every worker performs this sequence independently:

1. read root and nested `AGENTS.md`;
2. inspect current `main`, open PRs, active tasks and required checks;
3. read the owning architecture, audit, workstream and accepted producer contracts;
4. verify path and contract ownership;
5. create task, branch/worktree and draft PR;
6. declare lane state, dependencies and any shared-path lease;
7. implement only the bounded package;
8. update task after discoveries, failures and contract changes;
9. rebase/restack on required producer/current `main` before final validation;
10. inspect complete changed files/diff, reviews and CI;
11. merge through the autonomous gate;
12. archive the task separately.

## 11. Coordinator operating cycle

The coordinator periodically:

1. reads all active Rust task files and live PR state;
2. verifies that each lane still owns non-overlapping paths/contracts;
3. checks shared-path leases and required producer commits;
4. detects workers based on stale `main` after a producer merge;
5. records blockers through task/PR communication;
6. chooses the next integration lease and merge order;
7. does not mark another worker's validation successful without exact evidence;
8. closes the wave only when every lane is merged/archived or explicitly deferred.

The coordinator must not rewrite another worker's implementation branch unless the worker task explicitly hands off ownership.

## 12. CI and review rules

- Each PR validates only its actual layer plus repository required checks.
- Documentation research lanes do not claim product compilation or runtime compatibility.
- Implementation lanes pass the complete Rust workspace checks on their final rebased head.
- A shared-path or producer merge invalidates earlier consumer workspace evidence.
- CI failures are repaired in the owning task or split into a focused CI task; checks are never weakened.
- Review comments and unresolved threads are part of the lane state and must be cleared before `ready`.

## 13. Failure and stale-work handling

A lane becomes stale when:

- its required base/producer commit changed;
- another merged PR owns the same public interface;
- its draft PR has no current task record;
- its task claims paths that no longer match the diff;
- the selected external contract revision changed materially.

The worker or coordinator must then:

1. stop merge;
2. update the task to `blocked` or restack-required;
3. decide whether to rebase, split, supersede or close the PR;
4. preserve useful evidence and failed approaches;
5. never merge a stale compatibility claim.

## 14. Mandatory stop conditions

Stop the affected lane when:

- ownership overlap cannot be resolved;
- two workers define the same public type or schema;
- the task needs a shared path already leased elsewhere;
- a required producer contract is not merged;
- a cross-repository atomic contract is incomplete;
- asset rights, protocol evidence or security review is missing;
- integration requires weakening workspace or repository checks;
- secrets, proprietary data or private captures enter the proposed diff.

Other independent lanes may continue when their paths and contracts remain unaffected.

## 15. Completion standard

A parallel wave is successful when:

- every lane has an authoritative task and PR history;
- no shared contract has competing implementations;
- shared workspace paths were integrated serially;
- downstream branches validated against actual merged producers;
- every merged task is archived;
- deferred lanes have explicit blockers and one next action;
- the coordinator leaves the next wave recommendation without implementing it.
