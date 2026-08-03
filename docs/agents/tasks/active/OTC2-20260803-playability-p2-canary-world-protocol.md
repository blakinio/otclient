---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: implementing
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: pending-state-inbound
branch: feat/OTC2-20260803-canary-pending-state-inbound
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T09:18:00+02:00
required_base_commit: "3e88bf21db7dfea1066a1b6729946da282c2e283"
risk: high
related_prs:
  - 188
  - 190
  - 191
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
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
context_pressure: high
decomposition_decision: phased
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - remaining provenance-safe M2 inbound bootstrap/map/entity layouts and fixtures
  - asset decode and renderer resources
  - platform input adapter and product binding map
  - visible-world app composition and controlled M2 E2E
invocation_started_at: 2026-08-03T08:24:00+02:00
last_progress_at: 2026-08-03T09:18:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: pending-state-implementation
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Reconcile Canary Current evidence with the Rust client while preserving fail-closed real admission, and implement only bounded gameplay mappings whose complete layouts, gates and ordering can be established without inference.

# Completed phase

- Current baseline and bounded outbound movement/stop/logout encoder merged in PR #188;
- Windows generated-index LF repair merged in PR #190;
- outbound lifecycle closeout and Cargo.lock lease release merged in PR #191;
- exact-head Windows workspace, architecture, Supply Chain and repository CI passed;
- real wire admission remains fail-closed before network I/O.

# Active bounded inbound family

```yaml
family: bootstrap_pending_state_entered
direction: server_to_client
opcode: 0x0A
producer_method: sendPendingStateEntered
producer_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
producer_source: src/server/network/protocol/protocolgame.cpp
producer_opcode_line: 8502
wire_layout:
  bytes: [0x0A]
  payload_bytes: 0
producer_gates:
  - player exists
  - oldProtocol is false
  - login bootstrap version is at least 980
producer_order:
  after: sendTibiaTime
  before:
    - sendEnterWorld
    - sendMapDescription
semantic_mapping:
  event: GameEvent::BootstrapStarted
  classification: derived_from_exact_pending-state_boundary
consumer_precondition: caller explicitly awaits pending-state-entered
```

The exact source emits only opcode `0x0A`; the call site establishes that it occurs after Tibia time and immediately before enter-world/map bootstrap for version `>= 980`. The Current profile is version `1525` and is not the legacy protocol. The parser will not infer any adjacent packet layout.

# Acceptance

## Completed baseline and outbound phase

- [x] generated-index metadata and public descriptor mechanically agree;
- [x] historical cuts remain explicit historical evidence;
- [x] real admission remains `RealAdmissionUnavailable`;
- [x] outbound movement/stop/logout encoding is session-fenced and source-evidenced;
- [x] exact-head Windows workspace, architecture, Supply Chain and repository CI pass;
- [x] shared Cargo.lock lease is released.

## Pending-state inbound phase

- [ ] exact one-byte `0x0A` layout is represented without adjacent-packet inference;
- [ ] parser consumes an already decrypted/deframed logical message only;
- [ ] parser emits only a current-session `GameEventEnvelope::v1(GameEvent::BootstrapStarted)`;
- [ ] explicit bootstrap order state advances only after successful complete parsing;
- [ ] empty, wrong-opcode, trailing, oversized, duplicate/out-of-order and stale-session input fail closed;
- [ ] generated-index drift test proves direction, phase, family, method, opcode and source anchor;
- [ ] parser owns no transport, simulation, renderer, asset, input, UI or application state;
- [ ] focused format, strict Clippy, package tests and architecture validation pass;
- [ ] fresh exact-diff audit has zero open material finding;
- [ ] exact-head Windows workspace, Supply Chain and repository CI pass;
- [ ] bounded phase protected-merges and task continues to the next proven inbound family.

# Claim boundary

The packet body is exactly one opcode byte. The semantic mapping to `BootstrapStarted` is a Rust-domain interpretation of the producer's pending-state boundary, not a claim that any deployed server revision matches the inspected source. No real network admission, framing, encryption, map layout, entity layout or neighboring bootstrap packet is authorized by this phase.

## Context checkpoint

```yaml
checkpoint_version: 9
updated_at: 2026-08-03T09:18:00+02:00
base: 3e88bf21db7dfea1066a1b6729946da282c2e283
branch: feat/OTC2-20260803-canary-pending-state-inbound
status: implementing
phase: pending-state-inbound
proven:
  - generated index records server-to-client bootstrap sendPendingStateEntered at opcode 0x0A and source line 8502
  - exact producer method writes only 0x0A when player exists and oldProtocol is false
  - exact login call site invokes it for version >= 980 after sendTibiaTime and before sendEnterWorld and sendMapDescription
  - Current development profile is version 1525 and non-legacy
  - GameEvent vocabulary already contains BootstrapStarted and GameEventEnvelope session fencing
  - protocol-core provides bounded reads and trailing-data rejection
unknown:
  - deployed Canary revision and configuration
  - framing/encryption/admission transcript
  - layouts of enter-world, map-description and all other inbound families
shared_path_lease: []
blockers: []
next_action: Implement one isolated pending-state decoder and exhaustive negative tests inside protocol-canary, update evidence, then run retained exact-head validation and fresh audit.
```
