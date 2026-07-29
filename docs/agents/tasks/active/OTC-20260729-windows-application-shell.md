---
task_id: OTC-20260729-windows-application-shell
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R02
parallel_wave: OTERYN-W4-WINDOWS-SHELL
parallel_lane: W4-SHELL
parallel_lane_state: active
coordinator_task: OTC-20260729-plan-w4-windows-shell
branch: feat/OTC-20260729-windows-application-shell
base_branch: main
created: 2026-07-29T11:55:00+02:00
updated: 2026-07-29T11:55:00+02:00
last_verified_commit: "b16e0a8c17cf1ce7b0808ef577cce0d5bc76f0b3"
required_base_commit: "b16e0a8c17cf1ce7b0808ef577cce0d5bc76f0b3"
risk: medium
related_pr: pending
depends_on:
  - W4 plan PR #77 and archive PR #78
  - oteryn-foundation PR #54
  - oteryn-diagnostics PR #61
  - oteryn-test-support PR #73
  - Windows platform evidence PR #67
owned_paths:
  - oteryn-client/apps/client/**
  - oteryn-client/docs/research/windows-platform/W4_RUNTIME_EVIDENCE.md
  - docs/agents/tasks/active/OTC-20260729-windows-application-shell.md
  - .github/workflows/w4-lockfile-bootstrap.yml (temporary non-final bootstrap only if required)
shared_path_lease:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/deny.toml
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
  - oteryn-client/docs/operations/RUST_WORKSPACE.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
contract_role: producer
contracts_produced:
  - deterministic Windows application-shell state and main-thread lifecycle adapter
contracts_consumed:
  - oteryn-foundation generations/time contract
  - oteryn-diagnostics structured event contract
  - oteryn-test-support deterministic fixture contract
  - winit 0.30.13 application/window/event contracts
crates_touched:
  - oteryn-client
features_touched:
  - blank Windows window
  - deterministic shell lifecycle
  - bounded lifecycle diagnostics
contracts_touched:
  - new application-shell public API
modules_touched: []
reuses:
  - ProcessGeneration and Moment
  - DiagnosticEvent and classified values
  - DiagnosticEventFixture for deterministic tests
public_interfaces:
  - ShellState
  - ShellPhase
  - ShellCommand
  - ShellError
  - WindowSnapshot
cross_repo_tasks: []
performance_evidence:
  - no performance claim; interactive cycle evidence unavailable unless genuinely observed
security_evidence:
  - no secrets, arbitrary diagnostic text, direct Win32, unsafe code, protocol or asset input
---

# Goal

Add exactly one `oteryn-client` application package that compiles a bounded winit-based blank-window shell on Windows and exposes a deterministic testable lifecycle state machine without renderer, protocol or product-feature scope.

# Acceptance criteria

- [ ] Exactly one application package under `oteryn-client/apps/client/`, category `app`.
- [ ] Exact `winit = "=0.30.13"` is the sole new direct external dependency.
- [ ] Foundation, diagnostics and test-support contracts are reused concretely.
- [ ] Shell startup/running/closing/exited transitions and stale-generation rejection are deterministic.
- [ ] Commands and diagnostic history are bounded; duplicate close is idempotent.
- [ ] One main-thread `ApplicationHandler` creates a resizable blank window and handles required lifecycle/input event classes without renderer work.
- [ ] One named one-shot thread sends a bounded proxy event and is joined after event-loop return.
- [ ] No renderer/GPU, direct Win32/windows-sys/raw-window-handle, unsafe, async runtime, protocol, identity, network, assets, audio, feature UI or persistence.
- [ ] Runtime evidence distinguishes automated PASS from interactive BLOCKED cases.
- [ ] Workspace, lockfile, dependency policy and owning documentation are current.
- [ ] Exact-head Windows, supply-chain and repository CI pass.
- [ ] PR merges and task archives independently; lease is released.

# Dependency evidence

- `winit 0.30.13` remains current primary evidence on 2026-07-29.
- License: Apache-2.0.
- Declared MSRV: Rust 1.70; workspace pins Rust 1.94.
- Direct dependency will be exact-pinned and reviewed through cargo metadata/cargo-deny.
- No direct native/unsafe dependency is added by this package; transitive boundaries remain owned by winit and are recorded, not re-exported.

# Plan

1. Open early draft PR and confirm unique lease.
2. Implement deterministic library state and tests.
3. Implement minimal main-thread winit adapter.
4. Generate the lockfile through the pinned resolver. If local Cargo remains unavailable, use one temporary PR-only workflow to emit the generated lockfile artifact, record the blocker, import the artifact, and remove the workflow before final review.
5. Update dependency/runtime evidence and owning documentation.
6. Review full diff, validate exact head, merge and archive.

# Validation

| Revision | Check | Result |
|---|---|---|
| `b16e0a8c17cf1ce7b0808ef577cce0d5bc76f0b3` | live ownership/base/producer/dependency preflight | PASS |

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Shared-path lease: held by W4-SHELL
- Archived at: pending
