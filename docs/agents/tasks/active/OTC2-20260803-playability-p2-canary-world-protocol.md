---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: validating
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: player-owned-monster-summon-terminal-ci
branch: feat/OTC2-20260804-canary-player-summon-appearance
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-04T18:13:00+02:00
required_base_commit: "b6a76a264c9c1cc62d063fba3c968d1b8582ef8c"
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
  - invisible-outfit branch validation
  - complete local-player appended map-strip reconciliation
  - product binding map and visible-world composition
  - controlled real M2 acceptance
invocation_started_at: 2026-08-03T19:01:00+02:00
last_progress_at: 2026-08-04T18:13:00+02:00
ci_checks_for_current_head: 2
ci_check_generation: player-summon-appearance-final-restack
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
| session end | `0x18`, values `0x00/0x02` | `SessionEnded` | merged |

Every accepted boundary is bounded, session-fenced, trailing-data rejecting and state-atomic. Synthetic committed fixtures contain no credentials, private captures, deployed configuration or proprietary assets.

# Last completed phase — unknown monster/NPC

```yaml
implementation_pr: 261
implementation_head: 4fd05ec1380c76169b5aa1aeada6c5430ece9e3b
implementation_merge: 80f85bbc38ab86814193e8bb892d167ca63b25f5
product_validation_head: f913e5ff5e4813e7ec2590122fc2ee3224aa901f
product_rust_client_run: 30899069326
product_windows_job: 91958836539
product_supply_chain_job: 91958836582
product_repository_ci_run: 30899073315
product_repository_required_job: 91959144109
exact_restacked_rust_client_run: 30900104928
exact_restacked_windows_job: 91962179120
exact_restacked_supply_chain_job: 91962179079
exact_restacked_repository_ci_run: 30900105318
exact_restacked_repository_required_job: 91962448871
ready_state_repository_ci_run: 30900453124
ready_state_repository_required_job: 91963525582
fresh_audit_comment: 5177542802
critical_open: 0
high_open: 0
material_medium_open: 0
unresolved_review_threads: 0
result: PASS
```

# Active phase — player-owned monster summon appearance

Pinned producer evidence proves one additional source-reachable Current branch:

```yaml
pr: 268
branch: feat/OTC2-20260804-canary-player-summon-appearance
opcode: 0x6A
marker_u16_le: 0x61
cache_eviction_u32_le: 0
entity_id: nonzero_nonlocal
header_type: monster_1
name: nonempty_domain_bounded
health: 1_through_100
visible_outfit: required
final_type: player_summon_3
master_id: required_nonzero_u32_le
output: GameEvent::EntityAppeared(EntityKind::Creature)
master_relationship_exposed_to_domain: false
cache_mutation: false
```

`Monster::getType()` returns monster type `1`. `ProtocolGame::AddCreature` writes that header type, then rewrites only the final type when the monster has a player master and appends the master identity. Direct header types `3` and `4` are not inferred or admitted.

The parser consumes the master identity solely to prove the complete message boundary. It retains no Canary-only ownership relation. Positive, every-truncated-prefix, zero-master, wrong-header, direct-summon-header, invalid final-type, stale/pre-bootstrap and trailing-data cases are covered.

Evidence: `oteryn-client/docs/evidence/playability/p2/canary-player-summon-appearance.md`.

# Readiness matrix

| Required family | Classification | Exact remaining contract |
|---|---|---|
| session bootstrap | `PARTIAL` | Minimal item-free local-player map only; general map still needs item metadata. |
| map description | `PARTIAL` | General non-empty tile bodies and item branches unsupported. |
| tile/stack updates | `PARTIAL` | Empty-tile clear supported; item identity/replacement unresolved. |
| creature appearance | `PARTIAL` | Ordinary player, known player, monster, NPC and player-owned monster summon supported after #268; nonzero eviction, hidden/invisible and OTCR branches remain. |
| movement/reconciliation | `PARTIAL` | Remote entity movement supported through read-only resolver; local movement appends map strips. |
| removal | `PARTIAL` | Remote entity removal supported; generic item removal requires authoritative item identity. |
| session end/logout | `PARTIAL` | Values `0x00/0x02` supported; unknown values rejected. |
| product integration | `NOT_READY` | General map, simulation binding, renderer composition and controlled M2 acceptance incomplete. |

