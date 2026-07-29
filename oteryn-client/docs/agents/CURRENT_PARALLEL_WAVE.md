# Current Parallel Agent Wave

Status: accepted launch plan  
Wave ID: `OTERYN-W5-RENDER-SURFACE`  
Evidence cut: `main` `37c9b3496eef4b7360bf9f5d753491540b5a2727`

Live Git, active tasks and open PRs remain authoritative. W1, W2, W3 and W4 are completed, archived and not launchable. This plan authorizes exactly one implementation lane only after the W5 plan and its lifecycle archive merge.

## 1. Confirmed transition state

- W1 foundation primitives are merged/archived and must not be relaunched.
- All W2 implementation/evidence lanes are merged/archived and must not be relaunched.
- W3 deterministic test support is merged/archived and must not be relaunched.
- W4 planning and the Windows application shell are merged/archived and must not be relaunched.
- Legacy client-assets PR #37 and archive PR #83 are merged; their task owns no current Rust path.
- Open PR #23 owns legacy OTUI/Lua presentation only; PR #48 is isolated operational non-merge work.
- No active Rust task or open PR owns `oteryn-client/crates/renderer/`, the renderer-surface public contract or its Cargo/lockfile integration.
- All previous Rust Cargo/lockfile/dependency-policy/shared-document leases are released.

## 2. Objective

Implement one bounded Windows renderer surface-ownership spike that consumes the merged application-shell window/lifecycle contract and proves deterministic device/surface ownership, clear/present and orderly shutdown without beginning game rendering, assets, shader-framework, UI or protocol work.

The wave uses:

```text
1 coordinator
1 implementation worker
```

No secondary implementation or research lane is authorized.

## 3. Dependency graph

```text
merged foundation (#54)
merged diagnostics (#61)
merged test support (#73)
merged Windows application shell (#79)
W5 plan/archive
          |
          v
W5-RENDER renderer surface-ownership spike
```

## 4. Lane W5-C — Coordinator

Prompt: `prompts/COORDINATOR_AGENT.md`

Responsibilities:

- verify current ownership, exact base and the merged W5 plan lifecycle before worker launch;
- prevent W1-W4 relaunch and prevent a second renderer producer;
- grant one Cargo/lockfile/dependency-policy/shared-document lease only to W5-RENDER;
- require exact dependency, Windows workspace, architecture, supply-chain and repository CI evidence;
- require explicit automated versus interactive GPU evidence classification;
- merge/archive the worker independently;
- close W5 and record exactly one next bounded recommendation.

The coordinator does not implement the renderer package while preparing or closing the wave.

## 5. Lane W5-RENDER — Renderer surface ownership

Prompt: `prompts/NEXT_RENDERER_SURFACE_AGENT.md`

Workstream: WS-R08 renderer  
Contract role: producer

Required merged producers:

```text
oteryn-foundation: PR #54
oteryn-diagnostics: PR #61
oteryn-test-support: PR #73
oteryn-client application shell: PR #79
W5 plan/archive: current main at worker preflight
```

Purpose:

- add exactly one package under `oteryn-client/crates/renderer/` with package name `oteryn-renderer` and architecture category `renderer`;
- exact-pin `wgpu = "=30.0.0"` with default features disabled and Windows `std` plus `dx12` only, unless fresh primary evidence changes before the worker starts;
- exact-pin `pollster = "=1.0.1"` with default features disabled for one synchronous main-thread adapter/device bootstrap only;
- preserve the shell's main-thread event-loop/window ownership and deterministic close path;
- own one wgpu instance, surface, adapter, device and queue on the main/event thread;
- configure only for non-zero physical size and handle resize, minimize, suspend, loss, reconfigure and close explicitly;
- clear and present one original constant color only;
- expose a deterministic CPU-side surface lifecycle independent of a GPU or interactive desktop;
- keep backend failures mapped into closed, non-secret error kinds without arbitrary backend text.

Required design boundaries:

