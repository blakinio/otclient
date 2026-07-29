---
task_id: OTC-20260729-plan-w5-render-surface
status: awaiting_ci
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W5-RENDER-SURFACE
parallel_lane: W5-C
parallel_lane_state: validating
branch: docs/OTC-20260729-plan-w5-render-surface
base_branch: main
created: 2026-07-29T15:31:00+02:00
updated: 2026-07-29T15:48:00+02:00
last_verified_commit: "383e7942e972822b3c05870e820946f266799863"
required_base_commit: "37c9b3496eef4b7360bf9f5d753491540b5a2727"
risk: low
related_pr: "#84"
depends_on:
  - W4 shell PR #79 and archive PR #80
  - W4 closure PR #81 and archive PR #82
  - W1 foundation PR #54
  - W2 diagnostics PR #61
  - W3 test support PR #73
owned_paths:
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/NEXT_RENDERER_SURFACE_AGENT.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260729-plan-w5-render-surface.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - merged Windows application-shell contract from PR #79
  - normative renderer ownership and presentation boundaries
crates_touched: []
features_touched: []
contracts_touched:
  - W5 launch authorization and worker routing only
modules_touched: []
reuses:
  - merged W4 shell lifecycle and runtime evidence
  - existing renderer architecture category and WS-R08 ownership
  - existing Cargo/lockfile/shared-path lease protocol
public_interfaces:
  - coordination documentation only
cross_repo_tasks: []
performance_evidence:
  - no renderer performance claim; interactive GPU evidence remains blocked
security_evidence:
  - no secrets, assets, shader input, protocol data or external-repository writes
---

# Goal

Accept one bounded W5 launch plan for a renderer surface-ownership spike that consumes the merged Windows application shell without beginning game rendering, asset, shader-framework, UI or protocol work.

# Acceptance criteria

- [x] Current `main`, active tasks, open PRs and shared leases are revalidated.
- [x] W1, W2, W3 and W4 remain completed and prohibited from relaunch.
- [x] Exactly one implementation worker `W5-RENDER` is authorized.
- [x] The worker owns one `oteryn-renderer` crate and the narrow shell composition changes only.
- [x] Exact dependency candidates, licenses, MSRV, source and advisory gate are recorded from current primary evidence.
- [x] Main-thread window/surface ownership and deterministic shell shutdown remain authoritative.
- [x] CPU-side zero-size, suspend, loss, reconfigure and closing behavior is deterministic and testable without a GPU.
- [x] No game/map/entity rendering, textures/assets, shader framework, UI, protocol, identity, networking, audio, persistence or extension runtime is authorized.
- [x] No global renderer singleton, hidden service, reusable async runtime or scheduler is authorized.
- [x] Interactive GPU, driver, hardware and performance claims remain explicitly blocked unless genuinely observed.
- [x] Planning changes no Rust source, Cargo, lockfile, dependency policy, CI, architecture or legacy runtime.
- [ ] Final task-record head passes exact required CI; plan merges and archives independently before any worker task/branch/lease exists.

# Live preflight

- Current required `main`: `37c9b3496eef4b7360bf9f5d753491540b5a2727`.
- W1-W4 implementation, closure and lifecycle records are merged and archived.
- Legacy client-assets PR #37 and archive PR #83 are merged; their task is no longer active.
- Open PR #23 owns legacy OTUI/Lua presentation only.
- Open PR #48 is isolated operational non-merge work.
- No active Rust task or open PR owns `crates/renderer`, the renderer surface contract, Cargo/lockfile integration or the proposed W5 lease.
- The architecture checker already recognizes category `renderer` and permits renderer dependencies except protocol adapters/features; no checker/rule/fixture change is justified by this plan.

# Primary dependency evidence

Candidate exact worker dependencies:

```toml
wgpu = { version = "=30.0.0", default-features = false, features = ["std", "dx12"] }
pollster = { version = "=1.0.1", default-features = false }
```

Evidence cut on 2026-07-29:

- crates.io/docs.rs source for `wgpu 30.0.0` declares Rust 1.87 and dual MIT/Apache-2.0 licensing; workspace Rust is 1.94;
- `dx12` is an explicit native feature and the worker will not enable WGSL, Vulkan, Metal, GLES or WebGPU by default;
- `pollster 1.0.1` declares Rust 1.69, dual MIT/Apache-2.0 licensing and no dependencies;
- `pollster::block_on` is authorized only for the single main-thread adapter/device bootstrap; no reusable executor, reactor, scheduler or background runtime is authorized;
- exact cargo-deny advisories, licenses, bans and sources remain a merge gate and may reject the candidates without weakening policy.

The GitHub release view for wgpu may lag the crates.io/docs.rs registry release; the worker must use the exact registry package/source resolved by Cargo and record the generated lockfile evidence.

# Planned W5 worker

Exactly one implementation lane: `W5-RENDER` under WS-R08.

Owned product paths:

```text
oteryn-client/crates/renderer/**
oteryn-client/docs/research/renderer/W5_RUNTIME_EVIDENCE.md
```

Unique shared-path lease after the plan lifecycle merges:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/deny.toml
oteryn-client/apps/client/Cargo.toml
oteryn-client/apps/client/src/main.rs
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
```

`deny.toml` is leased only for an exactly evidenced license/source adjustment if cargo-deny proves the current allowlist insufficient. Architecture checker/rules/fixtures, Rust toolchain and CI workflows remain read-only unless a separate blocker is recorded.

# Worker acceptance envelope

- one package `oteryn-renderer`, category `renderer`;
- deterministic backend-neutral CPU-side surface lifecycle using typed process-generation ownership;
- main-thread Windows adapter owns wgpu instance, surface, adapter, device and queue;
- surface is configured only for non-zero physical size;
- resize/minimize/suspend/loss/reconfigure/close policy is explicit and idempotent;
- one original constant clear color and clear/present only; no shader module, pipeline, texture, asset or render graph;
- redraw is event-driven, not an unbounded animation/poll loop;
- public errors are closed, non-secret and do not retain arbitrary backend text;
- shell close remains the sole orderly application exit path and renderer shutdown completes before the window is released;
- exact Windows workspace, formatting, Clippy, tests, architecture, supply-chain and repository CI pass;
- runtime evidence distinguishes automated `PASS`, genuinely exercised `OBSERVED` and unavailable interactive `BLOCKED` cases.

# Validation

| Revision | Check | Result |
|---|---|---|
| `37c9b3496eef4b7360bf9f5d753491540b5a2727` | live base/open-PR/active-task/lease preflight | PASS |
| `383e7942e972822b3c05870e820946f266799863` | complete five-file path/content review | PASS |
| `383e7942e972822b3c05870e820946f266799863` | Rust Client run `30457406425` | PASS: Windows workspace and Supply Chain |
| `383e7942e972822b3c05870e820946f266799863` | repository CI run `30457407027` | PASS: all emitted required jobs and `CI / Required` |
| final task-record head | exact-head required CI pending |

# Boundaries

This plan changes coordination documentation only. It creates no worker task, implementation branch, dependency change or shared lease. It makes no interactive Windows, GPU, driver, hardware or performance compatibility claim.

# Completion

- Final status: awaiting final exact-head CI
- PR: #84
- Merge commit: pending
- Worker launch: prohibited until plan and plan archive merge
- Archived at: pending