# Remaining blocker normalization

## Authoritative item catalogue

General `AddItem` length and semantics depend on producer-owned item type and runtime instance metadata, including subtype/count, fluid/splash subtype, tier, animation phase, custom attributes and profile features. The protocol adapter must not infer those branches. A consumer-ready, version-pinned catalogue contract is required.

## Stack identity ownership

Generic removal/replacement carries position and stack observations while domain mutations require session-fenced authoritative handles. A caller-owned read-only resolver exists for remote entities only. Item identity and ambiguity behavior remain unresolved.

## Nonzero known-cache eviction

Unknown creature appearance may evict a prior known identity. Silently discarding a nonzero eviction would desynchronize adapter/session cache semantics. The branch requires an explicit adapter-session cache transition or a normalized multi-event contract; neither may be invented inside this parser.

## Hidden health

The producer masks the unknown header type as hidden type `5`, sends an empty name and zero health. The original concrete entity kind is therefore not recoverable from the wire branch. A protocol-neutral hidden-entity kind/appearance contract is required before admission.

## Invisible outfit

The producer writes a zero/default outfit for invisible or ghost creatures. Exact `AddOutfit` zero-layout and supported presentation semantics must be verified before relaxing the current nonzero-outfit guard.

## Local-player map strips

Local movement appends directional map strips. Accepting only the fixed movement prefix would leave unread authoritative world changes. Complete strip decoding remains dependent on general tile/item decoding.

# Validation policy

Required for every new slice:

- pinned producer revision and exact source-reachable path;
- positive synthetic logical-message case;
- every truncated prefix;
- malformed enum/length/boundary cases;
- stale, pre-bootstrap and terminal-order rejection;
- trailing-data rejection;
- strict workspace formatting and Clippy;
- full workspace tests and architecture policy;
- Supply Chain and repository required CI;
- fresh exact-head diff audit;
- current-main restack when producer/governance base moves;
- protected merge and post-merge checkpoint.

E2E remains `NOT_APPLICABLE` for isolated already-decrypted/deframed parser slices. No live gameplay compatibility claim is made until a controlled M2 journey exists.

# Durable checkpoint

```yaml
checkpoint_version: 39
updated_at: 2026-08-04T18:13:00+02:00
observed_main: b6a76a264c9c1cc62d063fba3c968d1b8582ef8c
status: validating
phase: player-owned-monster-summon-terminal-ci
active_branch: feat/OTC2-20260804-canary-player-summon-appearance
pr: 268
focused_validated_head: 029782e9246a6a3e5f9663214053b2f302902c15
validation:
  rust_client_run: 30927430884
  windows_job: 92053432011
  supply_chain_job: 92053432190
  repository_ci_run: 30927437588
  repository_required_job: 92053819757
  locked_metadata: PASS
  formatting: PASS
  strict_workspace_clippy: PASS
  workspace_tests: PASS
  architecture_policy: PASS
  supply_chain: PASS
  repository_required_ci: PASS
  result: PASS
fresh_audit:
  comment: 5181653994
  audited_head: 029782e9246a6a3e5f9663214053b2f302902c15
  critical_open: 0
  high_open: 0
  material_medium_open: 0
  unresolved_review_threads: 0
  result: PASS
final_current_main_restack: pending
exact_final_ci: pending
protected_merge: pending
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
ownership:
  protocol_canary: retained
  shared_paths: released
next_action: Restack the four intended paths on current main, run exact-head CI and audit, protected-merge PR 268, persist the merge, then implement the complete invisible-outfit branch.
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 4
  session_id: OTC2-20260804T1741+0200-player-summon
  session_started_at: 2026-08-04T17:41:00+02:00
  checkpointed_at: 2026-08-04T18:13:00+02:00
  last_progress_at: 2026-08-04T18:13:00+02:00
  phase: player-owned-monster-summon-terminal-ci
  exact_head: pending_current_main_restack
  pull_request: 268
  active_operation: current-main restack, exact-head CI, audit and protected merge
  external_run_ids:
    - 30927430884
    - 30927437588
  check_generation: player-summon-appearance-final-restack
  status: active
  safe_to_resume: true
  resume_condition: Continue PR 268; do not recreate the branch or admit direct summon header types.
  next_action: Clean-restack four intended paths on main, validate exact head and merge.
```
