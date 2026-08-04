---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: blocked
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: invisible-outfit-source-ready
branch: main
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-04T18:22:00+02:00
required_base_commit: "85f3b91ab19114e0b4fd2f1259c7f28a66ea977e"
risk: high
related_prs: [188, 190, 191, 192, 193, 196, 198, 203, 204, 219, 220, 221, 222, 223, 224, 225, 227, 228, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 254, 256, 258, 261, 268]
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/crates/protocol-canary/**
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
  - oteryn-client/docs/evidence/playability/p2/canary-player-summon-appearance.md
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
  - hidden-health entity-kind contract
  - invisible-outfit branch implementation
  - complete local-player appended map-strip reconciliation
  - product binding map and visible-world composition
  - controlled real M2 acceptance
invocation_started_at: 2026-08-03T19:01:00+02:00
last_progress_at: 2026-08-04T18:22:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: player-summon-merged
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Reconcile pinned Canary Current producer evidence with the Rust client while preserving fail-closed real admission. Implement only inbound protocol families whose complete byte layout, ordering, feature gates, bounds and semantic ownership are proven without inference.

# Normative boundaries

```yaml
producer_repository: blakinio/canary
producer_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
producer_profile: ProtocolProfileId::Current
consumer_repository: blakinio/otclient
consumer_adapter: oteryn-client/crates/protocol-canary
network_message_max_bytes: 65500
real_admission: RealAdmissionUnavailable
cache_ownership: producer_or_future_adapter_session_state_not_simulation
transport_ownership: protocol_neutral
shared_path_lease: []
```

`protocol-canary` remains an independent exact-compatibility adapter under ADR-001. It does not wrap `protocol-oteryn`, own transport, mutate simulation or expose raw Canary packets to UI/features.

# Merged source-proven slices

| Family | Exact branch | Output | Merge |
|---|---|---|---|
| local identity | `0x17` | session-fenced local `EntityHandle` | merged |
| login preamble | `0x1A`, `0xEF`, `0x0A`, `0x0F` | bounded order and `BootstrapStarted` | merged |
| minimal map | item-free local-player-only `0x64` | `BootstrapCompleted` | merged |
| absent tile | `0x69 + Position + 0x01 + 0xFF` | `TileCleared` | merged |
| unknown remote player | `0x6A + 0x61`, zero eviction, player type | `EntityAppeared` | #248/#249 |
| remote move/remove | `0x6D` / entity-resolved `0x6C` | `EntityMoved` / `EntityRemoved` | #252/#254 |
| known remote player | `0x6A + 0x62` | `EntityAppeared`, `name: None` | #256/#258 |
| unknown monster/NPC | `0x6A + 0x61`, zero eviction, types `1/2` | `EntityAppeared` | #261 |
| player-owned monster summon | header `1`, final `3`, nonzero master | `EntityAppeared(Creature)` | #268 |
| session end | `0x18`, values `0x00/0x02` | `SessionEnded` | merged |

Every accepted boundary is bounded, session-fenced, trailing-data rejecting and state-atomic. Synthetic committed fixtures contain no credentials, private captures, deployed configuration or proprietary assets.

# Completed player-owned summon phase

```yaml
implementation_pr: 268
implementation_head: 392883490dc7a66cfd05094b7bd5af1e58118efa
implementation_merge: 85f3b91ab19114e0b4fd2f1259c7f28a66ea977e
base: b6a76a264c9c1cc62d063fba3c968d1b8582ef8c
rust_client_run: 30928206240
windows_job: 92056006376
supply_chain_job: 92056006319
repository_ci_run: 30928203871
repository_required_job: 92056360956
ready_state_repository_ci_run: 30928649446
ready_state_repository_required_job: 92057728494
focused_audit_comment: 5181653994
exact_final_audit_comment: 5181748881
critical_open: 0
high_open: 0
material_medium_open: 0
unresolved_review_threads: 0
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
result: PASS
```

The producer writes monster type `1` in the unknown header, rewrites only the final type to player-summon `3` when the master is a player, and appends a nonzero master identity. The adapter consumes that identity only to prove the message boundary and emits no Canary-only ownership authority.

# Next source-proven phase — invisible/default outfit

Pinned `ProtocolGame::AddOutfit` evidence proves the Current non-OTCR default outfit layout:

```yaml
look_type_u16_le: 0
look_type_ex_u16_le: 0
mount_u16_le: 0
additional_color_bytes: 0
custom_otcr_extension: absent
```

`AddCreature` writes this default outfit for invisible or ghost creatures. The existing player, known-player and non-player parsers already discard appearance fields after structural validation, so accepting this exact zero/default layout does not require a domain contract change. Nonzero `lookTypeEx`, nonzero mount in the default branch and OTCR extensions remain fail-closed.

# Readiness matrix

| Required family | Classification | Exact remaining contract |
|---|---|---|
| session bootstrap | `PARTIAL` | Minimal item-free local-player map only; general map needs item metadata. |
| map description | `PARTIAL` | General non-empty tile bodies and item branches unsupported. |
| tile/stack updates | `PARTIAL` | Empty-tile clear supported; item identity/replacement unresolved. |
| creature appearance | `PARTIAL` | Player, known player, monster, NPC and player-owned summon supported; invisible/default outfit is next; nonzero eviction, hidden and OTCR remain. |
| movement/reconciliation | `PARTIAL` | Remote entity movement supported; local movement appends map strips. |
| removal | `PARTIAL` | Remote entity removal supported; item removal requires authoritative item identity. |
| session end/logout | `PARTIAL` | Values `0x00/0x02` supported; unknown values rejected. |
| product integration | `NOT_READY` | General map, simulation binding, renderer composition and controlled M2 acceptance incomplete. |

# Remaining blocker normalization

## Authoritative item catalogue

General `AddItem` length and semantics depend on producer-owned item type and runtime instance metadata, including subtype/count, fluid/splash subtype, tier, animation phase, custom attributes and profile features. A consumer-ready, version-pinned catalogue contract is required.

## Stack identity ownership

Generic item removal/replacement needs session-fenced authoritative handles. A caller-owned read-only resolver exists for remote entities only.

## Nonzero known-cache eviction

Unknown creature appearance may evict a prior known identity. The branch requires an explicit adapter-session cache transition or normalized multi-event contract; silently ignoring the eviction is forbidden.

## Hidden health

The producer masks the unknown header type as hidden type `5`, sends an empty name and zero health. The original concrete entity kind is not recoverable from the wire. A protocol-neutral hidden-entity kind/appearance contract is required.

## Local-player map strips

Local movement appends directional map strips. Complete strip decoding remains dependent on general tile/item decoding.

# Validation policy

Every new slice requires pinned producer evidence, positive and every-prefix tests, malformed/bounds/order/trailing negatives, strict workspace CI, Supply Chain, repository required CI, fresh exact-head audit, current-main restack, protected merge and post-merge checkpoint.

E2E remains `NOT_APPLICABLE` for isolated already-decrypted/deframed parser slices. No live gameplay compatibility claim is made until controlled M2 acceptance.

# Durable checkpoint

```yaml
checkpoint_version: 40
updated_at: 2026-08-04T18:22:00+02:00
observed_main: 85f3b91ab19114e0b4fd2f1259c7f28a66ea977e
status: blocked
phase: invisible-outfit-source-ready
active_branch: none
last_merge:
  pr: 268
  head: 392883490dc7a66cfd05094b7bd5af1e58118efa
  merge: 85f3b91ab19114e0b4fd2f1259c7f28a66ea977e
  validation: PASS
  audit: PASS
shared_path_lease: []
ownership:
  protocol_canary: retained
  shared_paths: released
blocker: Lifecycle checkpoint must merge before the next implementation branch mutates the active task.
next_action: Merge this two-file closeout, then implement exact zero/default outfit parsing in the already supported player, known-player and non-player appearance families.
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 5
  session_id: OTC2-20260804T1822+0200-summon-closeout
  session_started_at: 2026-08-04T18:22:00+02:00
  checkpointed_at: 2026-08-04T18:22:00+02:00
  last_progress_at: 2026-08-04T18:22:00+02:00
  phase: player-summon-post-merge-closeout
  exact_head: pending_closeout_commit
  pull_request: pending
  active_operation: persist merge evidence and return parent to the next source-proven phase
  external_run_ids:
    - 30928206240
    - 30928203871
    - 30928649446
  check_generation: player-summon-closeout
  status: active
  safe_to_resume: true
  resume_condition: Do not recreate PR 268; continue from merge 85f3b91a.
  next_action: Validate and merge the closeout, then start invisible/default outfit implementation.
```
