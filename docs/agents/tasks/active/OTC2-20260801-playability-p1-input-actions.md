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
updated: 2026-08-02T21:53:00+02:00
last_verified_commit: "ce5f9f550df4f1d03c978bbeadced91a35b352f7"
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
last_progress_at: 2026-08-02T21:53:00+02:00
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Implement the framework-neutral normalized input and semantic action/context producer defined by `P1_INPUT_ACTIONS_AGENT.md`.

# Acceptance

- [x] normalized keyboard, mouse, pointer, wheel, text, focus, capture and device-loss contracts exist without winit/Win32 types;
- [x] physical codes, modifiers, chords, identifiers, contexts, bindings, repeat and semantic lifecycle records are bounded and deterministic;
- [x] binding conflicts, reserved combinations and unknown contexts fail explicitly;
- [x] modal/text/gameplay/global precedence is deterministic;
- [x] focus/capture/device loss and context changes clean held/active state predictably;
- [x] no widgets, game commands, settings persistence, default product keymap or app composition entered the crate;
- [x] pinned package rustfmt, strict Clippy and all focused/component tests pass;
- [ ] exact-head heavy gates pass after serialized integration;
- [x] exact changed-path, lockfile, API and trust-boundary review has no open material finding;
- [ ] PR is merged and the task is separately archived.

## Contract invariants

- Adapters provide stable numeric physical positions and bounded values; public contracts expose no framework or OS type.
- Chords normalize modifier bits and sort unique non-modifier inputs.
- Modal contexts suppress text/gameplay, text suppresses gameplay, and global remains eligible.
- Priority, context kind and context identifier break ties deterministically.
- Press, repeat, release, context invalidation, focus loss, capture loss and device loss emit explicit phases.
- Committed text is bounded and Debug-redacted.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-02T21:53:00+02:00
head: ce5f9f550df4f1d03c978bbeadced91a35b352f7
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
  integration: exact main 3887a0b7 is merged into the branch; workspace member and minimal no-dependency lockfile package are present; existing category `input` covers the crate.
proven:
  - Public API contains no winit, Win32, UI, game-domain, settings or default-keymap type.
  - InputRouter deterministically resolves contexts, repeat and held-state lifecycle.
  - Original synthetic ordered stream, context precedence, conflict, bounds, repeat, focus, capture, device-loss and redaction tests pass.
  - Cargo.lock diff contains only local package oteryn-input-actions with no dependencies.
  - Pinned focused run 30764305750 job 91540213774 passed rustfmt, strict package Clippy and all 11 tests.
  - Temporary PR 178 is closed without merge with zero final changed files.
derived:
  - No architecture checker or fixture mutation is required because the accepted `input` category has no dependency edges for this package.
  - This checkpoint commit triggers retained PR workflows after GITHUB_TOKEN integration pushes.
unknown:
  - Locked workspace metadata, full workspace Clippy/tests, architecture, supply-chain and repository required CI outcome on this checkpoint head.
conflicts: []
first_failure:
  marker: focused package validation
  evidence: strict lint identified two test-only allocations, then one fixture pressed Shift+S while binding S.
  causal_hypothesis: test construction, not router/API behavior, was inconsistent.
  repair: use `slice::from_ref`, an array stream and a Shift+S binding; focused validation now passes.
rejected_hypotheses:
  - Add platform adapters, settings, UI/game command mapping or a default keymap: rejected as later consumer/product scope.
  - Add a new architecture category: rejected; existing category `input` is authoritative.
  - Relax strict lints or change router semantics to accommodate a mismatched fixture: rejected.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/crates/input-actions/**
validation:
  - command: ownership, API, architecture and minimal lockfile audit
    result: PASS
    evidence: ten authorized paths, accepted `input` category, no dependencies, no framework/product leakage.
  - command: focused/component run 30764305750 / job 91540213774
    result: PASS
    evidence: pinned rustfmt, strict Clippy and 11 lifecycle/stream tests passed.
  - command: temporary harness cleanup
    result: PASS
    evidence: PR 178 closed without merge with zero final changed files.
blockers: []
next_action: Inspect retained Rust Client and repository CI on this checkpoint head, isolate one actionable failure if present, otherwise mark ready, auto-merge and archive separately.
```
