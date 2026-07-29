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
updated: 2026-07-29T16:04:00+02:00
last_verified_commit: "e9dcf70e8d60bcb5ba3e82280482108d43306f5f"
required_base_commit: "e9dcf70e8d60bcb5ba3e82280482108d43306f5f"
risk: medium
related_pr: pending
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

- [ ] Fresh base/open-PR/active-task/lease and dependency preflight passes.
- [ ] Exactly one renderer crate is added with category `renderer`.
- [ ] Exact `wgpu 30.0.0` and `pollster 1.0.1` are the only new direct external dependencies.
- [ ] wgpu default features are disabled and only Windows `std` plus `dx12` are enabled.
- [ ] `pollster::block_on` is used only for one synchronous main-thread bootstrap.
- [ ] CPU-side lifecycle covers unconfigured/configured/suspended/lost/closing, zero-size, stale generation, bounded reconfiguration and idempotent close.
- [ ] Windows adapter owns instance/surface/adapter/device/queue and clears/presents one constant original color only.
- [ ] Redraw is event-driven; no continuous loop, background service or worker thread is added.
- [ ] Fatal renderer failures route through the existing shell close path and renderer resources release before the window.
- [ ] No game rendering, assets, shaders/pipelines, UI, protocol, identity, network, audio, persistence or extensions.
- [ ] No direct Win32/windows-sys/raw-window-handle dependency, unsafe, global singleton, reusable async runtime or scheduler.
- [ ] Runtime evidence distinguishes automated PASS from interactive BLOCKED cases.
- [ ] Workspace, generated lockfile, dependency policy and owner documentation are current.
- [ ] Exact-head Windows, supply-chain, architecture and repository CI pass; PR merges and task archives independently.

# Live preflight

- Required `main`: `e9dcf70e8d60bcb5ba3e82280482108d43306f5f`.
- W5 plan/archive: PR #84 / PR #85, both merged.
- Open PR #23 is legacy OTUI/Lua only; PR #48 is isolated operational non-merge work.
- No active task or open PR owns renderer paths, Cargo/lockfile integration or this public contract.
- Architecture category `renderer` already exists and forbids renderer dependencies only on protocol adapters/features.
- Candidate primary evidence: `wgpu 30.0.0` Rust 1.87 MIT/Apache-2.0; `pollster 1.0.1` Rust 1.69 MIT/Apache-2.0 with no dependencies; workspace Rust 1.94.
- Exact cargo-deny remains authoritative for advisories, licenses, bans and sources.

# Boundaries

No interactive launch/presentation, real resize/minimize, suspend/resume, surface/device loss, GPU/driver/hardware or performance compatibility is claimed without genuinely observed named-environment evidence.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Shared-path lease: held by W5-RENDER until archive merge
- Archived at: pending
