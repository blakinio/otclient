---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: ready
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: next-inbound-family-evidence
branch: docs/OTC2-20260803-canary-pending-state-closeout
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T09:46:00+02:00
required_base_commit: "ee4ce5fa6da70ccd49c492ea4c6406694197d68d"
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
last_progress_at: 2026-08-03T09:46:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: next-inbound-evidence
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Reconcile Canary Current evidence with the Rust client while preserving fail-closed real admission, and implement only bounded gameplay mappings whose complete layouts, gates, ordering and semantic envelopes can be established without inference.

# Completed phases

- Current baseline and bounded outbound movement/stop/logout encoder merged in PR #188;
- Windows generated-index LF repair merged in PR #190;
- outbound lifecycle closeout and Cargo.lock lease release merged in PR #191;
- pending-state-entered inbound decoder merged in PR #192 as `ee4ce5fa6da70ccd49c492ea4c6406694197d68d`;
- exact-head Windows workspace, architecture and Supply Chain passed for the final PR #192 head;
- general repository CI passed on the exact implementation head before the documentation/evidence checkpoint;
- the final documentation/evidence checkpoint general CI generation was cancelled by the protected auto-merge transition, while the retained Rust exact-head workflow completed successfully;
- real wire admission remains fail-closed before network I/O;
- no shared-path lease is held.

# Completed pending-state family

```yaml
family: bootstrap_pending_state_entered
direction: server_to_client
opcode: 0x0A
producer_method: sendPendingStateEntered
producer_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
wire_layout:
  bytes: [0x0A]
  payload_bytes: 0
semantic_mapping:
  event: GameEvent::BootstrapStarted
order_state: session_fenced
result: merged
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
- [x] bounded phase protected-merged and the task continues.

## Remaining inbound programme

- [ ] identify the next family whose complete wire layout, gates, ordering and existing `GameEvent` semantic mapping are all proven;
- [ ] leave source-complete packets unimplemented when no accepted domain event exists;
- [ ] normalize complete map/entity/bootstrap layouts and original sanitized negative fixtures;
- [ ] reach controlled visible-world integration without weakening real admission.

# Claim boundary

The pending-state packet body is exactly one opcode byte. Its mapping to `BootstrapStarted` is a Rust-domain interpretation of the exact producer boundary, not a claim that a deployed server matches the inspected source. No real network admission, framing, encryption, map layout, entity layout or neighboring bootstrap packet is authorized by this phase.

## Context checkpoint

```yaml
checkpoint_version: 11
updated_at: 2026-08-03T09:46:00+02:00
base: ee4ce5fa6da70ccd49c492ea4c6406694197d68d
branch: docs/OTC2-20260803-canary-pending-state-closeout
status: ready
phase: next-inbound-family-evidence
terminal_pr:
  number: 192
  state: merged
  merge_commit: ee4ce5fa6da70ccd49c492ea4c6406694197d68d
validation:
  implementation_head: e745f1ede79d6a1e70857c5e7e4fdd2fa267445d
  implementation_rust_client_run: 30794151809
  implementation_windows_job: 91623840188
  implementation_repository_ci_run: 30794152312
  implementation_repository_ci: PASS
  final_checkpoint_head: 9c71de1b9e7d5500d36ef6eea6c8147a6aca4dc4
  final_rust_client_run: 30794506470
  final_windows_job: 91624972972
  final_windows_workspace: PASS
  final_supply_chain_job: 91624973079
  final_supply_chain: PASS
  final_repository_ci_run: 30794506696
  final_repository_ci: CANCELLED_DURING_AUTO_MERGE_TRANSITION
fresh_audit:
  result: PASS
  validator: fresh_connector_audit_role
  material_findings_open: 0
  resolved_findings:
    - id: P2-CANARY-INBOUND-BOUND-001
      disposition: use CANARY_NETWORK_MESSAGE_MAX_BYTES
    - id: P2-CANARY-INBOUND-SESSION-001
      disposition: bootstrap order state owns and validates SessionToken
e2e:
  result: NOT_APPLICABLE
  reason: The isolated decoder consumes no real transport and has no reachable application composition; controlled visible-world E2E remains a later P2 integration gate.
pr_hygiene:
  open_related_phase_prs: 0
  unresolved_review_threads: 0
  requested_changes: 0
shared_path_lease: []
unknown:
  - deployed Canary revision and configuration
  - framing, encryption and admission transcript
  - complete layouts and semantic mappings of remaining inbound families
blockers: []
next_action: Inspect the exact source and generated index for candidate server-to-client families, then select one only when the entire layout, gates, ordering and an accepted existing GameEvent mapping are all proven; otherwise record it as evidence-only UNKNOWN without implementation.
```
