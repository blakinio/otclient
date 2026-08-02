---
task_id: OTC2-20260801-playability-p1-input-actions
status: validating
agent: "P1 input-actions worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-input-actions
phase: exact-head-validation
branch: feat/OTC2-20260801-playability-p1-input-actions
base_branch: main
created: 2026-08-01T22:28:00+02:00
updated: 2026-08-02T23:59:00+02:00
last_verified_commit: "6f38a3c1c48f79ef51050c46397c33d5ee4ae07b"
required_base_commit: "3887a0b7369e99ad200990d42a5314f1d5531e97"
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
policy_version: 2
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
invocation_started_at: 2026-08-02T23:54:00+02:00
last_progress_at: 2026-08-02T23:59:00+02:00
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Implement the framework-neutral normalized input and semantic action/context producer defined by `P1_INPUT_ACTIONS_AGENT.md`.

# Acceptance

- [x] bounded normalized keyboard, mouse, pointer, wheel, text, focus, capture and device-loss contracts exist without framework/OS types;
- [x] chords, semantic IDs, contexts, bindings, conflicts and lifecycle are deterministic;
- [x] conflicts, reserved, unreachable and invalid bindings fail explicitly;
- [x] no widgets, game commands, settings, default keymap or app composition entered the crate;
- [ ] focused rustfmt, strict Clippy and all lifecycle/component tests pass on the repaired head;
- [ ] final exact-head heavy gates pass;
- [x] ownership, API, architecture and minimal lockfile audits have no unresolved material finding;
- [ ] PR is merged and the task is separately archived.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-02T23:59:00+02:00
head: d92f2f17399c3307ab0103dfbf8f9a7ba03be3e8
branch: feat/OTC2-20260801-playability-p1-input-actions
pr: 157
status: validating
phase: exact-head-validation
context_routes:
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/GITHUB_ONLY_EXECUTION.md
  - docs/agents/DELIVERY_COMPLETENESS_AND_CLOSEOUT.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md
  - oteryn-client/docs/agents/prompts/P1_INPUT_ACTIONS_AGENT.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md
  - oteryn-client/crates/input-actions/**
shared_lease:
  state: granted
  integration: exact main 3887a0b7 is in branch history; workspace member and minimal no-dependency lockfile package are present; accepted category `input` covers the crate.
proven:
  - Public API contains no winit, Win32, UI, game-domain, settings or default-keymap types.
  - InputRouter deterministically handles context precedence, repeat, release, focus/capture/device cleanup and ordered output.
  - Focused run 30764305750 job 91540213774 passed pinned rustfmt, strict Clippy and all 11 original tests.
  - Format repair run 30764475580 job 91540644130 applied pinned formatting to the complete crate and re-passed strict focused validation.
  - Cargo.lock adds only local package oteryn-input-actions with no dependencies.
  - Temporary PR 178 is closed without merge with zero final changed files.
  - Fresh-session static control-flow audit proved composite wheel chords were accepted although InputRouter can emit wheel bindings only as single-atom impulses.
  - The repaired code introduces stable InvalidWheelChord rejection plus two public-API negative tests for key-plus-wheel and multi-wheel combinations.
derived:
  - The previous exact-head runs 30768948709 and 30768948791 are superseded by the material audit repair and cannot be merge evidence.
  - A task-record commit is required to trigger retained workflows on the repaired exact head.
unknown:
  - Pinned format, strict Clippy, 13 total tests, workspace heavy gates and repository required CI outcome on the repaired checkpoint head.
conflicts: []
audit_findings:
  - id: INPUT-WHEEL-CHORD-001
    severity: medium
    status: repaired_pending_validation
    evidence: InputChord accepted a wheel atom with other atoms, while InputRouter::process_impulse always constructs a one-wheel-atom chord.
    repair: reject every wheel chord whose non-modifier input count is not exactly one and cover both unreachable forms through integration tests.
first_failure:
  marker: retained Rust Client rustfmt
  evidence: run 30764404973 job 91540470054 showed formatting differences only in input-actions/error.rs and semantic.rs.
  causal_hypothesis: the initial harness formatted all files but committed only a subset.
  repair: pinned Cargo/rustfmt committed the complete crate in 6f38a3c1; focused rustfmt, strict Clippy and tests passed before the later audit repair.
rejected_hypotheses:
  - Relax rustfmt or bypass the retained gate: rejected.
  - Change router/API semantics beyond unreachable wheel validation: rejected as outside the material finding.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/crates/input-actions/**
validation:
  - command: focused/component run 30764305750 / job 91540213774
    result: PASS_BEFORE_AUDIT_REPAIR
  - command: format repair run 30764475580 / job 91540644130
    result: PASS_BEFORE_AUDIT_REPAIR
  - command: exact changed-path, API, architecture and lockfile audit
    result: PASS
  - command: second retained heavy run 30764535021 / Windows job 91540801099
    result: FAIL_UNRELATED_TEST
    evidence: locked metadata, rustfmt, strict workspace Clippy and supply-chain passed; existing app-runtime shutdown test failed before architecture.
  - command: targeted diagnostic run 30764694730 / job 91541216153
    result: PASS
    evidence: the exact unrelated app-runtime shutdown test passed five consecutive times on the same input-actions implementation and pinned toolchain.
  - command: independent fresh-session public-contract and router reachability audit
    result: FINDING_REPAIRED_PENDING_VALIDATION
    evidence: INPUT-WHEEL-CHORD-001 repaired in error.rs, semantic.rs and tests/chord_validation.rs.
blockers: []
next_action: Inspect retained Rust Client and repository CI on the repaired task-record head; if green, update PR exact-head evidence, mark ready, squash-merge and archive separately.
```
