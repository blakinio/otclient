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
updated: 2026-08-03T00:02:00+02:00
last_verified_commit: "8fd75c11e0bdc1494e2c9d8697849ccacd6a5fa7"
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
last_progress_at: 2026-08-03T00:02:00+02:00
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

- [x] bounded normalized keyboard, mouse, pointer, wheel, text, focus, capture and device-loss contracts exist without framework/OS types;
- [x] chords, semantic IDs, contexts, bindings, conflicts and lifecycle are deterministic;
- [x] conflicts, reserved, unreachable and invalid bindings fail explicitly;
- [x] no widgets, game commands, settings, default keymap or app composition entered the crate;
- [ ] focused rustfmt, strict Clippy and all lifecycle/component tests pass on the final exact head;
- [ ] final exact-head heavy gates pass;
- [x] ownership, API, architecture and minimal lockfile audits have no unresolved material finding;
- [ ] PR is merged and the task is separately archived.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-03T00:02:00+02:00
head: 8fd75c11e0bdc1494e2c9d8697849ccacd6a5fa7
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
  - Format repair run 30764475580 job 91540644130 applied pinned formatting to the complete original crate and re-passed strict focused validation.
  - Cargo.lock adds only local package oteryn-input-actions with no dependencies.
  - Temporary PR 178 is closed without merge with zero final changed files.
  - Fresh-session static control-flow audit proved composite wheel chords were accepted although InputRouter can emit wheel bindings only as single-atom impulses.
  - The repaired code introduces stable InvalidWheelChord rejection plus two public-API negative tests for key-plus-wheel and multi-wheel combinations.
  - Superseded Rust Client run 30769122762 passed locked metadata and Supply Chain job 91553062585; Windows job 91553062600 failed only because pinned rustfmt required one import line in the new test.
  - Commit 8fd75c11 applies exactly the pinned rustfmt output from job 91553062600 without semantic change.
derived:
  - Runs on heads before 8fd75c11 are supporting evidence only and cannot satisfy final exact-head validation.
  - This task-record commit is the final intended head trigger; no implementation change is pending unless final CI exposes a new actionable failure.
unknown:
  - Pinned format, strict Clippy, 13 total tests, workspace heavy gates, architecture and repository required CI outcome on the final checkpoint head.
conflicts: []
audit_findings:
  - id: INPUT-WHEEL-CHORD-001
    severity: medium
    status: repaired_pending_validation
    evidence: InputChord accepted a wheel atom with other atoms, while InputRouter::process_impulse always constructs a one-wheel-atom chord.
    repair: reject every wheel chord whose non-modifier input count is not exactly one and cover both unreachable forms through integration tests.
first_failure:
  marker: final repaired-head rustfmt
  evidence: run 30769122762 / Windows job 91553062600 requested a one-line import in tests/chord_validation.rs; metadata and Supply Chain passed.
  causal_hypothesis: the GitHub contents write used valid Rust formatting that differed from pinned rustfmt 1.94 output.
  repair: commit 8fd75c11 applies the exact one-line import emitted by the pinned formatter.
rejected_hypotheses:
  - Relax rustfmt or bypass the retained gate: rejected.
  - Rerun unchanged head 1c803c65: rejected because the log contained a deterministic formatting repair.
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
  - command: repaired-head Rust Client run 30769122762
    result: FAIL_FORMAT_ONLY
    evidence: metadata and Supply Chain passed; Windows job 91553062600 stopped at one deterministic import formatting diff.
  - command: exact pinned formatting repair
    result: APPLIED
    evidence: commit 8fd75c11 matches the formatter output from job 91553062600.
blockers: []
next_action: Inspect retained Rust Client and repository CI on this final checkpoint head; if green, update PR exact-head evidence, mark ready, squash-merge and archive separately.
```
