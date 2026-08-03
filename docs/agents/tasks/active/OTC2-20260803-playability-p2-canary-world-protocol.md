---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: blocked
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: inbound-map-layout-and-general-identity-blocker
branch: docs/OTC2-20260803-canary-bootstrap-identity-closeout
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T16:25:00+02:00
required_base_commit: "d6ac5c89a378d58ef4bdbd7ba0e5a61f686e4e0a"
risk: high
related_prs: [188, 190, 191, 192, 193, 196, 198, 203, 204, 219, 220, 221]
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/crates/protocol-canary/**
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
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
  - complete provenance-safe Current map/tile/item/creature layouts
  - complete movement/removal branch layouts
  - accepted general position/stack-to-domain-handle identity-resolution ownership contract
  - product binding map and visible-world composition
  - controlled real M2 acceptance
invocation_started_at: 2026-08-03T10:16:00+02:00
last_progress_at: 2026-08-03T16:25:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: bootstrap-identity-closeout
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 2
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 3
stall_warnings: 0
---

# Goal

Reconcile Canary Current evidence with the Rust client while preserving fail-closed real admission, and implement only bounded gameplay mappings whose complete layouts, gates, ordering and semantic envelopes can be established without inference.

# Completed bootstrap identity phase

The pinned Current/non-legacy login path proves and now implements this exact order:

```yaml
local_player_initialization:
  opcode: 0x17
  retained_output: session_fenced_EntityHandle
  discarded_fields:
    - server_beat
    - three LoginSpeedFormula components
    - fixed capability bytes
    - store URL
    - store coin packet
    - exiva flag
pending_state:
  opcode: 0x0A
  prerequisite: local_player_identity
  output: GameEvent::BootstrapStarted
enter_world:
  opcode: 0x0F
  prerequisites: [local_player_identity, pending_state]
  output: caller_owned_order_state_only
bootstrap_completed:
  emitted: false
  reason: validated map position is still unavailable
```

The decoder is session-fenced and state-atomic. It rejects truncation, wrong opcode, bad Current precision, non-zero fixed capability bytes, invalid boolean, zero identity, oversize, trailing data, stale session, duplicates and impossible order. Producer tuning/store fields never escape the adapter.

# Previously completed protocol slices

- PR #188 merged the Current baseline and bounded outbound movement/stop/logout encoder.
- PR #190 merged the generated-index Windows LF repair.
- PR #191 recorded outbound closeout and released the `Cargo.lock` lease.
- PR #192 merged pending-state parsing.
- PR #193 persisted its continuation checkpoint.
- PR #196 merged known session-end parsing and sanitized fixtures.
- PR #198 recorded exact validation, audit and the earlier provenance blocker.
- PR #203 refreshed the P2 barrier after independent producers archived.

# Phase integration

```yaml
focused_product_head: ec34134aee42fd687f4f195025362189e49c9dbc
superseded_validation_prs: [204, 219]
restacked_head: 0690084045c5dc70b6632a424c9c6ede2cc20b62
implementation_pr: 220
implementation_merge: 1c820ff6b87f8459bc300e5baeed0e395b6147c8
temporary_runner_cleanup_pr: 221
cleanup_merge: d6ac5c89a378d58ef4bdbd7ba0e5a61f686e4e0a
changed_product_paths: 10
temporary_workflows_remaining: 0
shared_path_lease: []
```

PR #204 and PR #219 were closed without merge only to obtain a check suite on an exact current-main restack. Their product tree was preserved exactly in PR #220. One-shot helper PRs #209, #210, #211, #212, #214, #216 and #218 were closed without merge. Temporary registration/repair PRs #205, #206, #207, #208, #213, #215 and #217 were fully removed from permanent workflow state by PR #221.

# Validation

```yaml
focused_validation:
  run: 30820529534
  job: 91709031623
  locked_metadata: PASS
  formatting: PASS
  strict_package_clippy: PASS
  protocol_canary_tests: 39_PASS
  architecture: PASS
historical_exact_product_validation:
  rust_client_run: 30820898939
  windows_job: 91710269111
  supply_chain_job: 91710269088
  repository_ci_run: 30820901761
  repository_required_job: 91710582767
  ready_state_ci_run: 30821199078
  ready_state_required_job: 91711540014
  result: PASS
restacked_exact_head_validation:
  head: 0690084045c5dc70b6632a424c9c6ede2cc20b62
  rust_client_run: 30821884378
  windows_job: 91713561582
  supply_chain_job: 91713561705
  repository_ci_run: 30821887730
  repository_required_job: 91713897019
  result: PASS
cleanup_validation:
  repository_ci_run: 30822271162
  repository_required_job: 91715246698
  result: PASS
fresh_audit:
  product_review_id: 4844933812
  restack_review_id: 4845040720
  critical_open: 0
  high_open: 0
  material_medium_open: 0
unresolved_review_threads: 0
e2e:
  result: NOT_APPLICABLE
  reason: The isolated decoder consumes already decrypted and deframed logical messages and has no reachable real transport, simulation composition or user journey.
```

# Inbound readiness matrix

| Family | Classification | Durable decision |
|---|---|---|
| session bootstrap | `PARTIAL` | Local-player identity `0x17`, pending-state `0x0A` and enter-world `0x0F` are proven and implemented in exact order. Complete map-description position/body remains required before `BootstrapCompleted`. |
| map description | `UNKNOWN` | Floor/tile iteration, skip markers and nested item/creature writers are not normalized as one complete Current layout. |
| tile and stack updates | `PARTIAL` | Outer opcodes and positions are visible; nested tile bodies and authoritative stack identity remain incomplete. |
| creature/entity appearance | `UNKNOWN` | Known-creature cache branches, removals, appearance fields, gates and nested bounds are incomplete. |
| movement and reconciliation | `PARTIAL` | Local/remote/teleport/floor/map-strip branches remain incomplete; position plus stack does not prove a domain handle. |
| removal | `PARTIAL` | Position plus stack index cannot be converted to a protocol-neutral handle without authoritative state ownership. |
| session end/logout | `PARTIAL` | Exact `0x18` layout and values `0x00`/`0x02` are implemented; `0x01`/`0x03` remain unknown and rejected. |

No partial map, tile, entity, movement or removal decoder is implemented. No parser mutates simulation state. Real admission remains `RealAdmissionUnavailable` before network I/O.

# P2 barrier

```yaml
simulation_snapshot: archived
asset_decode: archived
renderer_resource: archived
input_platform: archived
canary_world_protocol: blocked_not_archived
visible_world_integration: not_ready
controlled_m2_acceptance: not_ready
```

The Visible World Integration worker requires all five prerequisite producers to be merged and separately archived. This parent Canary producer remains incomplete and therefore retains exclusive `protocol-canary` ownership. No shared lease is held.

# Stop condition

The bounded source/evidence pass now proves local bootstrap identity and order, but still does not establish one complete Current map-description family, all nested tile/item/creature branches, or an accepted general position/stack-to-domain-handle identity-resolution owner. Guessing those fields or ownership is forbidden.

# Durable checkpoint

```yaml
checkpoint_version: 18
updated_at: 2026-08-03T16:25:00+02:00
observed_main: d6ac5c89a378d58ef4bdbd7ba0e5a61f686e4e0a
status: blocked
phase: inbound-map-layout-and-general-identity-blocker
implemented_bootstrap_order: [local_player_0x17, pending_state_0x0A, enter_world_0x0F]
implementation_pr: 220
implementation_merge: 1c820ff6b87f8459bc300e5baeed0e395b6147c8
cleanup_pr: 221
cleanup_merge: d6ac5c89a378d58ef4bdbd7ba0e5a61f686e4e0a
shared_path_lease: []
ownership:
  protocol_canary: retained_by_blocked_parent_task
  shared_paths: released
blocker: Complete provenance-safe Current map/tile/item/creature layouts, remaining movement/removal branches and an accepted general position/stack-to-domain-handle identity-resolution ownership contract are unavailable at the pinned revision after bounded normalization.
next_action: Obtain and accept one complete pinned map-description layout plus its nested writer bounds and authoritative identity-resolution contract, then resume this same task without inferring fields or ownership.
```
