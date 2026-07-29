---
task_id: OTC-20260729-renderer-surface-ownership
status: completed
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R08
parallel_wave: OTERYN-W5-RENDER-SURFACE
parallel_lane: W5-RENDER
parallel_lane_state: archived
coordinator_task: OTC-20260729-plan-w5-render-surface
branch: feat/OTC-20260729-renderer-surface-ownership
base_branch: main
created: 2026-07-29T16:04:00+02:00
updated: 2026-07-29T19:11:00+02:00
last_verified_commit: "cb6042875f51a71cbbd84cd7e6a1af7acad5a4f0"
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
  - docs/agents/tasks/archive/OTC-20260729-renderer-surface-ownership.md
shared_path_lease: []
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

# Result

PR #86 implemented the single authorized W5-RENDER package and added exactly one `oteryn-renderer` crate plus narrow composition into the merged Windows application shell.

Delivered:

- typed transactional surface lifecycle keyed by `ProcessGeneration`;
- unconfigured, configured, suspended, lost and closing states with zero-size suspension, stale-generation rejection, checked counters, bounded recovery and idempotent close;
- Windows-only safe wgpu ownership of instance, surface, adapter, device and queue;
- one original constant clear/present path with event-driven redraw;
- exact `wgpu 30.0.0` with default features disabled and only `std` plus `dx12`;
- exact `pollster 1.0.1` for one synchronous main-thread bootstrap;
- renderer failures routed through the existing shell close path and renderer resources released before the window;
- generated locked dependency graph, narrow cargo-deny exceptions and current architecture, workspace, module, build-test and changelog documentation.

# Validation

| Evidence | Result |
|---|---|
| final head | `cb6042875f51a71cbbd84cd7e6a1af7acad5a4f0` |
| Rust Client run `30470014282` | PASS: locked metadata, formatting, Clippy with warnings denied, all workspace tests, architecture policy and cargo-deny advisories/licenses/bans/sources |
| repository CI run `30470017491` | PASS: Lua Syntax, workflow/YAML/XML validation, informational static analysis and `CI / Required` job `90638159006`; legacy Windows build correctly skipped for Rust-only scope |
| full changed-file review | PASS: exactly 15 authorized paths and no final `.github/workflows/**` change |
| comments, reviews and unresolved threads | none |
| base before merge | unchanged at `e9dcf70e8d60bcb5ba3e82280482108d43306f5f` |
| squash merge | `247837ad405a79fe6d9a8d2bc18b86911a2dcefa` |

# Runtime evidence boundary

Hosted compilation and deterministic tests do not prove interactive runtime compatibility.

Visible Windows launch/presentation, real resize/minimize/suspend/resume behavior, actual surface or device-loss recovery, GPU/driver/hardware compatibility, minimum-Windows support and performance remain explicitly unproven. No game/map/entity rendering, assets, textures, shader modules or pipelines, render graph, UI, protocol, identity, networking, audio, persistence, updater or extension-runtime compatibility is claimed.

# Completion

- Final status: completed
- PR: #86
- Merge commit: `247837ad405a79fe6d9a8d2bc18b86911a2dcefa`
- Shared-path lease: released
- Archived at: `docs/agents/tasks/archive/OTC-20260729-renderer-surface-ownership.md`