- no game/map/entity rendering, render snapshot schema or domain extraction;
- no textures, assets, asset schemas, upload pipeline or proprietary material;
- no WGSL/shader module, shader framework, render graph, pipeline or bind group;
- no UI, text, input feature, protocol, identity, networking, audio, settings, persistence, updater or extension runtime;
- no direct Win32/windows-sys dependency, unsafe code or direct raw-window-handle dependency;
- no global renderer singleton, global mutable registry or global logger/subscriber;
- no reusable async runtime, executor, reactor, scheduler, polling loop, hidden service or background thread;
- no continuous animation loop or frame-time/performance claim;
- no minimum Windows, GPU, driver, adapter, hardware or device-loss recovery compatibility claim.

Expected exclusive paths:

```text
oteryn-client/crates/renderer/**
oteryn-client/docs/research/renderer/W5_RUNTIME_EVIDENCE.md
```

Expected shared-path lease:

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

`deny.toml` is leased only for a narrowly evidenced license/source adjustment if exact cargo-deny proves the existing allowlist insufficient. Architecture checker/rules/fixtures, Rust toolchain and CI workflows remain read-only unless a separate blocker is recorded.

## 6. Dependency evidence cut

Primary registry/source evidence reviewed on 2026-07-29:

- `wgpu 30.0.0`: Rust 1.87, MIT/Apache-2.0, explicit `dx12` feature; workspace Rust is 1.94;
- `pollster 1.0.1`: Rust 1.69, MIT/Apache-2.0, no dependencies;
- Cargo registry resolution and the generated lockfile are authoritative when a GitHub release page lags the registry;
- exact cargo-deny advisories, licenses, bans and sources remain a required worker gate and may reject the candidates without policy weakening.

No dependency is added by this planning task.

## 7. Deterministic acceptance envelope

The worker must test a backend-neutral state contract covering at least:

- unconfigured to configured for non-zero size;
- zero-size/minimized suspension without surface configuration;
- resize and restore reconfiguration;
- stale process-generation rejection without mutation;
- timeout/occluded skip policy;
- outdated/lost transition and bounded reconfigure policy;
- validation/fatal failure classification;
- idempotent closing and no presentation after close;
- bounded counters with explicit overflow behavior.

The Windows adapter must:

- create the surface from a shell-owned window without storing borrowed stack data;
- request the adapter/device once during startup on the main thread;
- use event-driven redraw only;
- clear/present without shaders or assets;
- drop renderer resources before releasing the shell window;
- route a fatal renderer error through the existing shell close path.

## 8. Runtime evidence policy

Hosted Windows compilation and CPU-side tests do not prove interactive GPU behavior. The worker must publish a matrix distinguishing:

- `PASS` for exact automated state/build/architecture/supply-chain evidence;
- `OBSERVED` only for behavior genuinely exercised on a named interactive Windows/GPU environment;
- `BLOCKED` for visible presentation, resize/minimize, suspend/resume, real surface loss, adapter/device loss, GPU/driver/hardware compatibility and performance when unavailable.

Unavailable interactive evidence is not inferred from compilation and is not a blocker to merging this bounded ownership spike when all automated acceptance and documentation requirements pass.

## 9. Shared-path lease

| Path group | Lease holder after worker launch | Other work |
|---|---|---|
| Cargo workspace/lockfile and dependency policy | W5-RENDER | read-only |
| renderer package/public surface contract | W5-RENDER | no duplicate producer |
| shell Cargo/main composition | W5-RENDER | no parallel shell integration |
| shared catalogue/matrix/changelog/layout/workspace docs | W5-RENDER | read-only |
| architecture checker/rules/fixtures | none | read-only |
| Rust CI/toolchain | none | read-only |

The worker claims the lease only through its active task and live draft PR after a fresh overlap check.

## 10. Merge and completion rules

- W5-RENDER starts only after this plan and its archive merge.
- Any material shell producer, dependency evidence or `main` change requires restack and exact-head revalidation.
- The worker merges only through the root autonomous gate and receives a separate archive PR.
- W5 closes only after the worker is merged/archived, no lease remains and one evidence-based next package is recorded.

Candidate next package after successful closure: a small normalized synthetic asset schema/compiler slice only if W5 proves a stable clear/present boundary. It is not authorized by this plan.
