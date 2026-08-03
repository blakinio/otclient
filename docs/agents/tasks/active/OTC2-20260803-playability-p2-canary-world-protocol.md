---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: blocked
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: inbound-provenance-and-identity-contract-blocker
branch: docs/OTC2-20260803-canary-session-end-closeout
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T11:03:00+02:00
required_base_commit: "ceb24e22fc19305cb10c7ea29f7f16928def2a04"
risk: high
related_prs: [188, 190, 191, 192, 193, 196, 198]
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
  - asset decode and renderer resources
  - platform input adapter and product binding map
  - visible-world app composition and controlled M2 E2E
invocation_started_at: 2026-08-03T10:16:00+02:00
last_progress_at: 2026-08-03T11:03:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: closeout-terminal
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Reconcile Canary Current evidence with the Rust client while preserving fail-closed real admission, and implement only bounded gameplay mappings whose complete layouts, gates, ordering and semantic envelopes can be established without inference.

# Completed phases

- PR #188 merged the Current baseline and bounded outbound movement/stop/logout encoder.
- PR #190 merged the Windows generated-index LF repair.
- PR #191 recorded outbound closeout and released the `Cargo.lock` lease.
- PR #192 merged the pending-state-entered inbound decoder.
- PR #193 persisted the pending-state continuation checkpoint.
- PR #196 merged the bounded session-end inbound decoder and sanitized fixtures as `ceb24e22fc19305cb10c7ea29f7f16928def2a04`.
- Exact-head locked metadata, formatting, Clippy, workspace tests, architecture, Supply Chain and repository CI passed.
- Fresh exact-final-diff audit found zero open critical, high or material-medium findings.
- Real wire admission remains fail-closed before network I/O.
- No shared-path lease is held.

# Completed session-end family

```yaml
family: bootstrap_session_end
direction: server_to_client
producer_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
producer_method: sendSessionEndInformation
source_anchor: src/server/network/protocol/protocolgame.cpp:2932
wire_layout:
  opcode_u8: 0x18
  information_u8: SessionEndInformations
  post_send_effect: disconnect
accepted_values:
  0x00: SESSION_END_LOGOUT
  0x02: SESSION_END_FORCECLOSE
unknown_values: [0x01, 0x03]
semantic_mapping:
  accepted_values: GameEvent::SessionEnded(ServerClosed)
  rationale: isolated decoder has no proven caller-owned command history for Requested
order_state:
  session_fenced: true
  terminal_before_or_after_pending_state: true
  duplicate_end_rejected: true
result: merged
```

Original logical-message fixtures under `oteryn-client/tests/integration/canary-world-protocol/fixtures/` are synthetic and sanitized. They contain no credential, session key, private capture, proprietary asset byte or copied producer body.

# Inbound readiness matrix

| Family | Classification | Durable decision |
|---|---|---|
| session bootstrap | `PARTIAL` | `sendPendingStateEntered` is `PROVEN` and implemented. Exact one-byte `sendEnterWorld` cannot supply the player handle and position required by `BootstrapCompleted`; semantic completion is `BLOCKED`. |
| map description | `UNKNOWN` | Nested floor/tile/item/creature writers, branches, skip terminators and bounds are not normalized as one complete Current layout. |
| tile and stack updates | `PARTIAL` | Outer opcodes and positions are visible; nested tile bodies and stack-only identity resolution remain incomplete. |
| creature/entity appearance | `UNKNOWN` | Known-creature cache branches, removals, appearance fields, feature gates and nested bounds are incomplete. |
| movement and reconciliation | `PARTIAL` | Local/remote/teleport/floor/map-strip branches are incomplete; position plus stack does not prove a domain handle. |
| removal | `PARTIAL` | Position plus stack index cannot be converted to a protocol-neutral handle without an accepted authoritative identity-resolution contract. |
| session end/logout | `PARTIAL` | Exact `0x18` layout and values `0x00`/`0x02` are `PROVEN` and implemented; `0x01`/`0x03` remain `UNKNOWN` and fail closed. |

No partial map, tile, entity, movement or removal decoder is implemented. No parser owns or mutates simulation state.

# Acceptance

## Completed

