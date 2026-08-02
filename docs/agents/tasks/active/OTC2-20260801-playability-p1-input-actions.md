---
task_id: OTC2-20260801-playability-p1-input-actions
status: validating
agent: "P1 input-actions worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-input-actions
phase: integration-and-validation
branch: feat/OTC2-20260801-playability-p1-input-actions
base_branch: main
created: 2026-08-01T22:28:00+02:00
updated: 2026-08-02T21:41:00+02:00
last_verified_commit: "f05adb2ddec80132b630778011f5784678981afc"
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
invocation_started_at: 2026-08-02T21:38:43+02:00
last_progress_at: 2026-08-02T21:41:00+02:00
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Implement the framework-neutral normalized input and semantic action/context producer defined by `P1_INPUT_ACTIONS_AGENT.md`.

# Acceptance

- [x] normalized key/button/pointer/wheel/text/focus/capture/device-loss contracts exist without winit/Win32 types;
- [x] stable physical codes are independent of localized display labels;
- [x] bounded semantic action/context/binding/chord/repeat APIs exist;
- [x] context precedence, conflicts and reserved bindings are explicit and deterministic;
- [x] focus/capture/device loss clears held and active semantic state predictably;
- [x] no widgets, game commands, settings persistence, default product keymap or app composition entered the crate;
- [x] original synthetic ordered event-stream tests are implemented;
- [ ] package formatting, strict Clippy and focused/component tests pass;
- [ ] exact-head heavy gates pass after serialized integration;
- [ ] independent API/ownership audit has no open material finding;
- [ ] PR is merged and the task is separately archived.

## Contract invariants

- Platform adapters supply numeric physical positions, bounded pointer/wheel data and committed text; the crate exposes no framework or OS types.
- Modifier sets and non-modifier chord inputs have canonical deterministic ordering.
- Binding conflicts and caller-reserved chords fail construction instead of silently overriding earlier bindings.
- Modal contexts suppress text/gameplay contexts; text contexts suppress gameplay contexts; global contexts remain eligible.
- Priority, context kind and context identifier produce deterministic precedence.
- Press, repeat, release, focus loss, capture loss, device loss and context deactivation produce explicit semantic lifecycle records.
- Text Debug output is length-only and does not emit committed content.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-02T21:41:00+02:00
head: f05adb2ddec80132b630778011f5784678981afc
branch: feat/OTC2-20260801-playability-p1-input-actions
pr: 157
status: validating
phase: integration-and-validation
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
  reason: game-domain and asset-runtime implementations and lifecycle archives are merged; no competing shared holder exists.
  expected_integration: restack on main 3887a0b7, add one workspace member and minimal local lockfile package; accepted architecture category is `input` and the crate has no dependencies.
proven:
  - Current main is 3887a0b7369e99ad200990d42a5314f1d5531e97.
  - PR 157 owned only its task path before implementation and no other open P1 runtime PR owns input-actions paths.
  - Framework-neutral physical events, bounded text/pointer values, semantic identifiers, contexts, chords, bindings and action lifecycle records are implemented.
  - InputRouter maintains deterministic held state, modal/text/gameplay precedence, repeat, release and focus/capture/device cleanup.
  - The architecture checker already has category `input`; metadata was corrected from the crate-name spelling `input-actions` to the accepted category.
  - No external dependency, platform adapter, settings, UI, game-domain or default keymap was introduced.
derived:
  - No architecture checker or fixture mutation is expected because the crate has no dependency edges and uses an existing category.
  - One isolated remote run can restack, integrate the workspace, regenerate a minimal lockfile, apply pinned rustfmt and isolate focused compiler/test failures.
unknown:
  - Compiler, rustfmt, strict Clippy, tests, architecture and supply-chain outcome on the integrated head.
conflicts: []
first_failure:
  marker: architecture metadata review
  evidence: initial manifest used unknown category `input-actions` while policy publishes category `input`.
  causal_hypothesis: crate name was copied into architecture metadata instead of reusing the accepted category catalogue.
  repair: manifest now declares category `input`; checker mutation is unnecessary.
rejected_hypotheses:
  - Expose winit or Win32 types: rejected by the framework-neutral producer boundary.
  - Map actions directly to GameCommand or UI feature enums: rejected; later consumers own mapping.
  - Publish default product keymaps or settings serialization: rejected as later product scope.
  - Add gamepad behavior now: rejected as speculative beyond the minimum keyboard/pointer/text spine.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md
  - oteryn-client/crates/input-actions/**
validation:
  - command: live main, P1 archive and ownership reconciliation
    result: PASS
    evidence: main 3887a0b7; game-domain and asset-runtime merged/archived; serialized lease free before grant.
  - command: public API and scope review
    result: PASS_WITH_VALIDATION_PENDING
    evidence: no framework/UI/game-domain/settings/default-keymap types; package has no external dependency.
  - command: architecture category review
    result: PASS_AFTER_REPAIR
    evidence: accepted category `input` reused; no new architecture policy required.
blockers: []
next_action: Run the isolated exact-main integration and focused validation harness, repair the first compiler/test failure if present, then trigger retained exact-head heavy CI.
```
