---
task_id: OTC-20260729-renderer-surface-ownership
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R08
parallel_wave: OTERYN-W5-RENDER-SURFACE
parallel_lane: W5-RENDER
parallel_lane_state: active
coordinator_task: OTC-20260729-plan-w5-render-surface
branch: feat/OTC-20260729-renderer-surface-ownership
base_branch: main
created: 2026-07-29T16:04:00+02:00
updated: 2026-07-29T17:18:00+02:00
last_verified_commit: "e9dcf70e8d60bcb5ba3e82280482108d43306f5f"
required_base_commit: "e9dcf70e8d60bcb5ba3e82280482108d43306f5f"
risk: medium
related_pr: "#86"
depends_on:
  - W5 plan PR #84 and archive PR #85
  - W4 application shell PR #79 and archive PR #80
  - foundation PR #54
  - diagnostics PR #61
  - test support PR #73
owned_paths:
  - oteryn-client/crates/renderer/**
  - oteryn-client/docs/research/renderer/W5_RUNTIME_EVIDENCE.md
  - docs/agents/tasks/active/OTC-20260729-renderer-surface-ownership.md
shared_path_lease:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/deny.toml
  - oteryn-client/apps/client/Cargo.toml
  - oteryn-client/apps/client/src/main.rs
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
  - oteryn-client/docs/operations/RUST_WORKSPACE.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
contract_role: producer
contracts_produced:
  - deterministic renderer surface lifecycle and Windows clear/present adapter
contracts_consumed:
  - oteryn-foundation process generation contract
  - merged application-shell main-thread lifecycle contract
  - wgpu 30.0.0 surface/device/presentation contracts
crates_touched:
  - oteryn-renderer
  - oteryn-client
features_touched:
  - renderer surface ownership
  - constant clear/present lifecycle
contracts_touched:
  - new renderer public API
modules_touched: []
reuses:
  - ProcessGeneration
  - existing ShellState close path and WindowSnapshot sizing
  - oteryn-test-support deterministic fixtures where applicable
public_interfaces:
  - SurfaceState
  - SurfaceEvent
  - SurfaceDecision
  - RendererError
  - WindowsRenderer
cross_repo_tasks: []
performance_evidence:
  - no frame-time or throughput claim; interactive GPU performance remains blocked
security_evidence:
  - no secrets, assets, shaders, protocol data, arbitrary backend text or unsafe code
---

# Goal

Add exactly one `oteryn-renderer` package and narrowly compose it into the merged Windows application shell to own wgpu instance/surface/adapter/device/queue plus one constant clear/present path, with deterministic CPU-side lifecycle tests and explicit interactive evidence blockers.

# Acceptance criteria

- [x] Fresh base/open-PR/active-task/lease and dependency preflight passes.
- [x] Exactly one renderer crate is added with category `renderer`.
- [x] Exact `wgpu 30.0.0` and `pollster 1.0.1` are the only new direct external dependencies.
- [x] wgpu default features are disabled and only Windows `std` plus `dx12` are enabled.
- [x] `pollster::block_on` is used only for one synchronous main-thread bootstrap.
- [x] CPU-side lifecycle covers unconfigured/configured/suspended/lost/closing, zero-size, stale generation, bounded reconfiguration and idempotent close.
- [x] Windows adapter owns instance/surface/adapter/device/queue and clears/presents one constant original color only.
- [x] Redraw is event-driven; no continuous loop, background service or worker thread is added.
- [x] Fatal renderer failures route through the existing shell close path and renderer resources release before the window.
- [x] No game rendering, assets, shaders/pipelines, UI, protocol, identity, network, audio, persistence or extensions.
- [x] No direct Win32/windows-sys/raw-window-handle dependency, unsafe, global singleton, reusable async runtime or scheduler.
- [ ] Runtime evidence distinguishes automated PASS from interactive BLOCKED cases.
- [ ] Workspace, generated lockfile, dependency policy and owner documentation are current.
- [ ] Exact-head Windows, supply-chain, architecture and repository CI pass; PR merges and task archives independently.

# Live preflight

- Required `main`: `e9dcf70e8d60bcb5ba3e82280482108d43306f5f`.
- W5 plan/archive: PR #84 / PR #85, both merged.
- Open PR #23 is legacy OTUI/Lua only; PR #48 is isolated operational non-merge work.
- No active task or open PR owns renderer paths, Cargo/lockfile integration or this public contract.
- Architecture category `renderer` already exists and forbids renderer dependencies only on protocol adapters/features.
- Current primary evidence confirms `wgpu 30.0.0` exposes the planned safe surface creation and closed acquisition outcomes; `pollster 1.0.1` provides synchronous `block_on` with no default features.
- Exact cargo-deny remains authoritative for advisories, licenses, bans and sources.

# Implementation

- `SurfaceState` applies typed-generation events transactionally and fails closed on stale generations, invalid transitions, counter overflow or excessive recovery attempts.
- Zero-size resize suspends configuration; non-zero resize/restore requests deterministic configuration.
- Timeout and occlusion skip one presentation without mutating lifecycle state.
- Outdated/suboptimal/lost outcomes use the fixed bounded reconfigure/recreate policy.
- The Windows adapter owns one DX12 instance/surface/adapter/device/queue, performs one synchronous startup bootstrap and renders only one original constant clear color.
- `apps/client` retains the `winit` main-thread event loop, requests redraw only for concrete events and releases renderer resources before the window and shell exit.

# Work log

## 2026-07-29 preflight and implementation

- Verified live `main`, W5 plan/archive, open PRs and unique shared-path lease before implementation.
- Reviewed root/nested agent policy, the accepted W5 wave, architecture checker, application-shell source and foundation generation contract.
- Revalidated the exact `wgpu 30.0.0` surface acquisition/recovery API and `pollster 1.0.1` synchronous bootstrap contract from current primary documentation.
- The execution environment has no local Rust/Cargo toolchain and cannot resolve GitHub for a clone, while repository access remains available through the GitHub connector.
- To avoid manually fabricating `Cargo.lock`, one transient CI bootstrap commit will run `cargo generate-lockfile` and upload only the generated lockfile. The workflow change must be reverted immediately after retrieval and cannot appear in the final diff or final validation head.
- No local compile/test result is claimed; exact hosted Windows, architecture and cargo-deny evidence remains mandatory on the final unmodified workflow.

# Boundaries

No interactive launch/presentation, real resize/minimize, suspend/resume, surface/device loss, GPU/driver/hardware or performance compatibility is claimed without genuinely observed named-environment evidence.

# Completion

- Final status: in progress
- PR: #86
- Merge commit: pending
- Shared-path lease: held by W5-RENDER until archive merge
- Archived at: pending
