---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: active
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: baseline-alignment
branch: feat/OTC2-20260803-playability-p2-canary-world-protocol
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T02:04:00+02:00
required_base_commit: "f1a5a1873dbb9ce164aefed7537d5c3004eeb696"
risk: high
related_pr: null
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
user_communication: low_noise
context_pressure: high
decomposition_decision: phased
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - exact provenance-safe M2 gameplay field layouts and bounded fixtures
  - asset decode and renderer resources
  - platform input adapter and product binding map
  - visible-world app composition and controlled M2 E2E
invocation_started_at: 2026-08-03T02:04:00+02:00
last_progress_at: 2026-08-03T02:04:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: baseline-exclusive
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Reconcile the Canary Current development runtime descriptor with the merged generated P1 source index, preserving fail-closed real admission, then implement only those bounded M2 bootstrap/map/entity/movement/logout mappings whose exact field layouts can be established from provenance-safe evidence.

# Proven launch state

- P1 aggregation implementation #184 and archive #185 are merged;
- P2 simulation/snapshot implementation #186 and archive #187 are merged;
- current exact base is `main@f1a5a1873dbb9ce164aefed7537d5c3004eeb696`;
- all prior shared integration leases are released;
- no open PR owns `protocol-canary`, its P2 evidence path or integration-test path;
- architecture category `protocol-canary` already permits the later `game-domain` dependency;
- generated P1 index is pinned to `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`, release 3.6.1, client 1525, profile `current`;
- current runtime descriptor still names source revisions `95b276db311cf6e9acd58b847f1fb0ca6697b137` and `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`;
- real wire admission is intentionally fail-closed and must remain so.

# Acceptance

## Phase 1 — baseline alignment

- [ ] development runtime metadata mechanically agrees with the generated `current-index.json` revision, release, client version, profile and enabled-feature/source-hash evidence;
- [ ] historical cuts remain explicit historical evidence and are not silently called current;
- [ ] descriptor/debug output remains non-secret and bounded;
- [ ] tests consume the generated index as read-only evidence and fail on drift;
- [ ] real admission remains `RealAdmissionUnavailable` and no credential/network lifecycle is weakened;
- [ ] evidence document distinguishes inspected development baseline from deployed runtime equality;
- [ ] focused format, strict Clippy and complete package tests pass;
- [ ] fresh source-provenance/trust/API audit has zero open material finding.

## Phase 2 — bounded gameplay wire mapping

- [ ] exact provenance-safe source/fixture evidence is classified per required M2 family;
- [ ] unsupported field layouts remain explicit `UNKNOWN` and are not guessed;
- [ ] only exactly supported bootstrap/map/entity/movement/logout decode/encode families enter the package;
- [ ] malformed/truncated/trailing/oversized/invalid-order/stale-session input fails closed;
- [ ] merged `GameEvent`/`GameCommand` remain the only semantic envelopes;
- [ ] parser owns no simulation, renderer, asset, input, UI or app state;
- [ ] component/fuzz-style negative evidence passes for every implemented layout;
- [ ] any `game-domain` dependency and lockfile delta occur only after exclusive validation under a serialized shared lease;
- [ ] exact-head Windows workspace, architecture, Supply Chain and repository CI pass;
- [ ] implementation protected-merges, task archives separately and lease releases.

## Claim boundary

Source declarations, opcodes and dispatch phases prove source shape only. They do not prove deployed revision, configuration, ordering, field layout or compatibility. Missing exact layout evidence blocks that subfamily; it never authorizes inference from neighboring handlers.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-03T02:04:00+02:00
head: pending_task_commit
branch: feat/OTC2-20260803-playability-p2-canary-world-protocol
pr: null
status: active
phase: baseline-alignment
proven:
  - The archived P1 barrier authorizes this sole protocol producer.
  - Current runtime descriptor and generated P1 index name different inspected revisions.
  - Existing admission lifecycle is fail-closed for real wire use.
  - Architecture already permits protocol-canary -> game-domain when a later lease is granted.
derived:
  - Baseline alignment can be completed without adding a dependency or changing admission lifecycle.
  - Gameplay mapping may proceed only per-family after exact field-layout evidence is proven.
unknown:
  - exact deployed Canary revision/configuration/build;
  - provenance-safe complete M2 gameplay field layouts and fixtures;
  - controlled post-admission ordering evidence.
conflicts:
  - id: P1-AGG-CANARY-REVISION-001
    generated_index: bc0068ab80bbf003e128fce0589b4cc89d2682d3
    runtime_descriptor: 95b276db311cf6e9acd58b847f1fb0ca6697b137
    historical_accepted_cut: 4b2d6f432d92628c42bde1d95daed6ae0d0eb88f
    disposition: mandatory_mechanical_development_baseline_alignment
changed_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
validation:
  - command: live barrier/archive/ownership/architecture preflight
    result: PASS
blockers: []
next_action: Open the draft PR, inspect exact generated-index metadata and source hashes, then implement and validate development baseline alignment exclusively within protocol-canary and the P2 evidence document before considering any gameplay layout.
```
