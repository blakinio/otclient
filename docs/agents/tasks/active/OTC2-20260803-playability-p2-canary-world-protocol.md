---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: validating
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: session-end-inbound-exact-head-validation
branch: feat/OTC2-20260803-canary-session-end-inbound
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T10:40:00+02:00
required_base_commit: "d18b618fc68c0e67598be10dee6f1d0119bc8aa8"
risk: high
related_prs:
  - 188
  - 190
  - 191
  - 192
  - 193
  - 196
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
  - provenance-safe complete M2 map/entity/movement/removal layouts and identity resolution
  - asset decode and renderer resources
  - platform input adapter and product binding map
  - visible-world app composition and controlled M2 E2E
invocation_started_at: 2026-08-03T10:16:00+02:00
last_progress_at: 2026-08-03T10:40:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: session-end-implementation
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Reconcile Canary Current evidence with the Rust client while preserving fail-closed real admission, and implement only bounded gameplay mappings whose complete layouts, gates, ordering and semantic envelopes can be established without inference.

# Completed phases

- Current baseline and bounded outbound movement/stop/logout encoder merged in PR #188;
- Windows generated-index LF repair merged in PR #190;
- outbound lifecycle closeout and `Cargo.lock` lease release merged in PR #191;
- pending-state-entered inbound decoder merged in PR #192;
- pending-state continuation checkpoint merged in PR #193;
- real wire admission remains fail-closed before network I/O;
- no shared-path lease is held.

# Current bounded family

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
unknown_values:
  - 0x01
  - 0x03
semantic_mapping:
  accepted_values: GameEvent::SessionEnded(ServerClosed)
  rationale: isolated decoder has no proven caller-owned command history for Requested
order_state:
  session_fenced: true
  terminal_before_or_after_pending_state: true
  duplicate_end_rejected: true
pr: 196
result: validating
```

Original sanitized logical-message fixtures are stored under `oteryn-client/tests/integration/canary-world-protocol/fixtures/`. They contain no credential, session key, private capture, proprietary asset byte or copied producer implementation body.

# Inbound readiness decision

| Family | State | Decision |
|---|---|---|
| pending-state bootstrap | `PROVEN` | merged and implemented |
| enter-world/bootstrap completion | `PARTIAL` | exact one-byte layout exists, but payload cannot supply the player handle and position required by `BootstrapCompleted`; unimplemented |
| map description | `UNKNOWN` | nested floor/tile/item/creature writers, terminators, branches and bounds are not yet normalized completely |
| tile/stack updates | `PARTIAL` | outer layouts exist, but nested tile bodies and stack-only identity resolution are incomplete |
| creature/entity appearance | `UNKNOWN` | known-creature branches, feature fields and nested appearance bounds are incomplete |
| movement/reconciliation | `PARTIAL` | multiple local/remote/teleport/floor branches and stack-based identity require complete normalization and accepted identity resolution |
| removal | `PARTIAL` | position plus stack does not prove a protocol-neutral handle without authoritative state |
| session end/logout | `PARTIAL` | known codes are proven and implemented; `0x01` and `0x03` remain `UNKNOWN` and rejected |

No partial map, tile, entity, movement or removal decoder is implemented. No parser owns or mutates simulation state.

# Acceptance

## Completed baseline and outbound phase

- [x] generated-index metadata and public descriptor mechanically agree;
- [x] historical cuts remain explicit historical evidence;
- [x] real admission remains `RealAdmissionUnavailable`;
- [x] outbound movement/stop/logout encoding is session-fenced and source-evidenced;
- [x] exact-head Windows workspace, architecture, Supply Chain and repository CI passed;
- [x] shared `Cargo.lock` lease is released.

## Pending-state inbound phase

- [x] exact one-byte `0x0A` layout is represented without adjacent-packet inference;
- [x] parser emits only `GameEventEnvelope::v1(GameEvent::BootstrapStarted)`;
- [x] malformed, duplicate/out-of-order and stale-session input fails closed;
- [x] exact-head validation and fresh audit passed;
- [x] bounded phase merged.

## Session-end inbound phase

- [x] generated index and exact producer body prove opcode, one-byte reason layout and terminal disconnect;
- [x] exact enum definition proves numeric values and unknown values remain explicit;
- [x] only `0x00` and `0x02` are accepted; `0x01` and `0x03` fail closed;
- [x] raw Canary reason bytes do not escape the adapter;
- [x] parser is session-fenced, terminal and state-atomic;
- [x] truncation, wrong opcode, trailing, oversized, unknown reason, duplicate end and stale session are covered;
- [x] positive and negative fixtures are original and sanitized;
- [ ] focused and exact-head package/workspace validation pass;
- [ ] fresh exact-final-diff audit has zero open material finding;
- [ ] PR #196 is intentionally terminal.

## Remaining package acceptance

- [ ] complete provenance-safe map/entity/movement/removal layouts and semantic identity resolution become available;
- [ ] map, tile, stack, entity and reconciliation parsing is deterministic and complete;
- [ ] package final audit, merge, archive and ownership release occur only when the declared P2 producer package is genuinely complete.

# Claim boundary

This phase consumes already decrypted and deframed logical messages only. It does not change admission, TLS, authentication, framing, compression, credentials, transport lifecycle, simulation, rendering, assets, input, UI or application composition. It does not prove deployed Canary equality, visible-world functionality or M2 completion.

## Context checkpoint

```yaml
checkpoint_version: 12
updated_at: 2026-08-03T10:40:00+02:00
base: d18b618fc68c0e67598be10dee6f1d0119bc8aa8
branch: feat/OTC2-20260803-canary-session-end-inbound
head_before_checkpoint: 5350b354ce78edb5fa193fae7fa8bff9eb7cfd77
pr:
  number: 196
  state: draft
status: validating
phase: session-end-inbound-exact-head-validation
changed_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/crates/protocol-canary/src/inbound.rs
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/README.md
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/pending-state-entered.hex
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/pending-state-wrong-opcode.hex
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/session-end-logout.hex
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/session-end-force-close.hex
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/session-end-unknown-reason.hex
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/session-end-trailing.hex
validation:
  current_head_runs:
    rust_client: 30798395871
    repository_ci: 30798395841
  state: pending
fresh_audit:
  result: pending
  validator: fresh_connector_audit_role
  material_findings_open: unknown
e2e:
  result: NOT_APPLICABLE
  reason: This isolated logical-message producer has no real transport or reachable application consumer; controlled visible-world E2E belongs to the later P2 integration and acceptance tasks.
pr_hygiene:
  unresolved_review_threads: 0
  requested_changes: 0
shared_path_lease: []
blockers: []
next_action: Complete exact-head CI and a fresh falsification audit for PR 196, remediate material findings, then merge the bounded family and persist the exact remaining provenance blocker without taking a shared lease.
```
