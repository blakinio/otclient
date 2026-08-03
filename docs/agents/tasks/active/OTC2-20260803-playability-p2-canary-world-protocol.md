---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: validating
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: pending-state-terminal-ci
branch: feat/OTC2-20260803-canary-pending-state-inbound
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T09:36:00+02:00
required_base_commit: "3e88bf21db7dfea1066a1b6729946da282c2e283"
risk: high
related_prs:
  - 188
  - 190
  - 191
  - 192
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
last_progress_at: 2026-08-03T09:36:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: pending-state-final-exact-head
terminal_ci_wait_started_at: 2026-08-03T09:36:00+02:00
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Reconcile Canary Current evidence with the Rust client while preserving fail-closed real admission, and implement only bounded gameplay mappings whose complete layouts, gates and ordering can be established without inference.

# Completed phases

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
  classification: derived_from_exact_pending-state-boundary
consumer_precondition: session-fenced bootstrap state explicitly awaits pending-state-entered
```

# Acceptance

## Completed baseline and outbound phase

- [x] generated-index metadata and public descriptor mechanically agree;
- [x] historical cuts remain explicit historical evidence;
- [x] real admission remains `RealAdmissionUnavailable`;
- [x] outbound movement/stop/logout encoding is session-fenced and source-evidenced;
- [x] exact-head Windows workspace, architecture, Supply Chain and repository CI pass;
- [x] shared Cargo.lock lease is released.

## Pending-state inbound phase

- [x] exact one-byte `0x0A` layout is represented without adjacent-packet inference;
- [x] parser consumes an already decrypted/deframed logical message only;
- [x] parser emits only `GameEventEnvelope::v1(GameEvent::BootstrapStarted)` for the current session;
- [x] bootstrap order state owns its `SessionToken` and advances only after complete success;
- [x] empty, wrong-opcode, trailing, oversized, duplicate/out-of-order and stale-session input fail closed;
- [x] generated-index drift test proves direction, phase, family, method, opcode and source anchor;
- [x] parser owns no transport, simulation, renderer, asset, input, UI or application state;
- [x] pinned format, workspace Clippy, workspace tests, architecture and Supply Chain pass;
- [x] fresh exact-diff audit has zero open material finding;
- [ ] final checkpoint exact-head Windows workspace, Supply Chain and repository CI pass;
- [ ] bounded phase protected-merges and task continues to the next proven inbound family.

# Claim boundary

The packet body is exactly one opcode byte. The semantic mapping to `BootstrapStarted` is a Rust-domain interpretation of the producer pending-state boundary, not a claim that any deployed server matches the inspected source. No real network admission, framing, encryption, map layout, entity layout or neighboring bootstrap packet is authorized by this phase.

## Context checkpoint

```yaml
checkpoint_version: 10
updated_at: 2026-08-03T09:36:00+02:00
base: 3e88bf21db7dfea1066a1b6729946da282c2e283
branch: feat/OTC2-20260803-canary-pending-state-inbound
pr: 192
status: validating
phase: pending-state-terminal-ci
validated_implementation_head: e745f1ede79d6a1e70857c5e7e4fdd2fa267445d
proven:
  - exact source and generated index establish the complete one-byte 0x0A layout and source anchor
  - exact call site establishes version gate and order between Tibia time and enter-world/map bootstrap
  - bootstrap order state is fenced to one SessionToken and rejects reuse after relog
  - only BootstrapStarted is emitted and real admission remains fail-closed
  - all negative cases leave state unchanged except successful completion
validation:
  rust_client_run: 30794151809
  windows_job: 91623840188
  cargo_metadata_locked: PASS
  cargo_fmt: PASS
  workspace_clippy: PASS
  workspace_tests: PASS
  architecture: PASS
  supply_chain_job: 91623840192
  supply_chain: PASS
  repository_ci_run: 30794152312
  repository_ci: PASS
fresh_audit:
  result: PASS
  validator: fresh_connector_audit_role
  material_findings_open: 0
  resolved_findings:
    - id: P2-CANARY-INBOUND-BOUND-001
      disposition: use CANARY_NETWORK_MESSAGE_MAX_BYTES for server-to-client input
    - id: P2-CANARY-INBOUND-SESSION-001
      disposition: order state owns and validates SessionToken
  inspected:
    - exact source and generated-index evidence
    - public API and dependency direction
    - state mutation and error precedence
    - malformed, duplicate and stale-session negatives
    - real-admission, secret and private-fixture boundaries
e2e:
  result: NOT_APPLICABLE
  reason: This isolated decoder consumes no real transport and has no reachable application composition; controlled visible-world E2E remains a later P2 integration gate.
shared_path_lease: []
unknown:
  - deployed Canary revision and configuration
  - framing, encryption and admission transcript
  - layouts of enter-world, map-description and all other inbound families
blockers: []
next_action: Observe retained exact-head CI for this final checkpoint, mark PR 192 ready, enable protected auto-merge, verify merge, then write the mandatory continuation checkpoint for the next fully proven inbound family.
```
