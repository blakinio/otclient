---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: blocked
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: inbound-provenance-and-identity-contract-blocker
branch: docs/OTC2-20260803-canary-p2-barrier-refresh
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T13:58:00+02:00
required_base_commit: "bf764ee5c3cb546f5507fc1fbb2b7cad79a00cd0"
risk: high
related_prs: [188, 190, 191, 192, 193, 194, 195, 196, 198, 199, 200, 201, 202]
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
  - complete provenance-safe Current map/entity/movement/removal layouts
  - accepted position/stack-to-domain-handle identity-resolution ownership contract
  - product binding map and visible-world composition
  - controlled real M2 acceptance
invocation_started_at: 2026-08-03T10:16:00+02:00
last_progress_at: 2026-08-03T13:58:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: blocker-refresh
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 1
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 2
stall_warnings: 0
---

# Goal

Reconcile Canary Current evidence with the Rust client while preserving fail-closed real admission, and implement only bounded gameplay mappings whose complete layouts, gates, ordering and semantic envelopes can be established without inference.

# Completed protocol slices

- PR #188 merged the Current baseline and bounded outbound movement/stop/logout encoder.
- PR #190 merged the Windows generated-index LF repair.
- PR #191 recorded outbound closeout and released the `Cargo.lock` lease.
- PR #192 merged the pending-state-entered inbound decoder.
- PR #193 persisted the pending-state continuation checkpoint.
- PR #196 merged the bounded session-end inbound decoder and sanitized fixtures as `ceb24e22fc19305cb10c7ea29f7f16928def2a04`.
- PR #198 recorded exact validation, audit and the provenance blocker.
- Real wire admission remains `RealAdmissionUnavailable` and no shared-path lease is held.

# Proven inbound contract

```yaml
pending_state:
  producer_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
  method: sendPendingStateEntered
  bytes: [0x0A]
  event: GameEvent::BootstrapStarted
  result: implemented
session_end:
  producer_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
  method: sendSessionEndInformation
  layout: [opcode_0x18, information_u8]
  accepted_values:
    0x00: SESSION_END_LOGOUT
    0x02: SESSION_END_FORCECLOSE
  unknown_values: [0x01, 0x03]
  event: GameEvent::SessionEnded(ServerClosed)
  result: implemented
```

Both decoders consume already decrypted and deframed logical messages, are session-fenced and state-atomic, reject truncation/trailing/oversized/unknown/stale/duplicate input and expose no Canary wire field outside the adapter.

# Inbound readiness matrix

| Family | Classification | Durable decision |
|---|---|---|
| session bootstrap | `PARTIAL` | Pending-state is `PROVEN`. Exact one-byte `sendEnterWorld` cannot supply the player handle and position required by `BootstrapCompleted`; semantic completion is `BLOCKED`. |
| map description | `UNKNOWN` | Nested floor/tile/item/creature writers, branches, skip terminators and bounds are not normalized as one complete Current layout. |
| tile and stack updates | `PARTIAL` | Outer opcodes and positions are visible; nested tile bodies and stack-only identity resolution remain incomplete. |
| creature/entity appearance | `UNKNOWN` | Known-creature cache branches, removals, appearance fields, feature gates and nested bounds are incomplete. |
| movement and reconciliation | `PARTIAL` | Local/remote/teleport/floor/map-strip branches are incomplete; position plus stack does not prove a domain handle. |
| removal | `PARTIAL` | Position plus stack index cannot be converted to a protocol-neutral handle without an accepted authoritative identity-resolution contract. |
| session end/logout | `PARTIAL` | Exact `0x18` layout and values `0x00`/`0x02` are implemented; `0x01`/`0x03` remain `UNKNOWN` and fail closed. |

No partial map, tile, entity, movement or removal decoder is implemented. No parser owns or mutates simulation state.

# P2 barrier refresh

The independent P2 producers that do not depend on the missing Canary world layouts are now terminal:

```yaml
simulation_snapshot:
  implementation_pr: 186
  archive_pr: 187
  state: archived
asset_decode:
  implementation_pr: 194
  archive_pr: 199
  archive_commit: 1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2
renderer_resource:
  implementation_pr: 200
  archive_pr: 201
  archive_commit: 8a3ce18f8fe98c5654ac3ce36c098404bdfc3343
input_platform:
  implementation_pr: 195
  archive_pr: 202
  archive_commit: bf764ee5c3cb546f5507fc1fbb2b7cad79a00cd0
```

The Visible World Integration prompt requires all five prerequisite producers to be merged and separately archived. Canary World Protocol is not complete or archived, so creating a Visible World task, branch or PR would violate the accepted barrier. Controlled M2 acceptance is consequently also not READY.

# Validation and audit of implemented slices

```yaml
implementation_head: a2ea69ea3801df0bbba20caaf6ab7d8677b52bb7
implementation_merge: ceb24e22fc19305cb10c7ea29f7f16928def2a04
rust_client_run: 30798845230
windows_job: 91638521494
supply_chain_job: 91638521428
repository_ci_run: 30798845350
repository_required_job: 91638983873
ready_state_ci_run: 30799161107
ready_state_required_job: 91639989636
result: PASS
fresh_audit:
  review_id: 4842339967
  critical_open: 0
  high_open: 0
  material_medium_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: Isolated logical-message producer has no reachable real transport or application composition.
```

# Stop condition

The accepted evidence at the pinned source revision remains unchanged. It does not establish complete Current map/entity/movement/removal layouts or an accepted owner for position/stack-to-domain-handle identity resolution. Guessing either contract is forbidden. The parent task remains active and blocked; it is not archived and exclusive protocol ownership remains held. No shared lease is retained.

# Durable checkpoint

```yaml
checkpoint_version: 16
updated_at: 2026-08-03T13:58:00+02:00
observed_main: bf764ee5c3cb546f5507fc1fbb2b7cad79a00cd0
status: blocked
phase: inbound-provenance-and-identity-contract-blocker
unchanged_state_check: 1
protocol_implementation:
  pr: 196
  head: a2ea69ea3801df0bbba20caaf6ab7d8677b52bb7
  merge_commit: ceb24e22fc19305cb10c7ea29f7f16928def2a04
p2_barrier:
  simulation_snapshot: archived
  asset_decode: archived
  renderer_resource: archived
  input_platform: archived
  canary_world_protocol: blocked_not_archived
  visible_world_integration: not_ready
  controlled_m2_acceptance: not_ready
pr_hygiene:
  unresolved_review_threads: 0
  requested_changes: 0
shared_path_lease: []
ownership:
  protocol_canary: retained_by_blocked_parent_task
  shared_paths: released
blocker: Complete provenance-safe Current map/entity/movement/removal layouts and an accepted position/stack-to-domain-handle identity-resolution ownership contract are unavailable at the pinned revision after bounded evidence normalization.
next_action: Obtain and accept one complete pinned remaining-family layout plus its identity-resolution contract, then resume this same task; do not infer missing fields or ownership.
```