- [x] generated-index metadata and public descriptor mechanically agree;
- [x] historical cuts remain explicit historical evidence;
- [x] real admission remains `RealAdmissionUnavailable`;
- [x] outbound movement/stop/logout encoding is session-fenced and source-evidenced;
- [x] PR #190 is merged and the Windows newline failure is mechanically explained;
- [x] the `Cargo.lock` lease is released;
- [x] pending-state parsing is bounded, session-fenced and fail-closed;
- [x] session-end opcode, width, known values and terminal effect are proven;
- [x] only `0x00` and `0x02` are accepted; `0x01` and `0x03` fail closed;
- [x] raw Canary reason bytes do not escape the adapter;
- [x] truncation, wrong opcode, trailing, oversized, unknown reason, duplicate end and stale session are covered;
- [x] positive and negative fixtures are original and sanitized;
- [x] focused and exact-head package/workspace validation passed;
- [x] fresh exact-final-diff audit has zero open material finding;
- [x] PR #196 is merged and all review threads are terminal.

## Remaining package acceptance

- [ ] complete provenance-safe map/entity/movement/removal layouts and semantic identity resolution become available;
- [ ] map, tile, stack, entity and reconciliation parsing is deterministic and complete;
- [ ] package final audit, archive and ownership release occur only when the declared P2 producer package is genuinely complete.

# Stop condition

The bounded normalization pass exhausted the accepted evidence without establishing complete Current map/entity/movement/removal layouts or an accepted owner for position/stack-to-domain-handle identity resolution. Guessing those contracts is forbidden. The parent task remains active but blocked; it is not archived and exclusive protocol ownership is not released. No shared lease is retained.

# Claim boundary

This producer consumes already decrypted and deframed logical messages only. It does not change admission, TLS, authentication, framing, compression, credentials, transport lifecycle, simulation, rendering, assets, input, UI or application composition. It does not prove deployed Canary equality, visible-world functionality or M2 completion.

## Context checkpoint

```yaml
checkpoint_version: 15
updated_at: 2026-08-03T11:03:00+02:00
base: ceb24e22fc19305cb10c7ea29f7f16928def2a04
status: blocked
phase: inbound-provenance-and-identity-contract-blocker
implementation:
  pr: 196
  head: a2ea69ea3801df0bbba20caaf6ab7d8677b52bb7
  merge_commit: ceb24e22fc19305cb10c7ea29f7f16928def2a04
validation:
  repaired_generation:
    head: 8078a56411991ceb869f8965faf75bd3527e3db9
    rust_client_run: 30798587290
    windows_job: 91637729025
    result: FORMAT_FAILURE_REPAIRED
    supply_chain_job: 91637728937
    supply_chain: PASS
  validated_head: a2ea69ea3801df0bbba20caaf6ab7d8677b52bb7
  rust_client_run: 30798845230
  windows_job: 91638521494
  locked_metadata: PASS
  formatting: PASS
  clippy: PASS
  workspace_tests: PASS
  architecture: PASS
  supply_chain_job: 91638521428
  supply_chain: PASS
  repository_ci_run: 30798845350
  repository_required_job: 91638983873
  repository_ci: PASS
  ready_state_ci_run: 30799161107
  ready_state_required_job: 91639989636
  ready_state_ci: PASS
fresh_audit:
  result: PASS
  validator: fresh_connector_audit_role
  review_id: 4842339967
  critical_open: 0
  high_open: 0
  material_medium_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: The isolated producer consumes already decrypted and deframed logical messages and has no reachable application or real transport composition; controlled visible-world E2E belongs to later P2 integration and acceptance tasks.
pr_hygiene:
  merged_prs: [188, 190, 191, 192, 193, 196]
  unresolved_review_threads: 0
  requested_changes: 0
shared_path_lease: []
ownership:
  protocol_canary: retained_by_blocked_parent_task
  shared_paths: released
blocker: Complete provenance-safe Current map/entity/movement/removal layouts and an accepted position/stack-to-domain-handle identity-resolution ownership contract are unavailable at the pinned revision after bounded evidence normalization.
next_action: Obtain and accept one complete pinned remaining-family layout plus its identity-resolution contract, then resume this same task; do not infer missing fields or ownership.
```
