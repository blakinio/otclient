---
task_id: OTC2-20260803-playability-p2-simulation-snapshot
status: active
agent: "P2 simulation/snapshot worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-simulation-snapshot
phase: exclusive-implementation
branch: feat/OTC2-20260803-playability-p2-simulation-snapshot
base_branch: main
created: 2026-08-03T01:36:30+02:00
updated: 2026-08-03T01:36:30+02:00
required_base_commit: "07cbc0445241e50f439996b59024ca869c1b16cd"
risk: high
related_pr: null
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-simulation-snapshot.md
  - oteryn-client/crates/simulation-core/**
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
  - Canary gameplay decoder/encoder
  - asset decode and renderer resources
  - platform input adapter and product binding map
  - visible-world app composition and controlled M2 E2E
invocation_started_at: 2026-08-03T01:36:30+02:00
last_progress_at: 2026-08-03T01:36:30+02:00
ci_checks_for_current_head: 0
ci_check_generation: exclusive-focused
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Implement the sole protocol-neutral deterministic single-writer gameplay simulation and immutable renderer-facing snapshot producer accepted by the archived P1 aggregation barrier and `WAVE_P2_MINIMUM_VISIBLE_WORLD.md`.

# Proven launch state

- P1 aggregation implementation #184 merged as `95d18ca4e97920d1418a41762b86d92b7cf9516d`;
- P1 aggregation archive #185 merged as `07cbc0445241e50f439996b59024ca869c1b16cd`;
- all P1 shared integration leases are released;
- no open branch, PR or active task owns `oteryn-client/crates/simulation-core/**`;
- architecture category `game-simulation` already permits only the required lower-layer dependency direction;
- merged `game-domain` supplies ordered session-fenced handles, positions and the closed v1 `GameEventEnvelope` vocabulary.

# Acceptance

- [ ] one session-scoped owner atomically applies ordered `GameEventEnvelope` values;
- [ ] stale/wrong-session events and invalid lifecycle transitions fail with stable errors and no partial mutation;
- [ ] bootstrap establishes the local player and explicit bounded world state;
- [ ] floors, tiles, stacks, entities, items, containers and capacities are checked and deterministic;
- [ ] movement/removal/tile clear/resources/container/session-end families update state correctly;
- [ ] immutable generation-stable `RenderSnapshot` exposes only renderer-required semantic state;
- [ ] equal event streams produce equal snapshots;
- [ ] public API exposes no mutable storage, Canary, socket, winit/Win32/wgpu, asset, UI or app types;
- [ ] focused manifest-path format, strict Clippy and complete package tests pass before any shared lease;
- [ ] fresh API/determinism/allocation/lifecycle audit has no open material finding;
- [ ] coordinator grants only the minimal Cargo.toml/Cargo.lock lease after exclusive validation;
- [ ] restacked exact-head workspace, architecture, Supply Chain and repository CI pass;
- [ ] implementation protected-merges, task archives separately and lease releases.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-03T01:36:30+02:00
head: pending_task_commit
branch: feat/OTC2-20260803-playability-p2-simulation-snapshot
pr: null
status: active
phase: exclusive-implementation
proven:
  - Archived P1 barrier authorizes this sole producer.
  - game-simulation -> foundation/game-domain is already architecture-approved.
  - No new registry dependency or category policy change is required.
derived_design:
  - BTree-backed bounded state provides canonical ordering.
  - Event application uses a cloned bounded candidate and commits only after full validation.
  - Snapshot contains session, revision, phase, local player, resources, end reason and ordered visible tiles.
  - Containers remain simulation state but are not renderer snapshot data.
unknown: []
conflicts: []
changed_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-simulation-snapshot.md
validation:
  - command: live barrier/archive/ownership/architecture preflight
    result: PASS
blockers: []
next_action: Open the draft PR, implement the exclusive simulation-core manifest/public contract/tests, then run a self-removing focused validation workflow before requesting any shared integration lease.
```
