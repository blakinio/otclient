---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: blocked
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: hidden-health-contract-ready
branch: main
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-04T19:24:00+02:00
required_base_commit: "8002e2b51d9f0ba825f788815d814aed5101c925"
risk: high
related_prs: [188, 190, 191, 192, 193, 196, 198, 203, 204, 219, 220, 221, 222, 223, 224, 225, 227, 228, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 254, 256, 258, 261, 268, 269, 270]
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/crates/protocol-canary/**
  - oteryn-client/docs/evidence/playability/p2/**
  - oteryn-client/tests/integration/canary-world-protocol/**
shared_path_lease: []
implementation_authorized: true
policy_version: 2.1
prompting_standard_version: 2.1
task_kind: implementation
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
context_pressure: high
decomposition_decision: phased
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - authoritative Current item-type metadata and complete AddItem branch contract
  - authoritative item-instance identity for generic removal and replacement
  - nonzero known-cache eviction reconciliation
  - protocol-neutral hidden-health entity-kind contract
  - complete local-player appended map-strip reconciliation
  - product binding map and visible-world composition
  - controlled real M2 acceptance
invocation_started_at: 2026-08-03T19:01:00+02:00
last_progress_at: 2026-08-04T19:24:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: invisible-outfit-merged
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Implement exact source-proven Canary Current inbound gameplay families without inference, transport ownership leakage or simulation mutation.

# Producer and consumer boundary

```yaml
producer_repository: blakinio/canary
producer_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
producer_profile: ProtocolProfileId::Current
producer_wire_family: CipsoftVanilla
consumer_repository: blakinio/otclient
consumer_adapter: oteryn-client/crates/protocol-canary
real_admission: RealAdmissionUnavailable
shared_path_lease: []
```

# Merged source-proven slices

| Family | Exact branch | Output | Merge |
|---|---|---|---|
| bootstrap and minimal local map | fixed Current preamble plus item-free `0x64` | bootstrap state/events | merged |
| absent tile update | `0x69 + Position + 0x01 + 0xFF` | `TileCleared` | merged |
| unknown/known remote player | `0x6A + 0x61/0x62` | `EntityAppeared` | #248/#249/#256/#258 |
| remote entity move/remove | resolver-backed `0x6D/0x6C` | `EntityMoved` / `EntityRemoved` | #252/#254 |
| monster/NPC | zero-eviction types `1/2` | `EntityAppeared` | #261 |
| player-owned monster summon | header `1`, final `3`, nonzero master | `EntityAppeared(Creature)` | #268/#269 |
| invisible/default outfit | exact three-zero-`u16` Current layout | structural appearance admission | #270 |
| session end | `0x18`, values `0x00/0x02` | `SessionEnded` | merged |

# Last completed phase — invisible/default outfit

```yaml
implementation_pr: 270
implementation_head: 518fbe27ee85ae943110bad6ce693bbebadab016
implementation_merge: 8002e2b51d9f0ba825f788815d814aed5101c925
focused_validation_head: d26c308be08474d36deb9b5cd0fff71cdc8a2ec4
focused_rust_client_run: 30931418621
focused_repository_ci_run: 30931419201
exact_rust_client_run: 30933043153
exact_windows_job: 92072249531
exact_supply_chain_job: 92072249589
exact_repository_ci_run: 30933043306
exact_repository_required_job: 92073142000
ready_state_repository_ci_run: 30933437515
ready_state_repository_required_job: 92074052297
focused_audit_comment: 5182288763
exact_final_audit_comment: 5182367276
critical_open: 0
high_open: 0
material_medium_open: 0
unresolved_review_threads: 0
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
result: PASS
```

# Next contract — hidden-health entity

Pinned producer behavior masks an unknown creature header as type `5`, sends an empty name and zero health. The original concrete category (`Player`, `Creature` or `NonPlayerCharacter`) is not recoverable from the message. Mapping type `5` to an existing concrete `EntityKind` would be inference.

Required producer contract:

```yaml
wire_header_type: 5
wire_name: empty
wire_health: 0
wire_final_type: 5
concrete_kind_recoverable: false
required_domain_representation: protocol_neutral_unknown_or_hidden_entity_kind
contract_owner: WS-R04
consumer: WS-R06 protocol-canary
```

Repository inspection found no open PR or active task owning `EntityKind`. The next safe package is a dedicated WS-R04 contract task adding one neutral hidden/unknown entity category, simulation/replay compatibility tests and explicit consumer guidance. The Canary parser may consume it only after that producer contract merges.

# Remaining blockers

## Authoritative item catalogue

General `AddItem` length and semantics depend on producer-owned item type and runtime instance metadata. A version-pinned, legally usable consumer catalogue is required.

## Item identity ownership

Generic item removal/replacement requires session-fenced authoritative item handles. Existing resolver support covers remote entities only.

## Nonzero known-cache eviction

Unknown appearance can evict a prior known identity. The branch requires explicit adapter-session cache transition semantics or a normalized multi-event contract.

## Local-player map strips

Local movement appends directional map strips whose complete tile bodies depend on general item decoding.

## Product integration

General map admission, simulation binding, renderer composition and controlled real M2 acceptance remain incomplete.

# Durable checkpoint

```yaml
checkpoint_version: 43
updated_at: 2026-08-04T19:24:00+02:00
observed_main: 8002e2b51d9f0ba825f788815d814aed5101c925
status: blocked
phase: hidden-health-contract-ready
active_branch: none
last_merge:
  pr: 270
  head: 518fbe27ee85ae943110bad6ce693bbebadab016
  merge: 8002e2b51d9f0ba825f788815d814aed5101c925
  validation: PASS
  audit: PASS
shared_path_lease: []
ownership:
  protocol_canary: retained
  shared_paths: released
blocker: The hidden type requires a protocol-neutral WS-R04 domain contract before WS-R06 may decode it.
next_action: Merge this two-file closeout, create the dedicated hidden-entity contract task/branch/PR, validate and merge it, then resume Canary type-5 decoding.
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 7
  session_id: OTC2-20260804T1924+0200-invisible-closeout
  session_started_at: 2026-08-04T19:24:00+02:00
  checkpointed_at: 2026-08-04T19:24:00+02:00
  last_progress_at: 2026-08-04T19:24:00+02:00
  phase: invisible-outfit-post-merge-closeout
  exact_head: pending_closeout_commit
  pull_request: pending
  active_operation: persist merge evidence and hand off to the hidden-entity contract producer
  external_run_ids:
    - 30933043153
    - 30933043306
    - 30933437515
  check_generation: invisible-outfit-closeout
  status: active
  safe_to_resume: true
  resume_condition: Do not recreate PR 270; continue from merge 8002e2b5.
  next_action: Validate and merge the closeout, then start the WS-R04 hidden-entity contract.
```
