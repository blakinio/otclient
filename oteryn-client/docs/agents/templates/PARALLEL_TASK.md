# Parallel Rust Client Task Extension

Use the root task template and `templates/TASK.md`, then add the fields below for a task running in a coordinated parallel wave.

```yaml
parallel_wave: OTERYN-WX-NAME
parallel_lane: WX-XX
parallel_lane_state: proposed | claimed | active | blocked | integration_ready | validating | ready | merged | archived
coordinator_task: OTC-... | none
shared_path_lease: []
contract_role: none | producer | consumer
contracts_produced: []
contracts_consumed: []
required_base_commit: <sha | pending>
integration_after: []
```

## Field rules

### `parallel_wave`

Stable wave identifier from the accepted launch plan. Do not invent a second wave name for tasks intended to run together.

### `parallel_lane`

Unique lane identifier within the wave. It identifies responsibility, not a person or model.

### `parallel_lane_state`

Wave-specific execution state. Keep the root `status` consistent:

| Lane state | Typical task status |
|---|---|
| `proposed` | planned |
| `claimed`, `active` | in_progress |
| `blocked` | blocked |
| `integration_ready` | awaiting_integration |
| `validating` | awaiting_ci |
| `ready` | ready |
| `merged` | completed_pending_archive |
| `archived` | completed |

### `coordinator_task`

Current coordinator task when one exists. `none` is permitted when the protocol is followed directly from live tasks/PRs.

### `shared_path_lease`

Exact high-contention paths temporarily owned for integration. An empty list means the worker may not edit shared integration paths.

Before adding a path:

- inspect active tasks and open PRs;
- verify no existing lease/ownership;
- record why isolated work cannot finish without it;
- release it after merge, split or abandonment.

### Contract fields

`contract_role=producer` requires at least one `contracts_produced` entry. `consumer` requires `contracts_consumed`, `depends_on` and the producer's exact merged commit before final validation.

Do not use these fields for private implementation details. They identify public shared interfaces that constrain another lane.

### `required_base_commit`

The exact merge commit that must be present before final validation. Use `pending` while a required producer is unmerged. Update it after the producer merges.

### `integration_after`

Tasks/PRs that should merge before this lane because they own shared contracts or integration surfaces. This supplements but does not replace `depends_on`.

## Required parallel-task questions

Add answers to the task body:

- Why is this lane safe to run concurrently?
- Which paths and contracts are exclusive?
- Which shared paths are read-only?
- Does the lane produce or consume a public contract?
- Which merge invalidates the lane's previous validation?
- What exact state changes it to `integration_ready` or `blocked`?
- Can the lane merge independently, or must it wait for another PR?
- Which task archives/releases any shared-path lease?

## Example: isolated research lane

```yaml
parallel_wave: OTERYN-W1-FOUNDATION-EVIDENCE
parallel_lane: W1-CP
parallel_lane_state: active
coordinator_task: OTC-20260727-wave1-coordinator
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed: []
required_base_commit: 0123456789abcdef
integration_after: []
owned_paths:
  - oteryn-client/docs/research/canary-current/**
```

## Example: implementation producer with shared integration lease

```yaml
parallel_wave: OTERYN-W1-FOUNDATION-EVIDENCE
parallel_lane: W1-F
parallel_lane_state: active
coordinator_task: OTC-20260727-wave1-coordinator
shared_path_lease:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/tools/architecture-check/**
contract_role: producer
contracts_produced:
  - oteryn-foundation public primitives
contracts_consumed: []
required_base_commit: <current main sha>
integration_after: []
owned_paths:
  - oteryn-client/crates/foundation/**
```

## Handoff requirements

A parallel task handoff includes:

- current lane state;
- exact producer/base commit;
- currently held shared-path lease;
- merge order/dependency status;
- first unresolved failure or blocker;
- one concrete next action;
- whether prior CI is invalid after a newer producer/main merge.
