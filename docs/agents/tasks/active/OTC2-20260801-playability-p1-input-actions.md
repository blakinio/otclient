---
task_id: OTC2-20260801-playability-p1-input-actions
status: validating
agent: "P1 input-actions worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-input-actions
phase: final-exact-head-ci
branch: feat/OTC2-20260801-playability-p1-input-actions
base_branch: main
created: 2026-08-01T22:28:00+02:00
updated: 2026-08-03T00:51:00+02:00
last_verified_commit: "3f7feaef3f2a496393c7b541bd5590ed18e259e3"
required_base_commit: "4ac18a876385a8e5dc97efe474c98fd3df583b0a"
restack_commit: "eab52b7c5b69fb546afd9788d7d1a4d5abcaecd1"
risk: high
related_pr: 157
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md
  - oteryn-client/crates/input-actions/**
shared_path_lease:
  holder: OTC2-20260801-playability-p1-input-actions
  granted_at: 2026-08-02T21:41:00+02:00
  paths:
    - oteryn-client/Cargo.toml
    - oteryn-client/Cargo.lock
    - oteryn-client/tools/architecture-check/**
    - oteryn-client/tests/architecture-fixtures/**
    - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
    - oteryn-client/docs/operations/RUST_WORKSPACE.md
  release_condition: exact-head integration validation and merge or explicit rollback
implementation_authorized: true
policy_version: 2.1
task_kind: implementation
execution_mode: github-only
context_pressure: high
decomposition_decision: phased
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - platform adapters for winit and Windows events
  - settings persistence and user-configured keymaps
  - gameplay and UI action consumers
  - app composition and real staging E2E
invocation_started_at: 2026-08-03T00:45:00+02:00
last_progress_at: 2026-08-03T00:51:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: current-base-restack
terminal_ci_wait_started_at: 2026-08-03T00:51:00+02:00
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Implement and integrate the framework-neutral normalized input and semantic action/context producer defined by `P1_INPUT_ACTIONS_AGENT.md`.

# Acceptance

- [x] bounded normalized keyboard, mouse, pointer, wheel, text, focus, capture and device-loss contracts exist without framework/OS types;
- [x] chords, semantic IDs, contexts, bindings, conflicts and lifecycle are deterministic;
- [x] conflicts, reserved, unreachable and invalid bindings fail explicitly;
- [x] no widgets, game commands, settings, default keymap or app composition entered the crate;
- [x] focused rustfmt, strict Clippy and lifecycle/component tests passed;
- [x] full Rust Client, Supply Chain and repository CI passed on the proven implementation head;
- [x] ownership, API, architecture and minimal lockfile audits have no unresolved material finding;
- [x] branch was restacked onto exact current `main` without overlapping implementation paths;
- [ ] final current-base exact-head CI passes;
- [ ] PR is protected-merged and the task is separately archived.

## Proven implementation evidence

```yaml
implementation_head: 3f7feaef3f2a496393c7b541bd5590ed18e259e3
rust_client:
  run: 30769222634
  windows_job: 91553325023
  supply_chain_job: 91553325074
  result: PASS
repository_ci:
  run: 30769222733
  required_job: 91553474591
  result: PASS
ready_state_ci:
  run: 30769519720
  required_job: 91554176973
  result: PASS
audit:
  result: PASS
  open_material_findings: 0
  repaired_finding: INPUT-WHEEL-CHORD-001
review_threads: 0
```

## Current-base restack

`main` advanced through unrelated governance and Canary evidence changes. The original implementation branch was four commits behind, so branch protection correctly refused a manual merge even after the old merge generation passed.

A temporary self-removing workflow performed one guarded restack:

- expected parent `9ac81ab3f3898179a8080cd29696cd6624ecdf86` was verified;
- all current-main changed paths were checked against the task, workspace and input-actions ownership paths;
- zero overlap was found;
- current `main@4ac18a876385a8e5dc97efe474c98fd3df583b0a` was merged;
- the temporary workflow removed itself before the final restack commit;
- final PR diff remained exactly eleven authorized paths.

## Durable checkpoint

```yaml
checkpoint_version: 3
updated_at: 2026-08-03T00:51:00+02:00
pr: 157
branch: feat/OTC2-20260801-playability-p1-input-actions
current_main: 4ac18a876385a8e5dc97efe474c98fd3df583b0a
restack_commit: eab52b7c5b69fb546afd9788d7d1a4d5abcaecd1
status: validating
phase: final-exact-head-ci
product_code_changed_by_restack: false
final_diff:
  changed_paths: 11
  unexpected_paths: 0
  temporary_workflow_retained: false
validation:
  proven_implementation: PASS
  current_base_exact_head: RUNNING_AFTER_THIS_CHECKPOINT
review_threads: 0
blockers: []
next_action: Under the bounded terminal-CI policy, observe the final current-base Rust Client and repository CI; on PASS allow protected merge, verify the merge commit, then create and merge the lifecycle-only archive PR.
```
