---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: validating
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: invisible-outfit-terminal-ci
branch: feat/OTC2-20260804-canary-invisible-outfit-appearance
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-04T19:11:00+02:00
required_base_commit: "d52b0a91de4e166b5d95c52715a138041fd4c722"
risk: high
related_prs: [188, 190, 191, 192, 193, 196, 198, 203, 204, 219, 220, 221, 222, 223, 224, 225, 227, 228, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 254, 256, 258, 261, 268, 269, 270]
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/crates/protocol-canary/**
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
  - oteryn-client/docs/evidence/playability/p2/canary-player-summon-appearance.md
  - oteryn-client/docs/evidence/playability/p2/canary-invisible-outfit-appearance.md
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
  - complete local-player appended map-strip reconciliation
  - product binding map and visible-world composition
  - controlled real M2 acceptance
invocation_started_at: 2026-08-03T19:01:00+02:00
last_progress_at: 2026-08-04T19:11:00+02:00
ci_checks_for_current_head: 2
ci_check_generation: invisible-outfit-final-restack
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Reconcile pinned Canary Current producer evidence with the Rust client while preserving fail-closed real admission. Implement only inbound protocol families whose complete byte layout, ordering, feature gates, bounds and semantic ownership are proven without inference.

# Normative boundary

```yaml
producer_repository: blakinio/canary
producer_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
producer_profile: ProtocolProfileId::Current
producer_wire_family: CipsoftVanilla
consumer_repository: blakinio/otclient
consumer_adapter: oteryn-client/crates/protocol-canary
network_message_max_bytes: 65500
real_admission: RealAdmissionUnavailable
transport_ownership: protocol_neutral
cache_ownership: adapter_session_contract_not_simulation
shared_path_lease: []
```

`protocol-canary` remains independent from `protocol-oteryn`, transport, simulation, renderer and UI.

# Merged source-proven slices

| Family | Exact branch | Output | Merge |
|---|---|---|---|
| local identity and login preamble | `0x17`, `0x1A`, `0xEF`, `0x0A`, `0x0F` | session/bootstrap state | merged |
| minimal map | item-free local-player-only `0x64` | `BootstrapCompleted` | merged |
| absent tile | `0x69 + Position + 0x01 + 0xFF` | `TileCleared` | merged |
| unknown/known remote player | `0x6A + 0x61/0x62` | `EntityAppeared` | #248/#249/#256/#258 |
| remote move/remove | resolved `0x6D/0x6C` | `EntityMoved` / `EntityRemoved` | #252/#254 |
| unknown monster/NPC | zero-eviction types `1/2` | `EntityAppeared` | #261 |
| player-owned monster summon | header `1`, final `3`, nonzero master | `EntityAppeared(Creature)` | #268/#269 |
| session end | `0x18`, values `0x00/0x02` | `SessionEnded` | merged |

# Active phase — Current non-OTCR invisible/default outfit

Pinned producer evidence proves that invisible or ghost creatures use `AddOutfit(default Outfit_t)`. The accepted default payload is exactly:

```yaml
look_type_u16_le: 0
look_type_ex_u16_le: 0
mount_u16_le: 0
additional_bytes: 0
```

Visible outfits remain unchanged: nonzero look type, five color/addon bytes, mount id and four mount color bytes only when the mount is nonzero.

PR #270 implements one shared structural parser and consumes it from unknown player, known player, monster, NPC and player-owned summon appearance families. Outfit values remain discarded after structural validation; no domain authority or presentation state is introduced.

Covered:

- visible outfit without mount;
- visible outfit with mount colors;
- exact default invisible outfit;
- nonzero default `lookTypeEx` and mount rejection;
- every truncated prefix of all accepted outfit layouts;
- positive invisible logical messages and every message prefix for every supported appearance family;
- full existing visible-family regression suite.

Still rejected: OTCR extensions, hidden type `5`, nonzero known-cache eviction, malformed values and trailing data.

Evidence: `oteryn-client/docs/evidence/playability/p2/canary-invisible-outfit-appearance.md`.

# Focused validation and audit

```yaml
pr: 270
focused_head: d26c308be08474d36deb9b5cd0fff71cdc8a2ec4
rust_client_run: 30931418621
windows_job: 92066803009
supply_chain_job: 92066802553
repository_ci_run: 30931419201
repository_required_job: 92071083755
locked_metadata: PASS
formatting: PASS
strict_workspace_clippy: PASS
workspace_tests: PASS
architecture_policy: PASS
supply_chain: PASS
repository_required_ci: PASS
fresh_audit_comment: 5182288763
critical_open: 0
high_open: 0
material_medium_open: 0
unresolved_review_threads: 0
result: PASS
```

The audit caught and repaired two pre-merge defects: accidental truncation of the existing `lib.rs` API surface and incorrect mutable-reader reborrowing. The final focused diff preserves the complete library surface and has exactly eight intended paths with no workflow or script.

# Remaining blockers

## Authoritative item catalogue

General `AddItem` length and semantics depend on producer-owned item type and runtime instance metadata. A consumer-ready, version-pinned catalogue contract is required.

## Item identity ownership

Generic item removal/replacement requires session-fenced authoritative handles. A caller-owned resolver exists for remote entities only.

## Nonzero known-cache eviction

Unknown appearance can evict a prior known identity. The branch requires explicit adapter-session cache transition semantics or a normalized multi-event contract.

## Hidden health

The producer masks unknown header type as hidden `5`, sends empty name and zero health. Original concrete kind is unrecoverable from the wire. A protocol-neutral hidden/unknown entity-kind contract owned by WS-R04 is required.

## Local-player map strips

Local movement appends directional map strips. Complete decoding depends on general tile/item decoding.

# Readiness

The Canary producer is still not a complete M2 world decoder. General non-empty map/tile data, item identity, local movement strips, simulation binding, renderer composition and controlled real M2 acceptance remain incomplete.

# Durable checkpoint

```yaml
checkpoint_version: 42
updated_at: 2026-08-04T19:11:00+02:00
observed_main: d52b0a91de4e166b5d95c52715a138041fd4c722
status: validating
phase: invisible-outfit-terminal-ci
active_branch: feat/OTC2-20260804-canary-invisible-outfit-appearance
pr: 270
focused_validated_head: d26c308be08474d36deb9b5cd0fff71cdc8a2ec4
validation: PASS
fresh_audit: PASS
final_current_main_restack: pending
exact_final_ci: pending
protected_merge: pending
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
ownership:
  protocol_canary: retained
  shared_paths: released
next_action: Clean-restack exactly eight intended paths on current main, run exact-final CI and audit, protected-merge PR 270 and persist the post-merge checkpoint.
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 6
  session_id: OTC2-20260804T1831+0200-invisible-outfit
  session_started_at: 2026-08-04T18:31:00+02:00
  checkpointed_at: 2026-08-04T19:11:00+02:00
  last_progress_at: 2026-08-04T19:11:00+02:00
  phase: invisible-outfit-terminal-ci
  exact_head: pending_current_main_restack
  pull_request: 270
  active_operation: clean restack, exact-final CI, audit and protected merge
  external_run_ids:
    - 30931418621
    - 30931419201
  check_generation: invisible-outfit-final-restack
  status: active
  safe_to_resume: true
  resume_condition: Continue PR 270; do not recreate the branch or modify domain contracts.
  next_action: Restack eight intended paths on current main, validate exact head and merge.
```
